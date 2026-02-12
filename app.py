import streamlit as st
import datetime
import pytz
import base64
import os
import pandas as pd

# Coba import plotly, kalau gagal pakai chart bawaan streamlit supaya gak error merah
try:
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

# --- 1. CONFIG & STATE ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'
if 'input_history' not in st.session_state:
    # Data default sesuai materi gambar
    st.session_state.input_history = {"NPP": 15.46, "Gilingan 2": 9.28, "Gilingan 3": 6.30, "Gilingan 4": 4.16}

# Standar KPI Management Cockpit
STANDAR = {"OR": 86.0, "ME": 96.2, "BHR": 90.0, "HPB 1": 78.0, "PSHK": 75.0, "KNT": 12.5}
AKTUAL = {"OR": 85.1, "ME": 96.0, "BHR": 88.5, "HPB 1": 76.2, "PSHK": 72.5, "KNT": 12.1}

# --- 2. ASSETS & UTILS ---
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

# --- 3. UI STYLE ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Poppins:wght@400;700&display=swap');
    .stApp {{ background: #0e1117; color: white; }}
    .hero-container {{ background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 15px; border: 1px solid #26c4b9; margin-bottom: 20px; }}
    div.stButton > button {{ background: #1f2937 !important; color: white !important; height: 100px !important; width: 100%; border-radius: 12px; font-family: 'Orbitron'; border: 1px solid #374151; }}
    div.stButton > button:hover {{ border-color: #26c4b9 !important; background: #26c4b922 !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. NAVIGATION LOGIC ---

if st.session_state.page == 'dashboard':
    st.markdown('<h1 style="font-family:Orbitron; color:#26c4b9;">CANE METRIX 2.0</h1>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: 
        if st.button("📝 INPUT DATA"): st.session_state.page = 'input_menu'; st.rerun()
    with c2: 
        if st.button("🧮 LAB ANALISA"): st.session_state.page = 'lab_menu'; st.rerun()
    with c3: 
        if st.button("📊 COCKPIT"): st.session_state.page = 'cockpit'; st.rerun()
    with c4: 
        if st.button("📈 KURVA BRIX"): st.session_state.page = 'kurva_brix'; st.rerun()

elif st.session_state.page == 'cockpit':
    st.markdown("<h2 style='font-family:Orbitron;'>📊 MANAGEMENT COCKPIT</h2>", unsafe_allow_html=True)
    cols = st.columns(6)
    for i, (kpi, target) in enumerate(STANDAR.items()):
        val = AKTUAL[kpi]
        warna = "#26c4b9" if val >= target else "#ff4b4b"
        cols[i].markdown(f"<div style='text-align:center; border-top:3px solid {warna}; padding:10px;'><b>{kpi}</b><br><span style='font-size:20px; color:{warna}; font-family:Orbitron;'>{val}%</span></div>", unsafe_allow_html=True)
    if st.button("🔙 BACK"): st.session_state.page = 'dashboard'; st.rerun()

elif st.session_state.page == 'input_menu':
    st.markdown("<h2 style='font-family:Orbitron;'>🚜 INPUT STASIUN GILINGAN</h2>", unsafe_allow_html=True)
    tabs = st.tabs(["NPP", "Gilingan 2", "Gilingan 3", "Gilingan 4"])
    
    for i, name in enumerate(["NPP", "Gilingan 2", "Gilingan 3", "Gilingan 4"]):
        with tabs[i]:
            # Gilingan 2-4 langsung input
            if name != "NPP": st.info(f"Analisa Langsung: (Brix, Pol, dan HK)")
            else: st.selectbox(f"Pilih Analisa {name}", ["(Brix, Pol, dan HK)"])
            
            c1, c2 = st.columns(2)
            bx = c1.number_input(f"Brix Baca {name}", value=0.0, key=f"bx_{name}")
            sh = c1.number_input(f"Suhu {name}", value=28.0, key=f"sh_{name}")
            pl = c1.number_input(f"Pol Baca {name}", value=0.0, key=f"pl_{name}")
            
            kor = hitung_interpolasi(sh, data_koreksi)
            bj = hitung_interpolasi(bx, data_bj)
            bx_f = bx + kor
            pol_f = (0.286 * pl) / bj if bj > 0 else 0
            hk_f = (pol_f/bx_f*100) if bx_f > 0 else 0
            
            c2.metric("BRIX AKHIR", f"{bx_f:.3f}")
            c2.metric("POL AKHIR", f"{pol_f:.3f}")
            c2.metric("HK", f"{hk_f:.2f}")
            if st.button(f"SAVE {name}"):
                st.session_state.input_history[name] = bx_f
                st.success("Data Tersimpan!")
    if st.button("🔙 BACK"): st.session_state.page = 'dashboard'; st.rerun()

elif st.session_state.page == 'lab_menu':
    st.markdown("<h2 style='font-family:Orbitron;'>🧪 LABORATORIUM</h2>", unsafe_allow_html=True)
    jam_list = [f"{(i%24):02d}:00" for i in range(6, 30)]
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("ICUMSA Gula")
        jam_ic = st.selectbox("Pilih Jam Analisa (ICUMSA)", options=jam_list, key="ic_jam") #
        abs_ic = st.number_input("Absorbansi", value=0.15, key="ic_abs") #
        bx_ic = st.number_input("Brix Gula", value=49.44, key="ic_bx") #
        bj_ic = hitung_interpolasi(bx_ic, data_bj)
        res_ic = (abs_ic * 100000) / (bx_ic * 1 * bj_ic) if bx_ic > 0 else 0
        st.metric("IU (ICUMSA)", f"{res_ic:.2f}")
        
    with col_b:
        st.subheader("Analisa Tetes")
        jam_t = st.selectbox("Pilih Jam Analisa (Tetes)", options=jam_list, key="t_jam") #
        st.write(f"Input data tetes untuk jam {jam_t}...")
    if st.button("🔙 BACK"): st.session_state.page = 'dashboard'; st.rerun()

elif st.session_state.page == 'kurva_brix':
    st.markdown("<h2 style='font-family:Orbitron;'>📈 ANALISA KURVA BRIX</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    imb = c1.number_input("Imbibisi % Tebu (I)", value=25.70) #
    sabut = c2.number_input("Kadar Sabut (ft)", value=13.49) #
    
    nyata = [st.session_state.input_history.get(n, 0.0) for n in ["NPP", "Gilingan 2", "Gilingan 3", "Gilingan 4"]]
    lamda = imb / sabut if sabut > 0 else 0 #
    
    # Rumus Bni
    teoritis = [nyata[0]]
    for gi in range(1, 4):
        bni = nyata[0] * (((lamda**(3-gi)) + 1 - gi) / (lamda**3 + 1 - 1))
        teoritis.append(round(bni, 2))
    
    if HAS_PLOTLY:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=["G1", "G2", "G3", "G4"], y=nyata, name='Brix Nyata', line=dict(color='#ff4b4b', dash='dash'))) #
        fig.add_trace(go.Scatter(x=["G1", "G2", "G3", "G4"], y=teoritis, name='Brix Teoritis', line=dict(color='#26c4b9'))) #
        fig.update_layout(title="Kurva Brix Gilingan", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Gagal memuat Plotly. Menampilkan tabel data:")
        st.table(pd.DataFrame({"Gilingan": ["G1", "G2", "G3", "G4"], "Nyata": nyata, "Teoritis": teoritis}))

    # Kesimpulan
    ratio = nyata[1] / teoritis[1] if teoritis[1] > 0 else 0
    if ratio > 1: st.warning(f"Hasil Ratio: {ratio:.2f} > 1. Pencampuran imbibisi kurang merata.")
    elif ratio < 1: st.error(f"Hasil Ratio: {ratio:.2f} < 1. Lubang kerja gilingan terlalu lebar.")
    
    if st.button("🔙 BACK"): st.session_state.page = 'dashboard'; st.rerun()
