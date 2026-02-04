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

# --- 2. FUNGSI KONEKSI GOOGLE SHEETS ---
def kirim_ke_excel(data_list, cell_range):
    """Fungsi untuk kirim data hasil hitung ke Excel"""
    try:
        creds_dict = st.secrets["gcp_service_account"]
        # Fix jika private_key mengandung karakter escape
        if "\\n" in creds_dict["private_key"]:
            creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
            
        creds = Credentials.from_service_account_info(
            creds_dict, 
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        client = gspread.authorize(creds)
        # Ganti dengan ID Spreadsheet lo
        sheet = client.open_by_key("1yQ2DbMy0ip_du1gqJ16jWwaWK8Psv6AB").worksheet("INPUT")
        
        # Kirim data ke range tertentu (misal: 'C124')
        sheet.update(cell_range, data_list)
        return True
    except Exception as e:
        st.error(f"Gagal Kirim: {e}")
        return False

# --- 3. FUNGSI LOGO & ASSETS ---
def get_base64_logo(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo_ptpn = get_base64_logo("ptpn.png")
logo_sgn = get_base64_logo("sgn.png")
logo_lpp = get_base64_logo("lpp.png")
logo_kb = get_base64_logo("kb.png")
logo_cane = get_base64_logo("canemetrix.png")

# --- 4. DATABASE TABEL (DARI KODINGAN LO) ---
data_koreksi = {27: -0.05, 28: 0.02, 29: 0.09, 30: 0.16, 31: 0.24, 32: 0.315, 33: 0.385, 34: 0.465, 35: 0.54, 36: 0.62, 37: 0.70, 38: 0.78, 39: 0.86, 40: 0.94}
data_bj = {0.0: 0.99640, 5.0: 1.01592, 10.0: 1.03608, 15.0: 1.05691, 20.0: 1.07844, 25.0: 1.10069, 30.0: 1.12368, 35.0: 1.14745, 40.0: 1.17203, 45.0: 1.19746, 49.0: 1.21839, 49.4: 1.22051, 49.5: 1.22104, 50.0: 1.22372, 55.0: 1.25083, 60.0: 1.27885, 65.0: 1.30781, 70.0: 1.33775}
data_tsai = {15.0: 336.00, 16.0: 316.00, 17.0: 298.00, 18.0: 282.00, 19.0: 267.00, 20.0: 254.50, 21.0: 242.90, 22.0: 231.80, 22.5: 223.60, 23.0: 222.20, 24.0: 213.30, 25.0: 204.80, 26.0: 197.40, 27.0: 190.40, 28.0: 183.70, 29.0: 177.60, 30.0: 171.70, 31.0: 166.30, 32.0: 161.20, 33.0: 156.60, 34.0: 152.20, 35.0: 147.90, 36.0: 143.90, 37.0: 140.20, 37.7: 136.67}

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

# --- 5. CSS (MODIFIKASI DIKIT UNTUK TOMBOL) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@300;400;700&display=swap');
    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.85), rgba(0, 10, 30, 0.85)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}
    .header-logo-box {{ background: white; padding: 10px 20px; border-radius: 15px; display: inline-flex; align-items: center; gap: 15px; margin-bottom: 20px; }}
    .header-logo-box img {{ height: 35px; width: auto; }}
    .hero-container {{ background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 30px; padding: 40px; margin-bottom: 30px; }}
    .card-result {{ background: rgba(38, 196, 185, 0.1); padding: 25px; border-radius: 20px; border: 2px solid #26c4b9; text-align: center; margin-bottom: 15px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 6. JAM REALTIME ---
@st.fragment(run_every="1s")
def jam_realtime():
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.datetime.now(tz)
    st.markdown(f'''<div style="text-align: right; color: white; font-family: 'Poppins';">{now.strftime("%d %B %Y")}<br><span style="font-family:'Orbitron'; color:#26c4b9; font-size:24px; font-weight:bold;">{now.strftime("%H:%M:%S")} WIB</span></div>''', unsafe_allow_html=True)

# --- 7. LOGIKA HALAMAN ---
if st.session_state.page == 'dashboard':
    col_h1, col_h2 = st.columns([2, 1])
    with col_h1:
        st.markdown(f'''<div class="header-logo-box">
            <img src="data:image/png;base64,{logo_ptpn}"><img src="data:image/png;base64,{logo_sgn}">
            <img src="data:image/png;base64,{logo_lpp}"><img src="data:image/png;base64,{logo_kb}">
        </div>''', unsafe_allow_html=True)
    with col_h2: jam_realtime()

    st.markdown(f'''<div class="hero-container" style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="font-family:Orbitron; color:white; font-size:55px; margin:0; line-height:1.1;">CANE METRIX</h1>
            <p style="color:#26c4b9; font-family:Poppins; font-weight:700; letter-spacing:5px; margin-top:10px;">ACCELERATING QA PERFORMANCE</p>
        </div>
        <img src="data:image/png;base64,{logo_cane}" style="height:150px; filter: drop-shadow(0 0 10px #26c4b9);">
    </div>''', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>📝</h1></div>", unsafe_allow_html=True)
        if st.button("INPUT DATA", key="dash_input", use_container_width=True): st.toast("Segera Hadir")
    with c2:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>🧮</h1></div>", unsafe_allow_html=True)
        if st.button("HITUNG ANALISA", key="dash_hitung", use_container_width=True):
            st.session_state.page = 'pilih_analisa'; st.rerun()
    with c3:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>📅</h1></div>", unsafe_allow_html=True)
        if st.button("DATABASE HARIAN", key="dash_db", use_container_width=True): st.toast("Segera Hadir")

elif st.session_state.page == 'pilih_analisa':
    st.markdown("<h2 style='text-align:center; color:white; font-family:Orbitron;'>PILIH JENIS ANALISA</h2>", unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    with m1:
        if st.button("🧪 ANALISA TETES", key="sel_tetes", use_container_width=True):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'tetes'; st.rerun()
    with m2:
        if st.button("🔬 OD TETES", key="sel_od", use_container_width=True):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'od'; st.rerun()

    m3, m4 = st.columns(2)
    with m3:
        if st.button("⚗️ ANALISA TSAI TETES", key="sel_tsai", use_container_width=True):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'tsai'; st.rerun()
    with m4:
        if st.button("💎 ANALISA ICUMSA GULA", key="sel_icumsa", use_container_width=True):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'icumsa'; st.rerun()
    
    if st.button("🔙 KEMBALI KE DASHBOARD", key="back_dash", use_container_width=True):
        st.session_state.page = 'dashboard'; st.rerun()

elif st.session_state.page == 'analisa_lab':
    # Ambil jam sekarang untuk menentukan baris
    tz = pytz.timezone('Asia/Jakarta')
    jam_now = datetime.datetime.now(tz).hour
    
    # --- UI ANALISA LAB (TEMPLATE UMUM) ---
    if st.session_state.analisa_type == 'tetes':
        st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="hero-container">', unsafe_allow_html=True)
            cx, cy = st.columns(2)
            with cx:
                bx_in = st.number_input("Brix Teramati", value=8.80, format="%.2f")
                sh_in = st.number_input("Suhu (°C)", value=28.0, format="%.1f")
                pol_baca = st.number_input("Pol Baca", value=11.00, format="%.2f")
                jam_analisa = st.selectbox("Analisa Jam", list(range(6, 24)) + list(range(0, 6)), index=jam_now-6 if 6<=jam_now<=23 else 0)
                
                kor = hitung_interpolasi(sh_in, data_koreksi)
                bj = hitung_interpolasi(bx_in, data_bj)
                brix_akhir = (bx_in + kor) * 10
                pol_akhir = (0.286 * pol_baca) / bj * 10
                hk = (pol_akhir / brix_akhir * 100) if brix_akhir != 0 else 0
                st.info(f"💡 Koreksi: {kor:+.3f} | BJ: {bj:.6f}")
            with cy:
                st.markdown(f'<div class="card-result"><h1 style="color:#26c4b9; font-family:Orbitron; margin:0;">{brix_akhir:.3f}</h1><p style="color:white;">% BRIX AKHIR</p></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="card-result" style="border-color:#ffcc00;"><h1 style="color:#ffcc00; font-family:Orbitron; margin:0;">{pol_akhir:.3f}</h1><p style="color:white;">% POL AKHIR</p></div>', unsafe_allow_html=True)
                if st.button("🚀 KIRIM KE DATABASE EXCEL"):
                    # Tentukan baris (Contoh Baris 124 untuk jam 6)
                    baris = 124 + (jam_analisa - 6) if jam_analisa >= 6 else 124 + (jam_analisa + 18)
                    success = kirim_ke_excel([[brix_akhir, pol_akhir]], f"C{baris}:D{baris}")
                    if success: st.success(f"Data Jam {jam_analisa} Masuk ke Baris {baris}!")
            st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.analisa_type == 'icumsa':
        st.markdown("<h2 style='text-align:center; color:#00d4ff; font-family:Orbitron;'>💎 ANALISA ICUMSA GULA</h2>", unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="hero-container">', unsafe_allow_html=True)
            cx, cy = st.columns(2)
            with cx:
                abs_icumsa = st.number_input("Absorbansi (Abs)", value=0.149, format="%.3f")
                brix_icumsa = st.number_input("% Brix Gula", value=49.44, format="%.2f")
                jam_analisa = st.selectbox("Analisa Jam", list(range(6, 24)) + list(range(0, 6)))
                bj_icumsa = hitung_interpolasi(brix_icumsa, data_bj)
                icumsa_res = (abs_icumsa * 100000) / (brix_icumsa * 1 * bj_icumsa) if brix_icumsa > 0 else 0
                st.info(f"🔍 BJ Terdeteksi: {bj_icumsa:.5f}")
            with cy:
                st.markdown(f'<div class="card-result" style="border-color:#00d4ff;"><h1 style="color:#00d4ff; font-size:60px; font-family:Orbitron; margin:0;">{icumsa_res:.2f}</h1><p style="color:white;">IU (ICUMSA UNIT)</p></div>', unsafe_allow_html=True)
                if st.button("🚀 SIMPAN KE EXCEL"):
                    baris = 124 + (jam_analisa - 6) if jam_analisa >= 6 else 124 + (jam_analisa + 18)
                    success = kirim_ke_excel([[icumsa_res]], f"I{baris}")
                    if success: st.success("Data ICUMSA Terupdate!")
            st.markdown('</div>', unsafe_allow_html=True)

    # Tambahkan menu lainnya (OD, TSAI) dengan pola yang sama...
    
    if st.button("🔙 KEMBALI KE MENU PILIHAN", use_container_width=True):
        st.session_state.page = 'pilih_analisa'; st.rerun()
