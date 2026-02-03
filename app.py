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

# --- 2. FUNGSI LOAD LOGO ---
def get_base64_logo(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

l_kb = get_base64_logo("kb.png")
l_sgn = get_base64_logo("sgn.png")
l_ptpn = get_base64_logo("ptpn.png")
l_lpp = get_base64_logo("lpp.png")
l_cane = get_base64_logo("canemetrix.png")

url_bumn_backup = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Logo_BUMN.svg/512px-Logo_BUMN.svg.png"

# --- 3. JURUS PAMUNGKAS CSS (Bongkar Container) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Michroma&family=Poppins:wght@400;700;900&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.85), rgba(0, 10, 30, 0.85)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover;
    }}

    /* MEMAKSA CONTAINER STREAMLIT UNTUK LEBAR */
    [data-testid="stHorizontalBlock"] {{
        align-items: center !important;
    }}

    /* PARTNER BOX: UKURAN MUTLAK */
    .partner-box-fixed {{ 
        background: white; 
        padding: 15px 30px; 
        border-radius: 15px; 
        display: flex !important; 
        flex-direction: row !important;
        align-items: center !important; 
        gap: 25px !important; 
        width: 550px !important; /* LEBAR FIX 550 PIXEL */
        min-width: 550px !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.5);
        margin-left: 0 !important;
    }}
    
    .partner-box-fixed img {{ 
        height: 38px !important; 
        width: auto !important;
        object-fit: contain !important;
        flex-shrink: 0 !important;
    }}

    .jam-digital {{
        color: #26c4b9; font-size: 45px; font-weight: 900; 
        font-family: 'Poppins'; line-height: 1.1; 
        text-shadow: 0 0 15px rgba(38, 196, 185, 0.6);
        text-align: right;
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

# --- 4. HEADER ---
@st.fragment
def render_header():
    # Gunakan satu baris container tanpa kolom ribet
    src_kb = f"data:image/png;base64,{l_kb}" if l_kb else url_bumn_backup
    
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.datetime.now(tz)
    
    # KITA PAKAI FLEXBOX MANUAL DI SINI
    header_html = f'''
    <div style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
        <div class="partner-box-fixed">
            <img src="{src_kb}">
            <img src="data:image/png;base64,{l_sgn if l_sgn else ''}">
            <img src="data:image/png;base64,{l_ptpn if l_ptpn else ''}">
            <img src="data:image/png;base64,{l_lpp if l_lpp else ''}">
        </div>
        <div>
            <div style="color:white; opacity:0.8; font-family:Poppins; text-align:right;">{now.strftime("%d %B %Y")}</div>
            <div class="jam-digital">{now.strftime("%H:%M:%S")} <span style="font-size:18px;">WIB</span></div>
        </div>
    </div>
    '''
    st.markdown(header_html, unsafe_allow_html=True)
    st_autorefresh(interval=1000, key="global_clock")

render_header()

# --- 5. NAVIGATION LOGIC ---
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

elif st.session_state.page == 'input_data':
    st.markdown("<h2 style='color:white; font-family:Michroma;'>📝 INPUT DATA</h2>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI"): pindah_halaman('dashboard')
elif st.session_state.page == 'analisa_tetes':
    st.markdown("<h2 style='color:white; font-family:Michroma;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI"): pindah_halaman('dashboard')
elif st.session_state.page == 'db_harian':
    st.markdown("<h2 style='color:white; font-family:Michroma;'>📅 DATABASE HARIAN</h2>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI"): pindah_halaman('dashboard')
