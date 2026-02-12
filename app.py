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

# --- 3. DATABASE ---
data_koreksi = {27: -0.05, 28: 0.02, 29: 0.09, 30: 0.16, 31: 0.24, 32: 0.315, 33: 0.385, 34: 0.465, 35: 0.54, 36: 0.62, 37: 0.70, 38: 0.78, 39: 0.86, 40: 0.94}
data_bj = {0.0: 0.99640, 5.0: 1.01592, 10.0: 1.03608, 15.0: 1.05691, 20.0: 1.07844, 25.0: 1.10069, 30.0: 1.12368, 35.0: 1.14745, 40.0: 1.17203, 45.0: 1.19746, 50.0: 1.22372}

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

# --- 4. CSS (VERSI SUPER LEBAR SESUAI GAMBAR) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Poppins:wght@400;700&display=swap');
    
    .stApp {{ background: #0e1117; color: white; }}

    /* Layout Utama: Input Kiri, Hasil Kanan */
    .main-container {{
        display: flex;
        gap: 30px;
        align-items: flex-start;
    }}

    /* Kolom Hasil (Tumpukan Vertikal Lebar) */
    .result-column {{
        flex: 2; /* Kasih ruang lebih banyak buat hasil */
        display: flex;
        flex-direction: column;
        gap: 20px;
    }}

    /* Card Box Raksasa */
    .huge-box {{
        background: rgba(255, 255, 255, 0.02);
        border-radius: 20px;
        padding: 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        min-height: 180px;
    }}

    .brix-border {{ border: 3px solid #26c4b9; box-shadow: 0 0 20px rgba(38, 196, 185, 0.2); }}
    .pol-border {{ border: 3px solid #ffcc00; box-shadow: 0 0 20px rgba(255, 204, 0, 0.2); }}
    .hk-border {{ border: 3px solid #ff4b4b; box-shadow: 0 0 20px rgba(255, 75, 75, 0.2); }}

    .val-text {{
        font-family: 'Orbitron', sans-serif;
        font-size: 110px !important; /* UKURAN RAKSASA */
        font-weight: 900;
        margin: 0;
        line-height: 1;
    }}

    .lbl-text {{
        font-family: 'Poppins', sans-serif;
        font-size: 20px;
        font-weight: 700;
        letter-spacing: 3px;
        text-align: right;
        opacity: 0.8;
    }}

    /* Input Styling */
    .stNumberInput, .stSelectbox {{ margin-bottom: 15px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. PAGE LOGIC ---

if st.session_state.page == 'dashboard':
    st.markdown("<h1 style='text-align:center; font-family:Orbitron;'>CANE METRIX</h1>", unsafe_allow_html=True)
    if st.button("🧮 HITUNG ANALISA", use_container_width=True):
        st.session_state.page = 'pilih_analisa'; st.rerun()

elif st.session_state.page == 'pilih_analisa':
    st.markdown("<h2 style='text-align:center; font-family:Orbitron;'>PILIH ANALISA</h2>", unsafe_allow_html=True)
    if st.button("🧪 ANALISA TETES", use_container_width=True):
        st.session_state.page = 'analisa_tetes_final'; st.rerun()
    if st.button("🔙 KEMBALI", use_container_width=True): st.session_state.page = 'dashboard'; st.rerun()

elif st.session_state.page == 'analisa_tetes_final':
    st.markdown(f"<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # PEMBAGIAN KOLOM SESUAI GAMBAR
    col_input, col_hasil = st.columns([1, 2.5]) # Kanan jauh lebih lebar

    with col_input:
        jam = st.selectbox("Analisa Jam", [f"{i:02d}:00" for i in range(24)], index=6)
        b_in = st.number_input("Brix Teramati", value=8.80, format="%.2f")
        s_in = st.number_input("Suhu (°C)", value=28.0, format="%.1f")
        p_in = st.number_input("Pol Baca", value=11.00, format="%.2f")
        
        # Logika Hitung
        kor = hitung_interpolasi(s_in, data_koreksi)
        bj = hitung_interpolasi(b_in, data_bj)
        bf = (b_in + kor) * 10
        pf = (0.286 * p_in) / bj * 10
        hf = (pf / bf * 100) if bf > 0 else 0
        
        st.markdown("<br>"*5, unsafe_allow_html=True)
        if st.button("🔙 KEMBALI", use_container_width=True):
            st.session_state.page = 'pilih_analisa'; st.rerun()

    with col_hasil:
        # TAMPILAN HASIL RAKSASA VERTIKAL (SESUAI GAMBAR FD9C9E)
        st.markdown(f"""
            <div class="huge-box brix-border">
                <div class="val-text" style="color: #26c4b9;">{bf:.3f}</div>
                <div class="lbl-text">% BRIX AKHIR</div>
            </div>
            <div style="height: 15px;"></div>
            <div class="huge-box pol-border">
                <div class="val-text" style="color: #ffcc00;">{pf:.3f}</div>
                <div class="lbl-text">% POL AKHIR</div>
            </div>
            <div style="height: 15px;"></div>
            <div class="huge-box hk-border">
                <div class="val-text" style="color: #ff4b4b;">{hf:.2f}</div>
                <div class="lbl-text">HK</div>
            </div>
        """, unsafe_allow_html=True)
