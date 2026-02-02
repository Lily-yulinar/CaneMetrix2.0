import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh

# 1. Konfigurasi Halaman
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

# 2. Jam Realtime (Ngedetik terus)
st_autorefresh(interval=1000, key="datarefresh")

tz = pytz.timezone('Asia/Jakarta')
now = datetime.datetime.now(tz)
tgl_skrg = now.strftime("%d %B %Y")
jam_skrg = now.strftime("%H:%M:%S")

# 3. CSS Maut - Fokus Bikin Judul "NENDANG"
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Poppins:wght@400;700&display=swap');

    /* Background dengan Overlay lebih gelap dikit biar Judul Pop Up */
    .stApp {
        background: linear-gradient(rgba(0, 10, 30, 0.8), rgba(0, 10, 30, 0.8)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* JUDUL YANG POP UP (NEON EFFECT) */
    .main-title {
        font-family: 'Orbitron', sans-serif;
        color: #ffffff;
        font-size: 110px; /* Tambah gede */
        font-weight: 900; /* Paling tebel */
        letter-spacing: 20px;
        text-align: center;
        margin-top: -20px;
        margin-bottom: 0px;
        /* Efek Glow & Shadow biar muncul ke depan */
        text-shadow: 
            0 0 10px rgba(255, 255, 255, 0.8),
            0 0 20px rgba(0, 255, 255, 0.5),
            5px 5px 15px rgba(0, 0, 0, 0.9);
    }

    .sub-title {
        color: #26c4b9;
        text-align: center;
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-style: italic;
        font-size: 24px;
        letter-spacing: 5px;
        margin-bottom: 50px;
        text-transform: uppercase;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    /* Container Logo Perusahaan */
    .logo-box {
        background: rgba(255, 255, 255, 0.9); /* Putih bersih biar logo keliatan */
        padding: 10px 20px;
        border-radius: 15px;
        display: flex;
        align-items: center;
        gap: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    .logo-img {
        height: 45px;
        width: auto;
    }

    /* Submenu Card */
    .menu-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        color: white;
        height: 230px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: 0.4s;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .menu-card:hover {
        background: rgba(38, 196, 185, 0.4);
        transform: translateY(-10px);
        border: 1px solid #26c4b9;
    }

    .menu-icon { font-size: 70px; margin-bottom: 10px; }
    .menu-text { font-size: 18px; font-weight: 700; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# 4. Header: Logo & Waktu
col_l, col_r = st.columns([2, 1])

with col_l:
    # Ganti link src dengan file lokal lo kalau udah diupload ke GitHub
    st.markdown("""
        <div class="logo-box">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Logo_PTPN_III_%28Persero%29.svg/1200px-Logo_PTPN_III_%28Persero%29.svg.png" class="logo-img">
            <img src="https://sgn.co.id/assets/img/logo-sgn.png" class="logo-img">
            <span style="color: #333; font-weight: bold; font-family: sans-serif;">PARTNERS</span>
        </div>
    """, unsafe_allow_html=True)

with col_r:
    st.selectbox("", ["SHIFT 1", "SHIFT 2", "SHIFT 3"], label_visibility="collapsed")
    st.markdown(f"""
        <div style="text-align: right; color: white; font-family: 'Poppins';">
            <span style="font-size: 18px; font-weight: bold;">{tgl_skrg}</span><br>
            <span style="font-size: 26px; color: #26c4b9; font-weight: bold;">{jam_skrg} WIB</span>
        </div>
    """, unsafe_allow_html=True)

# 5. Judul Utama (The Big Pop Up!)
st.markdown('<p style="text-align: center; color: white; margin-top: 50px; font-weight: 600; letter-spacing: 3px;">Welcome, Planters!</p>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">CANE METRIX</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Accelerating QA Performance</p>', unsafe_allow_html=True)

# 6. Grid Menu (3 Kolom)
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
                <div class="menu-icon">{icon}</div>
                <div class="menu-text">{text}</div>
            </div>
        """, unsafe_allow_html=True)

# 7. Status Footer
st.markdown(f"""
    <div style="background: linear-gradient(90deg, #26c4b9, #1a4a7a); padding: 15px; border-radius: 15px; text-align: center; color: white; font-weight: bold; font-size: 22px; margin-top:30px;">
        Jumlah sampel masuk hari ini: 45
    </div>
    """, unsafe_allow_html=True)
