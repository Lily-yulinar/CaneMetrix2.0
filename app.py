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

# --- 2. DATABASE & TABEL KOREKSI ---
# Data BJ (Gambar 4)
data_bj = {
    0.0: 0.996373, 8.8: 1.031047, 10.0: 1.035950, 15.0: 1.056841, 
    20.0: 1.078497, 23.9: 1.095939, 50.0: 1.2320 # Estimasi untuk brix tinggi
}

# Data Koreksi Suhu Brix (Gambar 1)
data_koreksi_suhu = {
    27: -0.05, 28: 0.02, 29: 0.09, 30: 0.16, 31: 0.24, 
    32: 0.315, 33: 0.385, 34: 0.465, 35: 0.54, 36: 0.62,
    37: 0.70, 38: 0.78, 39: 0.86, 40: 0.94
}

# Data Tabel TSAI (Gambar 2 & 3) - Sampel Mapping Titran ke mg Gula Reduksi
data_tsai_table = {
    22.4: 225.10, 22.5: 223.60, 22.6: 222.78, 23.0: 222.20,
    25.0: 204.90, 30.0: 171.70, 37.7: 136.67
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

# --- 3. CSS CUSTOM (KEMBALI KE DESAIN AWAL) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@300;400;700&display=swap');
    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.85), rgba(0, 10, 30, 0.85)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}
    .hero-container {{
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 30px;
        padding: 40px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center;
    }}
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.07) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important; color: white !important;
        height: 180px !important; width: 100% !important; transition: 0.3s !important;
    }}
    div.stButton > button:hover {{
        background: rgba(38, 196, 185, 0.2) !important;
        border-color: #26c4b9 !important; transform: translateY(-5px) !important;
    }}
    .btn-panjang div.stButton > button {{
        height: 60px !important; margin-top: 20px !important;
    }}
    .card-result {{
        background: rgba(38, 196, 185, 0.1); padding: 20px; border-radius: 15px; 
        border: 2px solid #26c4b9; text-align: center; margin-top: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. JAM REALTIME ---
@st.fragment(run_every="1s")
def jam_realtime():
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.datetime.now(tz)
    st.markdown(f'''<div style="text-align: right; color: white;">{now.strftime("%d %B %Y")}<br>
    <span style="font-family:'Orbitron'; color:#26c4b9; font-size:24px; font-weight:bold;">{now.strftime("%H:%M:%S")} WIB</span></div>''', unsafe_allow_html=True)

# --- 5. LOGIKA HALAMAN ---
if st.session_state.page == 'dashboard':
    col_h1, col_h2 = st.columns([2, 1])
    with col_h2: jam_realtime()

    st.markdown(f'''<div class="hero-container">
        <div>
            <h1 style="font-family:Orbitron; color:white; font-size:55px; margin:0;">CANE METRIX</h1>
            <p style="color:#26c4b9; font-family:Poppins; font-weight:700; letter-spacing:5px;">ACCELERATING QA PERFORMANCE</p>
        </div>
    </div>''', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<h1 style='text-align:center; margin-bottom:-55px;'>📝</h1>", unsafe_allow_html=True)
        if st.button("INPUT DATA", key="d1"): st.toast("Fitur Input Segera Hadir")
    with c2:
        st.markdown("<h1 style='text-align:center; margin-bottom:-55px;'>🧮</h1>", unsafe_allow_html=True)
        if st.button("HITUNG ANALISA", key="d2"): 
            st.session_state.page = 'pilih_analisa'; st.rerun()
    with c3:
        st.markdown("<h1 style='text-align:center; margin-bottom:-55px;'>📅</h1>", unsafe_allow_html=True)
        if st.button("DATABASE HARIAN", key="d3"): st.toast("Database Segera Hadir")

elif st.session_state.page == 'pilih_analisa':
    st.markdown("<h2 style='text-align:center; color:white; font-family:Orbitron;'>PILIH JENIS ANALISA</h2>", unsafe_allow_html=True)
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        if st.button("🧪 ANALISA TETES"): st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'tetes'; st.rerun()
    with r1c2:
        if st.button("🔬 OPTICAL DENSITY TETES"): st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'od'; st.rerun()
    
    r2c1, r2c2 = st.columns(2)
    with r2c1:
        if st.button("🍯 ANALISA TSAI TETES"): st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'tsai'; st.rerun()
    with r2c2:
        if st.button("💎 ICUMSA GULA"): st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'icumsa'; st.rerun()

    st.markdown('<div class="btn-panjang">', unsafe_allow_html=True)
    if st.button("🔙 KEMBALI KE DASHBOARD"): st.session_state.page = 'dashboard'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'analisa_lab':
    # --- A. ANALISA TETES (BRIX, POL, HK) ---
    if st.session_state.analisa_type == 'tetes':
        st.markdown("<h2 style='color:#26c4b9;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            bx_tm = st.number_input("Brix Teramati", value=8.80, format="%.2f")
            suhu = st.number_input("Suhu (°C)", value=28.0, format="%.1f")
            pol_baca = st.number_input("Pol Baca", value=11.00, format="%.2f")
            
            koreksi = hitung_interpolasi(suhu, data_koreksi_suhu)
            brix_akhir = (bx_tm + koreksi) * 10
            bj_tetes = hitung_interpolasi(bx_tm, data_bj)
            pol_akhir = (pol_baca * 0.26) / bj_tetes * 10
            hk = (pol_akhir / brix_akhir) * 100
        with col2:
            st.markdown(f'<div class="card-result"><h1>{brix_akhir:.3f}</h1><p>% BRIX AKHIR</p></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card-result"><h1>{pol_akhir:.3f}</h1><p>% POL AKHIR</p></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card-result"><h1>{hk:.2f}</h1><p>HARKAT KEMURNIAN (HK)</p></div>', unsafe_allow_html=True)

    # --- B. OPTICAL DENSITY TETES ---
    elif st.session_state.analisa_type == 'od':
        st.markdown("<h2 style='color:#ff4b4b;'>🔬 OPTICAL DENSITY TETES</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            bx_od = st.number_input("Brix Teramati (cari BJ)", value=8.80)
            abs_od = st.number_input("Nilai Absorbansi (Abs)", value=0.418, format="%.3f")
            bj_od = hitung_interpolasi(bx_od, data_bj)
            od_final = (abs_od * bj_od * 500) / 1
        with col2:
            st.markdown(f'<div class="card-result" style="border-color:#ff4b4b;"><h1>{od_final:.3f}</h1><p>NILAI OD TETES</p></div>', unsafe_allow_html=True)

    # --- C. ANALISA TSAI TETES (RUMUS BARU) ---
    elif st.session_state.analisa_type == 'tsai':
        st.markdown("<h2 style='color:#ffcc00;'>🍯 ANALISA TSAI TETES</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            titran = st.number_input("Volume Titran (ml)", value=22.5, format="%.1f")
            f_fehling = st.number_input("Faktor Fehling", value=0.979, format="%.3f")
            
            hasil_mentah = titran * f_fehling
            koreksi_tabel = hitung_interpolasi(titran, data_tsai_table)
            tsai_final = koreksi_tabel / 4
        with col2:
            st.write(f"Hasil (Titran x Faktor): {hasil_mentah:.3f}")
            st.write(f"Koreksi Tabel: {koreksi_tabel}")
            st.markdown(f'<div class="card-result" style="border-color:#ffcc00;"><h1>{tsai_final:.3f}</h1><p>% TSAI TETES</p></div>', unsafe_allow_html=True)

    # --- D. ICUMSA GULA (RUMUS BARU) ---
    elif st.session_state.analisa_type == 'icumsa':
        st.markdown("<h2 style='color:#ffffff;'>💎 ICUMSA GULA</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            abs_ic = st.number_input("Input Absorbansi (Abs)", value=0.149, format="%.3f")
            brix_ic = st.number_input("Input % Brix Gula", value=50.0, format="%.1f")
            cuvet = st.number_input("Tebal Cuvet (cm)", value=1.0)
            
            bj_ic = hitung_interpolasi(brix_ic, data_bj)
            # Rumus: (Abs * 100.000) / (Brix * BJ * Tebal)
            icumsa_final = (abs_ic * 100000) / (brix_ic * bj_ic * cuvet)
        with col2:
            st.write(f"BJ Terdeteksi: {bj_ic:.6f}")
            st.markdown(f'<div class="card-result" style="border-color:#ffffff;"><h1>{icumsa_final:.0f}</h1><p>ICUMSA UNIT (IU)</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="btn-panjang">', unsafe_allow_html=True)
    if st.button("🔙 KEMBALI KE MENU PILIHAN"): st.session_state.page = 'pilih_analisa'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
