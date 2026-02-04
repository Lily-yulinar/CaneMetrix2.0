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

# --- 2. FUNGSI LOAD LOGO & CSS ---
def get_base64_logo(file_name):
    # Cek berbagai kemungkinan nama file (case-sensitive)
    names_to_check = [file_name, file_name.lower(), file_name.upper()]
    for name in names_to_check:
        if os.path.exists(name):
            with open(name, "rb") as f:
                return base64.b64encode(f.read()).decode()
    return None

# Load Aset Lokal
l_kb = get_base64_logo("kb.png")
l_sgn = get_base64_logo("sgn.png")
l_ptpn = get_base64_logo("ptpn.png")
l_lpp = get_base64_logo("lpp.png")
l_cane = get_base64_logo("canemetrix.png")

# Link Backup (Kalau file di folder gagal load)
url_kb_backup = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Logo_BUMN.svg/512px-Logo_BUMN.svg.png"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Michroma&family=Poppins:wght@400;700;900&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.85), rgba(0, 10, 30, 0.85)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover;
    }}

    /* Container Logo Putih */
    .partner-box {{ 
        background: white; 
        padding: 8px 20px; 
        border-radius: 10px; 
        display: flex; 
        align-items: center; 
        gap: 15px; 
        width: fit-content;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}
    .partner-box img {{ height: 30px; width: auto; object-fit: contain; }}

    .jam-digital {{
        color: #26c4b9; font-size: 42px; font-weight: 900; 
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
        font-size: 18px !important; font-weight: 700 !important; transition: 0.3s;
    }}
    div.stButton > button:hover {{
        border: 1px solid #26c4b9 !important;
        background: rgba(38, 196, 185, 0.2) !important;
        transform: translateY(-5px);
    }}
    </style>
""", unsafe_allow_html=True)

# --- 3. COMPONENT: HEADER ---
@st.fragment
def render_header():
    h1, h2 = st.columns([3, 1])
    with h1:
        # Logika: Jika file lokal ada, pakai base64. Jika tidak, pakai URL backup.
        src_kb = f"data:image/png;base64,{l_kb}" if l_kb else url_kb_backup
        src_sgn = f"data:image/png;base64,{l_sgn}" if l_sgn else ""
        src_ptpn = f"data:image/png;base64,{l_ptpn}" if l_ptpn else ""
        src_lpp = f"data:image/png;base64,{l_lpp}" if l_lpp else ""

        html_logos = f'''
        <div class="partner-box">
            <img src="{src_kb}" alt="BUMN">
            <img src="{src_sgn}" alt="SGN">
            <img src="{src_ptpn}" alt="PTPN">
            <img src="{src_lpp}" alt="LPP">
        </div>
        '''
        st.markdown(html_logos, unsafe_allow_html=True)

    with h2:
        tz = pytz.timezone('Asia/Jakarta')
        now = datetime.datetime.now(tz)
        st.markdown(f'''
            <div style="text-align:right;">
                <div style="color:white; opacity:0.8; font-family:Poppins; font-size:14px;">{now.strftime("%d %B %Y")}</div>
                <div class="jam-digital">{now.strftime("%H:%M:%S")} <span style="font-size:18px;">WIB</span></div>
            </div>
        ''', unsafe_allow_html=True)
    st_autorefresh(interval=1000, key="clock_tick")

render_header()

# --- 4. NAVIGATION ---

# DASHBOARD
if st.session_state.page == 'dashboard':
    st.markdown(f'''
    <div class="glass-card" style="display:flex; justify-content:space-between; align-items:center; margin-top:20px; margin-bottom:30px;">
        <div>
            <h1 style="font-family:'Michroma'; color:white; font-size:clamp(30px, 5vw, 55px); margin:0; letter-spacing:8px;">CANE METRIX</h1>
            <p style="color:#26c4b9; font-family:'Poppins'; font-weight:700; letter-spacing:5px;">ACCELERATING QA PERFORMANCE</p>
        </div>
        <img src="data:image/png;base64,{l_cane if l_cane else ''}" height="150" style="filter: drop-shadow(0 0 10px rgba(38,196,185,0.5));">
    </div>
    ''', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("📝\nINPUT DATA"): pindah_halaman('input_data')
        st.rerun() if st.session_state.page != 'dashboard' else None
    with c2: 
        if st.button("🧮\nHITUNG ANALISA"): pindah_halaman('analisa_tetes')
        st.rerun() if st.session_state.page != 'dashboard' else None
    with c3: 
        if st.button("📅\nDATABASE HARIAN"): pindah_halaman('db_harian')
        st.rerun() if st.session_state.page != 'dashboard' else None

# INPUT DATA
elif st.session_state.page == 'input_data':
    st.markdown("<h2 style='color:white; font-family:Michroma;'>📝 INPUT DATA</h2>", unsafe_allow_html=True)
    with st.form("input_form"):
        st.text_input("Nama Afdeling")
        st.number_input("Brix Tebu", step=0.1)
        if st.form_submit_button("Simpan"):
            st.success("Data Tersimpan!")
    if st.button("🔙 Kembali"):
        pindah_halaman('dashboard')
        st.rerun()

# ANALISA TETES
elif st.session_state.page == 'analisa_tetes':
    st.markdown("<h2 style='color:white; font-family:Michroma;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
    brix = st.number_input("Brix", value=1.0)
    pol = st.number_input("Pol", value=0.0)
    hk = (pol/brix)*100
    st.metric("Harkat Kemurnian", f"{hk:.2f}%")
    if st.button("🔙 Kembali"):
        pindah_halaman('dashboard')
        st.rerun()

# DATABASE
elif st.session_state.page == 'db_harian':
    st.markdown("<h2 style='color:white; font-family:Michroma;'>📅 DATABASE</h2>", unsafe_allow_html=True)
    st.info("Fitur database akan segera hadir dengan integrasi SQL!")
    if st.button("🔙 Kembali"):
        pindah_halaman('dashboard')
        st.rerun()
