import streamlit as st
import datetime
import pytz
import base64
import os

# --- 1. CONFIG & STATE ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

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

# --- 3. DATABASE TABEL (DARI FOTO LO BEB) ---

# Tabel Koreksi Suhu
data_koreksi = {
    27: -0.05, 28: 0.02, 29: 0.09, 30: 0.16, 31: 0.24, 
    32: 0.315, 33: 0.385, 34: 0.465, 35: 0.54, 36: 0.62,
    37: 0.70, 38: 0.78, 39: 0.86, 40: 0.94
}

# Tabel Berat Jenis d27,5 (ICUMSA)
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

# --- 4. CSS (BALIK KE STYLE AWAL) ---
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
        display: inline-flex; align-items: center; gap: 15px;
    }}
    .header-logo-box img {{ height: 35px; width: auto; }}

    .hero-container {{
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 30px;
        padding: 40px; margin-bottom: 25px; display: flex; justify-content: space-between; align-items: center;
    }}

    /* Balikin Styling Tombol Sub-Menu Dashboard */
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
        box-shadow: 0 0 25px rgba(38, 196, 185, 0.4) !important;
        transform: translateY(-8px) !important;
    }}
    
    .card-result {{
        background: rgba(38, 196, 185, 0.1); padding: 30px; border-radius: 20px; 
        border: 2px solid #26c4b9; text-align: center; margin-bottom: 15px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. JAM REALTIME ---
@st.fragment(run_every="1s")
def jam_realtime():
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.datetime.now(tz)
    st.markdown(f"""
        <div style="text-align: right; color: white; font-family: 'Poppins';">
            {now.strftime("%d %B %Y")}<br>
            <span style="font-family:'Orbitron'; color:#26c4b9; font-size:24px; font-weight:bold;">
                {now.strftime("%H:%M:%S")} WIB
            </span>
        </div>
    """, unsafe_allow_html=True)

# --- 6. LOGIKA HALAMAN ---
if st.session_state.page == 'dashboard':
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown(f'''<div class="header-logo-box">
            <img src="data:image/png;base64,{logo_ptpn}"><img src="data:image/png;base64,{logo_sgn}">
            <img src="data:image/png;base64,{logo_lpp}"><img src="data:image/png;base64,{logo_kb}">
        </div>''', unsafe_allow_html=True)
    with c2: jam_realtime()

    st.markdown(f'''<div class="hero-container">
        <div>
            <h1 style="font-family:Orbitron; color:white; font-size:55px; margin:0;">CANE METRIX</h1>
            <p style="color:#26c4b9; font-family:Poppins; font-weight:700; letter-spacing:5px;">ACCELERATING QA PERFORMANCE</p>
        </div>
        <img src="data:image/png;base64,{logo_cane}" style="height:150px; filter:drop-shadow(0 0 15px #26c4b9);">
    </div>''', unsafe_allow_html=True)

    # Grid Menu Dashboard (Sesuai Dashboard Awal)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div style='text-align:center; margin-bottom:-50px; position:relative; z-index:10; pointer-events:none;'><h1>📝</h1></div>", unsafe_allow_html=True)
        if st.button("INPUT DATA", key="btn_input", use_container_width=True): st.toast("Segera hadir!")
    with col2:
        st.markdown("<div style='text-align:center; margin-bottom:-50px; position:relative; z-index:10; pointer-events:none;'><h1>🧮</h1></div>", unsafe_allow_html=True)
        if st.button("HITUNG ANALISA", key="btn_hitung", use_container_width=True):
            st.session_state.page = 'analisa_tetes'; st.rerun()
    with col3:
        st.markdown("<div style='text-align:center; margin-bottom:-50px; position:relative; z-index:10; pointer-events:none;'><h1>📅</h1></div>", unsafe_allow_html=True)
        if st.button("DATABASE HARIAN", key="btn_harian", use_container_width=True): st.toast("Segera hadir!")

elif st.session_state.page == 'analisa_tetes':
    st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="hero-container" style="display:block;">', unsafe_allow_html=True)
        cx, cy = st.columns(2)
        
        with cx:
            st.subheader("📥 Data Input Lab")
            bx_in = st.number_input("Brix Teramati", value=8.80, step=0.01, format="%.2f")
            sh_in = st.number_input("Suhu (°C)", value=28.3, step=0.1, format="%.1f")
            pol_baca = st.number_input("Pol Baca", value=11.00, step=0.01, format="%.2f")
            
            # --- LOGIKA HITUNG BEB ---
            kor = hitung_interpolasi(sh_in, data_koreksi)
            bj = hitung_interpolasi(bx_in, data_bj)
            
            brix_akhir = (bx_in + kor) * 10
            pol_akhir = (0.286 * pol_baca) / bj * 10
            hk = (pol_akhir / brix_akhir * 100) if brix_akhir != 0 else 0
            
            st.write("---")
            st.info(f"💡 Koreksi: {kor:+.3f} | BJ ICUMSA: {bj:.6f}")
            st.caption(f"Detail Brix: ({bx_in} + {kor:+.3f}) × 10")

        with cy:
            st.subheader("📊 Hasil Perhitungan")
            st.markdown(f'<div class="card-result"><h1 style="color:#26c4b9; font-size:50px; font-family:Orbitron; margin:0;">{brix_akhir:.3f}</h1><p style="color:white; margin:0;">% BRIX AKHIR</p></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card-result" style="border-color:#ffcc00; background:rgba(255,204,0,0.1);"><h1 style="color:#ffcc00; font-size:50px; font-family:Orbitron; margin:0;">{pol_akhir:.3f}</h1><p style="color:white; margin:0;">% POL AKHIR</p></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card-result" style="border-color:#ff4b4b; background:rgba(255,75,75,0.1);"><h1 style="color:#ff4b4b; font-size:50px; font-family:Orbitron; margin:0;">{hk:.2f}</h1><p style="color:white; margin:0;">HARKAT KEMURNIAN (HK)</p></div>', unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔙 KEMBALI KE DASHBOARD", use_container_width=True):
        st.session_state.page = 'dashboard'; st.rerun()
