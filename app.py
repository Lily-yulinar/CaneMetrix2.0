import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
import numpy as np

# ===============================
# 1. CONFIG & PAGE SETUP
# ===============================
st.set_page_config(
    page_title="CaneMetrix 2.0",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===============================
# 2. URL NAVIGATION (FIXED)
# ===============================
query_params = st.query_params
current_page = query_params.get("p", ["dash"])[0]

def navigasi(target):
    st.query_params.clear()
    st.query_params["p"] = target

# ===============================
# 3. DATA KOREKSI BRIX
# ===============================
data_koreksi = {
    25: -0.19, 26: -0.12, 27: -0.05, 28: 0.02, 29: 0.09,
    30: 0.16, 31: 0.24, 32: 0.31, 33: 0.38, 34: 0.46,
    35: 0.54, 36: 0.62, 37: 0.70, 38: 0.78, 39: 0.86,
    40: 0.94, 41: 1.02, 42: 1.10, 43: 1.18, 44: 1.26,
    45: 1.34, 46: 1.42, 47: 1.50, 48: 1.58, 49: 1.66, 50: 1.72
}

def hitung_koreksi(suhu):
    s_keys = sorted(data_koreksi.keys())
    s_vals = [data_koreksi[k] for k in s_keys]
    return float(np.interp(suhu, s_keys, s_vals))

# ===============================
# 4. CUSTOM CSS
# ===============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Michroma&family=Poppins:wght@400;700&display=swap');

.stApp {
    background: #0d1117;
    color: white;
}

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
    background: rgba(38, 196, 185, 0.05);
}

.jam-digital {
    color: #26c4b9;
    font-size: 30px;
    font-weight: 900;
    font-family: 'Poppins';
}
</style>
""", unsafe_allow_html=True)

# ===============================
# 5. HEADER & JAM DIGITAL
# ===============================
c1, c2 = st.columns([10, 3])
with c2:
    tz = pytz.timezone("Asia/Jakarta")
    now = datetime.datetime.now(tz)
    st.markdown(
        f"<div style='text-align:right'><div class='jam-digital'>{now.strftime('%H:%M:%S')}</div></div>",
        unsafe_allow_html=True
    )

st_autorefresh(interval=1000, key="clock")

# ===============================
# 6. PAGE LOGIC
# ===============================
if current_page == "dash":
    st.markdown(
        "<h1 style='font-family:Michroma; color:#26c4b9; text-align:center;'>CANE METRIX</h1>",
        unsafe_allow_html=True
    )
    st.write("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.button("📝\nINPUT DATA", on_click=navigasi, args=("input",), key="btn_input")

    with col2:
        st.button("🧮\nHITUNG ANALISA", on_click=navigasi, args=("analisa",), key="btn_analisa")

    with col3:
        st.button("📅\nDATABASE", on_click=navigasi, args=("db",), key="btn_db")

# ===============================
elif current_page == "analisa":
    st.markdown(
        "<h2 style='font-family:Michroma; color:#26c4b9;'>🧪 ANALISA TETES</h2>",
        unsafe_allow_html=True
    )

    st.button("🔙 KEMBALI KE DASHBOARD", on_click=navigasi, args=("dash",))

    st.write("---")

    col_inp, col_res = st.columns(2)

    with col_inp:
        st.subheader("📥 Input Data")
        brix_obs = st.number_input("Brix Teramati", value=8.80, format="%.2f")
        suhu_obs = st.number_input("Suhu Teramati (°C)", value=28.3, format="%.1f")

        koreksi = hitung_koreksi(suhu_obs)
        st.info(f"Koreksi Suhu: {koreksi:+.3f}")

    with col_res:
        st.subheader("📊 Hasil Analisa")
        total_brix = (brix_obs * 10) + koreksi

        st.markdown(f"""
        <div class="hasil-box">
            <p>Brix × 10 = {brix_obs * 10:.2f}</p>
            <p style="font-weight:bold;">% BRIX AKHIR</p>
            <h1 style="font-size:70px; font-family:Michroma;">{total_brix:.3f}</h1>
        </div>
        """, unsafe_allow_html=True)

# ===============================
elif current_page == "input":
    st.markdown("## 📝 INPUT DATA")
    st.button("🔙 Kembali", on_click=navigasi, args=("dash",))

# ===============================
elif current_page == "db":
    st.markdown("## 📅 DATABASE HARIAN")
    st.button("🔙 Kembali", on_click=navigasi, args=("dash",))

# ===============================
else:
    st.warning("Halaman tidak ditemukan.")
    st.button("🔙 Dashboard", on_click=navigasi, args=("dash",))
