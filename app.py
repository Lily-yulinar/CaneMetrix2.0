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

# --- 2. FUNGSI LOGO & ASSETS ---
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

# --- 3. DATABASE TABEL ---

# Tabel Koreksi Suhu Brix
data_koreksi = {
    27: -0.05, 28: 0.02, 29: 0.09, 30: 0.16, 31: 0.24, 
    32: 0.315, 33: 0.385, 34: 0.465, 35: 0.54, 36: 0.62,
    37: 0.70, 38: 0.78, 39: 0.86, 40: 0.94
}

# Tabel BJ
data_bj = {
    0.0: 0.996373, 1.0: 1.000201, 2.0: 1.004058, 3.0: 1.007944,
    4.0: 1.011858, 5.0: 1.015801, 6.0: 1.019772, 7.0: 1.023773,
    8.0: 1.027803, 8.8: 1.031047, 9.0: 1.031862, 10.0: 1.035950,
    11.0: 1.040068, 12.0: 1.044216, 13.0: 1.048394, 14.0: 1.052602,
    15.0: 1.056841, 16.0: 1.061110, 17.0: 1.065410, 18.0: 1.069741,
    19.0: 1.074103, 20.0: 1.078497, 21.0: 1.082923, 22.0: 1.087380,
    23.0: 1.091870, 23.9: 1.095939
}

