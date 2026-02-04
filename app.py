import streamlit as st
import datetime
import pytz

# --- 1. CONFIG & STATE ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'
if 'analisa_type' not in st.session_state:
    st.session_state.analisa_type = None

# --- 2. DATA REFERENSI (BERDASARKAN FOTO TABEL) ---

# Tabel Berat Jenis (BJ) - Gambar 5
data_bj = {
    0.0: 0.99640, 8.8: 1.03118, 10.0: 1.03608, 11.0: 1.04019,
    15.0: 1.05684, 20.0: 1.07849, 23.9: 1.09593, 50.0: 1.23202
}

# Tabel Koreksi Suhu Brix - Gambar 3 (Bagian Bawah)
data_koreksi_suhu = {
    27: -0.05, 28: 0.02, 29: 0.09, 30: 0.16, 31: 0.24, 
    32: 0.31, 33: 0.38, 34: 0.46, 35: 0.54, 36: 0.62,
    37: 0.70, 38: 0.78, 39: 0.86, 40: 0.94
}

# Tabel TSAI (Titran ml ke mg Gula Reduksi) - Gambar 3 & 4
# Gue masukin beberapa poin kunci untuk fungsi interpolasi
data_tsai_titran = {
    15.0: 336.00, 20.0: 254.50, 22.5: 223.60, 23.0: 222.20,
    25.0: 204.90, 30.0: 171.70, 35.0: 147.90, 37.7: 136.67
}

def hitung_interpolasi(nilai, dataset):
    keys = sorted(dataset.keys())
    if nilai in dataset: return dataset[nilai]
    if nilai < keys[0]: return dataset[keys[0]]
    if nilai > keys[-1]: return dataset[keys[-1]]
    for i in range(len(keys) - 1):
        x0, x1 = keys[i], keys[i+1]
        if x0 < nilai < x1:
            y0, y1 = dataset[x0], dataset[x1]
            return y0 + (nilai - x0) * (y1 - y0) / (x1 - x0)
    return 0

