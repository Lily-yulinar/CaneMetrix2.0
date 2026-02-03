import streamlit as st
import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
import base64
import os

# --- 1. INITIAL STATE ---
# Logic untuk perpindahan halaman (Dashboard <-> Analisa Tetes)
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")
st_autorefresh(interval=1000, key="datarefresh")

# Waktu & Jam
tz = pytz.timezone('Asia/Jakarta')
now = datetime.datetime.now(tz)
tgl_skrg = now.strftime("%d %B %Y")
jam_skrg = now.strftime("%H:%M:%S")

# Data Tabel Koreksi (Interpolasi)
data_koreksi = {
    25: -0.19, 26: -0.12, 27: -0.05, 28: 0.02, 29: 0.09, 30: 0.16,
    31: 0.24, 32: 0.31, 33: 0.38, 34: 0.46, 35: 0.54, 36: 0.62,
    37: 0.70, 38: 0.78, 39: 0.86, 40: 0.94, 41: 1.02, 42: 1.10,
    43: 1.18, 44: 1.26, 45: 1.34, 46: 1.42, 47: 1.50, 48: 1.58,
    49: 1.66, 50: 1.72
}

def hitung_interpolasi(suhu_user):
    suhu_keys = sorted(data_koreksi.keys())
    if suhu_user in data_koreksi: return data_koreksi[suhu_user]
    if suhu_user < suhu_keys[0]: return data_koreksi[suhu_keys[0]]
    if suhu_user > suhu_keys[-1]: return data_koreksi[suhu_keys[-1]]
    for i in range(len(suhu_keys) - 1):
        x0, x1 = suhu_keys[i], suhu_keys[i+1]
        if x0 < suhu_user < x1:
            y0, y1 = data_koreksi[x0], data_koreksi[x1]
            return y0 + (suhu_user - x0) * (y1 - y0) / (x1 - x0)
    return 0.0

def get_base64_logo(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo_ptpn = get_base64_logo("ptpn.png")
logo_sgn = get_base64_logo("sgn.png")
logo_lpp = get_base64_logo("lpp.png")
logo_cane = get_base64_logo("canemetrix.png")

# --- 2. CSS CUSTOM (FIX LOGO & FONT) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Michroma&family=Poppins:wght@300;400;700&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.75), rgba(0, 10, 30, 0.75)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* KOTAK LOGO PANJANG KE KANAN */
    .partner-box {{ 
        background: white; 
        padding: 12px 60px; 
        border-radius: 12px; 
        display: inline-flex; 
        align-items: center; 
        gap: 55px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        min-width: 450px;
    }}
    .img-partner {{ height: 35px; width: auto; }}

    .hero-container {{
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 40px;
        padding: 50px; margin: 10px auto 30px auto; display: flex; 
        justify-content: space-between; align-items: center; max-width: 95%;
    }}

    .title-text {{
        font-family: 'Michroma', sans-serif; 
        color: white; 
        font-size: 58px; 
        letter-spacing: 12px; 
        margin: 0; 
        font-weight: 400;
        text-shadow: 0 0 10px rgba(255,255,255,0.3), 0 0 25px #26c4b9;
        text-transform: uppercase;
    }}

    .menu-card-container {{
        position: relative; background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(10px); border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1); height: 180px;
        transition: 0.3s; margin-bottom: 25px; display: flex;
        flex-direction: column; justify-content: center; align-items: center;
    }}

    .menu-card-container:hover {{
        background: rgba(38, 196, 185, 0.15); border: 1px solid #26c4b9;
