import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# 1. INISIALISASI SESSION STATE (Penting agar tidak KeyError)
if 'brix_history' not in st.session_state:
    st.session_state.brix_history = {
        "NPP": 0.0, 
        "Gilingan 2": 0.0, 
        "Gilingan 3": 0.0, 
        "Gilingan 4": 0.0
    }

st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

# Header Aplikasi
st.markdown("<h1 style='text-align: center;'>🚜 INPUT DATA STASIUN GILINGAN</h1>", unsafe_allow_Html=True)

# 2. AREA INPUT DATA (Tab System)
tabs = st.tabs(["NPP (Gilingan 1)", "Gilingan 2", "Gilingan 3", "Gilingan 4", "Nira Mentah", "Ampas", "Imbibisi", "Putaran & Tekanan"])

with tabs[0]:
    st.subheader("Input Parameter NPP")
    npp_brix = st.number_input("Brix Baca NPP", min_value=0.0, value=st.session_state.brix_history["NPP"], key="in_npp")
    st.session_state.brix_history["NPP"] = npp_brix

with tabs[1]:
    st.subheader("Input Parameter Gilingan 2")
    g2_brix = st.number_input("Brix Baca G2", min_value=0.0, value=st.session_state.brix_history["Gilingan 2"], key="in_g2")
    st.session_state.brix_history["Gilingan 2"] = g2_brix

with tabs[2]:
    st.subheader("Input Parameter Gilingan 3")
    g3_brix = st.number_input("Brix Baca G3", min_value=0.0, value=st.session_state.brix_history["Gilingan 3"], key="in_g3")
    st.session_state.brix_history["Gilingan 3"] = g3_brix

with tabs[3]:
    st.subheader("Input Parameter Gilingan 4")
    g4_brix = st.number_input("Brix Baca G4", min_value=0.0, value=st.session_state.brix_history["Gilingan 4"], key="in_g4")
    st.session_state.brix_history["Gilingan 4"] = g4_brix

st.divider()

# 3. BAGIAN KURVA BRIX GILINGAN (Baris 161 dkk)
st.markdown("<h2 style='text-align: center;'>📈 KURVA BRIX GILINGAN</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    I = st.number_input("Imbibisi % Tebu (I)", value=25.70, format="%.2f")
with col2:
    ft = st.number_input("Kadar Sabut (ft)", value=13.49, format="%.2f")
with col3:
    jam_analisa = st.selectbox("Jam Analisa", ["06:00", "14:00", "22:00"])

# --- Logika Perhitungan Sesuai Dokumen Teknis ---
# bni = bn1 * ((lambda * (eg) + 1 - gi) / (lambda * (eg) + 1 - 1))
lambd = I / ft
eg = 4 # Jumlah gilingan basah (NPP dihitung sebagai titik awal)
bn1 = st.session_state.brix_history["NPP"]

def hitung_teoritis(gi):
    if bn1 == 0: return 0
    pembilang = (lambd * eg) + 1 - gi
    penyebut = (lambd * eg) + 1 - 1
    return bn1 * (pembilang / penyebut)

# Data untuk Grafik
labels = ["NPP", "Gilingan 2", "Gilingan 3", "Gilingan 4"]
teoritis = [bn1, hitung_teoritis(2), hitung_teoritis(3), hitung_teoritis(4)]

# PERBAIKAN BARIS 161: Menggunakan .get() agar aman dari KeyError
nyata = [st.session_state.brix_history.get(n, 0.0) for n in labels]

# 4. PEMBUATAN GRAFIK PLOTLY
fig = go.Figure()

# Garis Brix Teoritis (Hijau)
fig.add_trace(go.Scatter(x=labels, y=teoritis, name='Brix Teoritis',
                         line=dict(color='green', width=3), mode='lines+markers'))

# Garis Brix Nyata (Merah Putus-putus)
fig.add_trace(go.Scatter(x=labels, y=nyata, name='Brix Nyata',
                         line=dict(color='red', width=3, dash='dash'), mode='lines+markers'))

fig.update_layout(
    title="Grafik Realisasi vs Teoritis",
    xaxis_title="Stasiun Gilingan",
    yaxis_title="% Brix",
    template="plotly_dark",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)

# 5. KESIMPULAN (Sesuai gambar pedoman)
st.info("### Kesimpulan Operasional")
ratio_g2 = nyata[1]/teoritis[1] if teoritis[1] > 0 else 0

if ratio_g2 > 1:
    st.warning("⚠️ Brix Nyata/Teori > 1: Pencampuran imbibisi air/nira dalam ampas kurang merata.")
elif ratio_g2 < 1 and ratio_g2 > 0:
    st.error("⚠️ Brix Nyata/Teori < 1: Lubang kerja stelan gilingan terlalu lebar.")
else:
    st.success("✅ Kinerja gilingan dalam kondisi normal atau data belum diisi.")
