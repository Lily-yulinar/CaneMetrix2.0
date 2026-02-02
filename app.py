import streamlit as st
import datetime
import pytz

# 1. Konfigurasi Halaman
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

# 2. CSS Koreksi Total (Background & Font)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Poppins:wght@400;600&display=swap');

    /* Background Lab Baru - Pastikan Link Ini Stabil */
    .stApp {
        background: linear-gradient(rgba(0, 20, 40, 0.7), rgba(0, 20, 40, 0.7)), 
        url("https://images.unsplash.com/photo-1532187875605-1807662899ad?q=80&w=2070");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Judul Super Gede */
    .main-title {
        font-family: 'Orbitron', sans-serif;
        color: #ffffff;
        font-size: 80px; 
        font-weight: 700;
        letter-spacing: 15px;
        text-align: center;
        margin: 0;
        text-shadow: 0px 0px 30px rgba(0, 255, 255, 0.6);
    }

    /* Card Sub Menu - Icon Gede & Transparan Blur */
    .menu-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        padding: 30px;
        border-radius: 25px;
        text-align: center;
        color: white;
        font-family: 'Poppins', sans-serif;
        margin-bottom: 25px;
        height: 220px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: 0.5s ease;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .menu-card:hover {
        background: rgba(38, 196, 185, 0.5);
        transform: scale(1.05);
        border: 1px solid #26c4b9;
    }

    .menu-icon {
        font-size: 70px; /* Icon Dibikin Gede Banget */
        margin-bottom: 15px;
    }
    
    .menu-text {
        font-size: 18px; 
        font-weight: 600;
        text-transform: uppercase;
    }

    /* Logo Perusahaan */
    .logo-img {
        height: 50px;
        margin: 0 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Logika Jam Realtime (WIB - Asia/Jakarta)
tz = pytz.timezone('Asia/Jakarta')
now = datetime.datetime.now(tz)
tgl_skrg = now.strftime("%d %B %Y")
jam_skrg = now.strftime("%H:%M:%S")

# 4. Header: Logo & Waktu
col_l, col_r = st.columns([2, 1])

with col_l:
    # Pakai placeholder logo jika file belum diupload ke github
    st.markdown("""
        <div style="display: flex; align-items: center; background: rgba(255,255,255,0.1); padding: 10px; border-radius: 10px; width: fit-content;">
            <span style="color: white; font-weight: bold; margin-right: 10px;">PARTNERS:</span>
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Logo_PTPN_III_%28Persero%29.svg/1200px-Logo_PTPN_III_%28Persero%29.svg.png" class="logo-img">
            <img src="https://sgn.co.id/assets/img/logo-sgn.png" class="logo-img">
        </div>
    """, unsafe_allow_html=True)

with col_r:
    shift = st.selectbox("", ["SHIFT 1", "SHIFT 2", "SHIFT 3"], label_visibility="collapsed")
    st.markdown(f"""
        <div style="text-align: right; color: white; font-family: 'Poppins';">
            <span style="font-size: 18px; font-weight: bold;">{tgl_skrg}</span><br>
            <span style="font-size: 22px; color: #26c4b9; font-weight: bold;">{jam_skrg} WIB</span>
        </div>
    """, unsafe_allow_html=True)

# 5. Body Utama
st.markdown('<p style="text-align: center; color: white; margin-bottom: 0;">Welcome, Planters!</p>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">CANE METRIX</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#26c4b9; text-align:center; font-style:italic; font-size:20px; margin-bottom:40px;">Accelerating QA Performance</p>', unsafe_allow_html=True)

# 6. Grid Menu
m1, m2, m3 = st.columns(3)

items = [
    ("📋", "Input Data"), ("📅", "Database Harian"), ("📊", "Database Bulanan"),
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

# 7. Status Bar
st.markdown(f"""
    <div style="background: linear-gradient(90deg, #26c4b9, #1a4a7a); padding: 15px; border-radius: 15px; text-align: center; color: white; font-weight: bold; font-size: 22px; margin-top:20px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        Jumlah sampel masuk hari ini: 45
    </div>
    <p style="text-align: center; color: rgba(255,255,255,0.5); font-size: 12px; margin-top: 10px;">CaneMetrix 2.0 &copy; 2026 | Server Status: Online</p>
    """, unsafe_allow_html=True)
