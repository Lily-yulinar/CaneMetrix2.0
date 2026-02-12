import streamlit as st
import datetime
import pytz
import base64
import os
import pandas as pd
import plotly.graph_objects as go
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- 1. CONFIG & GSHEET SETUP ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")

# Fungsi Koneksi GSheet
def koneksi_gsheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # Pastikan file credentials.json ada di folder yang sama
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    # Ganti dengan NAMA Spreadsheet lo
    return client.open("KKKB_250711") 

if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'
if 'analisa_type' not in st.session_state:
    st.session_state.analisa_type = None

# --- 2. LOGIC SYNC (DATABASE) ---

def simpan_ke_gsheet(jam, data_brix_pol):
    try:
        sheet = koneksi_gsheet().worksheet("INPUT")
        # Cari baris berdasarkan Jam di Kolom B (Baris 66-89)
        list_jam = sheet.col_values(2) # Ambil Kolom B
        target_row = None
        for idx, val in enumerate(list_jam):
            if jam in val:
                target_row = idx + 1
                break
        
        if target_row:
            # Update Sel (C=3, D=4, I=9, J=10, K=11, L=12, M=13, N=14)
            updates = [
                {'range': f'C{target_row}', 'values': [[data_brix_pol["bx_NPP"]]]},
                {'range': f'D{target_row}', 'values': [[data_brix_pol["pol_NPP"]]]},
                {'range': f'I{target_row}', 'values': [[data_brix_pol["bx_G2"]]]},
                {'range': f'J{target_row}', 'values': [[data_brix_pol["pol_G2"]]]},
                {'range': f'K{target_row}', 'values': [[data_brix_pol["bx_G3"]]]},
                {'range': f'L{target_row}', 'values': [[data_brix_pol["pol_G3"]]]},
                {'range': f'M{target_row}', 'values': [[data_brix_pol["bx_G4"]]]},
                {'range': f'N{target_row}', 'values': [[data_brix_pol["pol_G4"]]]}
            ]
            for update in updates:
                sheet.update(update['range'], update['values'])
            return True
    except Exception as e:
        st.error(f"Gagal Sync: {e}")
        return False

def tarik_data_kurva():
    try:
        # Menarik data Rata-rata Real dari Spreadsheet (Mirip rumus AVERAGEIF di D8:D11 lo)
        sheet = koneksi_gsheet().worksheet("INPUT")
        data = sheet.get("C66:M89") # Tarik range data
        df = pd.DataFrame(data)
        # Ambil kolom brix NPP(0), G2(6), G3(8), G4(10)
        brix_cols = [0, 6, 8, 10]
        rata_rata = []
        for col in brix_cols:
            vals = pd.to_numeric(df[col], errors='coerce').dropna()
            avg = vals[vals > 0].mean()
            rata_rata.append(round(avg, 2) if not pd.isna(avg) else 0)
        return rata_rata
    except:
        return [0, 0, 0, 0]

# --- 3. DATABASE & INTERPOLASI ---
data_koreksi = {27: -0.05, 28: 0.02, 29: 0.09, 30: 0.16, 31: 0.24, 32: 0.315, 33: 0.385, 34: 0.465, 35: 0.54, 36: 0.62, 37: 0.70, 38: 0.78, 39: 0.86, 40: 0.94}
data_bj = {0.0: 0.99640, 5.0: 1.01592, 10.0: 1.03608, 15.0: 1.05691, 20.0: 1.07844, 25.0: 1.10069, 30.0: 1.12368, 35.0: 1.14745, 40.0: 1.17203, 45.0: 1.19746, 50.0: 1.22372}

def hitung_interpolasi(nilai_user, dataset):
    keys = sorted(dataset.keys())
    if nilai_user in dataset: return dataset[nilai_user]
    for i in range(len(keys) - 1):
        x0, x1 = keys[i], keys[i+1]
        if x0 < nilai_user < x1:
            y0, y1 = dataset[x0], dataset[x1]
            return y0 + (nilai_user - x0) * (y1 - y0) / (x1 - x0)
    return 1.0

