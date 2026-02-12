import streamlit as st
import datetime
import pytz
import base64
import os
import pandas as pd
import plotly.graph_objects as go

# --- 1. CONFIG & STATE ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'
if 'analisa_type' not in st.session_state:
    st.session_state.analisa_type = None

# State untuk simpan Brix Gilingan (Sinkron antara Input & Kurva)
if 'brix_history' not in st.session_state:
    st.session_state.brix_history = {
        "NPP": 15.46, 
        "Gilingan 2": 9.28, 
        "Gilingan 3": 6.30, 
        "Gilingan 4": 4.16
    }

# State untuk Angka Pengawasan (KPI)
if 'kpi_data' not in st.session_state:
    st.session_state.kpi_data = {
        "OR": 85.10, "ME": 96.05, "BHR": 88.50, "HPB 1": 76.20, "PSHK": 72.50, "KNT": 12.10
    }

# Standar Normatif Pabrik
STANDAR = {
    "OR": 86.00, "ME": 96.20, "BHR": 90.00, "HPB 1": 78.00, "PSHK": 75.00, "KNT": 12.50
}

# --- 2. ASSETS (LOGO) ---
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

# --- 3. DATABASE & INTERPOLASI ---
data_koreksi = {27: -0.05, 28: 0.02, 29: 0.09, 30: 0.16, 31: 0.24, 32: 0.315, 33: 0.385, 34: 0.465, 35: 0.54, 36: 0.62, 37: 0.70, 38: 0.78, 39: 0.86, 40: 0.94}
data_bj = {0.0: 0.99640, 5.0: 1.01592, 10.0: 1.03608, 15.0: 1.05691, 20.0: 1.07844, 25.0: 1.10069, 30.0: 1.12368, 35.0: 1.14745, 40.0: 1.17203, 45.0: 1.19746, 49.0: 1.21839, 50.0: 1.22372, 55.0: 1.25083, 60.0: 1.27885, 65.0: 1.30781, 70.0: 1.33775}
data_tsai = {15.0: 336.00, 20.0: 254.50, 22.5: 223.60, 25.0: 204.80, 30.0: 171.70, 35.0: 147.90, 37.7: 136.67}

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

# --- 4. UI COMPONENTS ---
def tampilkan_kartu_hasil(brix, pol, hk):
    st.markdown(f"""
    <div style="display: flex; flex-direction: column; gap: 15px;">
        <div style="background: rgba(38, 196, 185, 0.1); padding: 20px; border-radius: 15px; border: 2px solid #26c4b9; display: flex; justify-content: space-between; align-items: center;">
            <h1 style="color:#26c4b9; font-family:Orbitron; margin:0; font-size:50px;">{brix:.2f}</h1>
            <p style="color:white; font-family:Poppins; font-weight:bold; margin:0;">% BRIX</p>
        </div>
        <div style="background: rgba(255, 204, 0, 0.1); padding: 20px; border-radius: 15px; border: 2px solid #ffcc00; display: flex; justify-content: space-between; align-items: center;">
            <h1 style="color:#ffcc00; font-family:Orbitron; margin:0; font-size:50px;">{pol:.2f}</h1>
            <p style="color:white; font-family:Poppins; font-weight:bold; margin:0;">% POL</p>
        </div>
        <div style="background: rgba(255, 75, 75, 0.1); padding: 20px; border-radius: 15px; border: 2px solid #ff4b4b; display: flex; justify-content: space-between; align-items: center;">
            <h1 style="color:#ff4b4b; font-family:Orbitron; margin:0; font-size:50px;">{hk:.2f}</h1>
            <p style="color:white; font-family:Poppins; font-weight:bold; margin:0;">HK</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 5. CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@300;400;700&display=swap');
    .stApp {{ background: linear-gradient(rgba(0, 10, 30, 0.9), rgba(0, 10, 30, 0.9)), url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"); background-size: cover; background-position: center; }}
    .header-logo-box {{ background: white; padding: 10px 20px; border-radius: 15px; display: inline-flex; align-items: center; gap: 15px; margin-bottom: 20px; }}
    .header-logo-box img {{ height: 30px; }}
    .hero-container {{ background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 25px; padding: 30px; margin-bottom: 25px; }}
    div.stButton > button {{ background: rgba(255, 255, 255, 0.07) !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 15px !important; color: white !important; height: 150px !important; width: 100% !important; transition: 0.3s; }}
    div.stButton > button:hover {{ background: rgba(38, 196, 185, 0.2) !important; border-color: #26c4b9 !important; transform: translateY(-5px); }}
    </style>
    """, unsafe_allow_html=True)

