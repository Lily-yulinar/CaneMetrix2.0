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

logo_cane = get_base64_logo("canemetrix.png")
# Catatan: Logo instansi lainnya (ptpn, sgn, lpp, kb) diasumsikan ada di folder yang sama

# --- 3. DATABASE TABEL ---
data_koreksi = {
    27: -0.05, 28: 0.02, 29: 0.09, 30: 0.16, 31: 0.24, 
    32: 0.315, 33: 0.385, 34: 0.465, 35: 0.54, 36: 0.62,
    37: 0.70, 38: 0.78, 39: 0.86, 40: 0.94
}

data_bj = {
    0.0: 0.996373, 8.8: 1.031047, 10.0: 1.035950, 20.0: 1.078497, 23.9: 1.095939
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

# --- 4. CSS CUSTOM ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@300;400;700&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.85), rgba(0, 10, 30, 0.85)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    .hero-container {{
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 30px;
        padding: 40px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center;
    }}

    /* Styling Tombol Menu Utama */
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.07) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important; color: white !important;
        height: 180px !important; width: 100% !important; transition: 0.3s !important;
    }}

    div.stButton > button:hover {{
        background: rgba(38, 196, 185, 0.2) !important;
        border-color: #26c4b9 !important;
        transform: translateY(-5px) !important;
    }}

    /* Styling Tombol Kembali (PANJANG) */
    .btn-kembali-container div.stButton > button {{
        height: 60px !important;
        background: rgba(255, 75, 75, 0.1) !important;
        border: 1px solid rgba(255, 75, 75, 0.3) !important;
        margin-top: 20px !important;
    }}
    .btn-kembali-container div.stButton > button:hover {{
        background: rgba(255, 75, 75, 0.3) !important;
        border-color: #ff4b4b !important;
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
    c_header1, c_header2 = st.columns([2, 1])
    with c_header2: jam_realtime()

    st.markdown(f'''<div class="hero-container">
        <div>
            <h1 style="font-family:Orbitron; color:white; font-size:55px; margin:0; line-height:1.1;">CANE METRIX</h1>
            <p style="color:#26c4b9; font-family:Poppins; font-weight:700; letter-spacing:5px; margin-top:10px;">ACCELERATING QA PERFORMANCE</p>
        </div>
        <img src="data:image/png;base64,{logo_cane}" style="height:150px;">
    </div>''', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>📝</h1></div>", unsafe_allow_html=True)
        if st.button("INPUT DATA", key="d_in"): st.toast("Segera Hadir")
    with c2:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>🧮</h1></div>", unsafe_allow_html=True)
        if st.button("HITUNG ANALISA", key="d_calc"):
            st.session_state.page = 'pilih_analisa'; st.rerun()
    with c3:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>📅</h1></div>", unsafe_allow_html=True)
        if st.button("DATABASE HARIAN", key="d_db"): st.toast("Segera Hadir")

elif st.session_state.page == 'pilih_analisa':
    st.markdown("<h2 style='text-align:center; color:white; font-family:Orbitron;'>PILIH JENIS ANALISA</h2>", unsafe_allow_html=True)
    
    # Grid Menu 2x2
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>🧪</h1></div>", unsafe_allow_html=True)
        if st.button("ANALISA TETES", use_container_width=True):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'tetes'; st.rerun()
    with r1c2:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>🔬</h1></div>", unsafe_allow_html=True)
        if st.button("OPTICAL DENSITY TETES", use_container_width=True):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'od'; st.rerun()
            
    r2c1, r2c2 = st.columns(2)
    with r2c1:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>🍯</h1></div>", unsafe_allow_html=True)
        if st.button("ANALISA TSAI TETES", use_container_width=True):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'tsai'; st.rerun()
    with r2c2:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>💎</h1></div>", unsafe_allow_html=True)
        if st.button("ICUMSA GULA", use_container_width=True):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'icumsa'; st.rerun()

    # TOMBOL KEMBALI PANJANG (FULL WIDTH)
    st.markdown('<div class="btn-kembali-container">', unsafe_allow_html=True)
    if st.button("🔙 KEMBALI KE DASHBOARD", use_container_width=True):
        st.session_state.page = 'dashboard'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'analisa_lab':
    a_type = st.session_state.analisa_type
    
    # 1. ANALISA TETES
    if a_type == 'tetes':
        st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
        # Logika perhitungan Tetes (Brix, Pol, HK) tetap sama...
        st.info("Form Input Analisa Tetes Ready")

    # 2. OPTICAL DENSITY TETES
    elif a_type == 'od':
        st.markdown("<h2 style='text-align:center; color:#ff4b4b; font-family:Orbitron;'>🔬 OPTICAL DENSITY TETES</h2>", unsafe_allow_html=True)
        # Logika OD tetap sama...
        st.info("Form Input Optical Density Ready")

    # 3. ANALISA TSAI TETES (NEW)
    elif a_type == 'tsai':
        st.markdown("<h2 style='text-align:center; color:#ffcc00; font-family:Orbitron;'>🍯 ANALISA TSAI TETES</h2>", unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="hero-container" style="display:block;">', unsafe_allow_html=True)
            tc1, tc2 = st.columns(2)
            with tc1:
                berat_sampel = st.number_input("Berat Sampel (g)", value=5.0, format="%.4f")
                vol_labu = st.number_input("Volume Labu (ml)", value=250.0, format="%.1f")
                ml_titrasi = st.number_input("ml Titrasi (Fehling)", value=10.0, format="%.2f")
                factor_f = st.number_input("Faktor Fehling", value=0.05, format="%.4f")
                # Contoh Rumus Sederhana TSAI
                tsai_res = (factor_f * vol_labu * 100) / (berat_sampel * ml_titrasi)
            with tc2:
                st.markdown(f'<div class="card-result" style="border-color:#ffcc00;"><h1 style="color:#ffcc00; font-family:Orbitron;">{tsai_res:.3f}</h1><p>TOTAL SUGAR AS INVERT (%)</p></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # 4. ICUMSA GULA (NEW)
    elif a_type == 'icumsa':
        st.markdown("<h2 style='text-align:center; color:#ffffff; font-family:Orbitron;'>💎 ICUMSA GULA</h2>", unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="hero-container" style="display:block;">', unsafe_allow_html=True)
            ic1, ic2 = st.columns(2)
            with ic1:
                abs_420 = st.number_input("Absorbansi (420 nm)", value=0.150, format="%.3f")
                brix_ic = st.number_input("Brix Larutan", value=50.0, format="%.1f")
                tebal_cuvet = st.number_input("Tebal Cuvet (cm)", value=1.0, format="%.1f")
                bj_ic = hitung_interpolasi(brix_ic, data_bj)
                # Rumus ICUMSA: (Abs / (Brix * BJ * Tebal)) * 100.000
                icumsa_res = (abs_420 / (brix_ic * bj_ic * tebal_cuvet)) * 100000
            with ic2:
                st.markdown(f'<div class="card-result" style="border-color:#ffffff;"><h1 style="color:#ffffff; font-family:Orbitron;">{icumsa_res:.0f}</h1><p>IU (ICUMSA UNIT)</p></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # TOMBOL KEMBALI PANJANG (FULL WIDTH)
    st.markdown('<div class="btn-kembali-container">', unsafe_allow_html=True)
    if st.button("🔙 KEMBALI KE MENU PILIHAN", use_container_width=True):
        st.session_state.page = 'pilih_analisa'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
