import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh

# 1. Setting Halaman
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

# 2. Jam Realtime (Update tiap 1 detik)
st_autorefresh(interval=1000, key="datarefresh")

# Konfigurasi Waktu WIB
tz = pytz.timezone('Asia/Jakarta')
now = datetime.datetime.now(tz)
tgl_skrg = now.strftime("%d %B %Y")
jam_skrg = now.strftime("%H:%M:%S")

# 3. CSS Maut (Background Lab Baru & Font Orbitron)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Poppins:wght@400;600&display=swap');

    /* Background Lab Baru - Overlay Biru Gelap Transparan */
    .stApp {
        background: linear-gradient(rgba(0, 30, 60, 0.7), rgba(0, 30, 60, 0.7)), 
        url("https://images.unsplash.com/photo-1581093458791-9f3c3900df4b?q=80&w=2070");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Judul Raksasa ala Gambar 2 */
    .main-title {
        font-family: 'Orbitron', sans-serif;
        color: #ffffff;
        font-size: 90px; 
        font-weight: 700;
        letter-spacing: 20px;
        text-align: center;
        margin: 0;
        text-shadow: 0px 0px 25px rgba(0, 255, 255, 0.8);
    }

    /* Submenu Card - Lebih Proporsional */
    .menu-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        color: white;
        font-family: 'Poppins', sans-serif;
        margin-bottom: 25px;
        height: 220px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: 0.3s ease-in-out;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .menu-card:hover {
        background: rgba(38, 196, 185, 0.4);
        transform: translateY(-8px);
        border: 1px solid #26c4b9;
    }

    /* Icon Gede & Teks Font Sedang */
    .menu-icon {
        font-size: 75px; 
        margin-bottom: 15px;
    }
    
    .menu-text {
        font-size: 18px; 
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. Header Section
col_l, col_r = st.columns([2, 1])

with col_l:
    # Space untuk Logo yang bakal lo upload
    st.markdown('<p style="color:white; font-weight:bold; opacity:0.6;">[ LOGO UPLOAD SPACE ]</p>', unsafe_allow_html=True)

with col_r:
    shift = st.selectbox("", ["SHIFT 1", "SHIFT 2", "SHIFT 3"], label_visibility="collapsed")
    st.markdown(f"""
        <div style="text-align: right; color: white; font-family: 'Poppins';">
            <span style="font-size: 18px;">{tgl_skrg}</span><br>
            <span style="font-size: 26px; color: #26c4b9; font-weight: bold;">{jam_skrg} WIB</span>
        </div>
    """, unsafe_allow_html=True)

# 5. Judul Utama
st.markdown('<p style="text-align: center; color: white; margin-top: 30px; opacity:0.8;">Welcome, Planters!</p>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">CANE METRIX</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#26c4b9; text-align:center; font-style:italic; font-size:22px; margin-bottom:50px;">Accelerating QA Performance</p>', unsafe_allow_html=True)

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
    <div style="background: linear-gradient(90deg, #26c4b9, #1a4a7a); padding: 15px; border-radius: 15px; text-align: center; color: white; font-weight: bold; font-size: 22px; margin-top:30px; box-shadow: 0 10px 20px rgba(0,0,0,0.3);">
        Jumlah sampel masuk hari ini: 45
    </div>
    """, unsafe_allow_html=True)
