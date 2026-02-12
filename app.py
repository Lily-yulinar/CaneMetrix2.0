import streamlit as st
import datetime
import pytz
import base64
import os

# --- 1. CONFIG & STATE ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'
if 'analisa_type' not in st.session_state:
    st.session_state.analisa_type = None

# --- 2. ASSETS (LOGO) ---
def get_base64_logo(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# Note: Pastikan file gambar ini ada di folder yang sama atau ganti path-nya
logo_ptpn = get_base64_logo("ptpn.png"); logo_sgn = get_base64_logo("sgn.png")
logo_lpp = get_base64_logo("lpp.png"); logo_kb = get_base64_logo("kb.png")
logo_cane = get_base64_logo("canemetrix.png")

# --- 3. DATABASE & INTERPOLASI ---
data_koreksi = {27: -0.05, 28: 0.02, 29: 0.09, 30: 0.16, 31: 0.24, 32: 0.315, 33: 0.385, 34: 0.465, 35: 0.54, 36: 0.62, 37: 0.70, 38: 0.78, 39: 0.86, 40: 0.94}
data_bj = {0.0: 0.99640, 5.0: 1.01592, 10.0: 1.03608, 15.0: 1.05691, 20.0: 1.07844, 25.0: 1.10069, 30.0: 1.12368, 35.0: 1.14745, 40.0: 1.17203, 45.0: 1.19746, 49.0: 1.21839, 49.4: 1.22051, 49.5: 1.22104, 50.0: 1.22372, 55.0: 1.25083, 60.0: 1.27885, 65.0: 1.30781, 70.0: 1.33775}
data_tsai = {15.0: 336.00, 16.0: 316.00, 17.0: 298.00, 18.0: 282.00, 19.0: 267.00, 20.0: 254.50, 21.0: 242.90, 22.0: 231.80, 22.5: 223.60, 23.0: 222.20, 24.0: 213.30, 25.0: 204.80, 26.0: 197.40, 27.0: 190.40, 28.0: 183.70, 29.0: 177.60, 30.0: 171.70, 31.0: 166.30, 32.0: 161.20, 33.0: 156.60, 34.0: 152.20, 35.0: 147.90, 36.0: 143.90, 37.0: 140.20, 37.7: 136.67}

def hitung_interpolasi(nilai_user, dataset):
    keys = sorted(dataset.keys())
    if nilai_user in dataset: return dataset[nilai_user]
    if nilai_user < keys[0]: return dataset[keys[0]]
    if nilai_user > keys[-1]: return dataset[keys[-1]]
    for i in range(len(keys) - 1):
        x0, x1 = keys[i], keys[i+1]
        if x0 < nilai_user < x1:
            y0, y1 = dataset[x0], dataset[x1]
            return y0 + (nilai_user - x0) * (y1 - y0) / (x1 - x0)
    return 1.0

# --- 4. UI COMPONENTS (VERSI RAKSASA VERTIKAL) ---
def tampilkan_kartu_hasil(brix, pol, hk):
    st.markdown(f"""
    <div style="display: flex; flex-direction: column; gap: 15px;">
        <div style="background: rgba(38, 196, 185, 0.1); padding: 30px; border-radius: 20px; border: 3px solid #26c4b9; display: flex; justify-content: space-between; align-items: center;">
            <h1 style="color:#26c4b9; font-family:Orbitron; margin:0; font-size:80px;">{brix:.3f}</h1>
            <p style="color:white; font-family:Poppins; font-weight:bold; letter-spacing:2px; margin:0;">% BRIX AKHIR</p>
        </div>
        <div style="background: rgba(255, 204, 0, 0.1); padding: 30px; border-radius: 20px; border: 3px solid #ffcc00; display: flex; justify-content: space-between; align-items: center;">
            <h1 style="color:#ffcc00; font-family:Orbitron; margin:0; font-size:80px;">{pol:.3f}</h1>
            <p style="color:white; font-family:Poppins; font-weight:bold; letter-spacing:2px; margin:0;">% POL AKHIR</p>
        </div>
        <div style="background: rgba(255, 75, 75, 0.1); padding: 30px; border-radius: 20px; border: 3px solid #ff4b4b; display: flex; justify-content: space-between; align-items: center;">
            <h1 style="color:#ff4b4b; font-family:Orbitron; margin:0; font-size:80px;">{hk:.2f}</h1>
            <p style="color:white; font-family:Poppins; font-weight:bold; letter-spacing:2px; margin:0;">HK</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 5. CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@300;400;700&display=swap');
    .stApp {{ background: linear-gradient(rgba(0, 10, 30, 0.85), rgba(0, 10, 30, 0.85)), url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"); background-size: cover; background-position: center; background-attachment: fixed; }}
    .header-logo-box {{ background: white; padding: 10px 20px; border-radius: 15px; display: inline-flex; align-items: center; gap: 15px; margin-bottom: 20px; }}
    .header-logo-box img {{ height: 35px; width: auto; }}
    .hero-container {{ background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 30px; padding: 40px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center; }}
    div.stButton > button {{ background: rgba(255, 255, 255, 0.07) !important; backdrop-filter: blur(10px) !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 20px !important; color: white !important; height: 180px !important; width: 100% !important; transition: 0.3s !important; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
    div.stButton > button:hover {{ background: rgba(38, 196, 185, 0.2) !important; border-color: #26c4b9 !important; box-shadow: 0 0 25px rgba(38, 196, 185, 0.4) !important; transform: translateY(-8px) !important; }}
    </style>
    """, unsafe_allow_html=True)

@st.fragment(run_every="1s")
def jam_realtime():
    tz = pytz.timezone('Asia/Jakarta'); now = datetime.datetime.now(tz)
    st.markdown(f'''<div style="text-align: right; color: white; font-family: 'Poppins';">{now.strftime("%d %B %Y")}<br><span style="font-family:'Orbitron'; color:#26c4b9; font-size:24px; font-weight:bold;">{now.strftime("%H:%M:%S")} WIB</span></div>''', unsafe_allow_html=True)

# --- 6. PAGE LOGIC ---

if st.session_state.page == 'dashboard':
    col_h1, col_h2 = st.columns([2, 1])
    with col_h1: st.markdown(f'''<div class="header-logo-box"><img src="data:image/png;base64,{logo_ptpn}"><img src="data:image/png;base64,{logo_sgn}"><img src="data:image/png;base64,{logo_lpp}"><img src="data:image/png;base64,{logo_kb}"></div>''', unsafe_allow_html=True)
    with col_h2: jam_realtime()
    st.markdown(f'''<div class="hero-container"><div><h1 style="font-family:Orbitron; color:white; font-size:55px; margin:0; line-height:1.1;">CANE METRIX</h1><p style="color:#26c4b9; font-family:Poppins; font-weight:700; letter-spacing:5px; margin-top:10px;">ACCELERATING QA PERFORMANCE</p></div><img src="data:image/png;base64,{logo_cane}" style="height:150px; filter: drop-shadow(0 0 10px #26c4b9);"></div>''', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>📝</h1></div>", unsafe_allow_html=True)
        if st.button("INPUT DATA", key="dash_input", use_container_width=True): st.session_state.page = 'pilih_stasiun'; st.rerun()
    with c2:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>🧮</h1></div>", unsafe_allow_html=True)
        if st.button("HITUNG ANALISA", key="dash_hitung", use_container_width=True): st.session_state.page = 'pilih_analisa'; st.rerun()
    with c3:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>📅</h1></div>", unsafe_allow_html=True)
        if st.button("DATABASE HARIAN", key="dash_db", use_container_width=True): st.toast("Segera Hadir")

elif st.session_state.page == 'pilih_stasiun':
    st.markdown("<h2 style='text-align:center; color:white; font-family:Orbitron;'>PILIH STASIUN</h2>", unsafe_allow_html=True)
    r1c1, r1c2, r1c3 = st.columns(3)
    with r1c1:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>🚜</h1></div>", unsafe_allow_html=True)
        if st.button("STASIUN GILINGAN", use_container_width=True): st.session_state.page = 'input_gilingan'; st.rerun()
    with r1c2:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>🌫️</h1></div>", unsafe_allow_html=True)
        if st.button("STASIUN PEMURNIAN", use_container_width=True): st.toast("Coming Soon")
    with r1c3:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>🔥</h1></div>", unsafe_allow_html=True)
        if st.button("STASIUN PENGUAPAN", use_container_width=True): st.toast("Coming Soon")

    r2c1, r2c2, r2c3 = st.columns(3)
    with r2c1:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>🍳</h1></div>", unsafe_allow_html=True)
        if st.button("STASIUN MASAKAN", use_container_width=True): st.toast("Coming Soon")
    with r2c2:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>🌀</h1></div>", unsafe_allow_html=True)
        if st.button("STASIUN PUTERAN", use_container_width=True): st.toast("Coming Soon")
    with r2c3:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>📦</h1></div>", unsafe_allow_html=True)
        if st.button("STASIUN PENGEMASAN", use_container_width=True): st.toast("Coming Soon")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI KE DASHBOARD", use_container_width=True): st.session_state.page = 'dashboard'; st.rerun()

elif st.session_state.page == 'input_gilingan':
    st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>🚜 INPUT DATA STASIUN GILINGAN</h2>", unsafe_allow_html=True)
    tabs = st.tabs(["NPP (Gilingan 1)", "Gilingan 2", "Gilingan 3", "Gilingan 4", "Nira Mentah", "Ampas", "Imbibisi", "Putaran & Tekanan"])

    def render_logic_brix_pol(prefix):
        c_input, c_hasil = st.columns([1, 2.2])
        with c_input:
            st.caption(f"Input Parameter {prefix}")
            bx_in = st.number_input("Brix Baca", value=0.0, key=f"bx_{prefix}", format="%.2f")
            sh_in = st.number_input("Suhu (°C)", value=28.0, key=f"sh_{prefix}", format="%.1f")
            pol_in = st.number_input("Pol Baca", value=0.0, key=f"pol_{prefix}", format="%.2f")
            kor = hitung_interpolasi(sh_in, data_koreksi)
            bj = hitung_interpolasi(bx_in, data_bj)
            bx_fix = (bx_in + kor) if bx_in > 0 else 0
            pol_fix = (0.286 * pol_in) / bj if bj > 0 else 0
            hk_fix = (pol_fix / bx_fix * 100) if bx_fix > 0 else 0
            st.info(f"Koreksi: {kor:+.3f} | BJ: {bj:.4f}")
            if st.button(f"🚀 SIMPAN DATA {prefix}", key=f"btn_{prefix}"): st.toast(f"Data {prefix} Disimpan!")
        with c_hasil:
            tampilkan_kartu_hasil(bx_fix, pol_fix, hk_fix)
        return bx_fix, bj

    def render_logic_dextran(prefix, bx_koreksi, bj):
        st.markdown(f"#### ⚗️ Analisa Dextran {prefix}")
        c1, c2 = st.columns([1, 2.2])
        with c1:
            k_std = st.number_input("Kurva Standar", value=0.0, key=f"kstd_{prefix}", format="%.4f")
            abs_dex = st.number_input("Absorbansi", value=0.0, key=f"absdex_{prefix}", format="%.3f")
            pengenc = st.number_input("Pengenceran", value=1.0, key=f"panc_{prefix}")
            faktor = st.number_input("Faktor", value=1.0, key=f"fkt_{prefix}")
            pembagi = (bj * bx_koreksi * faktor)
            hasil_dex = (k_std * abs_dex * pengenc) / pembagi if pembagi > 0 else 0.0
        with c2:
            st.markdown(f'<div style="background:rgba(255,75,75,0.1); padding:40px; border-radius:20px; border:3px solid #ff4b4b; display:flex; justify-content:space-between; align-items:center;"><h1 style="color:#ff4b4b; font-family:Orbitron; margin:0; font-size:80px;">{hasil_dex:.4f}</h1><p style="color:white; font-weight:bold; letter-spacing:2px;">PPM DEXTRAN</p></div>', unsafe_allow_html=True)

    def render_input_lengkap(prefix, list_opsi):
        sub = st.selectbox(f"Pilih Analisa {prefix}", list_opsi, key=f"sel_{prefix}")
        st.markdown('<div class="hero-container" style="display:block; padding: 30px;">', unsafe_allow_html=True)
        bx_fix, bj = render_logic_brix_pol(prefix)
        if sub == "(Dextran)":
            st.divider(); render_logic_dextran(prefix, bx_fix, bj)
        elif sub == "(Gula Reduksi)":
            st.divider(); c1, c2 = st.columns(2)
            v_b = c1.number_input("Volume Blanko", value=0.0, key=f"vb_{prefix}")
            v_p = c2.number_input("Volume Penitran", value=0.0, key=f"vp_{prefix}")
            st.metric("Hasil Gula Reduksi", f"{(v_b - v_p) * 6.357:.2f}")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- UPDATE: ISTILAH NERACA WARNA ---
    menu_neraca = ["(Brix, Pol, dan HK)", "(Gula Reduksi)", "(Kadar Posfat)", "(Dextran)", "(Neraca Warna)"]
    menu_nm_lengkap = menu_neraca + ["(TSAS)"]

    with tabs[0]: render_input_lengkap("NPP", menu_neraca)
    with tabs[1]: render_input_lengkap("Gilingan 2", ["(Brix, Pol, dan HK)"])
    with tabs[2]: render_input_lengkap("Gilingan 3", ["(Brix, Pol, dan HK)"])
    with tabs[3]: render_input_lengkap("Gilingan 4", ["(Brix, Pol, dan HK)"])
    with tabs[4]: render_input_lengkap("Nira Mentah", menu_nm_lengkap)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI KE PILIH STASIUN", use_container_width=True): st.session_state.page = 'pilih_stasiun'; st.rerun()

elif st.session_state.page == 'pilih_analisa':
    st.markdown("<h2 style='text-align:center; color:white; font-family:Orbitron;'>PILIH JENIS ANALISA</h2>", unsafe_allow_html=True)
    m1, m2 = st.columns(2); m3, m4 = st.columns(2)
    with m1:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>🧪</h1></div>", unsafe_allow_html=True)
        if st.button("ANALISA TETES", key="btn_tetes", use_container_width=True):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'tetes'; st.rerun()
    with m2:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>🔬</h1></div>", unsafe_allow_html=True)
        if st.button("OD TETES", key="btn_od", use_container_width=True):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'od'; st.rerun()
    with m3:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>⚗️</h1></div>", unsafe_allow_html=True)
        if st.button("TSAI TETES", key="btn_tsai", use_container_width=True):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'tsai'; st.rerun()
    with m4:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>💎</h1></div>", unsafe_allow_html=True)
        if st.button("ICUMSA GULA", key="btn_icumsa", use_container_width=True):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'icumsa'; st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI KE DASHBOARD", use_container_width=True): st.session_state.page = 'dashboard'; st.rerun()

elif st.session_state.page == 'analisa_lab':
    list_jam = [f"{(i % 24):02d}:00" for i in range(6, 30)]
    
    if st.session_state.analisa_type == 'tetes':
        st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
        st.markdown('<div class="hero-container" style="display:block; padding:30px;">', unsafe_allow_html=True)
        cx, cy = st.columns([1, 2.2])
        with cx:
            jam = st.selectbox("Pilih Jam Analisa", options=list_jam)
            bx_in = st.number_input("Brix Teramati", value=8.80); sh_in = st.number_input("Suhu", value=28.0); pol_baca = st.number_input("Pol Baca", value=11.00)
            kor = hitung_interpolasi(sh_in, data_koreksi); bj = hitung_interpolasi(bx_in, data_bj)
            bx_f = (bx_in + kor) * 10; pol_f = (0.286 * pol_baca) / bj * 10; hk_f = (pol_f / bx_f * 100) if bx_f > 0 else 0
        with cy: tampilkan_kartu_hasil(bx_f, pol_f, hk_f)
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.analisa_type == 'od':
        st.markdown("<h2 style='text-align:center; color:#ff4b4b; font-family:Orbitron;'>🔬 OD TETES</h2>", unsafe_allow_html=True)
        st.markdown('<div class="hero-container" style="display:block; padding:30px;">', unsafe_allow_html=True)
        cx, cy = st.columns([1, 2.2])
        with cx:
            jam = st.selectbox("Pilih Jam Analisa", options=list_jam)
            bx_od = st.number_input("Brix Teramati", value=8.80); abs_od = st.number_input("Absorbansi", value=0.418)
            bj_od = hitung_interpolasi(bx_od, data_bj); res = (abs_od * bj_od * 500)
        with cy: st.markdown(f'<div style="background:rgba(255,75,75,0.1); padding:40px; border-radius:20px; border:3px solid #ff4b4b; display:flex; justify-content:space-between; align-items:center;"><h1 style="color:#ff4b4b; font-family:Orbitron; margin:0; font-size:80px;">{res:.3f}</h1><p style="color:white; font-weight:bold; letter-spacing:2px;">HASIL OD</p></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.analisa_type == 'tsai':
        st.markdown("<h2 style='text-align:center; color:#ffcc00; font-family:Orbitron;'>⚗️ TSAI TETES</h2>", unsafe_allow_html=True)
        st.markdown('<div class="hero-container" style="display:block; padding:30px;">', unsafe_allow_html=True)
        cx, cy = st.columns([1, 2.2])
        with cx:
            jam = st.selectbox("Pilih Jam Analisa", options=list_jam)
            titran = st.number_input("Volume Titran", value=22.5); ff = st.number_input("Faktor", value=0.979)
            val = titran * ff; tsai = hitung_interpolasi(val, data_tsai) / 4
        with cy: st.markdown(f'<div style="background:rgba(255,204,0,0.1); padding:40px; border-radius:20px; border:3px solid #ffcc00; display:flex; justify-content:space-between; align-items:center;"><h1 style="color:#ffcc00; font-family:Orbitron; margin:0; font-size:80px;">{tsai:.3f}</h1><p style="color:white; font-weight:bold; letter-spacing:2px;">% TSAI</p></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.analisa_type == 'icumsa':
        st.markdown("<h2 style='text-align:center; color:#00d4ff; font-family:Orbitron;'>💎 ICUMSA GULA</h2>", unsafe_allow_html=True)
        st.markdown('<div class="hero-container" style="display:block; padding:30px;">', unsafe_allow_html=True)
        cx, cy = st.columns([1, 2.2])
        with cx:
            abs_ic = st.number_input("Absorbansi", value=0.149); bx_ic = st.number_input("Brix Gula", value=49.44)
            bj_ic = hitung_interpolasi(bx_ic, data_bj); res = (abs_ic * 100000) / (bx_ic * 1 * bj_ic) if bx_ic > 0 else 0
        with cy: st.markdown(f'<div style="background:rgba(0,212,255,0.1); padding:40px; border-radius:20px; border:3px solid #00d4ff; display:flex; justify-content:space-between; align-items:center;"><h1 style="color:#00d4ff; font-family:Orbitron; margin:0; font-size:80px;">{res:.2f}</h1><p style="color:white; font-weight:bold; letter-spacing:2px;">IU (ICUMSA)</p></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔙 KEMBALI KE MENU PILIHAN", use_container_width=True): st.session_state.page = 'pilih_analisa'; st.rerun()