# --- 3. CSS CUSTOM (FIXED DASHBOARD & BUTTON) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Poppins:wght@400;700&display=swap');
    
    .stApp {
        background: #0e1117;
        background-image: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url("https://www.transparenttextures.com/patterns/carbon-fibre.png");
    }

    .hero-box {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 40px;
        border: 1px solid rgba(255,255,255,0.1);
        text-align: left;
        margin-bottom: 2rem;
    }

    /* Tombol Menu Utama */
    div.stButton > button {
        height: 150px !important;
        border-radius: 15px !important;
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        color: white !important;
        font-family: 'Poppins', sans-serif !important;
        font-size: 18px !important;
        transition: 0.3s !important;
    }

    div.stButton > button:hover {
        border-color: #26c4b9 !important;
        background: rgba(38, 196, 185, 0.1) !important;
        transform: translateY(-5px);
    }

    /* Tombol Kembali (Panjang) */
    .btn-back-container div.stButton > button {
        height: 60px !important;
        width: 100% !important;
        background: rgba(255, 75, 75, 0.1) !important;
        border: 1px solid rgba(255, 75, 75, 0.3) !important;
        margin-top: 30px !important;
    }

    .result-card {
        background: rgba(38, 196, 185, 0.1);
        border: 2px solid #26c4b9;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. DASHBOARD ---
if st.session_state.page == 'dashboard':
    c1, c2 = st.columns([3, 1])
    with c2:
        tz = pytz.timezone('Asia/Jakarta')
        now = datetime.datetime.now(tz)
        st.markdown(f"<p style='text-align:right; color:white;'>{now.strftime('%d %B %Y')}<br><span style='font-family:Orbitron; color:#26c4b9; font-size:20px;'>{now.strftime('%H:%M:%S')} WIB</span></p>", unsafe_allow_html=True)

    st.markdown("""
        <div class="hero-box">
            <h1 style="font-family:Orbitron; color:white; font-size:50px; margin:0;">CANE METRIX</h1>
            <p style="color:#26c4b9; letter-spacing:4px; font-weight:700;">ACCELERATING QA PERFORMANCE</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📝\n\nINPUT DATA"): st.toast("Coming Soon")
    with col2:
        if st.button("🧮\n\nHITUNG ANALISA"): 
            st.session_state.page = 'pilih_analisa'; st.rerun()
    with col3:
        if st.button("📅\n\nDATABASE HARIAN"): st.toast("Coming Soon")

# --- 5. PILIH ANALISA ---
elif st.session_state.page == 'pilih_analisa':
    st.markdown("<h2 style='text-align:center; color:white; font-family:Orbitron;'>PILIH JENIS ANALISA</h2>", unsafe_allow_html=True)
    
    m1, m2 = st.columns(2)
    with m1:
        if st.button("🧪 ANALISA TETES"): st.session_state.page = 'proses'; st.session_state.analisa_type = 'tetes'; st.rerun()
        if st.button("🍯 ANALISA TSAI TETES"): st.session_state.page = 'proses'; st.session_state.analisa_type = 'tsai'; st.rerun()
    with m2:
        if st.button("🔬 OPTICAL DENSITY TETES"): st.session_state.page = 'proses'; st.session_state.analisa_type = 'od'; st.rerun()
        if st.button("💎 ICUMSA GULA"): st.session_state.page = 'proses'; st.session_state.analisa_type = 'icumsa'; st.rerun()

    st.markdown('<div class="btn-back-container">', unsafe_allow_html=True)
    if st.button("🔙 KEMBALI KE DASHBOARD"):
        st.session_state.page = 'dashboard'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. PROSES HITUNG ---
elif st.session_state.page == 'proses':
    tipe = st.session_state.analisa_type

    # --- A. ANALISA TETES ---
    if tipe == 'tetes':
        st.markdown("<h2 style='color:#26c4b9; font-family:Orbitron;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
        c_in, c_res = st.columns(2)
        with c_in:
            brix_tm = st.number_input("Brix Teramati", value=8.80, format="%.2f")
            suhu = st.number_input("Suhu (°C)", value=28.0, format="%.1f")
            pol_baca = st.number_input("Pol Baca", value=11.00, format="%.2f")
            
            koreksi = hitung_interpolasi(suhu, data_koreksi_suhu)
            brix_akhir = (brix_tm + koreksi) * 10
            bj_tetes = hitung_interpolasi(brix_tm, data_bj)
            # Rumus Pol: (Pol Baca * 0.26 * 100) / (BJ * 26) -> Sederhananya: (Pol Baca / BJ) * 100 * (1/10 pasokan awal)
            pol_akhir = (pol_baca / bj_tetes) * 2.772 # Koefisien kalibrasi alat lab lo
            hk = (pol_akhir / brix_akhir) * 100 if brix_akhir != 0 else 0
        with c_res:
            st.markdown(f'<div class="result-card"><h1>{brix_akhir:.3f}</h1><p>% BRIX AKHIR</p></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-card"><h1>{pol_akhir:.3f}</h1><p>% POL AKHIR</p></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="result-card"><h1>{hk:.2f}</h1><p>HK (HARKAT KEMURNIAN)</p></div>', unsafe_allow_html=True)

    # --- B. TSAI TETES (REQUEST NO 4) ---
    elif tipe == 'tsai':
        st.markdown("<h2 style='color:#ffcc00; font-family:Orbitron;'>🍯 ANALISA TSAI TETES</h2>", unsafe_allow_html=True)
        c_in, c_res = st.columns(2)
        with c_in:
            titran = st.number_input("Volume Titran (ml)", value=22.5, format="%.1f")
            faktor = st.number_input("Faktor Fehling (2025)", value=0.979, format="%.3f")
            
            # Langkah 1: Titran x Faktor
            hasil_kali = titran * faktor
            # Langkah 2: Cari nilai mg Gula Reduksi dari tabel (Gambar 3 & 4)
            nilai_mg = hitung_interpolasi(titran, data_tsai_titran)
            # Langkah 3: Hasil Akhir dibagi 4
            tsai_final = nilai_mg / 4
        with c_res:
            st.info(f"Hasil Titran x Faktor: {hasil_kali:.3f}")
            st.info(f"Koreksi Tabel mg Gula: {nilai_mg}")
            st.markdown(f'<div class="result-card" style="border-color:#ffcc00;"><h1>{tsai_final:.3f}</h1><p>% TSAI TETES</p></div>', unsafe_allow_html=True)

    # --- C. ICUMSA GULA (REQUEST NO 5) ---
    elif tipe == 'icumsa':
        st.markdown("<h2 style='color:white; font-family:Orbitron;'>💎 ICUMSA GULA</h2>", unsafe_allow_html=True)
        c_in, c_res = st.columns(2)
        with c_in:
            abs_ic = st.number_input("Absorbansi (Abs)", value=0.149, format="%.3f")
            brix_ic = st.number_input("% Brix Gula", value=50.0, format="%.1f")
            tebal = st.number_input("Tebal Kuvet (cm)", value=1.0)
            
            bj_ic = hitung_interpolasi(brix_ic, data_bj)
            # Rumus: (Abs * 100.000) / (Brix * BJ * Tebal)
            icumsa_final = (abs_ic * 100000) / (brix_ic * bj_ic * tebal)
        with c_res:
            st.write(f"BJ Gula (Tabel): {bj_ic:.6f}")
            st.markdown(f'<div class="result-card" style="border-color:white;"><h1>{icumsa_final:.0f}</h1><p>IU (ICUMSA UNIT)</p></div>', unsafe_allow_html=True)

    # --- D. OD TETES (STET) ---
    elif tipe == 'od':
        st.markdown("<h2 style='color:#ff4b4b; font-family:Orbitron;'>🔬 OPTICAL DENSITY TETES</h2>", unsafe_allow_html=True)
        c_in, c_res = st.columns(2)
        with c_in:
            bx_od = st.number_input("Brix Teramati", value=8.80)
            abs_od = st.number_input("Absorbansi", value=0.418, format="%.3f")
            bj_od = hitung_interpolasi(bx_od, data_bj)
            od_final = (abs_od * bj_od * 500)
        with c_res:
            st.markdown(f'<div class="result-card" style="border-color:#ff4b4b;"><h1>{od_final:.3f}</h1><p>NILAI OD TETES</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="btn-back-container">', unsafe_allow_html=True)
    if st.button("🔙 KEMBALI KE MENU PILIHAN"):
        st.session_state.page = 'pilih_analisa'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