# --- 4. UI COMPONENTS ---
def tampilkan_kartu_hasil(brix, pol, hk):
    st.markdown(f"""
    <div style="display: flex; flex-direction: column; gap: 10px;">
        <div style="background: rgba(38, 196, 185, 0.1); padding: 20px; border-radius: 15px; border: 2px solid #26c4b9; display: flex; justify-content: space-between; align-items: center;">
            <h2 style="color:#26c4b9; font-family:Orbitron; margin:0;">{brix:.2f}</h2>
            <p style="color:white; margin:0; font-size:12px;">% BRIX</p>
        </div>
        <div style="background: rgba(255, 204, 0, 0.1); padding: 20px; border-radius: 15px; border: 2px solid #ffcc00; display: flex; justify-content: space-between; align-items: center;">
            <h2 style="color:#ffcc00; font-family:Orbitron; margin:0;">{pol:.2f}</h2>
            <p style="color:white; margin:0; font-size:12px;">% POL</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 5. PAGE LOGIC ---
if st.session_state.page == 'dashboard':
    st.markdown("<h1 style='text-align:center; color:white; font-family:Orbitron;'>CANE METRIX 2.0</h1>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: 
        if st.button("📝 INPUT DATA"): st.session_state.page = 'pilih_stasiun'; st.rerun()
    with c4: 
        if st.button("📈 KURVA BRIX"): st.session_state.page = 'kurva_brix'; st.rerun()

elif st.session_state.page == 'input_gilingan':
    st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>🚜 INPUT STASIUN GILINGAN</h2>", unsafe_allow_html=True)
    
    jam_analisa = st.selectbox("Pilih Jam untuk Sync ke Spreadsheet:", [f"{i:02d}:00" for i in range(6, 24)] + ["00:00","01:00","02:00","03:00","04:00","05:00"])
    
    tabs = st.tabs(["NPP (G1)", "G2", "G3", "G4"])
    payload = {}

    for i, t in enumerate(["NPP", "G2", "G3", "G4"]):
        with tabs[i]:
            col_in, col_res = st.columns([1, 2])
            with col_in:
                bx_b = st.number_input(f"Brix Baca {t}", 0.0, 30.0, 10.0, key=f"bx_{t}")
                sh_b = st.number_input(f"Suhu {t}", 20.0, 45.0, 28.0, key=f"sh_{t}")
                pol_b = st.number_input(f"Pol Baca {t}", 0.0, 30.0, 5.0, key=f"pol_{t}")
                
                kor = hitung_interpolasi(sh_b, data_koreksi)
                bj = hitung_interpolasi(bx_b, data_bj)
                bx_fix = bx_b + kor
                pol_fix = (0.286 * pol_b) / bj if bj > 0 else 0
                
                payload[f"bx_{t}"] = bx_fix
                payload[f"pol_{t}"] = pol_fix
            with col_res:
                tampilkan_kartu_hasil(bx_fix, pol_fix, 0)

    if st.button("🚀 SYNC DATA KE SPREADSHEET", use_container_width=True):
        if simpan_ke_gsheet(jam_analisa, payload):
            st.success(f"Data Jam {jam_analisa} Berhasil Terkirim ke Spreadsheet!")
        else:
            st.error("Gagal Sync. Pastikan credentials.json benar.")

    if st.button("🔙 KEMBALI"): st.session_state.page = 'pilih_stasiun'; st.rerun()

elif st.session_state.page == 'kurva_brix':
    st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>📈 KURVA BRIX (DATA REALTIME SPREADSHEET)</h2>", unsafe_allow_html=True)
    
    # Tarik data rata-rata dari Spreadsheet
    nyata = tarik_data_kurva()
    
    c1, c2 = st.columns(2)
    imb = c1.number_input("Imbibisi % Tebu (I)", value=28.6)
    sabut = c2.number_input("Kadar Sabut (ft)", value=9.1)
    
    lamda = imb / sabut if sabut > 0 else 0
    teoritis = [nyata[0]]
    for gi in range(1, 4):
        bni = nyata[0] * (((lamda**(3-gi)) + 1 - gi) / (lamda**3)) if lamda > 0 else 0
        teoritis.append(round(bni, 2))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=["G1", "G2", "G3", "G4"], y=nyata, name='Real (Rata-rata GSheet)', line=dict(color='#ff4b4b', width=4), mode='lines+markers'))
    fig.add_trace(go.Scatter(x=["G1", "G2", "G3", "G4"], y=teoritis, name='Teoritis', line=dict(color='#26c4b9', width=4, dash='dash'), mode='lines+markers'))
    st.plotly_chart(fig, use_container_width=True)
    
    if st.button("🔙 KEMBALI"): st.session_state.page = 'dashboard'; st.rerun()

elif st.session_state.page == 'pilih_stasiun':
    if st.button("🚜 STASIUN GILINGAN", use_container_width=True): st.session_state.page = 'input_gilingan'; st.rerun()
    if st.button("🔙 KEMBALI"): st.session_state.page = 'dashboard'; st.rerun()
