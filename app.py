import streamlit as st
import numpy as np

# --- 1. CONFIG ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

# Inisialisasi session state
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

# --- 2. LOGIKA KOREKSI ---
data_koreksi = {
    25: -0.19, 26: -0.12, 27: -0.05, 28: 0.02, 29: 0.09,
    30: 0.16, 31: 0.24, 32: 0.31, 33: 0.38, 34: 0.46,
    35: 0.54, 36: 0.62, 37: 0.70, 38: 0.78, 39: 0.86,
    40: 0.94, 41: 1.02, 42: 1.10, 43: 1.18, 44: 1.26,
    45: 1.34, 46: 1.42, 47: 1.5, 48: 1.58, 49: 1.66, 50: 1.72
}

def hitung_koreksi(suhu_val):
    s_keys = sorted(data_koreksi.keys())
    s_vals = [data_koreksi[k] for k in s_keys]
    return float(np.interp(suhu_val, s_keys, s_vals))

# --- 3. CSS SEDERHANA (Biar gak berat) ---
st.markdown("""
    <style>
    .stButton>button {
        height: 120px; width: 100%; border-radius: 15px;
        font-size: 20px; font-weight: bold; margin: 10px 0px;
    }
    .main-card {
        background: rgba(255, 255, 255, 0.1); padding: 20px;
        border-radius: 20px; border: 1px solid #444;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. NAVIGASI ---

if st.session_state.page == 'dashboard':
    st.title("CANE METRIX")
    st.write("ACCELERATING QA PERFORMANCE")
    
    col1, col2, col3 = st.columns(3)
    
    # Teknik Tanpa Callback: Langsung Ubah State & Rerun
    with col1:
        if st.button("📝 INPUT DATA", key="btn1"):
            st.session_state.page = 'input'
            st.rerun()
            
    with col2:
        if st.button("🧮 HITUNG ANALISA", key="btn2"):
            st.session_state.page = 'analisa'
            st.rerun()
            
    with col3:
        if st.button("📅 DATABASE", key="btn3"):
            st.session_state.page = 'database'
            st.rerun()

elif st.session_state.page == 'analisa':
    st.title("🧪 ANALISA TETES (% BRIX)")
    
    if st.button("🔙 KEMBALI KE DASHBOARD"):
        st.session_state.page = 'dashboard'
        st.rerun()
        
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Input")
        b_obs = st.number_input("Brix Teramati", value=8.50)
        suhu = st.number_input("Suhu (°C)", value=28.0)
    with c2:
        st.subheader("Hasil")
        k = hitung_koreksi(suhu)
        hasil = (b_obs * 10) + k
        st.success(f"Hasil % Brix: {hasil:.2f}")
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.write(f"Halaman {st.session_state.page} sedang progress.")
    if st.button("KEMBALI"):
        st.session_state.page = 'dashboard'
        st.rerun()
