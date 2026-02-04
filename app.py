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

# --- 2. FUNGSI LOGO & ASSETS ---
def get_base64_logo(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo_ptpn = get_base64_logo("ptpn.png")
logo_sgn = get_base64_logo("sgn.png")
logo_lpp = get_base64_logo("lpp.png")
logo_kb = get_base64_logo("kb.png")
logo_cane = get_base64_logo("canemetrix.png")

# --- 3. DATABASE TABEL (ICUMSA d27,5) ---
data_koreksi = {
    27: -0.05, 28: 0.02, 29: 0.09, 30: 0.16, 31: 0.24, 
    32: 0.315, 33: 0.385, 34: 0.465, 35: 0.54, 36: 0.62,
    37: 0.70, 38: 0.78, 39: 0.86, 40: 0.94
}

data_bj = {
    0.0: 0.996373, 1.0: 1.000201, 2.0: 1.004058, 3.0: 1.007944,
    4.0: 1.011858, 5.0: 1.015801, 6.0: 1.019772, 7.0: 1.023773,
    8.0: 1.027803, 8.8: 1.031047, 9.0: 1.031862, 10.0: 1.035950,
    11.0: 1.040068, 12.0: 1.044216, 13.0: 1.048394, 14.0: 1.052602,
    15.0: 1.056841, 16.0: 1.061110, 17.0: 1.065410, 18.0: 1.069741,
    19.0: 1.074103, 20.0: 1.078497, 21.0: 1.082923, 22.0: 1.087380,
    23.0: 1.091870, 23.9: 1.095939
}

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
    
    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.85), rgba(0, 10, 30, 0.85)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    .header-logo-box {{
        background: white; padding: 10px 20px; border-radius: 15px; 
        display: inline-flex; align-items: center; gap: 15px; margin-bottom: 20px;
    }}
    .header-logo-box img {{ height: 35px; width: auto; }}

    .hero-container {{
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 30px;
        padding: 40px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center;
    }}

    div.stButton > button {{
        background: rgba(255, 255, 255, 0.07) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        color: white !important;
        height: 180px !important;
        width: 100% !important;
        transition: 0.3s !important;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
    }}

    div.stButton > button:hover {{
        background: rgba(38, 196, 185, 0.2) !important;
        border-color: #26c4b9 !important;
        box-shadow: 0 0 25px rgba(38, 196, 185, 0.4) !important;
        transform: translateY(-8px) !important;
    }}
    
    .card-result {{
        background: rgba(38, 196, 185, 0.1); padding: 25px; border-radius: 20px; 
        border: 2px solid #26c4b9; text-align: center; margin-bottom: 15px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. JAM REALTIME ---
@st.fragment(run_every="1s")
def jam_realtime():
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.datetime.now(tz)
    st.markdown(f'''
        <div style="text-align: right; color: white; font-family: 'Poppins';">
            {now.strftime("%d %B %Y")}<br>
            <span style="font-family:'Orbitron'; color:#26c4b9; font-size:24px; font-weight:bold;">
                {now.strftime("%H:%M:%S")} WIB
            </span>
        </div>
    ''', unsafe_allow_html=True)

# --- 6. LOGIKA HALAMAN ---
if st.session_state.page == 'dashboard':
    col_h1, col_h2 = st.columns([2, 1])
    with col_h1:
        st.markdown(f'''<div class="header-logo-box">
            <img src="data:image/png;base64,{logo_ptpn}"><img src="data:image/png;base64,{logo_sgn}">
            <img src="data:image/png;base64,{logo_lpp}"><img src="data:image/png;base64,{logo_kb}">
        </div>''', unsafe_allow_html=True)
    with col_h2:
        jam_realtime()

    st.markdown(f'''<div class="hero-container">
        <div>
            <h1 style="font-family:Orbitron; color:white; font-size:55px; margin:0; line-height:1.1;">CANE METRIX</h1>
            <p style="color:#26c4b9; font-family:Poppins; font-weight:700; letter-spacing:5px; margin-top:10px;">ACCELERATING QA PERFORMANCE</p>
        </div>
        <img src="data:image/png;base64,{logo_cane}" style="height:150px; filter: drop-shadow(0 0 10px #26c4b9);">
    </div>''', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>📝</h1></div>", unsafe_allow_html=True)
        if st.button("INPUT DATA", key="dash_input", use_container_width=True): st.toast("Segera Hadir")
    with c2:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>🧮</h1></div>", unsafe_allow_html=True)
        if st.button("HITUNG ANALISA", key="dash_hitung", use_container_width=True):
            st.session_state.page = 'pilih_analisa'; st.rerun()
    with c3:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>📅</h1></div>", unsafe_allow_html=True)
        if st.button("DATABASE HARIAN", key="dash_db", use_container_width=True): st.toast("Segera Hadir")

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
    
    # TOMBOL KEMBALI PANJANG
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI KE DASHBOARD", key="back_dash", use_container_width=True):
        st.session_state.page = 'dashboard'; st.rerun()

elif st.session_state.page == 'analisa_lab':
    if st.session_state.analisa_type == 'tetes':
        st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="hero-container" style="display:block;">', unsafe_allow_html=True)
            cx, cy = st.columns(2)
            with cx:
                st.subheader("📥 Data Input Lab")
                bx_in = st.number_input("Brix Teramati", value=8.80, format="%.2f")
                sh_in = st.number_input("Suhu (°C)", value=28.0, format="%.1f")
                pol_baca = st.number_input("Pol Baca", value=11.00, format="%.2f")
                kor = hitung_interpolasi(sh_in, data_koreksi)
                bj = hitung_interpolasi(bx_in, data_bj)
                brix_akhir = (bx_in + kor) * 10
                pol_akhir = (0.286 * pol_baca) / bj * 10
                hk = (pol_akhir / brix_akhir * 100) if brix_akhir != 0 else 0
                st.info(f"💡 Koreksi: {kor:+.3f} | BJ: {bj:.6f}")
            with cy:
                st.subheader("📊 Hasil Akhir")
                st.markdown(f'<div class="card-result"><h1 style="color:#26c4b9; font-family:Orbitron; margin:0;">{brix_akhir:.3f}</h1><p style="color:white;">% BRIX AKHIR</p></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="card-result" style="border-color:#ffcc00;"><h1 style="color:#ffcc00; font-family:Orbitron; margin:0;">{pol_akhir:.3f}</h1><p style="color:white;">% POL AKHIR</p></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="card-result" style="border-color:#ff4b4b;"><h1 style="color:#ff4b4b; font-family:Orbitron; margin:0;">{hk:.2f}</h1><p style="color:white;">HARKAT KEMURNIAN (HK)</p></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.analisa_type == 'od':
        st.markdown("<h2 style='text-align:center; color:#ff4b4b; font-family:Orbitron;'>🔬 OPTICAL DENSITY TETES</h2>", unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="hero-container" style="display:block;">', unsafe_allow_html=True)
            cx, cy = st.columns(2)
            with cx:
                bx_od = st.number_input("Brix Teramati (cari BJ)", value=8.80, format="%.2f")
                abs_val = st.number_input("Nilai Absorbansi (Abs)", value=0.418, format="%.3f")
                bj_od = hitung_interpolasi(bx_od, data_bj)
                od_res = (abs_val * bj_od * 500) / 1
                st.info(f"🔍 BJ d27,5: {bj_od:.6f}")
            with cy:
                st.markdown(f'<div class="card-result" style="border-color:#ff4b4b; background:rgba(255,75,75,0.1); padding:50px;">'
                            f'<h1 style="color:#ff4b4b; font-size:60px; font-family:Orbitron; margin:0;">{od_res:.3f}</h1>'
                            f'<p style="color:white; margin:0;">NILAI OD TETES</p></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # TOMBOL KEMBALI PANJANG
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI KE MENU PILIHAN", key="back_sub", use_container_width=True):
        st.session_state.page = 'pilih_analisa'; st.rerun()
