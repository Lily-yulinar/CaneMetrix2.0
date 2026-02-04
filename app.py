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

# --- 3. DATABASE TABEL ---
data_koreksi = {
    27: -0.05, 28: 0.02, 29: 0.09, 30: 0.16, 31: 0.24, 
    32: 0.315, 33: 0.385, 34: 0.465, 35: 0.54, 36: 0.62,
    37: 0.70, 38: 0.78, 39: 0.86, 40: 0.94
}

data_bj = {
    0.0: 0.996373, 8.8: 1.031047, 10.0: 1.035950, 15.0: 1.056841, 
    20.0: 1.078497, 23.9: 1.095939, 50.0: 1.2320 # Standar BJ d27,5
}

# Mapping Tabel TSAI (Titran ke mg Gula Reduksi)
data_tsai_titran = {
    22.4: 225.10, 22.5: 223.60, 22.6: 222.78, 23.0: 222.20,
    25.0: 204.90, 30.0: 171.70, 37.7: 136.67
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

# --- 4. CSS (DASHBOARD & FULL WIDTH BUTTON) ---
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
    }}

    div.stButton > button:hover {{
        background: rgba(38, 196, 185, 0.2) !important;
        border-color: #26c4b9 !important;
        transform: translateY(-8px) !important;
    }}
    
    /* Style khusus tombol KEMBALI agar panjang kebawah */
    .btn-kembali div.stButton > button {{
        height: 60px !important;
        margin-top: 20px !important;
        background: rgba(255, 75, 75, 0.1) !important;
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
    with col_h2: jam_realtime()

    st.markdown(f'''<div class="hero-container">
        <div><h1 style="font-family:Orbitron; color:white; font-size:55px; margin:0;">CANE METRIX</h1>
        <p style="color:#26c4b9; font-family:Poppins; font-weight:700; letter-spacing:5px;">ACCELERATING QA PERFORMANCE</p></div>
        <img src="data:image/png;base64,{logo_cane}" style="height:150px;">
    </div>''', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<h1 style='text-align:center; margin-bottom:-55px;'>📝</h1>", unsafe_allow_html=True)
        if st.button("INPUT DATA", key="d1"): st.toast("Segera Hadir")
    with c2:
        st.markdown("<h1 style='text-align:center; margin-bottom:-55px;'>🧮</h1>", unsafe_allow_html=True)
        if st.button("HITUNG ANALISA", key="d2"): 
            st.session_state.page = 'pilih_analisa'; st.rerun()
    with c3:
        st.markdown("<h1 style='text-align:center; margin-bottom:-55px;'>📅</h1>", unsafe_allow_html=True)
        if st.button("DATABASE HARIAN", key="d3"): st.toast("Segera Hadir")

elif st.session_state.page == 'pilih_analisa':
    st.markdown("<h2 style='text-align:center; color:white; font-family:Orbitron;'>PILIH JENIS ANALISA</h2>", unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    with m1:
        if st.button("🧪 ANALISA TETES"):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'tetes'; st.rerun()
        if st.button("🍯 ANALISA TSAI TETES"):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'tsai'; st.rerun()
    with m2:
        if st.button("🔬 OPTICAL DENSITY TETES"):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'od'; st.rerun()
        if st.button("💎 ICUMSA GULA"):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'icumsa'; st.rerun()
    
    st.markdown('<div class="btn-kembali">', unsafe_allow_html=True)
    if st.button("🔙 KEMBALI KE DASHBOARD"):
        st.session_state.page = 'dashboard'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'analisa_lab':
    # --- PROSES ANALISA ---
    if st.session_state.analisa_type == 'tetes':
        st.markdown("<h2 style='color:#26c4b9;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
        cx, cy = st.columns(2)
        with cx:
            bx_in = st.number_input("Brix Teramati", value=8.80, format="%.2f")
            sh_in = st.number_input("Suhu (°C)", value=28.0, format="%.1f")
            pol_baca = st.number_input("Pol Baca", value=11.00, format="%.2f")
            kor = hitung_interpolasi(sh_in, data_koreksi)
            bj = hitung_interpolasi(bx_in, data_bj)
            brix_akhir = (bx_in + kor) * 10
            pol_akhir = (0.286 * pol_baca) / bj * 10
            hk = (pol_akhir / brix_akhir * 100) if brix_akhir != 0 else 0
        with cy:
            st.markdown(f'<div class="card-result"><h1>{brix_akhir:.3f}</h1><p>% BRIX AKHIR</p></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card-result"><h1>{pol_akhir:.3f}</h1><p>% POL AKHIR</p></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card-result"><h1>{hk:.2f}</h1><p>HK</p></div>', unsafe_allow_html=True)

    elif st.session_state.analisa_type == 'tsai':
        st.markdown("<h2 style='color:#ffcc00;'>🍯 ANALISA TSAI TETES</h2>", unsafe_allow_html=True)
        cx, cy = st.columns(2)
        with cx:
            titran = st.number_input("Volume Titran (ml)", value=22.5, format="%.1f")
            faktor = st.number_input("Faktor Fehling (2025)", value=0.979, format="%.3f")
            mg_gula = hitung_interpolasi(titran, data_tsai_titran)
            tsai_res = mg_gula / 4
            st.info(f"Koreksi Tabel: {mg_gula} mg")
        with cy:
            st.markdown(f'<div class="card-result" style="border-color:#ffcc00;"><h1>{tsai_res:.3f}</h1><p>% TSAI TETES</p></div>', unsafe_allow_html=True)

    elif st.session_state.analisa_type == 'icumsa':
        st.markdown("<h2 style='color:white;'>💎 ICUMSA GULA</h2>", unsafe_allow_html=True)
        cx, cy = st.columns(2)
        with cx:
            abs_v = st.number_input("Absorbansi (Abs)", value=0.149, format="%.3f")
            brix_g = st.number_input("% Brix Gula", value=50.0, format="%.1f")
            bj_g = hitung_interpolasi(brix_g, data_bj)
            icu_res = (abs_v * 100000) / (brix_g * bj_g * 1.0)
        with cy:
            st.markdown(f'<div class="card-result" style="border-color:white;"><h1>{icu_res:.0f}</h1><p>ICUMSA UNIT (IU)</p></div>', unsafe_allow_html=True)

    elif st.session_state.analisa_type == 'od':
        st.markdown("<h2 style='color:#ff4b4b;'>🔬 OPTICAL DENSITY TETES</h2>", unsafe_allow_html=True)
        # ... (Logika OD dari codingan ACC lo) ...
        bx_od = st.number_input("Brix Teramati", value=8.80)
        abs_val = st.number_input("Abs", value=0.418)
        bj_od = hitung_interpolasi(bx_od, data_bj)
        st.markdown(f'<div class="card-result"><h1>{(abs_val * bj_od * 500):.3f}</h1><p>OD</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="btn-kembali">', unsafe_allow_html=True)
    if st.button("🔙 KEMBALI KE MENU PILIHAN"):
        st.session_state.page = 'pilih_analisa'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
