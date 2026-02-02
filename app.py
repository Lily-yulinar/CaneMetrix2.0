import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
import base64

# 1. Konfigurasi Halaman
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

# 2. Jam Realtime (Ngedetik Terus)
st_autorefresh(interval=1000, key="datarefresh")

# Jam WIB
tz = pytz.timezone('Asia/Jakarta')
now = datetime.datetime.now(tz)
tgl_skrg = now.strftime("%d %B %Y")
jam_skrg = now.strftime("%H:%M:%S")

# 3. Fungsi Gambar Lab (Teknik Base64 biar PASTI MUNCUL)
def get_base64_background():
    # Gue pake gambar lab yang bener-bener pro dan clean
    bg_img = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Poppins:wght@400;600&display=swap');

    .stApp {
        background: linear-gradient(rgba(0, 20, 40, 0.75), rgba(0, 20, 40, 0.75)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Judul Super Gede & Glow */
    .main-title {
        font-family: 'Orbitron', sans-serif;
        color: #ffffff;
        font-size: 100px; 
        font-weight: 700;
        letter-spacing: 15px;
        text-align: center;
        margin: 0;
        text-shadow: 0px 0px 30px rgba(0, 255, 255, 0.9);
    }

    /* Submenu Card ala Gambar 2 */
    .menu-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        padding: 40px 20px;
        border-radius: 25px;
        text-align: center;
        color: white;
        font-family: 'Poppins', sans-serif;
        margin-bottom: 25px;
        height: 240px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        transition: all 0.4s ease;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .menu-card:hover {
        background: rgba(38, 196, 185, 0.3);
        transform: translateY(-12px) scale(1.02);
        border: 1px solid #26c4b9;
        box-shadow: 0 15px 35px rgba(0, 255, 255, 0.2);
    }

    .menu-icon {
        font-size: 80px; 
        margin-bottom: 20px;
        filter: drop-shadow(0 0 10px rgba(255,255,255,0.5));
    }
    
    .menu-text {
        font-size: 18px; 
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    </style>
    """
    st.markdown(bg_img, unsafe_allow_html=True)

get_base64_background()

# 4. Header: Logo & Waktu
col_logo, col_time = st.columns([2, 1])

with col_logo:
    # Space logo (Nanti lo tinggal upload & ganti nama file di sini)
    st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 12px; display: inline-flex; align-items: center;">
            <p style="color: white; margin: 0; font-weight: bold; font-size: 12px; letter-spacing: 2px;">LOGOS UPLOADED SOON</p>
        </div>
    """, unsafe_allow_html=True)

with col_time:
    st.selectbox("", ["SHIFT 1", "SHIFT 2", "SHIFT 3"], label_visibility="collapsed")
    st.markdown(f"""
        <div style="text-align: right; color: white; font-family: 'Poppins';">
            <span style="font-size: 16px; opacity: 0.8;">{tgl_skrg}</span><br>
            <span style="font-size: 28px; color: #26c4b9; font-weight: bold; text-shadow: 0 0 10px rgba(38, 196, 185, 0.5);">{jam_skrg} WIB</span>
        </div>
    """, unsafe_allow_html=True)

# 5. Body: Judul & Subtitle
st.markdown('<p style="text-align: center; color: white; margin-top: 40px; font-weight: 300;">Welcome, Planters!</p>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">CANE METRIX</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#26c4b9; text-align:center; font-style:italic; font-size:22px; margin-bottom:60px; letter-spacing: 3px;">Accelerating QA Performance</p>', unsafe_allow_html=True)

# 6. Menu Grid (3 Kolom)
c1, c2, c3 = st.columns(3)

menus = [
    ("📝", "Input Data"), ("📅", "Database Harian"), ("📊", "Database Bulanan"),
    ("⚖️", "Rekap Stasiun"), ("🧮", "Hitung"), ("👤", "Akun"),
    ("📈", "Trend"), ("⚙️", "Pengaturan"), ("📥", "Export Data")
]

for i, (icon, text) in enumerate(menus):
    with [c1, c2, c3][i % 3]:
        st.markdown(f"""
            <div class="menu-card">
                <div class="menu-icon">{icon}</div>
                <div class="menu-text">{text}</div>
            </div>
        """, unsafe_allow_html=True)

# 7. Footer Status
st.markdown(f"""
    <div style="background: linear-gradient(90deg, #26c4b9, #1a4a7a); padding: 20px; border-radius: 20px; text-align: center; color: white; font-weight: bold; font-size: 24px; margin-top:40px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
        JUMLAH SAMPEL MASUK HARI INI: 45
    </div>
    <p style="text-align: center; color: rgba(255,255,255,0.4); margin-top: 20px; font-size: 12px;">CaneMetrix 2.0 - Quality Assurance Digital System</p>
    """, unsafe_allow_html=True)
