import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh

# 1. Konfigurasi Halaman
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

# 2. Jam Realtime (Ngedetik per 1 detik)
st_autorefresh(interval=1000, key="datarefresh")

tz = pytz.timezone('Asia/Jakarta')
now = datetime.datetime.now(tz)
tgl_skrg = now.strftime("%d %B %Y")
jam_skrg = now.strftime("%H:%M:%S")

# 3. CSS Kustom: Kotak Judul & Glow
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Poppins:wght@400;700&display=swap');

    /* Background Lab */
    .stApp {
        background: linear-gradient(rgba(0, 10, 30, 0.75), rgba(0, 10, 30, 0.75)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* KOTAK JUDUL (Glassmorphism Container) */
    .title-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 30px;
        padding: 40px;
        margin: 20px auto 50px auto;
        max-width: 90%;
        text-align: center;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
    }

    .main-title {
        font-family: 'Orbitron', sans-serif;
        color: #ffffff;
        font-size: 85px; 
        font-weight: 900;
        letter-spacing: 15px;
        margin: 0;
        text-shadow: 0 0 20px rgba(0, 255, 255, 0.6);
        text-transform: uppercase;
    }

    .sub-title {
        color: #26c4b9;
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 22px;
        letter-spacing: 8px;
        margin-top: 10px;
        text-transform: uppercase;
    }

    /* Logo Box di Kiri Atas */
    .partner-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 10px 20px;
        border-radius: 15px;
        display: inline-flex;
        align-items: center;
        gap: 15px;
    }

    .logo-img { height: 40px; }

    /* Menu Card */
    .menu-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        color: white;
        height: 220px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: 0.4s;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .menu-card:hover {
        background: rgba(38, 196, 185, 0.3);
        transform: translateY(-10px);
        border: 1px solid #26c4b9;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. Header: Logo & Time
col_l, col_r = st.columns([2, 1])
with col_l:
    st.markdown("""
        <div class="partner-container">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Logo_PTPN_III_%28Persero%29.svg/1200px-Logo_PTPN_III_%28Persero%29.svg.png" class="logo-img">
            <img src="https://sgn.co.id/assets/img/logo-sgn.png" class="logo-img">
            <b style="color: #333; font-family: sans-serif; font-size: 14px;">PARTNERS</b>
        </div>
    """, unsafe_allow_html=True)

with col_r:
    st.selectbox("", ["SHIFT 1", "SHIFT 2", "SHIFT 3"], label_visibility="collapsed")
    st.markdown(f"""
        <div style="text-align: right; color: white; font-family: 'Poppins';">
            <span style="font-size: 18px;">{tgl_skrg}</span><br>
            <span style="font-size: 26px; color: #26c4b9; font-weight: bold;">{jam_skrg} WIB</span>
        </div>
    """, unsafe_allow_html=True)

# 5. JUDUL DALAM KOTAK (Ini yang lo mau Beb!)
st.markdown("""
    <div class="title-container">
        <p style="color: white; opacity: 0.7; letter-spacing: 3px; margin-bottom: 5px;">Welcome, Planters!</p>
        <h1 class="main-title">CANE METRIX</h1>
        <p class="sub-title">Accelerating QA Performance</p>
    </div>
""", unsafe_allow_html=True)

# 6. Grid Menu
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
                <div style="font-size: 70px; margin-bottom: 10px;">{icon}</div>
                <div style="font-size: 18px; font-weight: 700;">{text.upper()}</div>
            </div>
        """, unsafe_allow_html=True)

# 7. Footer
st.markdown(f"""
    <div style="background: linear-gradient(90deg, #26c4b9, #1a4a7a); padding: 15px; border-radius: 15px; text-align: center; color: white; font-weight: bold; font-size: 22px; margin-top:20px;">
        Jumlah sampel masuk hari ini: 45
    </div>
    """, unsafe_allow_html=True)
