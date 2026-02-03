import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
import base64
import os
import numpy as np

# --- 1. CONFIG & STATE ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

# --- 2. DATA KOREKSI SUHU (LENGKAP DARI FOTO LO) ---
# Gue masukin manual sesuai gambar tabel yang lo kirim
data_koreksi = {
    25: -0.19, 26: -0.12, 27: -0.05, 28: 0.02, 29: 0.09,
    30: 0.16, 31: 0.24, 32: 0.31, 33: 0.38, 34: 0.46,
    35: 0.54, 36: 0.62, 37: 0.70, 38: 0.78, 39: 0.86,
    40: 0.94, 41: 1.02, 42: 1.10, 43: 1.18, 44: 1.26,
    45: 1.34, 46: 1.42, 47: 1.50, 48: 1.58, 49: 1.66, 50: 1.72
}

def hitung_koreksi(suhu_input):
    s_list = sorted(data_koreksi.keys())
    k_list = [data_koreksi[s] for s in s_list]
    return float(np.interp(suhu_input, s_list, k_list))

# --- 3. CSS (LOGOS & GLASS UI) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Michroma&family=Poppins:wght@400;700;900&display=swap');
    .stApp { background: #000a1e; }
    
    .logo-container {
        background: white; padding: 10px 30px; border-radius: 12px;
        display: flex; align-items: center; gap: 20px; width: fit-content;
    }
    .logo-container img { height: 35px; width: auto; }
    
    .jam-box { text-align: right; color: white; font-family: 'Poppins'; }
    .jam-digital { color: #26c4b9; font-size: 32px; font-weight: 900; }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px);
        padding: 30px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* STYLE BUTTON AGAR BISA DI-KLIK JELAS */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important; border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 20px !important; height: 150px !important; width: 100% !important;
        font-size: 18px !important; font-weight: 700 !important; transition: 0.3s;
    }
    div.stButton > button:hover { border-color: #26c4b9 !important; background: rgba(38,196,185,0.2) !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. HEADER ---
c_head1, c_head2 = st.columns([10, 3])
with c_head1:
    # Logo Box (Gue pakai placeholder kalau file ga ada biar ga error)
    st.markdown('<div class="logo-container"><b>PARTNER LOGOS HERE</b></div>', unsafe_allow_html=True)

with c_head2:
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.datetime.now(tz)
    st.markdown(f'''
        <div class="jam-box">
            <div style="opacity:0.7;">{now.strftime("%d %B %Y")}</div>
            <div class="jam-digital">{now.strftime("%H:%M:%S")} WIB</div>
        </div>''', unsafe_allow_html=True)

st_autorefresh(interval=1000, key="timer")

# --- 5. LOGIKA NAVIGASI ---

if st.session_state.page == 'dashboard':
    st.markdown('<div class="glass-card" style="margin-top:20px;">'
                '<h1 style="font-family:Michroma; color:white; letter-spacing:5px;">CANE METRIX</h1>'
                '<p style="color:#26c4b9; font-weight:700;">ACCELERATING QA PERFORMANCE</p></div>', unsafe_allow_html=True)
    
    m1, m2, m3 = st.columns(3)
    with m1:
        if st.button("📝\nINPUT DATA", key="m1"):
            st.session_state.page = 'input'
            st.rerun()
    with m2:
        if st.button("🧮\nHITUNG ANALISA", key="m2"):
            st.session_state.page = 'analisa'
            st.rerun()
    with m3:
        if st.button("📅\nDATABASE HARIAN", key="m3"):
            st.session_state.page = 'db'
            st.rerun()

elif st.session_state.page == 'analisa':
    st.markdown("<h2 style='color:white; font-family:Michroma;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        L, R = st.columns(2)
        with L:
            st.write("### Input Data")
            b_obs = st.number_input("Brix Teramati", value=8.5, step=0.01, format="%.2f")
            b_pengenceran = b_obs * 10
            st.info(f"Brix Pengenceran (x10): {b_pengenceran:.2f}")
            suhu = st.number_input("Suhu (°C)", min_value=25.0, max_value=50.0, value=28.0)
            
        with R:
            st.write("### Hasil")
            koreksi = hitung_koreksi(suhu)
            b_akhir = b_pengenceran + koreksi
            st.markdown(f"""
                <div style="background:rgba(38,196,185,0.2); padding:30px; border-radius:20px; border:2px solid #26c4b9; text-align:center;">
                    <small style="color:white;">% BRIX AKHIR</small>
                    <h1 style="color:white; font-size:70px; margin:0;">{b_akhir:.2f}</h1>
                    <p style="color:#26c4b9; margin:0;">Koreksi Suhu: {koreksi:+.2f}</p>
                </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔙 KEMBALI"):
        st.session_state.page = 'dashboard'
        st.rerun()

# Halaman lain (Placeholder biar ga error)
elif st.session_state.page in ['input', 'db']:
    st.write("Halaman sedang dikembangkan")
    if st.button("🔙 KEMBALI"):
        st.session_state.page = 'dashboard'
        st.rerun()
