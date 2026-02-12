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

# Database Input (Simulasi agar Kurva Brix bisa narik data yang diinput)
if 'input_history' not in st.session_state:
    st.session_state.input_history = {}

# --- 2. ASSETS & UTILS ---
def get_base64_logo(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo_ptpn = get_base64_logo("ptpn.png"); logo_sgn = get_base64_logo("sgn.png")
logo_lpp = get_base64_logo("lpp.png"); logo_kb = get_base64_logo("kb.png")
logo_cane = get_base64_logo("canemetrix.png")

# Data Koreksi & Interpolasi
data_koreksi = {27: -0.05, 28: 0.02, 29: 0.09, 30: 0.16, 31: 0.24, 32: 0.315, 33: 0.385, 34: 0.465, 35: 0.54, 36: 0.62, 37: 0.70, 38: 0.78, 39: 0.86, 40: 0.94}
data_bj = {0.0: 0.99640, 5.0: 1.01592, 10.0: 1.03608, 15.0: 1.05691, 20.0: 1.07844, 25.0: 1.10069, 30.0: 1.12368, 35.0: 1.14745, 40.0: 1.17203, 45.0: 1.19746, 50.0: 1.22372, 60.0: 1.27885, 70.0: 1.33775}
data_tsai = {15.0: 336.0, 20.0: 254.5, 25.0: 204.8, 30.0: 171.7, 35.0: 147.9}

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

# --- 3. KURVA BRIX LOGIC (MATERI GAMBAR) ---
def hitung_kurva_teoritis(brix_npp, imb_tebu, sabut):
    # lamda = imbibisi % sabut
    lamda = imb_tebu / sabut if sabut > 0 else 0
    eg = 3 # jumlah gilingan basah
    
    # Rumus: Bni = bn1 * ((lamda^(eg-gi) + 1 - gi) / (lamda^eg + 1 - 1))
    teoritis = [brix_npp]
    for gi in range(1, 4):
        pembilang = (lamda**(eg - gi)) + 1 - gi
        penyebut = (lamda**eg) + 1 - 1
        bni = brix_npp * (pembilang / penyebut) if penyebut > 0 else 0
        teoritis.append(round(bni, 2))
    return teoritis

# --- 4. CSS & UI COMPONENTS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@300;400;700&display=swap');
    .stApp {{ background: linear-gradient(rgba(0, 10, 30, 0.9), rgba(0, 10, 30, 0.9)), url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"); background-size: cover; }}
    .hero-container {{ background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 30px; padding: 30px; margin-bottom: 20px; }}
    div.stButton > button {{ background: rgba(255, 255, 255, 0.07) !important; border-radius: 20px !important; color: white !important; height: 150px !important; width: 100% !important; transition: 0.3s; }}
    div.stButton > button:hover {{ background: rgba(38, 196, 185, 0.2) !important; border-color: #26c4b9 !important; transform: translateY(-5px) !important; }}
    </style>
    """, unsafe_allow_html=True)

def tampilkan_kartu_hasil(brix, pol, hk):
    st.markdown(f"""
    <div style="display: flex; flex-direction: column; gap: 10px;">
        <div style="background: rgba(38,196,185,0.1); padding:20px; border-radius:15px; border:2px solid #26c4b9; display:flex; justify-content:space-between; align-items:center;">
            <h2 style="color:#26c4b9; font-family:Orbitron; margin:0;">{brix:.3f}</h2><span style="color:white; font-size:12px;">% BRIX</span>
        </div>
        <div style="background: rgba(255,204,0,0.1); padding:20px; border-radius:15px; border:2px solid #ffcc00; display:flex; justify-content:space-between; align-items:center;">
            <h2 style="color:#ffcc00; font-family:Orbitron; margin:0;">{pol:.3f}</h2><span style="color:white; font-size:12px;">% POL</span>
        </div>
        <div style="background: rgba(255,75,75,0.1); padding:20px; border-radius:15px; border:2px solid #ff4b4b; display:flex; justify-content:space-between; align-items:center;">
            <h2 style="color:#ff4b4b; font-family:Orbitron; margin:0;">{hk:.2f}</h2><span style="color:white; font-size:12px;">HK</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 5. PAGE NAVIGATION ---
if st.session_state.page == 'dashboard':
    st.markdown(f'''<div class="hero-container"><h1 style="font-family:Orbitron; color:white; font-size:45px; margin:0;">CANE METRIX</h1><p style="color:#26c4b9; font-weight:700; letter-spacing:3px;">ACCELERATING QA PERFORMANCE</p></div>''', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: 
        if st.button("📝 INPUT DATA"): st.session_state.page = 'pilih_stasiun'; st.rerun()
    with c2:
        if st.button("🧮 HITUNG LAB"): st.session_state.page = 'pilih_analisa'; st.rerun()
    with c3:
        if st.button("📈 KURVA BRIX"): st.session_state.page = 'kurva_brix_page'; st.rerun()
    with c4:
        if st.button("📊 COCKPIT"): st.toast("Coming Soon")

elif st.session_state.page == 'pilih_stasiun':
    st.markdown("<h2 style='text-align:center; color:white; font-family:Orbitron;'>PILIH STASIUN</h2>", unsafe_allow_html=True)
    if st.button("🚜 STASIUN GILINGAN", use_container_width=True): st.session_state.page = 'input_gilingan'; st.rerun()
    if st.button("🔙 BACK", use_container_width=True): st.session_state.page = 'dashboard'; st.rerun()

elif st.session_state.page == 'input_gilingan':
    st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>🚜 INPUT GILINGAN</h2>", unsafe_allow_html=True)
    tabs = st.tabs(["NPP", "Gilingan 2", "Gilingan 3", "Gilingan 4", "Lainnya"])
    
    def render_gilingan(name, force_direct=False):
        st.markdown(f"### {name}")
        if not force_direct: st.selectbox(f"Opsi {name}", ["(Brix, Pol, dan HK)"])
        c1, c2 = st.columns([1, 2])
        with c1:
            bx = st.number_input(f"Brix Baca {name}", value=0.0, step=0.1, key=f"bx_{name}")
            sh = st.number_input(f"Suhu {name}", value=28.0, key=f"sh_{name}")
            pol = st.number_input(f"Pol Baca {name}", value=0.0, step=0.1, key=f"pl_{name}")
            kor = hitung_interpolasi(sh, data_koreksi); bj = hitung_interpolasi(bx, data_bj)
            bx_f = bx + kor; pol_f = (0.286 * pol) / bj if bj > 0 else 0; hk_f = (pol_f / bx_f * 100) if bx_f > 0 else 0
            if st.button(f"SAVE {name}"): 
                st.session_state.input_history[name] = bx_f
                st.success("Saved!")
        with c2: tampilkan_kartu_hasil(bx_f, pol_f, hk_f)

    with tabs[0]: render_gilingan("NPP")
    with tabs[1]: render_gilingan("Gilingan 2", True) #
    with tabs[2]: render_gilingan("Gilingan 3", True) # Langsung tanpa pilihan
    with tabs[3]: render_gilingan("Gilingan 4", True) #
    
    if st.button("🔙 BACK", use_container_width=True): st.session_state.page = 'pilih_stasiun'; st.rerun()

elif st.session_state.page == 'pilih_analisa':
    st.markdown("<h2 style='text-align:center; color:white; font-family:Orbitron;'>LABORATORIUM</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: 
        if st.button("🧪 TETES"): st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'tetes'; st.rerun()
    with c2: 
        if st.button("💎 ICUMSA"): st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'icumsa'; st.rerun()
    if st.button("🔙 BACK", use_container_width=True): st.session_state.page = 'dashboard'; st.rerun()

elif st.session_state.page == 'analisa_lab':
    list_jam = [f"{(i%24):02d}:00" for i in range(6, 30)]
    if st.session_state.analisa_type == 'icumsa':
        st.markdown("<h2 style='text-align:center; color:#00d4ff; font-family:Orbitron;'>💎 ICUMSA GULA</h2>", unsafe_allow_html=True)
        st.markdown('<div class="hero-container">', unsafe_allow_html=True)
        jam = st.selectbox("Pilih Jam Analisa", options=list_jam) #
        abs_ic = st.number_input("Absorbansi", value=0.15); bx_ic = st.number_input("Brix Gula", value=49.44) #
        bj_ic = hitung_interpolasi(bx_ic, data_bj)
        res = (abs_ic * 100000) / (bx_ic * 1 * bj_ic) if bx_ic > 0 else 0
        st.metric("HASIL IU", f"{res:.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    elif st.session_state.analisa_type == 'tetes':
        st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
        st.markdown('<div class="hero-container">', unsafe_allow_html=True)
        jam = st.selectbox("Pilih Jam Analisa", options=list_jam) #
        bx = st.number_input("Brix", value=8.8); pol = st.number_input("Pol", value=11.0)
        st.info(f"Analisa Jam: {jam}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔙 BACK", use_container_width=True): st.session_state.page = 'pilih_analisa'; st.rerun()

elif st.session_state.page == 'kurva_brix_page':
    st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>📈 KURVA BRIX GILINGAN</h2>", unsafe_allow_html=True)
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    imb = col1.number_input("Imbibisi % Tebu", value=25.70) #
    sabut = col2.number_input("Kadar Sabut (ft)", value=13.49) #
    jam_p = col3.selectbox("Jam Pantau", [f"{i:02d}:00" for i in range(6, 24)])
    
    # Ambil data input nyata (NPP, G2, G3, G4)
    nyata = [st.session_state.input_history.get(n, 0.0) for n in ["NPP", "Gilingan 2", "Gilingan 3", "Gilingan 4"]]
    if nyata[0] == 0: nyata = [15.46, 9.28, 6.30, 4.16] # Default data materi
    
    teoritis = hitung_kurva_teoritis(nyata[0], imb, sabut) #
    
    fig = go.Figure()
    x_axis = ["G1", "G2", "G3", "G4"]
    fig.add_trace(go.Scatter(x=x_axis, y=nyata, name='Brix Nyata', line=dict(color='#ff4b4b', dash='dash', width=4), mode='lines+markers+text', text=nyata, textposition="top center")) #
    fig.add_trace(go.Scatter(x=x_axis, y=teoritis, name='Brix Teoritis', line=dict(color='#26c4b9', width=4), mode='lines+markers+text', text=teoritis, textposition="bottom center")) #
    
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # KESIMPULAN
    ratio = nyata[1]/teoritis[1] if teoritis[1] > 0 else 0
    if ratio > 1: st.warning(f"⚠️ Ratio {ratio:.2f} > 1: Pencampuran imbibisi kurang merata.")
    elif ratio < 1: st.error(f"🚨 Ratio {ratio:.2f} < 1: Lubang kerja stelan gilingan terlalu lebar.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔙 BACK TO DASHBOARD", use_container_width=True): st.session_state.page = 'dashboard'; st.rerun()
