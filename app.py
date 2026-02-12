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

# --- 2. ASSETS ---
def get_base64_logo(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo_ptpn = get_base64_logo("ptpn.png"); logo_sgn = get_base64_logo("sgn.png")
logo_lpp = get_base64_logo("lpp.png"); logo_kb = get_base64_logo("kb.png")
logo_cane = get_base64_logo("canemetrix.png")

# --- 3. DATABASE & INTERPOLASI ---
data_koreksi = {27: -0.05, 28: 0.02, 29: 0.09, 30: 0.16, 31: 0.24, 32: 0.315, 33: 0.385, 34: 0.465, 35: 0.54, 36: 0.62, 37: 0.70, 38: 0.78, 39: 0.86, 40: 0.94}
data_bj = {0.0: 0.99640, 5.0: 1.01592, 10.0: 1.03608, 15.0: 1.05691, 20.0: 1.07844, 25.0: 1.10069, 30.0: 1.12368, 35.0: 1.14745, 40.0: 1.17203, 45.0: 1.19746, 50.0: 1.22372}
data_tsai = {15.0: 336.00, 22.5: 223.60, 37.7: 136.67} # Contoh interpolasi singkat

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

# --- 4. CSS (VERSI RAKSASA & MODERN) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@300;400;700&display=swap');
    
    .stApp {{ 
        background: linear-gradient(rgba(0, 10, 30, 0.9), rgba(0, 10, 30, 0.9)), 
        url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"); 
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* Container Hasil Raksasa */
    .huge-box {{
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        padding: 35px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        margin-bottom: 15px;
    }}
    .brix-border {{ border: 3px solid #26c4b9; box-shadow: 0 0 20px rgba(38, 196, 185, 0.2); }}
    .pol-border {{ border: 3px solid #ffcc00; box-shadow: 0 0 20px rgba(255, 204, 0, 0.2); }}
    .hk-border {{ border: 3px solid #ff4b4b; box-shadow: 0 0 20px rgba(255, 75, 75, 0.2); }}

    .val-text {{ font-family: 'Orbitron', sans-serif; font-size: 85px !important; font-weight: 900; margin: 0; line-height: 1; }}
    .lbl-text {{ font-family: 'Poppins', sans-serif; font-size: 16px; font-weight: 700; letter-spacing: 2px; text-align: right; opacity: 0.8; color: white; }}

    /* Button Styling */
    div.stButton > button {{
        background: rgba(255, 255, 255, 0.07) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        color: white !important;
        height: 150px !important;
        transition: 0.3s !important;
    }}
    div.stButton > button:hover {{ border-color: #26c4b9 !important; transform: translateY(-5px) !important; background: rgba(38, 196, 185, 0.2) !important; }}
    
    .header-logo-box {{ background: white; padding: 10px 20px; border-radius: 15px; display: inline-flex; align-items: center; gap: 15px; margin-bottom: 20px; }}
    .header-logo-box img {{ height: 30px; }}
    </style>
    """, unsafe_allow_html=True)

def render_hasil_raksasa(brix, pol, hk):
    st.markdown(f"""
        <div class="huge-box brix-border">
            <div class="val-text" style="color: #26c4b9;">{brix:.3f}</div>
            <div class="lbl-text">% BRIX AKHIR</div>
        </div>
        <div class="huge-box pol-border">
            <div class="val-text" style="color: #ffcc00;">{pol:.3f}</div>
            <div class="lbl-text">% POL AKHIR</div>
        </div>
        <div class="huge-box hk-border">
            <div class="val-text" style="color: #ff4b4b;">{hk:.2f}</div>
            <div class="lbl-text">HK</div>
        </div>
    """, unsafe_allow_html=True)

@st.fragment(run_every="1s")
def jam_realtime():
    tz = pytz.timezone('Asia/Jakarta'); now = datetime.datetime.now(tz)
    st.markdown(f'''<div style="text-align: right; color: white; font-family: 'Poppins';">{now.strftime("%d %B %Y")}<br><span style="font-family:'Orbitron'; color:#26c4b9; font-size:20px; font-weight:bold;">{now.strftime("%H:%M:%S")} WIB</span></div>''', unsafe_allow_html=True)

# --- 5. PAGE LOGIC ---

if st.session_state.page == 'dashboard':
    c_l, c_r = st.columns([2, 1])
    with c_l: st.markdown(f'''<div class="header-logo-box"><img src="data:image/png;base64,{logo_ptpn}"><img src="data:image/png;base64,{logo_sgn}"><img src="data:image/png;base64,{logo_lpp}"><img src="data:image/png;base64,{logo_kb}"></div>''', unsafe_allow_html=True)
    with c_r: jam_realtime()
    
    st.markdown("<h1 style='text-align:center; color:white; font-family:Orbitron; font-size:50px;'>CANE METRIX</h1>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("📝\n\nINPUT DATA", use_container_width=True): st.session_state.page = 'pilih_stasiun'; st.rerun()
    with c2:
        if st.button("🧮\n\nHITUNG ANALISA", use_container_width=True): st.session_state.page = 'pilih_analisa'; st.rerun()
    with c3:
        if st.button("📅\n\nDATABASE", use_container_width=True): st.toast("Coming Soon")

elif st.session_state.page == 'pilih_stasiun':
    st.markdown("<h2 style='text-align:center; color:white; font-family:Orbitron;'>PILIH STASIUN</h2>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    stations = [
        ("🚜 STASIUN GILINGAN", "input_gilingan"),
        ("🌫️ STASIUN PEMURNIAN", "input_pemurnian"),
        ("🔥 STASIUN PENGUAPAN", "input_penguapan"),
        ("🍯 STASIUN MASAKAN", "input_masakan"),
        ("🌀 STASIUN PUTARAN", "input_putaran"),
        ("📦 PENGEMASAN", "input_pengemasan")
    ]
    
    for i, (name, target) in enumerate(stations):
        with cols[i % 3]:
            if st.button(name, use_container_width=True): 
                st.session_state.page = target; st.rerun()
                
    if st.button("🔙 KEMBALI", use_container_width=True): st.session_state.page = 'dashboard'; st.rerun()

elif st.session_state.page == 'input_gilingan':
    st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>🚜 STASIUN GILINGAN</h2>", unsafe_allow_html=True)
    t1, t2, t3, t4 = st.tabs(["NPP", "G2", "G3", "G4"])
    
    with t1:
        ci, ch = st.columns([1, 2.2])
        with ci:
            bx = st.number_input("Brix Baca", value=0.0, key="npp_bx")
            sh = st.number_input("Suhu", value=28.0, key="npp_sh")
            pl = st.number_input("Pol Baca", value=0.0, key="npp_pl")
            kor = hitung_interpolasi(sh, data_koreksi)
            bj = hitung_interpolasi(bx, data_bj)
            brix_f = bx + kor if bx > 0 else 0
            pol_f = (0.286 * pl) / bj if bj > 0 else 0
            hk_f = (pol_f / brix_f * 100) if brix_f > 0 else 0
        with ch:
            render_hasil_raksasa(brix_f, pol_f, hk_f)
            
    if st.button("🔙 KEMBALI", use_container_width=True): st.session_state.page = 'pilih_stasiun'; st.rerun()

# --- TAMBAHAN SEMUA STASIUN ---
elif st.session_state.page in ['input_pemurnian', 'input_penguapan', 'input_masakan', 'input_putaran', 'input_pengemasan']:
    st.markdown(f"<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>{st.session_state.page.replace('_',' ').upper()}</h2>", unsafe_allow_html=True)
    ci, ch = st.columns([1, 2.2])
    with ci:
        bx = st.number_input("Brix Teramati", value=0.0)
        sh = st.number_input("Suhu", value=28.0)
        pl = st.number_input("Pol Baca", value=0.0)
        kor = hitung_interpolasi(sh, data_koreksi); bj = hitung_interpolasi(bx, data_bj)
        brix_f = bx + kor; pol_f = (0.286 * pl) / bj if bj > 0 else 0; hk_f = (pol_f / brix_f * 100) if brix_f > 0 else 0
    with ch:
        render_hasil_raksasa(brix_f, pol_f, hk_f)
    if st.button("🔙 KEMBALI", use_container_width=True): st.session_state.page = 'pilih_stasiun'; st.rerun()

elif st.session_state.page == 'pilih_analisa':
    st.markdown("<h2 style='text-align:center; color:white; font-family:Orbitron;'>HITUNG ANALISA LAB</h2>", unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    with m1:
        if st.button("🧪 ANALISA TETES", use_container_width=True):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'tetes'; st.rerun()
    with m2:
        if st.button("🔬 OD TETES", use_container_width=True):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'od'; st.rerun()
    if st.button("🔙 KEMBALI", use_container_width=True): st.session_state.page = 'dashboard'; st.rerun()

elif st.session_state.page == 'analisa_lab':
    st.markdown(f"<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>{st.session_state.analisa_type.upper()}</h2>", unsafe_allow_html=True)
    ci, ch = st.columns([1, 2.2])
    if st.session_state.analisa_type == 'tetes':
        with ci:
            bx = st.number_input("Brix Teramati", value=8.80); sh = st.number_input("Suhu", value=28.0); pl = st.number_input("Pol Baca", value=11.0)
            kor = hitung_interpolasi(sh, data_koreksi); bj = hitung_interpolasi(bx, data_bj)
            brix_f = (bx + kor) * 10; pol_f = (0.286 * pl) / bj * 10; hk_f = (pol_f / brix_f * 100) if brix_f > 0 else 0
        with ch:
            render_hasil_raksasa(brix_f, pol_f, hk_f)
    if st.button("🔙 KEMBALI", use_container_width=True): st.session_state.page = 'pilih_analisa'; st.rerun()