# Tabel TSAI (Dari Foto Yang Lo Kirim)
data_tsai = {
    15.0: 336.00, 15.1: 334.00, 15.2: 330.40, 15.3: 326.08, 15.4: 322.05, 15.5: 319.02, 15.6: 317.21, 15.7: 316.36, 15.8: 316.07, 15.9: 316.01,
    16.0: 316.00, 16.1: 314.20, 16.2: 310.96, 16.3: 307.07, 16.4: 303.44, 16.5: 300.72, 16.6: 299.09, 16.7: 298.33, 16.8: 298.07, 16.9: 298.01,
    17.0: 298.00, 17.1: 296.40, 17.2: 293.52, 17.3: 290.06, 17.4: 286.84, 17.5: 284.42, 17.6: 282.97, 17.7: 282.29, 17.8: 282.06, 17.9: 282.01,
    18.0: 282.00, 18.1: 280.50, 18.2: 277.80, 18.3: 274.56, 18.4: 271.54, 18.5: 269.27, 18.6: 267.91, 18.7: 267.27, 18.8: 267.05, 18.9: 267.01,
    19.0: 267.00, 19.1: 267.75, 19.2: 263.50, 19.3: 260.80, 19.4: 258.28, 19.5: 256.39, 19.6: 255.26, 19.7: 254.73, 19.8: 254.33, 19.9: 254.50,
    20.0: 254.50, 20.1: 253.34, 20.2: 251.25, 20.3: 248.75, 20.4: 246.41, 20.5: 244.65, 20.6: 243.60, 20.7: 243.41, 20.8: 242.94, 20.9: 242.90,
    21.0: 242.90, 21.1: 241.79, 21.2: 239.79, 21.3: 237.39, 21.4: 235.36, 21.5: 233.48, 21.6: 232.47, 21.7: 232.00, 21.8: 231.84, 21.9: 231.80,
    22.0: 231.80, 22.1: 230.84, 22.2: 229.34, 22.3: 227.04, 22.4: 225.10, 22.5: 223.60, 22.6: 222.78, 22.7: 222.37, 22.8: 222.23, 22.9: 222.20,
    23.0: 222.20, 23.1: 221.31, 23.2: 219.71, 23.3: 217.79, 23.4: 215.99, 23.5: 214.65, 23.6: 213.84, 23.7: 213.46, 23.8: 213.33, 23.9: 213.30,
    24.0: 213.30, 24.1: 212.45, 24.2: 210.92, 24.3: 209.08, 24.4: 207.37, 24.5: 206.09, 24.6: 205.31, 24.7: 204.95, 24.8: 204.83, 24.9: 204.80,
    25.0: 204.80, 25.1: 204.06, 25.2: 202.73, 25.3: 201.13, 25.4: 199.64, 25.5: 198.52, 25.6: 197.85, 25.7: 197.53, 25.8: 197.43, 25.9: 197.40,
    26.0: 197.40, 26.1: 196.70, 26.2: 195.44, 26.3: 193.93, 26.4: 192.52, 26.5: 191.46, 26.6: 190.82, 26.7: 190.53, 26.8: 190.43, 26.9: 190.40,
    27.0: 190.40, 27.1: 189.73, 27.2: 188.52, 27.3: 187.08, 27.4: 185.73, 27.5: 184.71, 27.6: 184.11, 27.7: 183.82, 27.8: 183.72, 27.9: 183.70,
    28.0: 183.70, 28.1: 183.09, 28.2: 181.99, 28.3: 180.67, 28.4: 179.44, 28.5: 178.52, 28.6: 177.97, 28.7: 177.71, 28.8: 177.62, 28.9: 177.60,
    29.0: 177.60, 29.1: 177.01, 29.2: 175.95, 29.3: 174.67, 29.4: 173.48, 29.5: 172.59, 29.6: 172.06, 29.7: 171.81, 29.8: 171.72, 29.9: 171.70,
    30.0: 171.70, 30.1: 171.16, 30.2: 170.19, 30.3: 169.07, 30.4: 167.93, 30.5: 167.12, 30.6: 166.63, 30.7: 166.40, 30.8: 166.32, 30.9: 166.30,
    31.0: 166.30, 31.1: 165.79, 31.2: 164.87, 31.3: 163.77, 31.4: 162.74, 31.5: 161.97, 31.6: 161.51, 31.7: 161.29, 31.8: 161.22, 31.9: 161.20,
    32.0: 161.20, 32.1: 160.74, 32.2: 159.91, 32.3: 158.92, 32.4: 157.99, 32.5: 157.30, 32.6: 156.88, 32.7: 156.68, 32.8: 156.62, 32.9: 156.60,
    33.0: 156.60, 33.1: 156.16, 33.2: 155.37, 33.3: 154.42, 33.4: 153.53, 33.5: 152.87, 33.6: 152.47, 33.7: 152.28, 33.8: 152.22, 33.9: 152.20,
    34.0: 152.20, 34.1: 151.71, 34.2: 151.00, 34.3: 150.07, 34.4: 149.20, 34.5: 148.55, 34.6: 148.16, 34.7: 147.98, 34.8: 147.92, 34.9: 147.90,
    35.0: 147.90, 35.1: 147.50, 35.2: 146.78, 35.3: 145.92, 35.4: 145.11, 35.5: 144.50, 35.6: 144.14, 35.7: 143.97, 35.8: 143.91, 35.9: 143.90,
    36.0: 143.90, 36.1: 143.53, 36.2: 142.64, 36.3: 142.06, 36.4: 141.32, 36.5: 140.76, 36.6: 140.42, 36.7: 142.27, 36.8: 140.21, 36.9: 140.20,
    37.0: 140.20, 37.1: 139.84, 37.2: 139.19, 37.3: 138.41, 37.4: 137.69, 37.5: 137.14, 37.6: 136.82, 37.7: 136.67
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

# --- 4. CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@300;400;700&display=swap');
    
    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.85), rgba(0, 10, 30, 0.85)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    .header-logo-box {{
        background: white; padding: 10px 20px; border-radius: 15px; 
        display: inline-flex; align-items: center; gap: 15px; margin-bottom: 20px;
    }}
    .header-logo-box img {{ height: 35px; width: auto; }}

    .hero-container {{
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 30px;
        padding: 40px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center;
    }}

    div.stButton > button {{
        background: rgba(255, 255, 255, 0.07) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        color: white !important;
        height: 180px !important;
        width: 100% !important;
        transition: 0.3s !important;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
    }}

    div.stButton > button:hover {{
        background: rgba(38, 196, 185, 0.2) !important;
        border-color: #26c4b9 !important;
        box-shadow: 0 0 25px rgba(38, 196, 185, 0.4) !important;
        transform: translateY(-8px) !important;
    }}
    
    .card-result {{
        background: rgba(38, 196, 185, 0.1); padding: 25px; border-radius: 20px; 
        border: 2px solid #26c4b9; text-align: center; margin-bottom: 15px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. JAM REALTIME ---
@st.fragment(run_every="1s")
def jam_realtime():
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.datetime.now(tz)
    st.markdown(f'''
        <div style="text-align: right; color: white; font-family: 'Poppins';">
            {now.strftime("%d %B %Y")}<br>
            <span style="font-family:'Orbitron'; color:#26c4b9; font-size:24px; font-weight:bold;">
                {now.strftime("%H:%M:%S")} WIB
            </span>
        </div>
    ''', unsafe_allow_html=True)

# --- 6. LOGIKA HALAMAN ---
if st.session_state.page == 'dashboard':
    col_h1, col_h2 = st.columns([2, 1])
    with col_h1:
        st.markdown(f'''<div class="header-logo-box">
            <img src="data:image/png;base64,{logo_ptpn}"><img src="data:image/png;base64,{logo_sgn}">
            <img src="data:image/png;base64,{logo_lpp}"><img src="data:image/png;base64,{logo_kb}">
        </div>''', unsafe_allow_html=True)
    with col_h2:
        jam_realtime()

    st.markdown(f'''<div class="hero-container">
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
            st.toast("Menu ICUMSA Segera Hadir")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI KE DASHBOARD", key="back_dash", use_container_width=True):
        st.session_state.page = 'dashboard'; st.rerun()

elif st.session_state.page == 'analisa_lab':
    # --- ANALISA TETES ---
    if st.session_state.analisa_type == 'tetes':
        st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="hero-container" style="display:block;">', unsafe_allow_html=True)
            cx, cy = st.columns(2)
            with cx:
                bx_in = st.number_input("Brix Teramati", value=8.80, format="%.2f")
                sh_in = st.number_input("Suhu (°C)", value=28.0, format="%.1f")
                pol_baca = st.number_input("Pol Baca", value=11.00, format="%.2f")
                kor = hitung_interpolasi(sh_in, data_koreksi)
                bj = hitung_interpolasi(bx_in, data_bj)
                brix_akhir = (bx_in + kor) * 10
                pol_akhir = (0.286 * pol_baca) / bj * 10
                hk = (pol_akhir / brix_akhir * 100) if brix_akhir != 0 else 0
                st.info(f"💡 Koreksi: {kor:+.3f} | BJ: {bj:.6f}")
            with cy:
                st.markdown(f'<div class="card-result"><h1 style="color:#26c4b9; font-family:Orbitron; margin:0;">{brix_akhir:.3f}</h1><p style="color:white;">% BRIX AKHIR</p></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="card-result" style="border-color:#ffcc00;"><h1 style="color:#ffcc00; font-family:Orbitron; margin:0;">{pol_akhir:.3f}</h1><p style="color:white;">% POL AKHIR</p></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="card-result" style="border-color:#ff4b4b;"><h1 style="color:#ff4b4b; font-family:Orbitron; margin:0;">{hk:.2f}</h1><p style="color:white;">HARKAT KEMURNIAN (HK)</p></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # --- OD TETES ---
    elif st.session_state.analisa_type == 'od':
        st.markdown("<h2 style='text-align:center; color:#ff4b4b; font-family:Orbitron;'>🔬 OPTICAL DENSITY TETES</h2>", unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="hero-container" style="display:block;">', unsafe_allow_html=True)
            cx, cy = st.columns(2)
            with cx:
                bx_od = st.number_input("Brix Teramati (cari BJ)", value=8.80, format="%.2f")
                abs_val = st.number_input("Nilai Absorbansi (Abs)", value=0.418, format="%.3f")
                bj_od = hitung_interpolasi(bx_od, data_bj)
                od_res = (abs_val * bj_od * 500) / 1
                st.info(f"🔍 BJ d27,5: {bj_od:.6f}")
            with cy:
                st.markdown(f'<div class="card-result" style="border-color:#ff4b4b; background:rgba(255,75,75,0.1); padding:50px;">'
                            f'<h1 style="color:#ff4b4b; font-size:60px; font-family:Orbitron; margin:0;">{od_res:.3f}</h1>'
                            f'<p style="color:white; margin:0;">NILAI OD TETES</p></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # --- ANALISA TSAI TETES (NEW LOGIC) ---
    elif st.session_state.analisa_type == 'tsai':
        st.markdown("<h2 style='text-align:center; color:#ffcc00; font-family:Orbitron;'>⚗️ ANALISA TSAI TETES</h2>", unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="hero-container" style="display:block;">', unsafe_allow_html=True)
            cx, cy = st.columns(2)
            with cx:
                st.subheader("📥 Input Data TSAI")
                vol_titran = st.number_input("Volume Titran (ml)", value=22.5, format="%.1f")
                f_fehling = st.number_input("Faktor Fehling", value=0.979, format="%.3f")
                
                # Step 1: Hitung Perkalian Dasar
                hasil_kali = vol_titran * f_fehling
                
                # Step 2: Tarik Nilai dari Tabel Koreksi (Interpolasi)
                konversi_tabel = hitung_interpolasi(hasil_kali, data_tsai)
                
                # Step 3: Hasil Akhir (Tabel / 4)
                tsai_final = konversi_tabel / 4
                
                st.warning(f"Hasil Titran x Faktor: {hasil_kali:.3f}")
                st.info(f"Koreksi Tabel: {konversi_tabel:.2f}")
                
            with cy:
                st.subheader("📊 Hasil Akhir")
                st.markdown(f'<div class="card-result" style="border-color:#ffcc00; background:rgba(255,204,0,0.1); padding:50px;">'
                            f'<h1 style="color:#ffcc00; font-size:60px; font-family:Orbitron; margin:0;">{tsai_final:.3f}</h1>'
                            f'<p style="color:white; margin:0;">% TSAI TETES</p></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # Tombol Kembali Panjang
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI KE MENU PILIHAN", key="back_sub", use_container_width=True):
        st.session_state.page = 'pilih_analisa'; st.rerun()
