import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
import base64
import os

# --- 1. SETTING PAGE ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

# Inisialisasi State Halaman
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

def pindah_halaman(nama_halaman):
    st.session_state.page = nama_halaman

# --- 2. FUNGSI LOGO & CSS ---
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

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Michroma&family=Poppins:wght@400;700;900&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.85), rgba(0, 10, 30, 0.85)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover;
    }}

    .partner-box {{ 
        background: white; padding: 10px 25px; border-radius: 12px; 
        display: flex; align-items: center; gap: 20px; width: fit-content;
    }}
    .partner-box img {{ height: 30px; width: auto; object-fit: contain; }}

    .jam-digital {{
        color: #26c4b9; font-size: 50px; font-weight: 900; 
        font-family: 'Poppins'; line-height: 1.1; text-shadow: 0 0 15px rgba(38, 196, 185, 0.6);
    }}

    /* Card Styling */
    .glass-card {{
        background: rgba(255, 255, 255, 0.05); 
        backdrop-filter: blur(15px); 
        padding: 30px; 
        border-radius: 30px; 
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}

    /* Button Styling */
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.07) !important;
        color: white !important; border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important; height: 150px !important; width: 100% !important;
        font-size: 18px !important; font-weight: 700 !important; transition: 0.3s;
    }}
    div.stButton > button:hover {{
        border: 1px solid #26c4b9 !important;
        background: rgba(38, 196, 185, 0.2) !important;
        transform: translateY(-5px);
    }}
    </style>
""", unsafe_allow_html=True)

# --- 3. COMPONENT: HEADER & CLOCK ---
@st.fragment
def render_header():
    h1, h2 = st.columns([3, 1])
    with h1:
        html_logos = '<div class="partner-box">'
        for img_data in [l_kb, l_sgn, l_ptpn, l_lpp]:
            if img_data:
                html_logos += f'<img src="data:image/png;base64,{img_data}">'
        html_logos += '</div>'
        st.markdown(html_logos, unsafe_allow_html=True)
        if not l_kb: st.caption("⚠️ kb.png not found")

    with h2:
        tz = pytz.timezone('Asia/Jakarta')
        now = datetime.datetime.now(tz)
        st.markdown(f'''
            <div style="text-align:right;">
                <div style="color:white; opacity:0.8; font-family:Poppins;">{now.strftime("%d %B %Y")}</div>
                <div class="jam-digital">{now.strftime("%H:%M:%S")}</div>
            </div>
        ''', unsafe_allow_html=True)
    st_autorefresh(interval=1000, key="global_refresh")

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
        <img src="data:image/png;base64,{l_cane}" height="150">
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
            st.success("Data berhasil disimpan ke sistem!")
            
    if st.button("🔙 KEMBALI"): pindah_halaman('dashboard')

# --- PAGE: ANALISA TETES ---
elif st.session_state.page == 'analisa_tetes':
    st.markdown("<h2 style='color:white; font-family:Michroma;'>🧪 ANALISA TETES (CALCULATOR)</h2>", unsafe_allow_html=True)
    
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            brix = st.number_input("Brix (%)", format="%.2f")
            pol = st.number_input("Pol (%)", format="%.2f")
        with c2:
            # Contoh rumus sederhana
            hk = (pol / brix) * 100 if brix > 0 else 0
            st.metric("Hasil HK (Harkat Kemurnian)", f"{hk:.2f}")
            
    if st.button("🔙 KEMBALI"): pindah_halaman('dashboard')

# --- PAGE: DATABASE ---
elif st.session_state.page == 'db_harian':
    st.markdown("<h2 style='color:white; font-family:Michroma;'>📅 DATABASE HARIAN</h2>", unsafe_allow_html=True)
    # Simulasi Tabel
    import pandas as pd
    df_dummy = pd.DataFrame({
        'Tanggal': [datetime.date.today()],
        'Kebun': ['Kebun A'],
        'HK': [75.5]
    })
    st.table(df_dummy)
    
    if st.button("🔙 KEMBALI"): pindah_halaman('dashboard')
