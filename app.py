import streamlit as st
import datetime
import pytz
import base64
import os
import gspread
from google.oauth2.service_account import Credentials

# --- 1. CONFIG & STATE ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'
if 'analisa_type' not in st.session_state:
    st.session_state.analisa_type = None

# --- 2. FUNGSI LOGO & ASSETS ---
def get_base64_logo(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo_ptpn = get_base64_logo("ptpn.png"); logo_sgn = get_base64_logo("sgn.png")
logo_lpp = get_base64_logo("lpp.png"); logo_kb = get_base64_logo("kb.png")
logo_cane = get_base64_logo("canemetrix.png")

# --- 3. DATABASE TABEL & HELPER ---
data_koreksi = {27: -0.05, 28: 0.02, 29: 0.09, 30: 0.16, 31: 0.24, 32: 0.315, 33: 0.385, 34: 0.465, 35: 0.54, 36: 0.62, 37: 0.70, 38: 0.78, 39: 0.86, 40: 0.94}
data_bj = {0.0: 0.99640, 5.0: 1.01592, 10.0: 1.03608, 15.0: 1.05691, 20.0: 1.07844, 25.0: 1.10069, 30.0: 1.12368, 35.0: 1.14745, 40.0: 1.17203, 45.0: 1.19746, 50.0: 1.22372}

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

# --- 4. CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@300;400;700&display=swap');
    .stApp {{ background: linear-gradient(rgba(0, 10, 30, 0.85), rgba(0, 10, 30, 0.85)), url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"); background-size: cover; background-position: center; background-attachment: fixed; }}
    .header-logo-box {{ background: white; padding: 10px 20px; border-radius: 15px; display: inline-flex; align-items: center; gap: 15px; margin-bottom: 20px; }}
    .header-logo-box img {{ height: 35px; width: auto; }}
    .hero-container {{ background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 30px; padding: 40px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center; }}
    div.stButton > button {{ background: rgba(255, 255, 255, 0.07) !important; backdrop-filter: blur(10px) !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 20px !important; color: white !important; transition: 0.3s !important; }}
    .card-result {{ background: rgba(38, 196, 185, 0.1); padding: 25px; border-radius: 20px; border: 2px solid #26c4b9; text-align: center; margin-bottom: 15px; }}
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI TAMPILAN GAMBAR 2 (Brix, Pol, HK) ---
def render_brix_pol_hk(label, key_prefix):
    st.markdown(f"### Analisa {label}")
    c_left, c_right = st.columns([1, 1.2])
    with c_left:
        bx_baca = st.number_input(f"Brix Teramati ({label})", value=0.0, key=f"{key_prefix}_bx")
        suhu = st.number_input(f"Suhu (°C) ({label})", value=28.0, key=f"{key_prefix}_sh")
        pol_baca = st.number_input(f"Pol Baca ({label})", value=0.0, key=f"{key_prefix}_pol")
        jam = st.selectbox("Analisa Jam", options=[f"{(i % 24):02d}:00" for i in range(6, 30)], key=f"{key_prefix}_jam")
        kor = hitung_interpolasi(suhu, data_koreksi); bj = hitung_interpolasi(bx_baca, data_bj)
        brix_fix = (bx_baca + kor) if bx_baca > 0 else 0
        pol_fix = (0.286 * pol_baca) / bj if bj > 0 else 0
        hk = (pol_fix / brix_fix * 100) if brix_fix > 0 else 0
        st.info(f"💡 Koreksi: {kor:+.3f} | BJ: {bj:.6f}")
        if st.button(f"🚀 SIMPAN DATA {label}", key=f"{key_prefix}_save", use_container_width=True): st.toast("Data Disimpan!")
    with c_right:
        st.markdown(f'<div class="card-result"><h1 style="color:#26c4b9; font-family:Orbitron; margin:0;">{brix_fix:.3f}</h1><p style="color:white;">% BRIX AKHIR</p></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card-result" style="border-color:#ffcc00;"><h1 style="color:#ffcc00; font-family:Orbitron; margin:0;">{pol_fix:.3f}</h1><p style="color:white;">% POL AKHIR</p></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card-result" style="border-color:#ff4b4b;"><h1 style="color:#ff4b4b; font-family:Orbitron; margin:0;">{hk:.2f}</h1><p style="color:white;">HK</p></div>', unsafe_allow_html=True)

@st.fragment(run_every="1s")
def jam_realtime():
    now = datetime.datetime.now(pytz.timezone('Asia/Jakarta'))
    st.markdown(f'''<div style="text-align: right; color: white;">{now.strftime("%d %B %Y")}<br><span style="color:#26c4b9; font-size:24px; font-weight:bold;">{now.strftime("%H:%M:%S")} WIB</span></div>''', unsafe_allow_html=True)

# === 1. DASHBOARD ===
if st.session_state.page == 'dashboard':
    col_h1, col_h2 = st.columns([2, 1])
    with col_h1: st.markdown(f'''<div class="header-logo-box"><img src="data:image/png;base64,{logo_ptpn}"><img src="data:image/png;base64,{logo_sgn}"><img src="data:image/png;base64,{logo_lpp}"><img src="data:image/png;base64,{logo_kb}"></div>''', unsafe_allow_html=True)
    with col_h2: jam_realtime()
    st.markdown(f'''<div class="hero-container"><div><h1 style="font-family:Orbitron; color:white; font-size:55px; margin:0;">CANE METRIX</h1><p style="color:#26c4b9; letter-spacing:5px;">ACCELERATING QA PERFORMANCE</p></div><img src="data:image/png;base64,{logo_cane}" style="height:150px;"></div>''', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("📝 INPUT DATA", use_container_width=True, height=180): st.session_state.page = 'pilih_stasiun'; st.rerun()
    with c2: 
        if st.button("🧮 HITUNG ANALISA", use_container_width=True, height=180): st.session_state.page = 'pilih_analisa'; st.rerun()
    with c3: 
        if st.button("📅 DATABASE HARIAN", use_container_width=True, height=180): st.toast("Segera Hadir")

# === 2. PILIH STASIUN (DIKEMBALIKAN) ===
elif st.session_state.page == 'pilih_stasiun':
    st.markdown("<h2 style='text-align:center; color:white; font-family:Orbitron;'>PILIH STASIUN</h2>", unsafe_allow_html=True)
    r1c1, r1c2, r1c3 = st.columns(3)
    r2c1, r2c2, r2c3 = st.columns(3)
    with r1c1:
        if st.button("🚜 GILINGAN", use_container_width=True): st.session_state.page = 'input_gilingan'; st.rerun()
    with r1c2:
        if st.button("🌫️ PEMURNIAN", use_container_width=True): st.toast("Fitur Pemurnian")
    with r1c3:
        if st.button("🔥 PENGUAPAN", use_container_width=True): st.toast("Fitur Penguapan")
    with r2c1:
        if st.button("💎 MASAKAN", use_container_width=True): st.toast("Fitur Masakan")
    with r2c2:
        if st.button("🌀 PUTARAN", use_container_width=True): st.toast("Fitur Putaran")
    with r2c3:
        if st.button("📦 PENGEMASAN", use_container_width=True): st.toast("Fitur Pengemasan")
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI KE DASHBOARD", use_container_width=True): st.session_state.page = 'dashboard'; st.rerun()

# === 3. HITUNG ANALISA (DIKEMBALIKAN KE 4 MENU) ===
elif st.session_state.page == 'pilih_analisa':
    st.markdown("<h2 style='text-align:center; color:white; font-family:Orbitron;'>PILIH JENIS ANALISA</h2>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        if st.button("🧪 ANALISA TETES", use_container_width=True, height=150): st.toast("Analisa Tetes")
    with m2:
        if st.button("🔬 OD TETES", use_container_width=True, height=150): st.toast("OD Tetes")
    with m3:
        if st.button("🌈 ICUMSA", use_container_width=True, height=150): st.toast("Icumsa")
    with m4:
        if st.button("📊 TSAI", use_container_width=True, height=150): st.toast("TSAI")
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI KE DASHBOARD", use_container_width=True): st.session_state.page = 'dashboard'; st.rerun()

# === 4. INPUT GILINGAN (UPDATE TERSTRUKTUR) ===
elif st.session_state.page == 'input_gilingan':
    st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>🚜 DATA STASIUN GILINGAN</h2>", unsafe_allow_html=True)
    tabs = st.tabs(["NPP", "Gilingan 2", "Gilingan 3", "Gilingan 4", "Nira Mentah", "Ampas", "Lainnya"])
    
    with tabs[0]: # NPP
        sub = st.tabs(["(Brix, Pol, HK)", "Gula Reduksi", "Kadar Posfat", "Dextran", "Icumsa"])
        with sub[0]: render_brix_pol_hk("NPP", "npp")
    with tabs[1]: render_brix_pol_hk("Gilingan 2", "g2")
    with tabs[2]: render_brix_pol_hk("Gilingan 3", "g3")
    with tabs[3]: render_brix_pol_hk("Gilingan 4", "g4")
    with tabs[4]: # Nira Mentah
        sub_nm = st.tabs(["(Brix, Pol, HK)", "Gula Reduksi", "Kadar Posfat", "Dextran", "Icumsa", "TSAS"])
        with sub_nm[0]: render_brix_pol_hk("Nira Mentah", "nm")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI KE PILIH STASIUN", use_container_width=True): st.session_state.page = 'pilih_stasiun'; st.rerun()
