import streamlit as st
import datetime
import pytz
import base64
import os
import gspread
from google.oauth2.service_account import Credentials

# --- 1. CONFIG & STATE ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

# (Koneksi Excel & State Awal Tetap Sama)
def init_connection():
    try:
        s = st.secrets["gcp_service_account"]
        pk = s["private_key"].replace("\\n", "\n")
        info = {
            "type": s["type"], "project_id": s["project_id"],
            "private_key_id": s["private_key_id"], "private_key": pk,
            "client_email": s["client_email"], "client_id": s["client_id"],
            "auth_uri": s["auth_uri"], "token_uri": s["token_uri"],
            "auth_provider_x509_cert_url": s["auth_provider_x509_cert_url"],
            "client_x509_cert_url": s["client_x509_cert_url"]
        }
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(info, scopes=scopes)
        return gspread.authorize(creds)
    except Exception as e:
        return None

if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'
if 'analisa_type' not in st.session_state:
    st.session_state.analisa_type = None

# --- 2. FUNGSI LOGO & ASSETS (Tetap Sama) ---
def get_base64_logo(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

logo_ptpn = get_base64_logo("ptpn.png"); logo_sgn = get_base64_logo("sgn.png")
logo_lpp = get_base64_logo("lpp.png"); logo_kb = get_base64_logo("kb.png")
logo_cane = get_base64_logo("canemetrix.png")

# --- 3. DATABASE TABEL (Sama + Tambahan Rumus) ---
data_koreksi = {27: -0.05, 28: 0.02, 29: 0.09, 30: 0.16, 31: 0.24, 32: 0.315, 33: 0.385, 34: 0.465, 35: 0.54, 36: 0.62, 37: 0.70, 38: 0.78, 39: 0.86, 40: 0.94}
data_bj = {0.0: 0.99640, 5.0: 1.01592, 10.0: 1.03608, 15.0: 1.05691, 20.0: 1.07844, 25.0: 1.10069, 30.0: 1.12368, 35.0: 1.14745, 40.0: 1.17203, 45.0: 1.19746, 50.0: 1.22372, 60.0: 1.27885, 70.0: 1.33775}
data_tsai = {15.0: 336.00, 20.0: 254.50, 25.0: 204.80, 30.0: 171.70, 37.7: 136.67}

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

# FUNGSI BARU: Hitung Brix/Pol Nira
def hitung_nira(bx_baca, suhu, pol_baca):
    kor = hitung_interpolasi(suhu, data_koreksi)
    bx_kor = bx_baca + kor
    bj = hitung_interpolasi(bx_baca, data_bj)
    pol = (0.286 * pol_baca) / bj
    hk = (pol / bx_kor * 100) if bx_kor != 0 else 0
    return bx_kor, pol, hk

# --- 4. CSS (Tetap Sama) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@300;400;700&display=swap');
    .stApp {{ background: linear-gradient(rgba(0, 10, 30, 0.85), rgba(0, 10, 30, 0.85)), url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"); background-size: cover; background-position: center; background-attachment: fixed; }}
    .header-logo-box {{ background: white; padding: 10px 20px; border-radius: 15px; display: inline-flex; align-items: center; gap: 15px; margin-bottom: 20px; }}
    .header-logo-box img {{ height: 35px; width: auto; }}
    .hero-container {{ background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 30px; padding: 40px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center; }}
    div.stButton > button {{ background: rgba(255, 255, 255, 0.07) !important; backdrop-filter: blur(10px) !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 20px !important; color: white !important; height: 180px !important; width: 100% !important; transition: 0.3s !important; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
    div.stButton > button:hover {{ background: rgba(38, 196, 185, 0.2) !important; border-color: #26c4b9 !important; box-shadow: 0 0 25px rgba(38, 196, 185, 0.4) !important; transform: translateY(-8px) !important; }}
    .card-result {{ background: rgba(38, 196, 185, 0.1); padding: 25px; border-radius: 20px; border: 2px solid #26c4b9; text-align: center; margin-bottom: 15px; }}
    .status-normatif {{ padding: 10px; border-radius: 10px; font-weight: bold; text-align: center; margin-top: 10px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. JAM REALTIME (Tetap Sama) ---
@st.fragment(run_every="1s")
def jam_realtime():
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.datetime.now(tz)
    st.markdown(f'''<div style="text-align: right; color: white; font-family: 'Poppins';">{now.strftime("%d %B %Y")}<br><span style="font-family:'Orbitron'; color:#26c4b9; font-size:24px; font-weight:bold;">{now.strftime("%H:%M:%S")} WIB</span></div>''', unsafe_allow_html=True)

# --- 6. LOGIKA HALAMAN ---
if st.session_state.page == 'dashboard':
    col_h1, col_h2 = st.columns([2, 1])
    with col_h1: st.markdown(f'''<div class="header-logo-box"><img src="data:image/png;base64,{logo_ptpn}"><img src="data:image/png;base64,{logo_sgn}"><img src="data:image/png;base64,{logo_lpp}"><img src="data:image/png;base64,{logo_kb}"></div>''', unsafe_allow_html=True)
    with col_h2: jam_realtime()
    st.markdown(f'''<div class="hero-container"><div><h1 style="font-family:Orbitron; color:white; font-size:55px; margin:0; line-height:1.1;">CANE METRIX</h1><p style="color:#26c4b9; font-family:Poppins; font-weight:700; letter-spacing:5px; margin-top:10px;">ACCELERATING QA PERFORMANCE</p></div><img src="data:image/png;base64,{logo_cane}" style="height:150px; filter: drop-shadow(0 0 10px #26c4b9);"></div>''', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>📝</h1></div>", unsafe_allow_html=True)
        # UBAH: Aktifkan Menu INPUT DATA
        if st.button("INPUT DATA", key="dash_input", use_container_width=True): 
            st.session_state.page = 'pilih_stasiun'; st.rerun()
    with c2:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>🧮</h1></div>", unsafe_allow_html=True)
        if st.button("HITUNG ANALISA", key="dash_hitung", use_container_width=True): st.session_state.page = 'pilih_analisa'; st.rerun()
    with c3:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>📅</h1></div>", unsafe_allow_html=True)
        if st.button("DATABASE HARIAN", key="dash_db", use_container_width=True): st.toast("Segera Hadir")

# HALAMAN BARU: PILIH STASIUN
elif st.session_state.page == 'pilih_stasiun':
    st.markdown("<h2 style='text-align:center; color:white; font-family:Orbitron;'>PILIH STASIUN</h2>", unsafe_allow_html=True)
    s1, s2 = st.columns(2)
    with s1:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>🚜</h1></div>", unsafe_allow_html=True)
        if st.button("STASIUN GILINGAN", key="st_gilingan", use_container_width=True):
            st.session_state.page = 'input_gilingan'; st.rerun()
    with s2:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>🌫️</h1></div>", unsafe_allow_html=True)
        if st.button("PEMURNIAN & PENGUAPAN", use_container_width=True): st.toast("Segera Hadir")
    
    if st.button("🔙 KEMBALI KE DASHBOARD", use_container_width=True): st.session_state.page = 'dashboard'; st.rerun()

# HALAMAN BARU: INPUT GILINGAN (REALTIME SIMULATION)
elif st.session_state.page == 'input_gilingan':
    st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>🚜 MONITORING STASIUN GILINGAN</h2>", unsafe_allow_html=True)
    
    tab_npp, tab_nm, tab_ops, tab_summary = st.tabs(["Nira Gilingan", "Nira Mentah", "Operasional & Ampas", "Summary Performa"])
    
    with tab_npp:
        c_npp1, c_npp2 = st.columns(2)
        with c_npp1:
            st.subheader("Nira Gilingan 1 (NPP)")
            bx_npp = st.number_input("Brix Baca NPP", value=18.5, key="bx_npp")
            suhu_npp = st.number_input("Suhu NPP", value=28.0, key="sh_npp")
            pol_npp = st.number_input("Pol Baca NPP", value=55.0, key="pl_npp")
            p2o5_npp = st.number_input("P2O5 (ppm)", value=200, key="p2_npp")
        with c_npp2:
            st.subheader("Detail NPP")
            dex_npp = st.number_input("Dextran", value=0, key="dx_npp")
            icu_npp = st.number_input("Icumsa NPP", value=0, key="ic_npp")
            # Hitung Otomatis
            bx_k, pl_k, hk_npp = hitung_nira(bx_npp, suhu_npp, pol_npp)
            st.success(f"Hasil NPP: Brix {bx_k:.2f} | Pol {pl_k:.2f} | HK {hk_npp:.2f}")

    with tab_nm:
        st.subheader("Analisa Nira Mentah (NM)")
        col_nm1, col_nm2, col_nm3 = st.columns(3)
        with col_nm1:
            bx_nm = st.number_input("Brix Baca NM", value=15.0)
            pl_nm = st.number_input("Pol Baca NM", value=40.0)
        with col_nm2:
            p2o5_nm = st.number_input("P2O5 NM", value=180)
            kapur_nm = st.number_input("Kadar Kapur", value=0)
        with col_nm3:
            icu_nm = st.number_input("Icumsa NM", value=0)
            tsas_nm = st.number_input("TSAS", value=0)

    with tab_ops:
        st.subheader("Data Operasional & Ampas")
        o1, o2 = st.columns(2)
        with o1:
            tebu_jam = st.number_input("Berat Tebu (Ton/Jam)", value=100.0)
            nm_jam = st.number_input("Berat Nira Mentah (Ton/Jam)", value=90.0)
        with o2:
            pol_ampas = st.number_input("% Pol Ampas", value=2.5)
            zk_ampas = st.number_input("% Zat Kering Ampas", value=50.0)
            imb_suhu = st.number_input("Suhu Imbibisi", value=70.0)

    with tab_summary:
        st.subheader("📊 Intelligence Performance")
        # Logika HPB Sederhana (Simulasi)
        hpb_i = 68.5  # Contoh hitung
        hpb_total = 93.2 # Contoh hitung
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            color_hpbi = "#26c4b9" if 65 <= hpb_i <= 70 else "#ff4b4b"
            st.markdown(f'<div class="card-result" style="border-color:{color_hpbi};"><h1>{hpb_i}%</h1><p>HPB GILINGAN I</p></div>', unsafe_allow_html=True)
            if hpb_i < 65: st.error("⚠️ HPB I Rendah! Cek Tekanan Gilingan 1")
        
        with col_res2:
            color_hpbt = "#26c4b9" if 92 <= hpb_total <= 95 else "#ff4b4b"
            st.markdown(f'<div class="card-result" style="border-color:{color_hpbt};"><h1>{hpb_total}%</h1><p>HPB TOTAL</p></div>', unsafe_allow_html=True)
            if hpb_total < 92: st.error("⚠️ Efisiensi Rendah! Cek Air Imbibisi")

    if st.button("🔙 KEMBALI KE PILIHAN STASIUN", use_container_width=True):
        st.session_state.page = 'pilih_stasiun'; st.rerun()

# --- SISANYA TETAP SAMA (Halaman Analisa Lab Tetes Dll) ---
elif st.session_state.page == 'pilih_analisa':
    st.markdown("<h2 style='text-align:center; color:white; font-family:Orbitron;'>PILIH JENIS ANALISA</h2>", unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    with m1:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>🧪</h1></div>", unsafe_allow_html=True)
        if st.button("ANALISA TETES", key="sel_tetes", use_container_width=True):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'tetes'; st.rerun()
    with m2:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>🔬</h1></div>", unsafe_allow_html=True)
        if st.button("OD TETES", key="sel_od", use_container_width=True):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'od'; st.rerun()
    m3, m4 = st.columns(2)
    with m3:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>⚗️</h1></div>", unsafe_allow_html=True)
        if st.button("ANALISA TSAI TETES", key="sel_tsai", use_container_width=True):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'tsai'; st.rerun()
    with m4:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>💎</h1></div>", unsafe_allow_html=True)
        if st.button("ANALISA ICUMSA GULA", key="sel_icumsa", use_container_width=True):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'icumsa'; st.rerun()
    if st.button("🔙 KEMBALI KE DASHBOARD", key="back_dash", use_container_width=True): st.session_state.page = 'dashboard'; st.rerun()

elif st.session_state.page == 'analisa_lab':
    # (Kode Analisa Lab Tetes, OD, TSAI, Icumsa yang sudah ada tetap di sini tanpa perubahan)
    list_jam = [f"{(i % 24):02d}:00" for i in range(6, 30)]
    if st.session_state.analisa_type == 'tetes':
        # ... (Kode Tetes lo)
        st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
        # (Lanjutin kode tetes lo yang asli di sini)
        if st.button("🔙 KEMBALI KE MENU PILIHAN", key="back_sub", use_container_width=True):
            st.session_state.page = 'pilih_analisa'; st.rerun()
