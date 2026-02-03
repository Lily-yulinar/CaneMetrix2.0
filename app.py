import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
import numpy as np

# --- 1. CONFIG & SESSION STATE ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

# Inisialisasi session state (Kunci Navigasi)
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

# Fungsi Callback (Sekali klik langsung pindah)
def ganti_halaman(nama_halaman):
    st.session_state.page = nama_halaman

# --- 2. LOGIKA KOREKSI SUHU (Interpolasi Tabel) ---
data_koreksi = {
    25: -0.19, 26: -0.12, 27: -0.05, 28: 0.02, 29: 0.09,
    30: 0.16, 31: 0.24, 32: 0.31, 33: 0.38, 34: 0.46,
    35: 0.54, 36: 0.62, 37: 0.70, 38: 0.78, 39: 0.86,
    40: 0.94, 41: 1.02, 42: 1.10, 43: 1.18, 44: 1.26,
    45: 1.34, 46: 1.42, 47: 1.50, 48: 1.58, 49: 1.66, 50: 1.72
}

def hitung_koreksi(suhu_val):
    s_keys = sorted(data_koreksi.keys())
    s_vals = [data_koreksi[k] for k in s_keys]
    return float(np.interp(suhu_val, s_keys, s_vals))

# --- 3. CSS CUSTOM (STYLE DARK & CYAN GLOW) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Michroma&family=Poppins:wght@400;700&display=swap');
    
    .stApp { background: #0d1117; color: #e6edf3; }

    .header-text {
        font-family: 'Michroma'; color: #26c4b9;
        text-align: center; font-size: 40px;
        letter-spacing: 5px; margin-top: 20px;
    }
    
    .sub-header {
        font-family: 'Poppins'; color: #26c4b9;
        text-align: center; font-size: 14px;
        letter-spacing: 4px; font-weight: bold; margin-bottom: 40px;
    }

    /* Box Hasil Style Sesuai Screenshot */
    .hasil-box {
        border: 2px solid #26c4b9; border-radius: 20px;
        padding: 40px; text-align: center;
        background: rgba(38, 196, 185, 0.05);
        box-shadow: 0 0 25px rgba(38, 196, 185, 0.2);
    }

    .angka-hasil { font-family: 'Michroma'; font-size: 70px; color: white; margin: 10px 0; }
    
    /* Tombol-tombol Dashboard */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.05) !important;
        color: white !important; border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important; height: 160px !important; width: 100% !important;
        font-size: 18px !important; font-weight: bold !important; transition: 0.3s;
    }
    div.stButton > button:hover {
        border-color: #26c4b9 !important; background: rgba(38, 196, 185, 0.15) !important;
        transform: translateY(-5px);
    }

    .jam-digital { color: #26c4b9; font-size: 30px; font-weight: 900; font-family: 'Poppins'; }
    </style>
""", unsafe_allow_html=True)

# --- 4. HEADER (JAM) ---
c_h1, c_h2 = st.columns([10, 3])
with c_h2:
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.datetime.now(tz)
    st.markdown(f'<div style="text-align:right;"><div class="jam-digital">{now.strftime("%H:%M:%S")}</div></div>', unsafe_allow_html=True)

st_autorefresh(interval=1000, key="global_clock")

# --- 5. LOGIKA NAVIGASI ---

# --- HALAMAN DASHBOARD ---
if st.session_state.page == 'dashboard':
    st.markdown("<h1 class='header-text'>CANE METRIX</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>ACCELERATING QA PERFORMANCE</p>", unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.button("📝\nINPUT DATA", on_click=ganti_halaman, args=('input',), key="btn_in")
    with col_b:
        # INI TOMBOLNYA BEB!
        st.button("🧮\nHITUNG ANALISA", on_click=ganti_halaman, args=('analisa',), key="btn_an")
    with col_c:
        st.button("📅\nDATABASE", on_click=ganti_halaman, args=('db',), key="btn_db")

# --- HALAMAN ANALISA (HITUNGAN % BRIX) ---
elif st.session_state.page == 'analisa':
    st.markdown("<div class='header-text' style='font-size:25px; text-align:left;'>🧪 ANALISA TETES</div>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #26c4b9; opacity: 0.5;'>", unsafe_allow_html=True)

    col_inp, col_gap, col_res = st.columns([10, 1, 10])

    with col_inp:
        st.markdown("### 📥 INPUT DATA")
        brix_obs = st.number_input("Brix Teramati", value=8.80, step=0.01, format="%.2f")
        suhu_obs = st.number_input("Suhu Teramati (°C)", value=28.3, step=0.1, format="%.1f")
        
        # Hitung Koreksi
        kor = hitung_koreksi(suhu_obs)
        st.markdown(f"""
            <div style="background: rgba(38,196,185,0.1); padding:15px; border-radius:10px; color:#26c4b9; border:1px solid #26c4b9; font-weight:bold; margin-top:20px;">
                Koreksi Suhu: {kor:+.3f}
            </div>
        """, unsafe_allow_html=True)

    with col_res:
        st.markdown("### 📊 HASIL")
        brix_10x = brix_obs * 10
        brix_akhir = brix_10x + kor
        
        st.markdown(f"""
            <div class="hasil-box">
                <p style="color:rgba(255,255,255,0.6); font-size:14px; margin-bottom:5px;">Brix x 10 = {brix_10x:.2f}</p>
                <p style="font-weight:bold; font-size:18px;">% BRIX AKHIR</p>
                <h1 class="angka-hasil">{brix_akhir:.3f}</h1>
            </div>
        """, unsafe_allow_html=True)

    st.write("##")
    if st.button("🔙 KEMBALI KE DASHBOARD", on_click=ganti_halaman, args=('dashboard',), key="btn_back"):
        pass

# --- HALAMAN LAIN ---
else:
    st.title(f"Halaman {st.session_state.page}")
    st.button("🔙 KEMBALI", on_click=ganti_halaman, args=('dashboard',), key="btn_back_alt")
