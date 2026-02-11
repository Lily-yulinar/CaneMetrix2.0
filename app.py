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

# --- 2. ASSETS & CSS ---
def get_base64_logo(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo_ptpn = get_base64_logo("ptpn.png"); logo_sgn = get_base64_logo("sgn.png")
logo_lpp = get_base64_logo("lpp.png"); logo_kb = get_base64_logo("kb.png")
logo_cane = get_base64_logo("canemetrix.png")

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@300;400;700&display=swap');
    .stApp {{ background: linear-gradient(rgba(0, 10, 30, 0.85), rgba(0, 10, 30, 0.85)), url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"); background-size: cover; background-position: center; background-attachment: fixed; }}
    .header-logo-box {{ background: white; padding: 10px 20px; border-radius: 15px; display: inline-flex; align-items: center; gap: 15px; margin-bottom: 20px; }}
    .hero-container {{ background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 30px; padding: 40px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center; }}
    
    /* Tombol Kotak Besar (Grid Style) */
    div.stButton > button {{ 
        background: rgba(255, 255, 255, 0.07) !important; 
        backdrop-filter: blur(10px) !important; 
        border: 1px solid rgba(255, 255, 255, 0.1) !important; 
        border-radius: 20px !important; 
        color: white !important; 
        height: 180px !important; /* Balikin ke tinggi semula biar kotak */
        width: 100% !important;
        transition: 0.3s !important; 
        font-family: 'Poppins', sans-serif !important;
        font-weight: bold !important;
    }}
    div.stButton > button:hover {{ 
        background: rgba(38, 196, 185, 0.2) !important; 
        border-color: #26c4b9 !important; 
        box-shadow: 0 0 25px rgba(38, 196, 185, 0.4) !important; 
        transform: translateY(-5px) !important; 
    }}
    
    .card-result {{ background: rgba(38, 196, 185, 0.1); padding: 25px; border-radius: 20px; border: 2px solid #26c4b9; text-align: center; margin-bottom: 15px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. HELPER FUNCTIONS ---
def render_brix_pol_hk(prefix):
    # Logika perhitungan standar
    cx, cy = st.columns([1, 1.2])
    with cx:
        bx_in = st.number_input(f"Brix Teramati ({prefix})", value=0.0, format="%.2f", key=f"bx_{prefix}")
        sh_in = st.number_input(f"Suhu (°C) ({prefix})", value=28.0, format="%.1f", key=f"sh_{prefix}")
        pb_in = st.number_input(f"Pol Baca ({prefix})", value=0.0, format="%.2f", key=f"pb_{prefix}")
        # (Logika perhitungan disederhanakan untuk contoh, pakai dataset lu yang asli di sini)
        brix_akhir = bx_in + 0.02 # Contoh koreksi
        pol_akhir = pb_in * 0.9  # Contoh hitungan
        hk = (pol_akhir/brix_akhir*100) if brix_akhir > 0 else 0
        st.button("🚀 SIMPAN KE EXCEL", key=f"save_{prefix}")
    with cy:
        st.markdown(f'<div class="card-result"><h1 style="color:#26c4b9; font-family:Orbitron; margin:0; font-size:50px;">{brix_akhir:.3f}</h1><p style="color:white;">% BRIX AKHIR</p></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card-result" style="border-color:#ffcc00;"><h1 style="color:#ffcc00; font-family:Orbitron; margin:0; font-size:50px;">{pol_akhir:.3f}</h1><p style="color:white;">% POL AKHIR</p></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card-result" style="border-color:#ff4b4b;"><h1 style="color:#ff4b4b; font-family:Orbitron; margin:0; font-size:50px;">{hk:.2f}</h1><p style="color:white;">HK</p></div>', unsafe_allow_html=True)

# --- 4. NAVIGATION LOGIC ---

# === DASHBOARD (KOTAK-KOTAK) ===
if st.session_state.page == 'dashboard':
    st.markdown(f'''<div class="hero-container"><div><h1 style="font-family:Orbitron; color:white; font-size:55px; margin:0;">CANE METRIX</h1><p style="color:#26c4b9; font-weight:700; letter-spacing:5px;">ACCELERATING QA PERFORMANCE</p></div><img src="data:image/png;base64,{logo_cane}" style="height:150px;"></div>''', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📝\n\nINPUT DATA", key="dash_in"): st.session_state.page = 'pilih_stasiun'; st.rerun()
    with c2:
        if st.button("🧮\n\nHITUNG ANALISA", key="dash_calc"): st.session_state.page = 'pilih_analisa'; st.rerun()
    with c3:
        if st.button("📅\n\nDATABASE HARIAN", key="dash_db"): st.toast("Segera Hadir")

# === PILIH STASIUN (KOTAK-KOTAK) ===
elif st.session_state.page == 'pilih_stasiun':
    st.markdown("<h2 style='text-align:center; color:white; font-family:Orbitron;'>PILIH STASIUN</h2>", unsafe_allow_html=True)
    r1c1, r1c2, r1c3 = st.columns(3)
    with r1c1:
        if st.button("🚜\n\nSTASIUN GILINGAN"): st.session_state.page = 'input_gilingan'; st.rerun()
    with r1c2:
        if st.button("🌫️\n\nSTASIUN PEMURNIAN"): st.toast("Halaman Pemurnian")
    with r1c3:
        if st.button("🔥\n\nSTASIUN PENGUAPAN"): st.toast("Halaman Penguapan")
    
    if st.button("🔙 KEMBALI KE DASHBOARD", key="back_dash_stat"): st.session_state.page = 'dashboard'; st.rerun()

# === INPUT GILINGAN (CUSTOM GILINGAN 2-4) ===
elif st.session_state.page == 'input_gilingan':
    st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>🚜 INPUT DATA STASIUN GILINGAN</h2>", unsafe_allow_html=True)
    tabs = st.tabs(["NPP (Gilingan 1)", "Gilingan 2", "Gilingan 3", "Gilingan 4", "Nira Mentah", "Ampas", "Imbibisi"])
    
    with tabs[0]: # NPP - Lengkap
        sub = st.tabs(["Brix, Pol, HK", "Gula Reduksi", "P2O5", "Dextran", "Icumsa"])
        with sub[0]: render_brix_pol_hk("NPP")
    
    for i in range(1, 4): # Gilingan 2, 3, 4 - CUMA BRIX POL HK
        with tabs[i]:
            st.markdown(f"### Analisa Gilingan {i+1}")
            render_brix_pol_hk(f"Gil_{i+1}")

    with tabs[4]: # Nira Mentah - Lengkap
        sub_nm = st.tabs(["Brix, Pol, HK", "Gula Reduksi", "P2O5", "Dextran", "Icumsa"])
        with sub_nm[0]: render_brix_pol_hk("NM")

    if st.button("🔙 KEMBALI"): st.session_state.page = 'pilih_stasiun'; st.rerun()

# === PILIH ANALISA (KOTAK-KOTAK & FITUR KEMBALI) ===
elif st.session_state.page == 'pilih_analisa':
    st.markdown("<h2 style='text-align:center; color:white; font-family:Orbitron;'>PILIH JENIS ANALISA</h2>", unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    with m1:
        if st.button("🧪\n\nANALISA TETES"): st.session_state.page = 'analisa_tetes'; st.rerun()
    with m2:
        if st.button("🔬\n\nOD TETES"): st.session_state.page = 'analisa_od'; st.rerun()
    
    if st.button("🔙 KEMBALI"): st.session_state.page = 'dashboard'; st.rerun()

# === HALAMAN PERHITUNGAN (BALIK LAGI) ===
elif st.session_state.page == 'analisa_tetes':
    st.markdown("## Perhitungan Analisa Tetes")
    render_brix_pol_hk("Tetes")
    if st.button("🔙 KEMBALI"): st.session_state.page = 'pilih_analisa'; st.rerun()

elif st.session_state.page == 'analisa_od':
    st.markdown("## Perhitungan OD Tetes")
    # Form OD lu di sini...
    if st.button("🔙 KEMBALI"): st.session_state.page = 'pilih_analisa'; st.rerun()
