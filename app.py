import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
import numpy as np

# ===============================
# CONFIG
# ===============================
st.set_page_config(
    page_title="CaneMetrix 2.0",
    layout="wide"
)

# ===============================
# INIT PAGE STATE
# ===============================
if "page" not in st.session_state:
    st.session_state.page = "dash"

def navigasi(target):
    st.session_state.page = target
    st.rerun()

# ===============================
# DATA KOREKSI BRIX
# ===============================
data_koreksi = {
    25: -0.19, 26: -0.12, 27: -0.05, 28: 0.02, 29: 0.09,
    30: 0.16, 31: 0.24, 32: 0.31, 33: 0.38, 34: 0.46,
    35: 0.54, 36: 0.62, 37: 0.70, 38: 0.78, 39: 0.86,
    40: 0.94, 41: 1.02, 42: 1.10, 43: 1.18, 44: 1.26,
    45: 1.34, 46: 1.42, 47: 1.50, 48: 1.58, 49: 1.66, 50: 1.72
}

def hitung_koreksi(suhu):
    keys = sorted(data_koreksi.keys())
    vals = [data_koreksi[k] for k in keys]
    return float(np.interp(suhu, keys, vals))

# ===============================
# CSS
# ===============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Michroma&family=Poppins:wght@400;700&display=swap');

.stApp { background: #0d1117; color: white; }

div.stButton > button {
    height: 160px;
    width: 100%;
    border-radius: 20px;
    font-size: 20px;
    background: rgba(255,255,255,0.05);
    color: white;
    border: 1px solid rgba(255,255,255,0.1);
    transition: 0.3s;
}

div.stButton > button:hover {
    border-color: #26c4b9;
    background: rgba(38,196,185,0.2);
}

.hasil-box {
    border: 2px solid #26c4b9;
    border-radius: 20px;
    padding: 40px;
    text-align: center;
    background: rgba(38,196,185,0.05);
}

.jam {
    color: #26c4b9;
    font-size: 30px;
    font-weight: 800;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# HEADER + JAM
# ===============================
c1, c2 = st.columns([10, 3])
with c2:
    tz = pytz.timezone("Asia/Jakarta")
    now = datetime.datetime.now(tz)
    st.markdown(f"<div class='jam'>{now.strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

st_autorefresh(interval=1000, key="clock")

# ===============================
# PAGE RENDER
# ===============================
page = st.session_state.page

# ---------- DASHBOARD ----------
if page == "dash":
    st.markdown(
        "<h1 style='font-family:Michroma; color:#26c4b9; text-align:center;'>CANE METRIX</h1>",
        unsafe_allow_html=True
    )
    st.write("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📝\nINPUT DATA"):
            navigasi("input")

    with col2:
        if st.button("🧮\nHITUNG ANALISA"):
            navigasi("analisa")

    with col3:
        if st.button("📅\nDATABASE"):
            navigasi("db")

# ---------- ANALISA ----------
elif page == "analisa":
    st.markdown(
        "<h2 style='font-family:Michroma; color:#26c4b9;'>🧪 ANALISA TETES</h2>",
        unsafe_allow_html=True
    )

    if st.button("🔙 KEMBALI"):
        navigasi("dash")

    st.write("---")

    col_inp, col_res = st.columns(2)

    with col_inp:
        st.subheader("📥 Input Data")
        brix = st.number_input("Brix Teramati", value=8.80, format="%.2f")
        suhu = st.number_input("Suhu Teramati (°C)", value=28.3, format="%.1f")
        koreksi = hitung_koreksi(suhu)
        st.info(f"Koreksi Suhu: {koreksi:+.3f}")

    with col_res:
        total = (brix * 10) + koreksi
        st.subheader("📊 Hasil")
        st.markdown(f"""
        <div class="hasil-box">
            <p>Brix × 10 = {brix*10:.2f}</p>
            <p><b>% BRIX AKHIR</b></p>
            <h1 style="font-size:64px;">{total:.3f}</h1>
        </div>
        """, unsafe_allow_html=True)

# ---------- INPUT ----------
elif page == "input":
    st.markdown("## 📝 INPUT DATA")
    if st.button("🔙 Kembali"):
        navigasi("dash")

# ---------- DATABASE ----------
elif page == "db":
    st.markdown("## 📅 DATABASE HARIAN")
    if st.button("🔙 Kembali"):
        navigasi("dash")
