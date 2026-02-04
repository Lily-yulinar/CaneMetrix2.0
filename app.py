import streamlit as st
import datetime
import pytz
import base64
import os

# --- 1. CONFIG & STATE ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'
if 'analisa_type' not in st.session_state:
    st.session_state.analisa_type = None

# --- 2. FUNGSI LOGO & ASSETS (Opsional jika file ada) ---
def get_base64_logo(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# --- 3. DATABASE & LOGIKA HITUNG ---
data_koreksi = {
    27: -0.05, 28: 0.02, 29: 0.09, 30: 0.16, 31: 0.24, 
    32: 0.315, 33: 0.385, 34: 0.465, 35: 0.54, 36: 0.62,
    37: 0.70, 38: 0.78, 39: 0.86, 40: 0.94
}

def hitung_interpolasi(nilai_user, dataset):
    keys = sorted(dataset.keys())
    if nilai_user in dataset: return dataset[nilai_user]
    if nilai_user < keys[0]: return dataset[keys[0]]
    if nilai_user > keys[-1]: return dataset[keys[-1]]
    for i in range(len(keys) - 1):
        x0, x1 = keys[i], keys[i+1]
        if x0 < nilai_user < x1:
            y0, y1 = dataset[x0], dataset[x1]
            return y0 + (nilai_user - x0) * (y1 - y0) / (x1 - x0)
    return 1.0

# --- 4. CSS CUSTOM ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Poppins:wght@300;400;700&display=swap');
    
    .stApp {
        background: #0e1117;
    }

    /* Card Style untuk Menu */
    [data-testid="stVerticalBlock"] > div:has(div.stButton) {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 10px;
    }

    /* Tombol Style */
    div.stButton > button {
        width: 100%;
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 20px !important;
        font-family: 'Poppins', sans-serif !important;
    }

    div.stButton > button:hover {
        border-color: #26c4b9 !important;
        background: rgba(38, 196, 185, 0.1) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 5. DASHBOARD ---
if st.session_state.page == 'dashboard':
    # Header Jam
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.datetime.now(tz)
    st.markdown(f"<p style='text-align:right; color:white;'>{now.strftime('%d %B %Y')} <br> <b style='color:#26c4b9; font-size:20px;'>{now.strftime('%H:%M:%S')} WIB</b></p>", unsafe_allow_html=True)

    # Hero Section
    st.markdown("<h1 style='font-family:Orbitron; color:white;'>CANE METRIX</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#26c4b9; letter-spacing:3px;'>ACCELERATING QA PERFORMANCE</p>", unsafe_allow_html=True)

    # Menu Utama (TETAP DALAM KOLOM)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📝\n\nINPUT DATA", key="btn_in"): st.toast("Input Data Page")
    with c2:
        if st.button("🧮\n\nHITUNG ANALISA", key="btn_hi"):
            st.session_state.page = 'pilih_analisa'; st.rerun()
    with c3:
        if st.button("📅\n\nDATABASE HARIAN", key="btn_db"): st.toast("Database Page")

# --- 6. PILIH JENIS ANALISA ---
elif st.session_state.page == 'pilih_analisa':
    st.markdown("<h2 style='text-align:center; color:white; font-family:Orbitron;'>PILIH JENIS ANALISA</h2>", unsafe_allow_html=True)
    
    # Sub Menu (TETAP DALAM KOLOM SEPERTI SEMULA)
    m1, m2 = st.columns(2)
    with m1:
        if st.button("🧪 ANALISA TETES", key="sub_tetes"):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'tetes'; st.rerun()
    with m2:
        if st.button("🔬 OD TETES", key="sub_od"):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'od'; st.rerun()
    
    # TOMBOL KEMBALI (DIBUAT PANJANG/FULL WIDTH)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI KE DASHBOARD", use_container_width=True):
        st.session_state.page = 'dashboard'; st.rerun()

# --- 7. HALAMAN ANALISA ---
elif st.session_state.page == 'analisa_lab':
    st.title(f"HALAMAN {st.session_state.analisa_type.upper()}")
    
    # Konten Analisa Lo di sini...
    st.write("Silahkan masukkan data lab...")

    # TOMBOL KEMBALI (DIBUAT PANJANG/FULL WIDTH)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI KE MENU PILIHAN", use_container_width=True):
        st.session_state.page = 'pilih_analisa'; st.rerun()
