import streamlit as st
import datetime
import pytz
import base64
import os

# --- 1. CONFIG & STATE ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

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

# --- 3. DATABASE TABEL (SESUAI FOTO LAMPIRAN) ---

# Tabel Koreksi Suhu (Halaman 68-69)
data_koreksi = {
    27: -0.05, 28: 0.02, 29: 0.09, 30: 0.16, 31: 0.24, 
    32: 0.315, 33: 0.385, 34: 0.465, 35: 0.54, 36: 0.62,
    37: 0.70, 38: 0.78, 39: 0.86, 40: 0.94
}

# Tabel Berat Jenis (d27,5) terhadap Brix Teramati (Halaman 68-69)
data_bj = {
    # Brix 0.0 - 2.9 (Hlm 68)
    0.0: 0.996373, 1.0: 1.000201, 2.0: 1.004058, 3.0: 1.007944,
    4.0: 1.011858, 5.0: 1.015801, 6.0: 1.019772, 7.0: 1.023773,
    8.0: 1.027803, 8.8: 1.031047, 9.0: 1.031862, 10.0: 1.035950,
    11.0: 1.040068, 12.0: 1.044216, 13.0: 1.048394, 14.0: 1.052602,
    # Brix 15.0 - 23.9 (Hlm 69)
    15.0: 1.056841, 16.0: 1.061110, 17.0: 1.065410, 18.0: 1.069741,
    19.0: 1.074103, 20.0: 1.078497, 21.0: 1.082923, 22.0: 1.087380,
    23.0: 1.091870, 23.9: 1.095939
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

# --- 4. CSS STYLING ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@300;400;700&display=swap');
    .stApp {{
        background: linear-gradient(rgba(0, 10, 30, 0.9), rgba(0, 10, 30, 0.9)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2");
        background-size: cover; background-attachment: fixed;
    }}
    .hero-container {{
        background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 25px;
        padding: 30px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;
    }}
    .card-result {{
        padding: 25px; border-radius: 20px; text-align: center; margin-bottom: 15px;
        border: 2px solid; backdrop-filter: blur(10px);
    }}
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.05) !important; color: white !important;
        height: 150px !important; border-radius: 20px !important; transition: 0.3s;
    }}
    div.stButton > button:hover {{
        border-color: #26c4b9 !important; background: rgba(38, 196, 185, 0.1) !important;
        transform: translateY(-5px);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. JAM REALTIME ---
@st.fragment(run_every="1s")
def jam_realtime():
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.datetime.now(tz)
    st.markdown(f'<div style="text-align: right; color: white; font-family:Poppins;">{now.strftime("%d %B %Y")}<br><span style="font-family:Orbitron; color:#26c4b9; font-size:22px;">{now.strftime("%H:%M:%S")} WIB</span></div>', unsafe_allow_html=True)

# --- 6. LOGIKA HALAMAN ---
if st.session_state.page == 'dashboard':
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown(f'<div style="background:white; padding:10px; border-radius:10px; display:inline-flex; gap:10px;">'
                    f'<img src="data:image/png;base64,{logo_ptpn}" height="30">'
                    f'<img src="data:image/png;base64,{logo_sgn}" height="30">'
                    f'<img src="data:image/png;base64,{logo_lpp}" height="30">'
                    f'<img src="data:image/png;base64,{logo_kb}" height="30"></div>', unsafe_allow_html=True)
    with c2: jam_realtime()
    
    st.markdown(f'<div class="hero-container"><div><h1 style="font-family:Orbitron; color:white; font-size:45px; margin:0;">CANE METRIX</h1><p style="color:#26c4b9; letter-spacing:3px;">ACCELERATING QA PERFORMANCE</p></div><img src="data:image/png;base64,{logo_cane}" height="120"></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1: 
        if st.button("📝\n\nINPUT DATA", use_container_width=True): st.toast("Coming Soon!")
    with col2:
        if st.button("🧮\n\nHITUNG ANALISA", use_container_width=True):
            st.session_state.page = 'analisa_tetes'; st.rerun()
    with col3:
        if st.button("📅\n\nDATABASE HARIAN", use_container_width=True): st.toast("Coming Soon!")

elif st.session_state.page == 'analisa_tetes':
    st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="hero-container" style="display:block;">', unsafe_allow_html=True)
        cx, cy = st.columns(2)
        
        with cx:
            st.subheader("📥 Input Data Lab")
            bx_teramati = st.number_input("Brix Teramati", value=8.80, step=0.01, format="%.2f")
            suhu_lab = st.number_input("Suhu (°C)", value=28.3, step=0.1, format="%.1f")
            pol_baca = st.number_input("Pol Baca", value=11.00, step=0.01, format="%.2f")
            
            # --- PERHITUNGAN BERDASARKAN TABEL BEB ---
            kor = hitung_interpolasi(suhu_lab, data_koreksi)
            bj_tabel = hitung_interpolasi(bx_teramati, data_bj)
            
            # Rumus 1: %Brix Akhir = (Brix + Koreksi) * 10
            brix_akhir = (bx_teramati + kor) * 10
            
            # Rumus 2: %Pol = (0.286 * Pol Baca) / BJ * 10
            pol_akhir = (0.286 * pol_baca) / bj_tabel * 10
            
            # Perhitungan Tambahan: Harkat Kemurnian (HK)
            hk = (pol_akhir / brix_akhir * 100) if brix_akhir != 0 else 0
            # ----------------------------------------
            
            st.write("---")
            st.caption(f"🔍 BJ Terdeteksi (Brix {bx_teramati}): **{bj_tabel:.6f}**")
            st.caption(f"🌡️ Koreksi Suhu: **{kor:+.3f}**")

        with cy:
            st.subheader("📊 Hasil Perhitungan")
            # Card Brix
            st.markdown(f'<div class="card-result" style="border-color:#26c4b9; background:rgba(38,196,185,0.05);">'
                        f'<h1 style="color:#26c4b9; font-family:Orbitron; margin:0;">{brix_akhir:.3f}</h1>'
                        f'<p style="color:white; margin:0;">% BRIX AKHIR</p></div>', unsafe_allow_html=True)
            # Card Pol
            st.markdown(f'<div class="card-result" style="border-color:#ffcc00; background:rgba(255,204,0,0.05);">'
                        f'<h1 style="color:#ffcc00; font-family:Orbitron; margin:0;">{pol_akhir:.3f}</h1>'
                        f'<p style="color:white; margin:0;">% POL AKHIR</p></div>', unsafe_allow_html=True)
            # Card HK (Bonus biar makin lengkap)
            st.markdown(f'<div class="card-result" style="border-color:#ff4b4b; background:rgba(255,75,75,0.05);">'
                        f'<h1 style="color:#ff4b4b; font-family:Orbitron; margin:0;">{hk:.2f}</h1>'
                        f'<p style="color:white; margin:0;">HARKAT KEMURNIAN (HK)</p></div>', unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔙 KEMBALI KE DASHBOARD", use_container_width=True):
        st.session_state.page = 'dashboard'; st.rerun()
