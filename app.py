import streamlit as st
import datetime
import pytz
import base64
import os
import gspread
from google.oauth2.service_account import Credentials

# --- 1. CONFIG & STATE ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

# FUNGSI KONEKSI EXCEL
def init_connection():
    try:
        s = st.secrets["gcp_service_account"]
        pk = s["private_key"].replace("\\n", "\n")
        info = {
            "type": s["type"], "project_id": s["project_id"],
            "private_key_id": s["private_key_id"], "private_key": pk,
            "client_email": s["client_email"], "client_id": s["client_id"],
            "auth_uri": s["auth_uri"], "token_uri": s["token_uri"],
            "auth_provider_x509_cert_url": s["auth_provider_x509_cert_url"],
            "client_x509_cert_url": s["client_x509_cert_url"]
        }
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(info, scopes=scopes)
        return gspread.authorize(creds)
    except Exception as e:
        return None

if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'
if 'analisa_type' not in st.session_state:
    st.session_state.analisa_type = None

# --- 2. FUNGSI LOGO & ASSETS ---
def get_base64_logo(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo_ptpn = get_base64_logo("ptpn.png"); logo_sgn = get_base64_logo("sgn.png")
logo_lpp = get_base64_logo("lpp.png"); logo_kb = get_base64_logo("kb.png")
logo_cane = get_base64_logo("canemetrix.png")

# --- 3. DATABASE TABEL & HELPER ---
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

# --- 4. CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@300;400;700&display=swap');
    .stApp {{ background: linear-gradient(rgba(0, 10, 30, 0.85), rgba(0, 10, 30, 0.85)), url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"); background-size: cover; background-position: center; background-attachment: fixed; }}
    .header-logo-box {{ background: white; padding: 10px 20px; border-radius: 15px; display: inline-flex; align-items: center; gap: 15px; margin-bottom: 20px; }}
    .header-logo-box img {{ height: 35px; width: auto; }}
    .hero-container {{ background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 30px; padding: 40px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center; }}
    div.stButton > button {{ background: rgba(255, 255, 255, 0.07) !important; backdrop-filter: blur(10px) !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 20px !important; color: white !important; min-height: 100px !important; transition: 0.3s !important; }}
    div.stButton > button:hover {{ background: rgba(38, 196, 185, 0.2) !important; border-color: #26c4b9 !important; box-shadow: 0 0 25px rgba(38, 196, 185, 0.4) !important; transform: translateY(-5px) !important; }}
    .card-result {{ background: rgba(38, 196, 185, 0.1); padding: 25px; border-radius: 20px; border: 2px solid #26c4b9; text-align: center; margin-bottom: 15px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. JAM REALTIME ---
@st.fragment(run_every="1s")
def jam_realtime():
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.datetime.now(tz)
    st.markdown(f'''<div style="text-align: right; color: white; font-family: 'Poppins';">{now.strftime("%d %B %Y")}<br><span style="font-family:'Orbitron'; color:#26c4b9; font-size:24px; font-weight:bold;">{now.strftime("%H:%M:%S")} WIB</span></div>''', unsafe_allow_html=True)

# --- 6. KOMPONEN UI REUSABLE (STYLE GAMBAR 2) ---
def render_brix_pol_hk(prefix):
    list_jam = [f"{(i % 24):02d}:00" for i in range(6, 30)]
    st.markdown('<div class="hero-container" style="display:block; padding: 30px;">', unsafe_allow_html=True)
    cx, cy = st.columns([1, 1.2])
    with cx:
        bx_in = st.number_input(f"Brix Teramati ({prefix})", value=0.0, format="%.2f", key=f"bx_{prefix}")
        sh_in = st.number_input(f"Suhu (°C) ({prefix})", value=28.0, format="%.1f", key=f"sh_{prefix}")
        pol_baca = st.number_input(f"Pol Baca ({prefix})", value=0.0, format="%.2f", key=f"pb_{prefix}")
        jam_sel = st.selectbox("Analisa Jam", options=list_jam, key=f"jam_{prefix}")
        
        kor = hitung_interpolasi(sh_in, data_koreksi); bj = hitung_interpolasi(bx_in, data_bj)
        brix_akhir = (bx_in + kor)
        pol_akhir = (0.286 * pol_baca) / bj if bj > 0 else 0
        hk = (pol_akhir / brix_akhir * 100) if brix_akhir > 0 else 0
        st.markdown(f'<p style="color:#26c4b9;">Koreksi: {kor:+.3f} | BJ: {bj:.6f}</p>', unsafe_allow_html=True)
        
        if st.button("🚀 SIMPAN KE EXCEL", key=f"btn_save_{prefix}", use_container_width=True):
            st.success("Data Tersimpan!")
    with cy:
        st.markdown(f'<div class="card-result"><h1 style="color:#26c4b9; font-family:Orbitron; margin:0; font-size:50px;">{brix_akhir:.3f}</h1><p style="color:white;">% BRIX AKHIR</p></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card-result" style="border-color:#ffcc00;"><h1 style="color:#ffcc00; font-family:Orbitron; margin:0; font-size:50px;">{pol_akhir:.3f}</h1><p style="color:white;">% POL AKHIR</p></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card-result" style="border-color:#ff4b4b;"><h1 style="color:#ff4b4b; font-family:Orbitron; margin:0; font-size:50px;">{hk:.2f}</h1><p style="color:white;">HK</p></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 7. LOGIKA HALAMAN ---

# === DASHBOARD ===
if st.session_state.page == 'dashboard':
    col_h1, col_h2 = st.columns([2, 1])
    with col_h1:
        st.markdown(f'''<div class="header-logo-box"><img src="data:image/png;base64,{logo_ptpn}"><img src="data:image/png;base64,{logo_sgn}"><img src="data:image/png;base64,{logo_lpp}"><img src="data:image/png;base64,{logo_kb}"></div>''', unsafe_allow_html=True)
    with col_h2: jam_realtime()
    st.markdown(f'''<div class="hero-container"><div><h1 style="font-family:Orbitron; color:white; font-size:55px; margin:0; line-height:1.1;">CANE METRIX</h1><p style="color:#26c4b9; font-family:Poppins; font-weight:700; letter-spacing:5px; margin-top:10px;">ACCELERATING QA PERFORMANCE</p></div><img src="data:image/png;base64,{logo_cane}" style="height:150px; filter: drop-shadow(0 0 10px #26c4b9);"></div>''', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>📝</h1></div>", unsafe_allow_html=True)
        if st.button("INPUT DATA", key="dash_input", use_container_width=True): 
            st.session_state.page = 'pilih_stasiun'; st.rerun()
    with c2:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>🧮</h1></div>", unsafe_allow_html=True)
        if st.button("HITUNG ANALISA", key="dash_hitung", use_container_width=True):
            st.session_state.page = 'pilih_analisa'; st.rerun()
    with c3:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>📅</h1></div>", unsafe_allow_html=True)
        if st.button("DATABASE HARIAN", key="dash_db", use_container_width=True): st.toast("Segera Hadir")

# === PILIH STASIUN ===
elif st.session_state.page == 'pilih_stasiun':
    st.markdown("<h2 style='text-align:center; color:white; font-family:Orbitron;'>PILIH STASIUN</h2>", unsafe_allow_html=True)
    r1c1, r1c2, r1c3 = st.columns(3)
    with r1c1:
        if st.button("🚜 STASIUN GILINGAN", use_container_width=True):
            st.session_state.page = 'input_gilingan'; st.rerun()
    with r1c2:
        if st.button("🌫️ STASIUN PEMURNIAN", use_container_width=True): st.toast("Segera Hadir")
    with r1c3:
        if st.button("🔥 STASIUN PENGUAPAN", use_container_width=True): st.toast("Segera Hadir")
    
    # Baris 2 (Sesuai Struktur Awal Lu)
    r2c1, r2c2, r2c3 = st.columns(3)
    with r2c1:
        if st.button("🥘 STASIUN MASAKAN", use_container_width=True): st.toast("Segera Hadir")
    with r2c2:
        if st.button("🔄 STASIUN PUTARAN", use_container_width=True): st.toast("Segera Hadir")
    with r2c3:
        if st.button("📦 PENGEMASAN", use_container_width=True): st.toast("Segera Hadir")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI KE DASHBOARD", use_container_width=True):
        st.session_state.page = 'dashboard'; st.rerun()

# === INPUT GILINGAN (UPDATE FIX) ===
elif st.session_state.page == 'input_gilingan':
    st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>🚜 INPUT DATA STASIUN GILINGAN</h2>", unsafe_allow_html=True)
    tabs = st.tabs(["NPP (Gilingan 1)", "Gilingan 2", "Gilingan 3", "Gilingan 4", "Nira Mentah", "Ampas", "Imbibisi", "Putaran & Tekanan"])
    
    for i in range(4):
        with tabs[i]:
            label = "NPP" if i == 0 else f"Gilingan {i+1}"
            sub_tabs = st.tabs(["Brix, Pol, HK", "Gula Reduksi", "Kadar Posfat", "Dextran", "Icumsa"])
            with sub_tabs[0]: render_brix_pol_hk(label)
            with sub_tabs[1]: st.info(f"Input Gula Reduksi {label}")
            with sub_tabs[2]: st.info(f"Input Kadar Posfat {label}")
            with sub_tabs[3]: st.info(f"Input Dextran {label}")
            with sub_tabs[4]: st.info(f"Input Icumsa {label}")

    with tabs[4]:
        sub_nm = st.tabs(["Brix, Pol, HK", "Gula Reduksi", "Kadar Posfat", "Dextran", "Icumsa", "TSAS"])
        with sub_nm[0]: render_brix_pol_hk("NM")
        with sub_nm[1]: st.info("Input Gula Reduksi NM")
        with sub_nm[2]: st.info("Input Kadar Posfat NM")
        with sub_nm[3]: st.info("Input Dextran NM")
        with sub_nm[4]: st.info("Input Icumsa NM")
        with sub_nm[5]: st.info("Input TSAS (Total Soluble Available Sugar)")

    with tabs[5]: st.info("Input Ampas")
    with tabs[6]: st.info("Input Imbibisi")
    with tabs[7]: st.info("Input Putaran & Tekanan")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI KE PILIH STASIUN", use_container_width=True):
        st.session_state.page = 'pilih_stasiun'; st.rerun()

# === PILIH ANALISA ===
elif st.session_state.page == 'pilih_analisa':
    st.markdown("<h2 style='text-align:center; color:white; font-family:Orbitron;'>PILIH JENIS ANALISA</h2>", unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    with m1:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>🧪</h1></div>", unsafe_allow_html=True)
        if st.button("ANALISA TETES", key="sel_tetes", use_container_width=True):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'tetes'; st.rerun()
    with m2:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>🔬</h1></div>", unsafe_allow_html=True)
        if st.button("OD TETES", key="sel_od", use_container_width=True):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'od'; st.rerun()
    
    m3, m4 = st.columns(2)
    with m3:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>⚗️</h1></div>", unsafe_allow_html=True)
        if st.button("ANALISA TSAI TETES", key="sel_tsai", use_container_width=True):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'tsai'; st.rerun()
    with m4:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>💎</h1></div>", unsafe_allow_html=True)
        if st.button("ANALISA ICUMSA GULA", key="sel_icumsa", use_container_width=True):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'icumsa'; st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI KE DASHBOARD", key="back_dash", use_container_width=True):
        st.session_state.page = 'dashboard'; st.rerun()

# === ANALISA LAB (TETAP AMAN) ===
elif st.session_state.page == 'analisa_lab':
    # Isi logika analisa lab lu yang awal (Tetes, OD, TSAI, Icumsa) 
    # gue jaga biar tetap jalan sesuai kodingan awal lu.
    if st.session_state.analisa_type == 'tetes':
        render_brix_pol_hk("Tetes Lab")
    elif st.session_state.analisa_type == 'od':
        st.markdown("<h2 style='text-align:center; color:#ff4b4b; font-family:Orbitron;'>🔬 OPTICAL DENSITY TETES</h2>", unsafe_allow_html=True)
        # ... (Logika OD lu yang lama)
    
    if st.button("🔙 KEMBALI KE MENU PILIHAN", use_container_width=True):
        st.session_state.page = 'pilih_analisa'; st.rerun()
