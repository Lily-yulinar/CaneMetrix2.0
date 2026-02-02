import streamlit as st
import datetime
import pytz # Tambahkan ini di requirements.txt nanti

# 1. Konfigurasi Halaman
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

# 2. CSS untuk Tampilan Mewah
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Poppins:wght@400;600&display=swap');

    /* Background Lab Baru yang lebih tajam */
    .stApp {
        background: linear-gradient(rgba(0, 20, 40, 0.6), rgba(0, 20, 40, 0.6)), 
        url("https://images.unsplash.com/photo-1579152276508-4903328e469c?q=80&w=2070");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Judul Super Gede ala Gambar 2 */
    .main-title {
        font-family: 'Orbitron', sans-serif;
        color: #ffffff;
        font-size: 85px; /* Lebih Gede */
        font-weight: 700;
        letter-spacing: 15px;
        text-align: center;
        margin: 20px 0 0 0;
        text-shadow: 0px 0px 20px rgba(0, 255, 255, 0.5);
    }

    /* Submenu Card Styling */
    .menu-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        color: white;
        font-family: 'Poppins', sans-serif;
        margin-bottom: 20px;
        height: 200px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: 0.4s;
    }
    
    .menu-card:hover {
        background: rgba(38, 196, 185, 0.4);
        transform: translateY(-10px);
    }

    /* Icon Gede, Teks Sedang */
    .menu-icon {
        font-size: 60px; /* Icon di-BOOM gedein */
        margin-bottom: 10px;
    }
    
    .menu-text {
        font-size: 18px; /* Ukuran pas, gak kekecilan gak kegedean */
        font-weight: 600;
        letter-spacing: 1px;
    }

    .logo-container img {
        height: 60px;
        margin: 0 15px;
        filter: drop-shadow(2px 2px 5px rgba(0,0,0,0.3));
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Logika Jam Realtime (WIB)
tz = pytz.timezone('Asia/Jakarta')
now = datetime.datetime.now(tz)
tgl_skrg = now.strftime("%d %B %Y")
jam_skrg = now.strftime("%H:%M:%S WIB")

# 4. Header: Logo Perusahaan & Jam
col_logo, col_time = st.columns([2, 1])

with col_logo:
    st.markdown(f"""
        <div class="logo-container" style="display: flex; align-items: center;">
            <img src="https://raw.githubusercontent.com/Lily-yulinar/CaneMetrix2.0/main/logo_lpp.png" alt="LPP">
            <img src="https://raw.githubusercontent.com/Lily-yulinar/CaneMetrix2.0/main/logo_ptpn.png" alt="PTPN">
            <img src="https://raw.githubusercontent.com/Lily-yulinar/CaneMetrix2.0/main/logo_sgn.png" alt="SGN">
        </div>
    """, unsafe_allow_html=True)

with col_time:
    shift = st.selectbox("", ["SHIFT 1", "SHIFT 2", "SHIFT 3"], index=0)
    st.markdown(f'<p style="color:white; text-align:right; font-weight:bold; font-size:18px;">{tgl_skrg}<br>{jam_skrg}</p>', unsafe_allow_html=True)

# 5. Judul Aplikasi
st.markdown('<h1 class="main-title">CANE METRIX</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#26c4b9; text-align:center; font-style:italic; font-size:22px; margin-bottom:40px;">Accelerating QA Performance</p>', unsafe_allow_html=True)

# 6. Grid Menu (Icon Gede)
c1, c2, c3 = st.columns(3)

menus = [
    ("📋", "INPUT DATA"), ("📅", "DATABASE HARIAN"), ("📊", "DATABASE BULANAN"),
    ("⚖️", "REKAP STASIUN"), ("🧮", "HITUNG"), ("👤", "AKUN"),
    ("📈", "TREND"), ("⚙️", "PENGATURAN"), ("📥", "EXPORT DATA")
]

for i, (icon, text) in enumerate(menus):
    with [c1, c2, c3][i % 3]:
        st.markdown(f"""
            <div class="menu-card">
                <div class="menu-icon">{icon}</div>
                <div class="menu-text">{text}</div>
            </div>
        """, unsafe_allow_html=True)

# 7. Status Bar
st.markdown(f"""
    <div style="background: #26c4b9; padding: 15px; border-radius: 15px; text-align: center; color: white; font-weight: bold; font-size: 22px; margin-top:30px;">
        Jumlah sampel masuk hari ini: *45
    </div>
    """, unsafe_allow_html=True)
