import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
import base64
import os

# --- 1. SETTING PAGE ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

def pindah_halaman(nama_halaman):
    st.session_state.page = nama_halaman
    st.rerun()

# --- 2. FUNGSI LOAD LOGO & CSS ---
def get_base64_logo(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# Load Aset
l_kb = get_base64_logo("kb.png")
l_sgn = get_base64_logo("sgn.png")
l_ptpn = get_base64_logo("ptpn.png")
l_lpp = get_base64_logo("lpp.png")
l_cane = get_base64_logo("canemetrix.png")

# Link Backup BUMN (Wajib ada buat jaga-jaga)
url_bumn_backup = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Logo_BUMN.svg/512px-Logo_BUMN.svg.png"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Michroma&family=Poppins:wght@400;700;900&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.85), rgba(0, 10, 30, 0.85)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover;
    }}

    /* PARTNER BOX - GUE LEBARIN PAKSA DI SINI */
    .partner-box {{ 
        background: white; 
        padding: 15px 40px; /* Padding lebih lega */
        border-radius: 15px; 
        display: flex; 
        align-items: center; 
        justify-content: space-around; /* Sebar logo secara merata */
        gap: 30px; 
        width: 450px !important; /* LOCK LEBARNYA BIAR GAK MENCIUT */
        box-shadow: 0 8px 25px rgba(0,0,0,0.5);
        margin-bottom: 10px;
    }}
    
    .partner-box img {{ 
        height: 35px; 
        width: auto; 
        object-fit: contain;
    }}

    .jam-digital {{
        color: #26c4b9; font-size: 45px; font-weight: 900; 
        font-family: 'Poppins'; line-height: 1.1; 
        text-shadow: 0 0 15px rgba(38, 196, 185, 0.6);
    }}

    .glass-card {{
        background: rgba(255, 255, 255, 0.05); 
        backdrop-filter: blur(15px); 
        padding: 40px; 
        border-radius: 30px; 
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}

    div.stButton > button {{
        background: rgba(255, 255, 255, 0.07) !important;
        color: white !important; border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important; height: 160px !important; width: 100% !important;
        font-size: 18px !important; font-weight: 700 !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 3. COMPONENT: HEADER ---
@st.fragment
def render_header():
    h1, h2 = st.columns([3, 1])
    with h1:
        # Gunakan file lokal jika ada, jika tidak gunakan URL backup
        src_kb = f"data:image/png;base64,{l_kb}" if l_kb else url_bumn_backup
        
        # HTML Header dengan Box yang sudah dilebarkan
        html_logos = f'''
        <div class="partner-box">
            <img src="{src_kb}" alt="BUMN">
            <img src="data:image/png;base64,{l_sgn if l_sgn else ''}" alt="SGN">
            <img src="data:image/png;base64,{l_ptpn if l_ptpn else ''}" alt="PTPN">
            <img src="data:image/png;base64,{l_lpp if l_lpp else ''}" alt="LPP">
        </div>
        '''
        st.markdown(html_logos, unsafe_allow_html=True)

    with h2:
        tz = pytz.timezone('Asia/Jakarta')
        now = datetime.datetime.now(tz)
        st.markdown(f'''
            <div style="text-align:right;">
                <div style="color:white; opacity:0.8; font-family:Poppins;">{now.strftime("%d %B %Y")}</div>
                <div class="jam-digital">{now.strftime("%H:%M:%S")} <span style="font-size:18px;">WIB</span></div>
            </div>
        ''', unsafe_allow_html=True)
    st_autorefresh(interval=1000, key="global_clock")

render_header()

# --- 4. DASHBOARD & NAV ---
if st.session_state.page == 'dashboard':
    st.markdown(f'''
    <div class="glass-card" style="display:flex; justify-content:space-between; align-items:center; margin-top:20px; margin-bottom:30px;">
        <div>
            <h1 style="font-family:'Michroma'; color:white; font-size:clamp(30px, 5vw, 55px); margin:0; letter-spacing:8px;">CANE METRIX</h1>
            <p style="color:#26c4b9; font-family:'Poppins'; font-weight:700; letter-spacing:5px;">ACCELERATING QA PERFORMANCE</p>
        </div>
        <img src="data:image/png;base64,{l_cane if l_cane else ''}" height="150">
    </div>
    ''', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("📝\nINPUT DATA"): pindah_halaman('input_data')
    with c2: 
        if st.button("🧮\nHITUNG ANALISA"): pindah_halaman('analisa_tetes')
    with c3: 
        if st.button("📅\nDATABASE HARIAN"): pindah_halaman('db_harian')

# Sisa logika halaman (input_data, dll) tetap sama...
elif st.session_state.page == 'input_data':
    st.markdown("<h2 style='color:white; font-family:Michroma;'>📝 INPUT DATA</h2>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI"): pindah_halaman('dashboard')
elif st.session_state.page == 'analisa_tetes':
    st.markdown("<h2 style='color:white; font-family:Michroma;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI"): pindah_halaman('dashboard')
elif st.session_state.page == 'db_harian':
    st.markdown("<h2 style='color:white; font-family:Michroma;'>📅 DATABASE HARIAN</h2>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI"): pindah_halaman('dashboard')
