import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
import base64
import os

if 'page' not in st.session_state: st.session_state.page = 'dashboard'

# --- 1. SETUP HALAMAN ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")
st_autorefresh(interval=1000, key="datarefresh")

# Waktu & Jam
tz = pytz.timezone('Asia/Jakarta')
now = datetime.datetime.now(tz)
tgl_skrg = now.strftime("%d %B %Y")
jam_skrg = now.strftime("%H:%M:%S")

# Fungsi Logo
def get_base64_logo(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo_ptpn = get_base64_logo("ptpn.png")
logo_sgn = get_base64_logo("sgn.png")
logo_lpp = get_base64_logo("lpp.png")
logo_cane = get_base64_logo("canemetrix.png")

# --- 2. CSS DENGAN EFEK GLOW ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@300;400;700&display=swap');

    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.75), rgba(0, 10, 30, 0.75)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* Container Logo Partner */
    .partner-box {{
        background: rgba(255, 255, 255, 1);
        padding: 8px 20px;
        border-radius: 12px;
        display: inline-flex;
        align-items: center;
        gap: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}
    .img-partner {{ height: 35px; width: auto; }}

    /* Hero Box (Glassmorphism) */
    .hero-container {{
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 30px;
        padding: 25px;
        margin: 10px auto 30px auto;
        text-align: center;
        max-width: 90%;
    }}

    .main-logo-cane {{
        height: 120px; 
        margin-bottom: -10px;
        filter: brightness(1.2) drop-shadow(0 0 15px rgba(38, 196, 185, 0.8));
    }}

    /* EFEK JUDUL GLOW */
    .title-text {{
        font-family: 'Orbitron'; 
        color: white;
        font-size: 65px; 
        letter-spacing: 12px; 
        margin: 0;
        font-weight: 900;
        /* Neon Glow Effect */
        text-shadow: 
            0 0 7px #fff,
            0 0 10px #fff,
            0 0 21px #fff,
            0 0 42px #26c4b9,
            0 0 82px #26c4b9,
            0 0 92px #26c4b9,
            0 0 102px #26c4b9,
            0 0 151px #26c4b9;
    }}

    .sub-text {{
        color: #26c4b9; 
        font-family: 'Poppins';
        font-weight: 700; 
        font-size: 18px; 
        letter-spacing: 5px;
        margin-top: 5px;
        text-transform: uppercase;
    }}

    /* Menu Cards */
    .menu-card {{
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(10px);
        padding: 25px 10px;
        border-radius: 20px;
        text-align: center;
        color: white;
        height: 180px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: 0.3s ease-in-out;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        margin-bottom: 20px;
    }}
    .menu-card:hover {{
        background: rgba(38, 196, 185, 0.2);
        transform: translateY(-8px);
        border: 1px solid #26c4b9;
        box-shadow: 0 0 20px rgba(38, 196, 185, 0.4);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. TAMPILAN HEADER ---
c1, c2 = st.columns([2, 1])
with c1:
    st.markdown(f"""
        <div class="partner-box">
            <img src="data:image/png;base64,{logo_ptpn}" class="img-partner">
            <img src="data:image/png;base64,{logo_sgn}" class="img-partner">
            <img src="data:image/png;base64,{logo_lpp}" class="img-partner">
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.selectbox("", ["SHIFT 1", "SHIFT 2", "SHIFT 3"], label_visibility="collapsed")
    st.markdown(f"""
        <div style="text-align: right; color: white; font-family: 'Poppins';">
            <span style="font-size: 14px; opacity: 0.7;">{tgl_skrg}</span><br>
            <span style="font-size: 24px; color: #26c4b9; font-weight: bold;">{jam_skrg} WIB</span>
        </div>
    """, unsafe_allow_html=True)

# --- 4. HERO SECTION ---
st.markdown(f"""
    <div class="hero-container">
        <img src="data:image/png;base64,{logo_cane}" class="main-logo-cane">
        <h1 class="title-text">CANE METRIX</h1>
        <p class="sub-text">Accelerating QA Performance</p>
    </div>
""", unsafe_allow_html=True)

# --- 5. GRID MENU ---
if st.button("🧮\n\nHITUNG"):
    st.session_state.page = 'analisa_tetes'
    st.rerun()
    
]

for i in range(0, len(items), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(items):
            icon, text = items[i+j]
            with cols[j]:
                st.markdown(f"""
                    <div class="menu-card">
                        <div style="font-size: 50px; margin-bottom: 10px;">{icon}</div>
                        <div style="font-size: 16px; font-weight: 700; letter-spacing: 1px;">{text.upper()}</div>
                    </div>
                """, unsafe_allow_html=True)

# --- 1. DATA TABEL KOREKSI SUHU (GAMBAR 4) ---
# Gue masukin data dari foto lo ya Beb
data_koreksi = {
    25: -0.19, 26: -0.12, 27: -0.05, 28: 0.02, 29: 0.09, 30: 0.16,
    31: 0.24, 32: 0.31, 33: 0.38, 34: 0.46, 35: 0.54, 36: 0.62,
    37: 0.70, 38: 0.78, 39: 0.86, 40: 0.94, 41: 1.02, 42: 1.10,
    43: 1.18, 44: 1.26, 45: 1.34, 46: 1.42, 47: 1.50, 48: 1.58,
    49: 1.66, 50: 1.72
}

# --- 2. FUNGSI INTERPOLASI ---
def hitung_interpolasi(suhu_user):
    suhu_keys = sorted(data_koreksi.keys())
    
    # Kalau suhu pas ada di tabel
    if suhu_user in data_koreksi:
        return data_koreksi[suhu_user]
    
    # Kalau di luar range tabel
    if suhu_user < suhu_keys[0]: return data_koreksi[suhu_keys[0]]
    if suhu_user > suhu_keys[-1]: return data_koreksi[suhu_keys[-1]]
    
    # Cari tetangga atas dan bawah (Interpolasi Linear)
    for i in range(len(suhu_keys) - 1):
        x0, x1 = suhu_keys[i], suhu_keys[i+1]
        if x0 < suhu_user < x1:
            y0, y1 = data_koreksi[x0], data_koreksi[x1]
            # Rumus: y = y0 + (x - x0) * (y1 - y0) / (x1 - x0)
            return y0 + (suhu_user - x0) * (y1 - y0) / (x1 - x0)

# --- 3. FUNGSI TAMPILAN ANALISA TETES ---
def show_analisa_tetes():
    st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>🧪 PERHITUNGAN ANALISA TETES</h2>", unsafe_allow_html=True)
    
    # Wadah Input & Output
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📥 INPUT")
        brix_obs = st.number_input("Brix Teramati", value=8.80, step=0.01, format="%.2f")
        suhu_obs = st.number_input("Suhu Teramati (°C)", value=28.3, step=0.1, format="%.1f")
        
        koreksi = hitung_interpolasi(suhu_obs)
        st.success(f"Koreksi Suhu (Interpolasi): {koreksi:+.3f}")

    with col2:
        st.markdown("### 📤 OUTPUT")
        # Logika: (Brix x 10) + Koreksi
        brix_pencengeraan = brix_obs * 10
        brix_akhir = brix_pencengeraan + koreksi
        
        st.markdown(f"""
            <div style="background: rgba(38, 196, 185, 0.2); padding: 20px; border-radius: 15px; border: 2px solid #26c4b9; text-align: center;">
                <p style="margin:0; font-family:Poppins; opacity:0.8;">Brix Pengenceran (x10): <b>{brix_pencengeraan:.2f}</b></p>
                <hr style="border-color: rgba(255,255,255,0.1);">
                <h4 style="margin:0; font-family:Poppins;">% BRIX AKHIR</h4>
                <h1 style="margin:0; color:#26c4b9; font-family:Orbitron; font-size:45px; text-shadow: 0 0 10px #26c4b9;">{brix_akhir:.3f}</h1>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔙 KEMBALI KE DASHBOARD"):
        st.session_state.page = 'dashboard'
        st.rerun()
        

if st.session_state.page == 'dashboard':
    # (Isi kodingan Dashboard lo yang lama)
elif st.session_state.page == 'analisa_tetes':
    show_analisa_tetes()
