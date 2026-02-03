import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
import numpy as np

# --- 1. CONFIG & INITIAL STATE ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

# Inisialisasi session state
if 'page' not in st.session_state:
    st.session_state.page = 'Dashboard'

# --- 2. DATA KOREKSI BRIX (Sesuai Foto Tabel) ---
data_koreksi = {
    25: -0.19, 26: -0.12, 27: -0.05, 28: 0.02, 29: 0.09,
    30: 0.16, 31: 0.24, 32: 0.31, 33: 0.38, 34: 0.46,
    35: 0.54, 36: 0.62, 37: 0.70, 38: 0.78, 39: 0.86,
    40: 0.94, 41: 1.02, 42: 1.10, 43: 1.18, 44: 1.26,
    45: 1.34, 46: 1.42, 47: 1.5, 48: 1.58, 49: 1.66, 50: 1.72
}

def hitung_koreksi(suhu_val):
    s_keys = sorted(data_koreksi.keys())
    s_vals = [data_koreksi[k] for k in s_keys]
    return float(np.interp(suhu_val, s_keys, s_vals))

# --- 3. CSS UNTUK UI ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Michroma&family=Poppins:wght@400;700;900&display=swap');
    .stApp { background: #000a1e; color: white; }
    .glass {
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px);
        padding: 25px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1);
    }
    .jam-text { color: #26c4b9; font-family: 'Poppins'; font-size: 30px; font-weight: 900; }
    
    /* Bikin tombol menu utama gede dan mantap */
    div.stButton > button {
        height: 150px !important; width: 100% !important;
        border-radius: 20px !important; font-size: 20px !important;
        background: rgba(255,255,255,0.1) !important; color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }
    div.stButton > button:hover { border-color: #26c4b9 !important; background: rgba(38,196,185,0.2) !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR NAVIGASI (BACKUP BIAR GAK GAGAL KLIK) ---
with st.sidebar:
    st.title("🧭 MENU")
    pilihan = st.radio("Pilih Halaman:", ["Dashboard", "Hitung Analisa", "Input Data", "Database"], 
                      index=["Dashboard", "Hitung Analisa", "Input Data", "Database"].index(st.session_state.page))
    st.session_state.page = pilihan

# --- 5. HEADER (JAM DIGITAL) ---
c1, c2 = st.columns([8, 2])
with c2:
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.datetime.now(tz)
    st.markdown(f'<div class="jam-text">{now.strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)

st_autorefresh(interval=1000, key="jam_refresh")

# --- 6. LOGIKA HALAMAN ---

if st.session_state.page == "Dashboard":
    st.markdown('<div class="glass"><h1 style="font-family:Michroma;">CANE METRIX</h1>'
                '<p style="color:#26c4b9;">ACCELERATING QA PERFORMANCE</p></div>', unsafe_allow_html=True)
    st.write("---")
    
    m1, m2, m3 = st.columns(3)
    with m1:
        if st.button("📝\nINPUT DATA"):
            st.session_state.page = "Input Data"
            st.rerun()
    with m2:
        if st.button("🧮\nHITUNG ANALISA"):
            st.session_state.page = "Hitung Analisa"
            st.rerun()
    with m3:
        if st.button("📅\nDATABASE"):
            st.session_state.page = "Database"
            st.rerun()

elif st.session_state.page == "Hitung Analisa":
    st.markdown("## 🧪 KALKULATOR % BRIX")
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    
    col_input, col_hasil = st.columns(2)
    with col_input:
        st.subheader("Data Lab")
        b_obs = st.number_input("Brix Teramati (Lab)", value=8.50, step=0.01)
        b_10x = b_obs * 10
        st.info(f"Brix Pengenceran: {b_10x:.2f}")
        suhu = st.number_input("Suhu (°C)", min_value=25.0, max_value=50.0, value=28.0)
        
    with col_hasil:
        st.subheader("Hasil Akhir")
        kor = hitung_koreksi(suhu)
        total_brix = b_10x + kor
        
        st.markdown(f"""
            <div style="background:rgba(38,196,185,0.1); padding:20px; border-radius:15px; border:2px solid #26c4b9; text-align:center;">
                <p style="margin:0;">HASIL % BRIX</p>
                <h1 style="font-size:80px; margin:0;">{total_brix:.2f}</h1>
                <p style="color:#26c4b9;">Koreksi Suhu: {kor:+.2f}</p>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔙 KEMBALI KE DASHBOARD"):
        st.session_state.page = "Dashboard"
        st.rerun()

else:
    st.write(f"Halaman {st.session_state.page} sedang dalam perbaikan.")
    if st.button("KEMBALI"):
        st.session_state.page = "Dashboard"
        st.rerun()
