import streamlit as st
import datetime
import time

# 1. Konfigurasi Halaman
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

# 2. CSS Canggih (Background Lab, Font Orbitron, & Styling)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto:wght@400;700&display=swap');

    /* Background lab transparan */
    .stApp {
        background: linear-gradient(rgba(10, 40, 70, 0.7), rgba(10, 40, 70, 0.7)), 
        url("https://images.unsplash.com/photo-1581093588401-fbb62a02f120?q=80&w=2070");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Judul ala Gambar 2 */
    .main-title {
        font-family: 'Orbitron', sans-serif;
        color: white;
        font-size: 60px;
        font-weight: 700;
        letter-spacing: 12px;
        text-align: center;
        margin-top: 10px;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }

    .sub-title {
        font-family: 'Roboto', sans-serif;
        color: #26c4b9;
        text-align: center;
        font-style: italic;
        margin-bottom: 30px;
        font-size: 20px;
    }

    /* Card Sub Menu - Font Gede & Menarik */
    .menu-card {
        background: rgba(122, 184, 225, 0.9); /* Transparansi biar estetik */
        padding: 35px 20px;
        border-radius: 20px;
        text-align: center;
        color: #ffffff;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        font-size: 24px; /* Font lebih gede */
        margin-bottom: 25px;
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        border: 2px solid rgba(255,255,255,0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: 0.3s;
    }
    
    .menu-card:hover {
        background: #26c4b9;
        transform: translateY(-10px);
        box-shadow: 0 12px 40px 0 rgba(38, 196, 185, 0.5);
    }

    /* Header Info */
    .header-info {
        color: white;
        font-family: 'Roboto', sans-serif;
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Fitur Jam & Kalender Realtime (Placeholder)
# Note: Realtime detik di web butuh sedikit trik JavaScript, 
# tapi ini versi Python yang update tiap refresh/interaksi.
now = datetime.datetime.now()
tgl_skrg = now.strftime("%d %B %Y")
jam_skrg = now.strftime("%H:%M:%S WIB")

# 4. Header Section
col_head1, col_head2 = st.columns([2, 1])

with col_head1:
    st.markdown('<p class="header-info">Welcome, Planters!</p>', unsafe_allow_html=True)
with col_head2:
    # Opsi Shift (Pake Selectbox biar fungsional)
    shift = st.selectbox("", ["SHIFT 1", "SHIFT 2", "SHIFT 3"], index=0)
    st.markdown(f'<p style="color:white; text-align:right; font-weight:bold;">{tgl_skrg}<br>{jam_skrg}</p>', unsafe_allow_html=True)

st.markdown('<h1 class="main-title">CANE METRIX</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Accelerating QA Performance</p>', unsafe_allow_html=True)

# 5. Grid Menu dengan Komposisi Warna Setara
# Kita bagi jadi 3 kolom
c1, c2, c3 = st.columns(3)

menu_items = [
    ("📝", "INPUT DATA"), ("📅", "DATABASE HARIAN"), ("📊", "DATABASE BULANAN"),
    ("⚖️", "REKAP STASIUN"), ("🧮", "HITUNG"), ("👤", "AKUN"),
    ("📈", "TREND"), ("⚙️", "PENGATURAN"), ("📥", "EXPORT DATA")
]

for i, (icon, text) in enumerate(menu_items):
    with [c1, c2, c3][i % 3]:
        st.markdown(f'<div class="menu-card">{icon}<br><br>{text}</div>', unsafe_allow_html=True)

# 6. Footer Status
st.markdown("---")
st.markdown("""
    <div style="background-color: #26c4b9; padding: 15px; border-radius: 15px; text-align: center; color: white; font-weight: bold; font-size: 22px;">
        Jumlah sampel masuk hari ini: *45
    </div>
    """, unsafe_allow_html=True)
