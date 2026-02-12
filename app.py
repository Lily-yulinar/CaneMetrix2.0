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
if 'input_history' not in st.session_state:
    st.session_state.input_history = {"NPP": 15.46, "Gilingan 2": 9.28, "Gilingan 3": 6.30, "Gilingan 4": 4.16}

# Data Standar KPI untuk Management Cockpit
STANDAR = {"OR": 86.0, "ME": 96.2, "BHR": 90.0, "HPB 1": 78.0, "PSHK": 75.0, "KNT": 12.5}
AKTUAL = {"OR": 85.1, "ME": 96.0, "BHR": 88.5, "HPB 1": 76.2, "PSHK": 72.5, "KNT": 12.1}

# --- 2. ASSETS & UTILS ---
def get_base64_logo(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

logo_ptpn = get_base64_logo("ptpn.png"); logo_sgn = get_base64_logo("sgn.png")
logo_cane = get_base64_logo("canemetrix.png")

data_koreksi = {27: -0.05, 28: 0.02, 29: 0.09, 30: 0.16, 31: 0.24, 32: 0.315, 33: 0.385, 34: 0.465, 35: 0.54}
data_bj = {0.0: 0.99640, 10.0: 1.03608, 20.0: 1.07844, 30.0: 1.12368, 40.0: 1.17203, 50.0: 1.22372}

def hitung_interpolasi(nilai, dataset):
    keys = sorted(dataset.keys())
    if nilai in dataset: return dataset[nilai]
    if nilai < keys[0]: return dataset[keys[0]]
    if nilai > keys[-1]: return dataset[keys[-1]]
    for i in range(len(keys)-1):
        x0, x1 = keys[i], keys[i+1]
        if x0 < nilai < x1:
            y0, y1 = dataset[x0], dataset[x1]
            return y0 + (nilai - x0) * (y1 - y0) / (x1 - x0)
    return 1.0

# --- 3. CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Poppins:wght@300;400;700&display=swap');
    .stApp {{ background: linear-gradient(rgba(0, 10, 30, 0.9), rgba(0, 10, 30, 0.9)), url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"); background-size: cover; }}
    .hero-container {{ background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 25px; margin-bottom: 20px; }}
    div.stButton > button {{ background: rgba(255, 255, 255, 0.07) !important; border-radius: 15px !important; color: white !important; height: 120px !important; width: 100% !important; transition: 0.3s; font-family: 'Orbitron'; }}
    div.stButton > button:hover {{ background: rgba(38, 196, 185, 0.2) !important; border-color: #26c4b9 !important; transform: translateY(-3px) !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. NAVIGATION ---
if st.session_state.page == 'dashboard':
    st.markdown(f'''<div class="hero-container"><h1 style="font-family:Orbitron; color:white; margin:0;">CANE METRIX</h1><p style="color:#26c4b9; font-weight:700; letter-spacing:3px;">ACCELERATING QA PERFORMANCE</p></div>''', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: 
        if st.button("📝 INPUT DATA"): st.session_state.page = 'pilih_stasiun'; st.rerun()
    with c2:
        if st.button("🧮 HITUNG LAB"): st.session_state.page = 'pilih_analisa'; st.rerun()
    with c3:
        if st.button("📊 COCKPIT"): st.session_state.page = 'cockpit'; st.rerun()
    with c4:
        if st.button("📈 KURVA BRIX"): st.session_state.page = 'kurva_brix'; st.rerun()

elif st.session_state.page == 'cockpit':
    st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>📊 MANAGEMENT COCKPIT</h2>", unsafe_allow_html=True)
    cols = st.columns(6)
    for i, (kpi, target) in enumerate(STANDAR.items()):
        val = AKTUAL[kpi]
        warna = "#26c4b9" if val >= target else "#ff4b4b"
        with cols[i]:
            st.markdown(f"""<div style="background:rgba(255,255,255,0.05); padding:15px; border-radius:15px; border-top:4px solid {warna}; text-align:center;">
                <p style="color:white; font-size:12px; margin:0;">{kpi}</p><h3 style="color:{warna}; font-family:Orbitron;">{val}%</h3>
                <p style="color:#888; font-size:10px;">Std: {target}%</p></div>""", unsafe_allow_html=True)
    
    st.markdown("<br><div class='hero-container'><h3>📉 Recovery Trend</h3>", unsafe_allow_html=True)
    chart_data = pd.DataFrame({"Jam": ["06:00", "08:00", "10:00", "12:00"], "OR": [85.0, 85.5, 85.1, 84.8]}).set_index("Jam")
    st.line_chart(chart_data)
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("🔙 BACK"): st.session_state.page = 'dashboard'; st.rerun()

elif st.session_state.page == 'pilih_stasiun':
    st.markdown("<h2 style='text-align:center; color:white; font-family:Orbitron;'>STASIUN GILINGAN</h2>", unsafe_allow_html=True)
    if st.button("🚜 INPUT DATA GILINGAN", use_container_width=True): st.session_state.page = 'input_gilingan'; st.rerun()
    if st.button("🔙 BACK", use_container_width=True): st.session_state.page = 'dashboard'; st.rerun()

elif st.session_state.page == 'input_gilingan':
    tabs = st.tabs(["NPP", "Gilingan 2", "Gilingan 3", "Gilingan 4"])
    def input_template(name, direct=False):
        st.markdown(f"### {name}")
        c1, c2 = st.columns([1, 2])
        with c1:
            bx = st.number_input(f"Brix Baca {name}", value=0.0, key=f"bx_{name}")
            sh = st.number_input(f"Suhu {name}", value=28.0, key=f"sh_{name}")
            pl = st.number_input(f"Pol Baca {name}", value=0.0, key=f"pl_{name}")
            kor = hitung_interpolasi(sh, data_koreksi); bj = hitung_interpolasi(bx, data_bj)
            bx_f = bx + kor; pol_f = (0.286 * pl) / bj if bj > 0 else 0; hk_f = (pol_f/bx_f*100) if bx_f > 0 else 0
            if st.button(f"SAVE {name}"): 
                st.session_state.input_history[name] = bx_f
                st.success(f"{name} Updated!")
        with c2: st.metric("Brix Akhir", f"{bx_f:.3f}"); st.metric("Pol Akhir", f"{pol_f:.3f}"); st.metric("HK", f"{hk_f:.2f}")

    with tabs[0]: input_template("NPP")
    with tabs[1]: input_template("Gilingan 2", True) #
    with tabs[2]: input_template("Gilingan 3", True) #
    with tabs[3]: input_template("Gilingan 4", True) #
    if st.button("🔙 BACK"): st.session_state.page = 'pilih_stasiun'; st.rerun()

elif st.session_state.page == 'pilih_analisa':
    c1, c2 = st.columns(2)
    with c1: 
        if st.button("🧪 ANALISA TETES"): st.session_state.page = 'lab'; st.session_state.analisa_type = 'tetes'; st.rerun()
    with c2: 
        if st.button("💎 ICUMSA GULA"): st.session_state.page = 'lab'; st.session_state.analisa_type = 'icumsa'; st.rerun()
    if st.button("🔙 BACK"): st.session_state.page = 'dashboard'; st.rerun()

elif st.session_state.page == 'lab':
    jam_list = [f"{(i%24):02d}:00" for i in range(6, 30)]
    if st.session_state.analisa_type == 'icumsa':
        st.markdown("<h2 style='text-align:center; color:#00d4ff; font-family:Orbitron;'>💎 ICUMSA GULA</h2>", unsafe_allow_html=True)
        st.selectbox("Pilih Jam Analisa", options=jam_list) #
        st.number_input("Absorbansi", value=0.15); st.number_input("Brix Gula", value=49.44) #
    elif st.session_state.analisa_type == 'tetes':
        st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
        st.selectbox("Pilih Jam Analisa", options=jam_list) #
    if st.button("🔙 BACK"): st.session_state.page = 'pilih_analisa'; st.rerun()

elif st.session_state.page == 'kurva_brix':
    st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>📈 KURVA BRIX</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    imb = c1.number_input("Imbibisi % Tebu", value=25.70); sabut = c2.number_input("Sabut (ft)", value=13.49)
    jam_p = c3.selectbox("Jam", [f"{i:02d}:00" for i in range(6, 24)])
    
    nyata = [st.session_state.input_history.get(n, 0.0) for n in ["NPP", "Gilingan 2", "Gilingan 3", "Gilingan 4"]]
    lamda = imb / sabut if sabut > 0 else 0 #
    teoritis = [nyata[0]]
    for gi in range(1, 4):
        bni = nyata[0] * (((lamda**(3-gi)) + 1 - gi) / (lamda**3)) #
        teoritis.append(round(bni, 2))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=["G1", "G2", "G3", "G4"], y=nyata, name='Nyata', line=dict(color='#ff4b4b', dash='dash'))) #
    fig.add_trace(go.Scatter(x=["G1", "G2", "G3", "G4"], y=teoritis, name='Teoritis', line=dict(color='#26c4b9'))) #
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)
    if st.button("🔙 BACK"): st.session_state.page = 'dashboard'; st.rerun()
