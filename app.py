import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
import base64
import os

# --- 1. SETTING PAGE ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

# Inisialisasi State Halaman agar tidak reset saat refresh
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

def pindah_halaman(nama_halaman):
    st.session_state.page = nama_halaman
    # Kita tidak perlu st.rerun() di sini karena fragment header sudah menangani refresh

# --- 2. FUNGSI LOAD LOGO & CSS ---
def get_base64_logo(file_name):
    # Coba beberapa kemungkinan lokasi/nama file
    possible_names = [file_name, file_name.lower(), file_name.upper()]
    for name in possible_names:
        if os.path.exists(name):
            with open(name, "rb") as f:
                return base64.b64encode(f.read()).decode()
    return None

# Load Semua Logo
l_kb = get_base64_logo("kb.png")
l_sgn = get_base64_logo("sgn.png")
l_ptpn = get_base64_logo("ptpn.png")
l_lpp = get_base64_logo("lpp.png")
l_cane = get_base64_logo("canemetrix.png")

# CSS Custom
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Michroma&family=Poppins:wght@400;700;900&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.85), rgba(0, 10, 30, 0.85)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover;
    }}

    /* KOTAK LOGO PUTIH - FIX UNTUK KB.PNG */
    .partner-box {{ 
        background: white; 
        padding: 10px 25px; 
        border-radius: 12px; 
        display: flex; 
        align-items: center; 
        gap: 20px; 
        width: fit-content;
    }}
    .partner-box img {{ height: 35px; width: auto; object-fit: contain; }}

    .jam-digital {{
        color: #26c4b9; font-size: 50px; font-weight: 900; 
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

# --- 3. COMPONENT: HEADER & REAL-TIME CLOCK ---
@st.fragment
def render_header():
    h1, h2 = st.columns([3, 1])
    with h1:
        # Tampilkan Logo Box
        html_logos = '<div class="partner-box">'
        # Urutan: KB, SGN, PTPN, LPP
        for label, img_data in [("BUMN", l_kb), ("SGN", l_sgn), ("PTPN", l_ptpn), ("LPP", l_lpp)]:
            if img_data:
                html_logos += f'<img src="data:image/png;base64,{img_data}" title="{label}">'
        html_logos += '</div>'
        st.markdown(html_logos, unsafe_allow_html=True)
        
        # Peringatan jika KB.png tidak ada
        if not l_kb:
            st.warning("⚠️ File 'kb.png' tidak ditemukan. Pastikan file ada di folder aplikasi.")

    with h2:
        tz = pytz.timezone('Asia/Jakarta')
        now = datetime.datetime.now(tz)
        st.markdown(f'''
            <div style="text-align:right;">
                <div style="color:white; opacity:0.8; font-family:Poppins;">{now.strftime("%d %B %Y")}</div>
                <div class="jam-digital">{now.strftime("%H:%M:%S")}</div>
            </div>
        ''', unsafe_allow_html=True)
    
    # Auto-refresh khusus untuk header (jam) setiap 1 detik
    st_autorefresh(interval=1000, key="clock_refresh")

render_header()

# --- 4. NAVIGATION LOGIC ---

# --- PAGE: DASHBOARD ---
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

# --- PAGE: INPUT DATA ---
elif st.session_state.page == 'input_data':
    st.markdown("<h2 style='color:white; font-family:Michroma;'>📝 INPUT DATA QA</h2>", unsafe_allow_html=True)
    with st.container(border=True):
        col_a, col_b = st.columns(2)
        with col_a:
            st.text_input("Nama Kebun / Afdeling")
            st.number_input("Berat Tebu (Ton)", min_value=0.0)
        with col_b:
            st.date_input("Tanggal Giling")
            st.selectbox("Shift", ["Shift 1", "Shift 2", "Shift 3"])
        
        if st.button("SIMPAN DATA"):
            st.success("Data berhasil disimpan!")
    
    if st.button("🔙 KEMBALI"): pindah_halaman('dashboard')

# --- PAGE: ANALISA TETES ---
elif st.session_state.page == 'analisa_tetes':
    st.markdown("<h2 style='color:white; font-family:Michroma;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            brix = st.number_input("Brix (%)", format="%.2f", value=0.0)
            pol = st.number_input("Pol (%)", format="%.2f", value=0.0)
        with c2:
            hk = (pol / brix) * 100 if brix > 0 else 0
            st.metric("Harkat Kemurnian (HK)", f"{hk:.2f}%")
            
    if st.button("🔙 KEMBALI"): pindah_halaman('dashboard')

# --- PAGE: DATABASE ---
elif st.session_state.page == 'db_harian':
    st.markdown("<h2 style='color:white; font-family:Michroma;'>📅 DATABASE HARIAN</h2>", unsafe_allow_html=True)
    import pandas as pd
    df = pd.DataFrame({'Contoh': ['Data 1', 'Data 2'], 'Nilai': [80.5, 78.2]})
    st.dataframe(df, use_container_width=True)
    
    if st.button("🔙 KEMBALI"): pindah_halaman('dashboard')
