import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
import numpy as np

# --- 1. CONFIG & URL NAVIGATION ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

# Ambil status halaman dari URL browser
query_params = st.query_params
if "p" not in query_params:
    st.query_params["p"] = "dash"

current_page = st.query_params["p"]

# Fungsi pindah halaman yang paling bandel
def navigasi(target):
    st.query_params["p"] = target

# --- 2. DATA KOREKSI BRIX ---
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

# --- 3. CSS CUSTOM (DARK & CYAN) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Michroma&family=Poppins:wght@400;700&display=swap');
    .stApp { background: #0d1117; color: white; }
    
    /* Style Tombol Menu Gede */
    div.stButton > button {
        height: 160px !important; width: 100% !important;
        border-radius: 20px !important; font-size: 20px !important;
        background: rgba(255,255,255,0.05) !important; color: white !important;
        border: 1px solid rgba(255,255,255,0.1) !important; transition: 0.3s;
    }
    div.stButton > button:hover { border-color: #26c4b9 !important; background: rgba(38,196,185,0.2) !important; }
    
    .hasil-box {
        border: 2px solid #26c4b9; border-radius: 20px; padding: 40px;
        text-align: center; background: rgba(38, 196, 185, 0.05);
    }
    .jam-digital { color: #26c4b9; font-size: 30px; font-weight: 900; font-family: 'Poppins'; }
    </style>
""", unsafe_allow_html=True)

# --- 4. HEADER & JAM ---
c1, c2 = st.columns([10, 3])
with c2:
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.datetime.now(tz)
    st.markdown(f'<div style="text-align:right;"><div class="jam-digital">{now.strftime("%H:%M:%S")}</div></div>', unsafe_allow_html=True)

st_autorefresh(interval=1000, key="refresh_global")

# --- 5. LOGIKA HALAMAN ---

if current_page == "dash":
    st.markdown("<h1 style='font-family:Michroma; color:#26c4b9; text-align:center;'>CANE METRIX</h1>", unsafe_allow_html=True)
    st.write("---")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.button("📝\nINPUT DATA", on_click=navigasi, args=("input",), key="btn_in")
    with col_b:
        # INI TOMBOL YANG LO MAKSUD!
        st.button("🧮\nHITUNG ANALISA", on_click=navigasi, args=("analisa",), key="btn_an")
    with col_c:
        st.button("📅\nDATABASE", on_click=navigasi, args=("db",), key="btn_db")

elif current_page == "analisa":
    st.markdown("<h2 style='font-family:Michroma; color:#26c4b9;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
    
    if st.button("🔙 KEMBALI KE DASHBOARD", on_click=navigasi, args=("dash",), key="back_btn"):
        pass
        
    st.write("---")
    col_inp, col_res = st.columns(2)
    
    with col_inp:
        st.subheader("📥 Input Data")
        b_obs = st.number_input("Brix Teramati", value=8.80, format="%.2f")
        suhu_obs = st.number_input("Suhu Teramati (°C)", value=28.3, format="%.1f")
        kor = hitung_koreksi(suhu_obs)
        st.info(f"Koreksi Suhu: {kor:+.3f}")
        
    with col_res:
        st.subheader("📊 Hasil")
        total_brix = (b_obs * 10) + kor
        st.markdown(f"""
            <div class="hasil-box">
                <p>Brix x 10 = {b_obs*10:.2f}</p>
                <p style="font-weight:bold;">% BRIX AKHIR</p>
                <h1 style="font-size:70px; font-family:Michroma;">{total_brix:.3f}</h1>
            </div>
        """, unsafe_allow_html=True)

else:
    st.write("Halaman sedang dikembangkan.")
    st.button("Kembali", on_click=navigasi, args=("dash",), key="back_err")
