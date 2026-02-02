import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
import base64
import os

# --- KONFIGURASI ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")
st_autorefresh(interval=1000, key="datarefresh")

tz = pytz.timezone('Asia/Jakarta')
now = datetime.datetime.now(tz)
tgl_skrg = now.strftime("%d %B %Y")
jam_skrg = now.strftime("%H:%M:%S")

def get_base64_logo(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo_ptpn = get_base64_logo("ptpn.png")
logo_sgn = get_base64_logo("sgn.png")
logo_lpp = get_base64_logo("lpp.png")
logo_cane = get_base64_logo("canemetrix.png")

# --- CSS SLIM & BRIGHT ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Poppins:wght@400;700&display=swap');

    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.8), rgba(0, 10, 30, 0.8)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* Container Logo Partner (Compact & Bright) */
    .partner-box {{
        background: rgba(255, 255, 255, 0.95);
        padding: 8px 20px;
        border-radius: 15px;
        display: inline-flex;
        align-items: center;
        gap: 20px;
        box-shadow: 0 4px 15px rgba(255,255,255,0.2);
    }}
    .img-partner {{ height: 45px; width: auto; }}

    /* KOTAK JUDUL (Slimmer & Brighter) */
    .hero-container {{
        background: rgba(255, 255, 255, 0.15); /* Lebih terang Beb */
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 30px;
        padding: 30px 20px; /* Padding dikecilin biar slim */
        margin: 10px auto 30px auto; /* Margin atas-bawah dikecilin */
        max-width: 90%;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.4);
    }}

    /* Jarak Logo ke Judul Dideketin */
    .main-logo-cane {{
        height: 160px; /* Dikecilin dikit biar nggak menuhin kotak */
        margin-bottom: -10px; /* Efek merapat ke judul */
        filter: drop-shadow(0 0 15px rgba(255,255,255,0.5));
    }}

    .title-text {{
        font-family: 'Orbitron'; color: white;
        font-size: 70px; /* Sikit lebih kecil biar proporsional */
        letter-spacing: 12px;
        margin: 0;
        text-shadow: 0 0 20px rgba(38, 196, 185, 0.8);
    }}

    .sub-text {{
        color: #26c4b9; font-family: 'Poppins';
        font-weight: 700; font-size: 18px; letter-spacing: 6px;
        margin-top: -5px;
    }}

    /* MENU CARDS */
    .menu-card {{
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        padding: 30px 15px;
        border-radius: 25px;
        text-align: center;
        color: white;
        height: 220px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: 0.4s;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
    }}
    .menu-card:hover {{
        background: rgba(38, 196, 185, 0.25);
        transform: translateY(-8px);
        border: 1px solid #26c4b9;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
col_head_l, col_head_r = st.columns([2, 1])
with col_head_l:
    st.markdown(f"""
        <div class="partner-box">
            <img src="data:image/png;base64,{logo_ptpn}" class="img-partner">
            <img src="data:image/png;base64,{logo_sgn}" class="img-partner">
            <img src="data:image/png;base64,{logo_lpp}" class="img-partner">
        </div>
    """, unsafe_allow_html=True)

with col_head_r:
    st.selectbox("", ["SHIFT 1", "SHIFT 2", "SHIFT 3"], label_visibility="collapsed")
    st.markdown(f"""
        <div style="text-align: right; color: white; font-family: 'Poppins';">
            <span style="font-size: 16px; opacity: 0.8;">{tgl_skrg}</span><br>
            <span style="font-size: 28px; color: #26c4b9; font-weight: bold;">{jam_skrg} WIB</span>
        </div>
    """, unsafe_allow_html=True)

# --- HERO SECTION (Slim & Compact) ---
st.markdown(f"""
    <div class="hero-container">
        <img src="data:image/png;base64,{logo_cane}" class="main-logo-cane">
        <h1 class="title-text">CANE METRIX</h1>
        <p class="sub-text">Accelerating QA Performance</p>
    </div>
""", unsafe_allow_html=True)

# --- SUB-MENU GRID ---
m1, m2, m3 = st.columns(3)
items = [
    ("📝", "Input Data"), ("📅", "Database Harian"), ("📊", "Database Bulanan"),
    ("⚖️", "Rekap Stasiun"), ("🧮", "Hitung"), ("👤", "Akun"),
    ("📈", "Trend"), ("⚙️", "Pengaturan"), ("📥", "Export Data")
]

for i, (icon, text) in enumerate(items):
    with [m1, m2, m3][i % 3]:
        st.markdown(f"""
            <div class="menu-card">
                <div style="font-size: 60px; margin-bottom: 10px;">{icon}</div>
                <div style="font-size: 18px; font-weight: 700; letter-spacing: 2px;">{text.upper()}</div>
            </div>
        """, unsafe_allow_html=True)
        st.write("")