@st.fragment(run_every="1s")
def jam_realtime():
    tz = pytz.timezone('Asia/Jakarta'); now = datetime.datetime.now(tz)
    st.markdown(f'''<div style="text-align: right; color: white; font-family: 'Poppins';">{now.strftime("%d %B %Y")}<br><span style="font-family:'Orbitron'; color:#26c4b9; font-size:20px;">{now.strftime("%H:%M:%S")} WIB</span></div>''', unsafe_allow_html=True)

# --- 6. PAGE LOGIC ---

# PAGE: DASHBOARD
if st.session_state.page == 'dashboard':
    col_h1, col_h2 = st.columns([2, 1])
    with col_h1: st.markdown(f'''<div class="header-logo-box"><img src="data:image/png;base64,{logo_ptpn}"><img src="data:image/png;base64,{logo_sgn}"><img src="data:image/png;base64,{logo_lpp}"><img src="data:image/png;base64,{logo_kb}"></div>''', unsafe_allow_html=True)
    with col_h2: jam_realtime()
    
    st.markdown(f'''<div class="hero-container" style="display:flex; justify-content:space-between; align-items:center;"><div><h1 style="font-family:Orbitron; color:white; font-size:45px; margin:0;">CANE METRIX</h1><p style="color:#26c4b9; font-family:Poppins; font-weight:700; letter-spacing:3px;">ACCELERATING QA PERFORMANCE</p></div><img src="data:image/png;base64,{logo_cane}" style="height:100px;"></div>''', unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("<h3 style='text-align:center;'>📝</h3>", unsafe_allow_html=True)
        if st.button("INPUT DATA", key="dash_input"): st.session_state.page = 'pilih_stasiun'; st.rerun()
    with c2:
        st.markdown("<h3 style='text-align:center;'>🧮</h3>", unsafe_allow_html=True)
        if st.button("HITUNG ANALISA", key="dash_hitung"): st.session_state.page = 'pilih_analisa'; st.rerun()
    with c3:
        st.markdown("<h3 style='text-align:center;'>📊</h3>", unsafe_allow_html=True)
        if st.button("COCKPIT", key="dash_kpi"): st.session_state.page = 'kpi_monitoring'; st.rerun()
    with c4:
        st.markdown("<h3 style='text-align:center;'>📈</h3>", unsafe_allow_html=True)
        if st.button("KURVA BRIX", key="dash_kurva"): st.session_state.page = 'kurva_brix'; st.rerun()

# PAGE: KURVA BRIX (LOGIKA FIX)
elif st.session_state.page == 'kurva_brix':
    st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>📈 KURVA BRIX GILINGAN</h2>", unsafe_allow_html=True)
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    imb = c1.number_input("Imbibisi % Tebu (I)", value=25.70)
    sabut = c2.number_input("Kadar Sabut (ft)", value=13.49)
    npp_real = st.session_state.brix_history.get("NPP", 15.46)
    
    lamda = imb / sabut if sabut > 0 else 0
    nyata = [st.session_state.brix_history[n] for n in ["NPP", "Gilingan 2", "Gilingan 3", "Gilingan 4"]]
    
    # Rumus Brix Teoretis
    teoritis = []
    for i in range(1, 5):
        teori = (lamda**(4-i) / lamda**3) * npp_real
        teoritis.append(round(teori, 2))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=["G1 (NPP)", "G2", "G3", "G4"], y=teoritis, name='Brix Teoretis', line=dict(color='#26c4b9', width=4), mode='lines+markers'))
    fig.add_trace(go.Scatter(x=["G1 (NPP)", "G2", "G3", "G4"], y=nyata, name='Brix Nyata', line=dict(color='#ff4b4b', dash='dash', width=4), mode='lines+markers'))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=450)
    st.plotly_chart(fig, use_container_width=True)
    
    ratio = nyata[1] / teoritis[1] if teoritis[1] > 0 else 0
    if ratio > 1.05:
        st.warning(f"⚠️ Ratio G2: {ratio:.2f} (>1.0). Pencampuran imbibisi kurang merata.")
    elif ratio < 0.95:
        st.error(f"🚨 Ratio G2: {ratio:.2f} (<1.0). Cek tekanan gilingan / kerja alat.")
    else:
        st.success(f"✅ Ratio G2: {ratio:.2f}. Kondisi Gilingan Ideal.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("🔙 KEMBALI"): st.session_state.page = 'dashboard'; st.rerun()

# PAGE: INPUT GILINGAN
elif st.session_state.page == 'input_gilingan':
    st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>🚜 INPUT DATA STASIUN GILINGAN</h2>", unsafe_allow_html=True)
    tabs = st.tabs(["NPP", "Gilingan 2", "Gilingan 3", "Gilingan 4", "Nira Mentah"])

    def render_input(prefix):
        st.markdown('<div class="hero-container">', unsafe_allow_html=True)
        c_in, c_res = st.columns([1, 2])
        with c_in:
            bx_in = st.number_input("Brix Baca", value=0.0, key=f"bx_{prefix}")
            sh_in = st.number_input("Suhu", value=28.0, key=f"sh_{prefix}")
            pol_in = st.number_input("Pol Baca", value=0.0, key=f"pol_{prefix}")
            
            kor = hitung_interpolasi(sh_in, data_koreksi)
            bj = hitung_interpolasi(bx_in, data_bj)
            bx_fix = bx_in + kor if bx_in > 0 else 0
            pol_fix = (0.286 * pol_in) / bj if bj > 0 else 0
            hk_fix = (pol_fix / bx_fix * 100) if bx_fix > 0 else 0
            
            if st.button(f"SAVE {prefix}"):
                st.session_state.brix_history[prefix] = bx_fix
                st.toast(f"Data {prefix} Updated!")
        with c_res:
            tampilkan_kartu_hasil(bx_fix, pol_fix, hk_fix)
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[0]: render_input("NPP")
    with tabs[1]: render_input("Gilingan 2")
    with tabs[2]: render_input("Gilingan 3")
    with tabs[3]: render_input("Gilingan 4")
    with tabs[4]: render_input("Nira Mentah")

    if st.button("🔙 KEMBALI"): st.session_state.page = 'pilih_stasiun'; st.rerun()

# PAGE: PILIH STASIUN
elif st.session_state.page == 'pilih_stasiun':
    st.markdown("<h2 style='text-align:center; color:white; font-family:Orbitron;'>PILIH STASIUN</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🚜 GILINGAN"): st.session_state.page = 'input_gilingan'; st.rerun()
    with c2:
        if st.button("🌫️ PEMURNIAN"): st.toast("Coming Soon")
    with c3:
        if st.button("🔥 PENGUAPAN"): st.toast("Coming Soon")
    if st.button("🔙 DASHBOARD"): st.session_state.page = 'dashboard'; st.rerun()

# PAGE: PILIH ANALISA (LAB)
elif st.session_state.page == 'pilih_analisa':
    st.markdown("<h2 style='text-align:center; color:white; font-family:Orbitron;'>PILIH JENIS ANALISA</h2>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    with m1:
        if st.button("🧪 TETES"): st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'tetes'; st.rerun()
    with m2:
        if st.button("🔬 OD TETES"): st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'od'; st.rerun()
    with m3:
        if st.button("💎 ICUMSA"): st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'icumsa'; st.rerun()
    if st.button("🔙 DASHBOARD"): st.session_state.page = 'dashboard'; st.rerun()

# PAGE: KPI MONITORING
elif st.session_state.page == 'kpi_monitoring':
    st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>📊 MANAGEMENT COCKPIT</h2>", unsafe_allow_html=True)
    cols = st.columns(6)
    for i, (kpi, val) in enumerate(st.session_state.kpi_data.items()):
        target = STANDAR.get(kpi, 0)
        warna = "#ff4b4b" if val < target else "#26c4b9"
        with cols[i]:
            st.markdown(f'<div style="background:rgba(255,255,255,0.05); padding:15px; border-radius:10px; border-top:4px solid {warna}; text-align:center;"><p style="font-size:12px; margin:0;">{kpi}</p><h3 style="color:{warna}; margin:5px 0;">{val}%</h3></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.line_chart(pd.DataFrame({"Recovery": [85.0, 85.5, 85.1, 84.8, 85.1]}))
    
    if st.button("🔙 DASHBOARD"): st.session_state.page = 'dashboard'; st.rerun()

# ANALISA LAB DETAILED
elif st.session_state.page == 'analisa_lab':
    st.markdown(f"<h2 style='text-align:center; color:#ffcc00; font-family:Orbitron;'>🧪 ANALISA {st.session_state.analisa_type.upper()}</h2>", unsafe_allow_html=True)
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    # Form Logika untuk lab bisa disesuaikan di sini seperti coding sebelumnya
    st.info("Form input analisa laboratorium sedang aktif.")
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("🔙 KEMBALI"): st.session_state.page = 'pilih_analisa'; st.rerun()
