import streamlit as st
import datetime
import pytz
import base64
import os
import gspread
from google.oauth2.service_account import Credentials

# --- 1. CONFIG & STATE ---
st.set_page_config(page_title="CaneMetrix 2.0", layout="wide")# --- Tambahkan fungsi helper ini di bagian atas (setelah fungsi hitung_interpolasi) ---
def tampilkan_kartu_hasil(brix, pol, hk):
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="card-result"><h1 style="color:#26c4b9; font-family:Orbitron; margin:0; font-size:35px;">{brix:.3f}</h1><p style="color:white; font-size:12px;">% BRIX AKHIR</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="card-result" style="border-color:#ffcc00;"><h1 style="color:#ffcc00; font-family:Orbitron; margin:0; font-size:35px;">{pol:.3f}</h1><p style="color:white; font-size:12px;">% POL AKHIR</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="card-result" style="border-color:#ff4b4b;"><h1 style="color:#ff4b4b; font-family:Orbitron; margin:0; font-size:35px;">{hk:.2f}</h1><p style="color:white; font-size:12px;">HK</p></div>', unsafe_allow_html=True)

# --- REVISI BAGIAN HALAMAN INPUT GILINGAN ---
elif st.session_state.page == 'input_gilingan':
    st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>🚜 INPUT DATA STASIUN GILINGAN</h2>", unsafe_allow_html=True)
    
    tabs = st.tabs([
        "NPP (Gilingan 1)", "Gilingan 2", "Gilingan 3", "Gilingan 4", 
        "Nira Mentah", "Ampas", "Imbibisi", "Putaran & Tekanan"
    ])

    def render_analisa_nira(label_nira, show_tsas=False):
        list_sub = ["Brix, Pol, HK", "Gula Reduksi", "Kadar Posfat", "Dextran", "Icumsa"]
        if show_tsas: list_sub.append("TSAS")
        
        sub = st.selectbox(f"Pilih Analisa {label_nira}", list_sub, key=f"sub_{label_nira}")
        
        st.markdown('<div class="hero-container" style="display:block; padding: 20px;">', unsafe_allow_html=True)
        
        if sub == "Brix, Pol, HK":
            col_in, col_res = st.columns([1, 2])
            with col_in:
                bx_baca = st.number_input("Brix Teramati", value=0.0, key=f"bx_{label_nira}")
                sh_in = st.number_input("Suhu (°C)", value=28.0, key=f"sh_{label_nira}")
                pol_baca = st.number_input("Pol Baca", value=0.0, key=f"pol_{label_nira}")
                
                kor = hitung_interpolasi(sh_in, data_koreksi)
                bj = hitung_interpolasi(bx_baca, data_bj)
                bx_fix = (bx_baca + kor) if bx_baca > 0 else 0
                pol_fix = (0.286 * pol_baca) / bj if bj > 0 else 0
                hk_fix = (pol_fix / bx_fix * 100) if bx_fix > 0 else 0
                
                st.info(f"Koreksi: {kor:+.3f} | BJ: {bj:.4f}")
            
            with col_res:
                tampilkan_kartu_hasil(bx_fix, pol_fix, hk_fix)
                if st.button("🚀 SIMPAN EXCEL", key=f"save_{label_nira}"):
                    st.toast(f"Data {label_nira} tersimpan!")

        elif sub == "Gula Reduksi":
            c1, c2 = st.columns(2)
            v_blanko = c1.number_input("Volume Blanko (ml)", value=0.0, key=f"vb_{label_nira}")
            v_penitran = c2.number_input("Volume Penitran (ml)", value=0.0, key=f"vp_{label_nira}")
            gr = (v_blanko - v_penitran) * 0.1 * 63.57
            st.metric("Gula Reduksi", f"{gr:.2f}")

        elif sub == "Kadar Posfat":
            p2o5 = st.number_input("P2O5 (ppm)", value=0.0, key=f"p2_{label_nira}")
            st.write(f"Hasil Analisa Posfat: {p2o5} ppm")

        elif sub == "Dextran":
            dex = st.number_input("Dextran (ppm)", value=0.0, key=f"dx_{label_nira}")
            st.write(f"Hasil Analisa Dextran: {dex} ppm")

        elif sub == "Icumsa":
            st.caption("Analisa Warna Icumsa")
            abs_ic = st.number_input("Absorbansi", value=0.0, key=f"ic_{label_nira}")
            st.info("Rumus Icumsa Nira sedang disinkronkan...")
            
        elif sub == "TSAS" and show_tsas:
            tsas_val = st.number_input("Total Soluble Amino Sulphate", value=0.0, key=f"ts_{label_nira}")
            st.write(f"Hasil TSAS: {tsas_val}")

        st.markdown('</div>', unsafe_allow_html=True)

    # Implementasi ke Tabs
    with tabs[0]: render_analisa_nira("NPP")
    with tabs[1]: render_analisa_nira("Gilingan 2")
    with tabs[2]: render_analisa_nira("Gilingan 3")
    with tabs[3]: render_analisa_nira("Gilingan 4")
    with tabs[4]: render_analisa_nira("Nira Mentah", show_tsas=True)

    # Tab sisanya tetap dipertahankan
    with tabs[5]: st.info("Input Ampas")
    with tabs[6]: st.info("Input Imbibisi")
    with tabs[7]: st.info("Input Putaran Roll & Tekanan Hidraulik")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI KE PILIH STASIUN", use_container_width=True):
        st.session_state.page = 'pilih_stasiun'; st.rerun()
# FUNGSI KONEKSI EXCEL
def init_connection():
    try:
        s = st.secrets["gcp_service_account"]
        pk = s["private_key"].replace("\\n", "\n")
        info = {
            "type": s["type"], "project_id": s["project_id"],
            "private_key_id": s["private_key_id"], "private_key": pk,
            "client_email": s["client_email"], "client_id": s["client_id"],
            "auth_uri": s["auth_uri"], "token_uri": s["token_uri"],
            "auth_provider_x509_cert_url": s["auth_provider_x509_cert_url"],
            "client_x509_cert_url": s["client_x509_cert_url"]
        }
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(info, scopes=scopes)
        return gspread.authorize(creds)
    except Exception as e:
        return None

if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'
if 'analisa_type' not in st.session_state:
    st.session_state.analisa_type = None

# --- 2. FUNGSI LOGO & ASSETS ---
def get_base64_logo(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo_ptpn = get_base64_logo("ptpn.png"); logo_sgn = get_base64_logo("sgn.png")
logo_lpp = get_base64_logo("lpp.png"); logo_kb = get_base64_logo("kb.png")
logo_cane = get_base64_logo("canemetrix.png")

# --- 3. DATABASE TABEL & HELPER ---
data_koreksi = {27: -0.05, 28: 0.02, 29: 0.09, 30: 0.16, 31: 0.24, 32: 0.315, 33: 0.385, 34: 0.465, 35: 0.54, 36: 0.62, 37: 0.70, 38: 0.78, 39: 0.86, 40: 0.94}
data_bj = {0.0: 0.99640, 5.0: 1.01592, 10.0: 1.03608, 15.0: 1.05691, 20.0: 1.07844, 25.0: 1.10069, 30.0: 1.12368, 35.0: 1.14745, 40.0: 1.17203, 45.0: 1.19746, 49.0: 1.21839, 49.4: 1.22051, 49.5: 1.22104, 50.0: 1.22372, 55.0: 1.25083, 60.0: 1.27885, 65.0: 1.30781, 70.0: 1.33775}
data_tsai = {15.0: 336.00, 16.0: 316.00, 17.0: 298.00, 18.0: 282.00, 19.0: 267.00, 20.0: 254.50, 21.0: 242.90, 22.0: 231.80, 22.5: 223.60, 23.0: 222.20, 24.0: 213.30, 25.0: 204.80, 26.0: 197.40, 27.0: 190.40, 28.0: 183.70, 29.0: 177.60, 30.0: 171.70, 31.0: 166.30, 32.0: 161.20, 33.0: 156.60, 34.0: 152.20, 35.0: 147.90, 36.0: 143.90, 37.0: 140.20, 37.7: 136.67}

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

# --- 4. CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@300;400;700&display=swap');
    .stApp {{ background: linear-gradient(rgba(0, 10, 30, 0.85), rgba(0, 10, 30, 0.85)), url("https://images.pexels.com/photos/2280571/pexels-photo-2280571.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"); background-size: cover; background-position: center; background-attachment: fixed; }}
    .header-logo-box {{ background: white; padding: 10px 20px; border-radius: 15px; display: inline-flex; align-items: center; gap: 15px; margin-bottom: 20px; }}
    .header-logo-box img {{ height: 35px; width: auto; }}
    .hero-container {{ background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 30px; padding: 40px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center; }}
    div.stButton > button {{ background: rgba(255, 255, 255, 0.07) !important; backdrop-filter: blur(10px) !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 20px !important; color: white !important; height: 180px !important; width: 100% !important; transition: 0.3s !important; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
    div.stButton > button:hover {{ background: rgba(38, 196, 185, 0.2) !important; border-color: #26c4b9 !important; box-shadow: 0 0 25px rgba(38, 196, 185, 0.4) !important; transform: translateY(-8px) !important; }}
    .card-result {{ background: rgba(38, 196, 185, 0.1); padding: 25px; border-radius: 20px; border: 2px solid #26c4b9; text-align: center; margin-bottom: 15px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. JAM REALTIME ---
@st.fragment(run_every="1s")
def jam_realtime():
    tz = pytz.timezone('Asia/Jakarta')
    now = datetime.datetime.now(tz)
    st.markdown(f'''<div style="text-align: right; color: white; font-family: 'Poppins';">{now.strftime("%d %B %Y")}<br><span style="font-family:'Orbitron'; color:#26c4b9; font-size:24px; font-weight:bold;">{now.strftime("%H:%M:%S")} WIB</span></div>''', unsafe_allow_html=True)

# --- 6. LOGIKA HALAMAN ---

# === DASHBOARD ===
if st.session_state.page == 'dashboard':
    col_h1, col_h2 = st.columns([2, 1])
    with col_h1:
        st.markdown(f'''<div class="header-logo-box"><img src="data:image/png;base64,{logo_ptpn}"><img src="data:image/png;base64,{logo_sgn}"><img src="data:image/png;base64,{logo_lpp}"><img src="data:image/png;base64,{logo_kb}"></div>''', unsafe_allow_html=True)
    with col_h2: jam_realtime()
    st.markdown(f'''<div class="hero-container"><div><h1 style="font-family:Orbitron; color:white; font-size:55px; margin:0; line-height:1.1;">CANE METRIX</h1><p style="color:#26c4b9; font-family:Poppins; font-weight:700; letter-spacing:5px; margin-top:10px;">ACCELERATING QA PERFORMANCE</p></div><img src="data:image/png;base64,{logo_cane}" style="height:150px; filter: drop-shadow(0 0 10px #26c4b9);"></div>''', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>📝</h1></div>", unsafe_allow_html=True)
        # BUTTON INPUT DATA SEKARANG AKTIF KE PILIH STASIUN
        if st.button("INPUT DATA", key="dash_input", use_container_width=True): 
            st.session_state.page = 'pilih_stasiun'; st.rerun()
    with c2:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>🧮</h1></div>", unsafe_allow_html=True)
        # BUTTON HITUNG ANALISA TETAP AMAN
        if st.button("HITUNG ANALISA", key="dash_hitung", use_container_width=True):
            st.session_state.page = 'pilih_analisa'; st.rerun()
    with c3:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>📅</h1></div>", unsafe_allow_html=True)
        if st.button("DATABASE HARIAN", key="dash_db", use_container_width=True): st.toast("Segera Hadir")

# === HALAMAN PILIH STASIUN (MENU BARU) ===
elif st.session_state.page == 'pilih_stasiun':
    st.markdown("<h2 style='text-align:center; color:white; font-family:Orbitron;'>PILIH STASIUN</h2>", unsafe_allow_html=True)
    
    # Baris 1
    r1c1, r1c2, r1c3 = st.columns(3)
    with r1c1:
        if st.button("🚜 STASIUN GILINGAN", use_container_width=True):
            st.session_state.page = 'input_gilingan'; st.rerun()
    with r1c2:
        if st.button("🌫️ STASIUN PEMURNIAN", use_container_width=True): st.toast("Segera Hadir")
    with r1c3:
        if st.button("🔥 STASIUN PENGUAPAN", use_container_width=True): st.toast("Segera Hadir")
    
    # Baris 2
    r2c1, r2c2, r2c3 = st.columns(3)
    with r2c1:
        if st.button("🥘 STASIUN MASAKAN", use_container_width=True): st.toast("Segera Hadir")
    with r2c2:
        if st.button("🔄 STASIUN PUTARAN", use_container_width=True): st.toast("Segera Hadir")
    with r2c3:
        if st.button("📦 PENGEMASAN", use_container_width=True): st.toast("Segera Hadir")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI KE DASHBOARD", use_container_width=True):
        st.session_state.page = 'dashboard'; st.rerun()

# === HALAMAN INPUT GILINGAN (MENU BARU DETAILED) ===
elif st.session_state.page == 'input_gilingan':
    st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>🚜 INPUT DATA STASIUN GILINGAN</h2>", unsafe_allow_html=True)
    
    # Tab Menu Sesuai Gambar 2
    tabs = st.tabs([
        "NPP (Gilingan 1)", "Gilingan 2", "Gilingan 3", "Gilingan 4", 
        "Nira Mentah", "Ampas", "Imbibisi", "Putaran & Tekanan"
    ])
    
    # TAB 1: NIRA PERAHAN PERTAMA (NPP)
    with tabs[0]:
        st.markdown('<div class="hero-container" style="display:block;">', unsafe_allow_html=True)
        st.subheader("Analisa Nira Gilingan I (NPP)")
        c_npp1, c_npp2 = st.columns(2)
        
        with c_npp1:
            st.caption("Data Umum & Fisik")
            bx_npp = st.number_input("Brix Baca", value=0.0)
            sh_npp = st.number_input("Suhu (°C)", value=28.0)
            pol_npp_baca = st.number_input("Pol Baca", value=0.0)
            
            # Hitung Otomatis Brix Pol (Sama kayak Tetes logic)
            kor_npp = hitung_interpolasi(sh_npp, data_koreksi)
            bj_npp = hitung_interpolasi(bx_npp, data_bj)
            
            bx_npp_fix = (bx_npp + kor_npp) if bx_npp > 0 else 0
            pol_npp_fix = (0.286 * pol_npp_baca) / bj_npp if bj_npp > 0 else 0
            hk_npp = (pol_npp_fix / bx_npp_fix * 100) if bx_npp_fix > 0 else 0
            
            st.markdown(f"**Hasil:** Brix: `{bx_npp_fix:.2f}` | Pol: `{pol_npp_fix:.2f}` | HK: `{hk_npp:.2f}`")

        with c_npp2:
            st.caption("Analisa Kimia Lanjutan")
            p2o5_npp = st.number_input("P2O5 (ppm)", value=0.0)
            dextran_npp = st.number_input("Dextran (ppm)", value=0.0)
            icumsa_npp = st.number_input("Icumsa (IU)", value=0.0) # Rumus menyusul
            
            st.markdown("---")
            st.caption("Gula Reduksi")
            v_blanko = st.number_input("Volume Blanko (ml)", value=0.0)
            v_penitran = st.number_input("Volume Penitran (ml)", value=0.0)
            
            # Rumus Gula Reduksi
            gula_reduksi = (v_blanko - v_penitran) * 0.1 * 63.57
            st.info(f"🍭 Gula Reduksi: {gula_reduksi:.2f}")

    # TAB 2: GILINGAN 2 (Bisa dicopas logicnya nanti)
    with tabs[1]:
        st.info("Input Nira Gilingan 2 - Coming Soon")
    
    # TAB 5: NIRA MENTAH
    with tabs[4]:
        st.subheader("Analisa Nira Mentah (NM)")
        st.info("Menu Input Nira Mentah (Logic sama dengan NPP + Analisa Kapur dll) - Coming Soon")

    # TAB LAINNYA
    with tabs[5]: st.info("Input Ampas")
    with tabs[6]: st.info("Input Imbibisi")
    with tabs[7]: st.info("Input Putaran Roll & Tekanan Hidraulik")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI KE PILIH STASIUN", use_container_width=True):
        st.session_state.page = 'pilih_stasiun'; st.rerun()

# === HALAMAN PILIH ANALISA (TETAP ADA) ===
elif st.session_state.page == 'pilih_analisa':
    st.markdown("<h2 style='text-align:center; color:white; font-family:Orbitron;'>PILIH JENIS ANALISA</h2>", unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    with m1:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>🧪</h1></div>", unsafe_allow_html=True)
        if st.button("ANALISA TETES", key="sel_tetes", use_container_width=True):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'tetes'; st.rerun()
    with m2:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>🔬</h1></div>", unsafe_allow_html=True)
        if st.button("OD TETES", key="sel_od", use_container_width=True):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'od'; st.rerun()
    m3, m4 = st.columns(2)
    with m3:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>⚗️</h1></div>", unsafe_allow_html=True)
        if st.button("ANALISA TSAI TETES", key="sel_tsai", use_container_width=True):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'tsai'; st.rerun()
    with m4:
        st.markdown("<div style='text-align:center; margin-bottom:-55px; position:relative; z-index:10; pointer-events:none;'><h1>💎</h1></div>", unsafe_allow_html=True)
        if st.button("ANALISA ICUMSA GULA", key="sel_icumsa", use_container_width=True):
            st.session_state.page = 'analisa_lab'; st.session_state.analisa_type = 'icumsa'; st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI KE DASHBOARD", key="back_dash", use_container_width=True):
        st.session_state.page = 'dashboard'; st.rerun()

# === HALAMAN ANALISA LAB (TETAP ADA & JALAN) ===
elif st.session_state.page == 'analisa_lab':
    list_jam = [f"{(i % 24):02d}:00" for i in range(6, 30)]

    # --- ANALISA TETES ---
    if st.session_state.analisa_type == 'tetes':
        st.markdown("<h2 style='text-align:center; color:#26c4b9; font-family:Orbitron;'>🧪 ANALISA TETES</h2>", unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="hero-container" style="display:block;">', unsafe_allow_html=True)
            cx, cy = st.columns(2)
            with cx:
                bx_in = st.number_input("Brix Teramati", value=8.80, format="%.2f")
                sh_in = st.number_input("Suhu (°C)", value=28.0, format="%.1f")
                pol_baca = st.number_input("Pol Baca", value=11.00, format="%.2f")
                analisa_jam = st.selectbox("Analisa Jam", options=list_jam)
                
                kor = hitung_interpolasi(sh_in, data_koreksi); bj = hitung_interpolasi(bx_in, data_bj)
                brix_akhir = (bx_in + kor) * 10; pol_akhir = (0.286 * pol_baca) / bj * 10
                hk = (pol_akhir / brix_akhir * 100) if brix_akhir != 0 else 0
                st.info(f"💡 Koreksi: {kor:+.3f} | BJ: {bj:.6f}")
                
                if st.button("🚀 SIMPAN KE EXCEL", key="btn_tetes", use_container_width=True):
                    client = init_connection()
                    if client:
                        try:
                            sh = client.open("KKKB_250711")
                            worksheet = sh.worksheet("INPUT")
                            tanggal = datetime.datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%Y-%m-%d")
                            worksheet.append_row([tanggal, analisa_jam, "Tetes", brix_akhir, pol_akhir, hk])
                            st.success(f"Data jam {analisa_jam} Berhasil Disimpan! ✅")
                        except Exception as e: st.error(f"Gagal Simpan: {e}")
                    else: st.error("Koneksi ke Google Service Gagal.")
            with cy:
                st.markdown(f'<div class="card-result"><h1 style="color:#26c4b9; font-family:Orbitron; margin:0;">{brix_akhir:.3f}</h1><p style="color:white;">% BRIX AKHIR</p></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="card-result" style="border-color:#ffcc00;"><h1 style="color:#ffcc00; font-family:Orbitron; margin:0;">{pol_akhir:.3f}</h1><p style="color:white;">% POL AKHIR</p></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="card-result" style="border-color:#ff4b4b;"><h1 style="color:#ff4b4b; font-family:Orbitron; margin:0;">{hk:.2f}</h1><p style="color:white;">HK</p></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # --- OD TETES ---
    elif st.session_state.analisa_type == 'od':
        st.markdown("<h2 style='text-align:center; color:#ff4b4b; font-family:Orbitron;'>🔬 OPTICAL DENSITY TETES</h2>", unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="hero-container" style="display:block;">', unsafe_allow_html=True)
            cx, cy = st.columns(2)
            with cx:
                bx_od = st.number_input("Brix Teramati (cari BJ)", value=8.80, format="%.2f")
                abs_val = st.number_input("Nilai Absorbansi (Abs)", value=0.418, format="%.3f")
                analisa_jam = st.selectbox("Analisa Jam", options=list_jam)
                bj_od = hitung_interpolasi(bx_od, data_bj); od_res = (abs_val * bj_od * 500) / 1
                st.info(f"🔍 BJ d27,5: {bj_od:.6f}")
                
                if st.button("🚀 SIMPAN KE EXCEL", key="btn_od", use_container_width=True):
                    client = init_connection()
                    if client:
                        try:
                            sh = client.open("KKKB_250711"); worksheet = sh.worksheet("INPUT")
                            tanggal = datetime.datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%Y-%m-%d")
                            worksheet.append_row([tanggal, analisa_jam, "OD Tetes", bx_od, abs_val, od_res])
                            st.success(f"Data OD jam {analisa_jam} Berhasil Disimpan! ✅")
                        except Exception as e: st.error(f"Gagal: {e}")
            with cy:
                st.markdown(f'<div class="card-result" style="border-color:#ff4b4b; background:rgba(255,75,75,0.1); padding:50px;"><h1 style="color:#ff4b4b; font-size:60px; font-family:Orbitron; margin:0;">{od_res:.3f}</h1><p style="color:white;">OD TETES</p></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # --- ANALISA TSAI TETES ---
    elif st.session_state.analisa_type == 'tsai':
        st.markdown("<h2 style='text-align:center; color:#ffcc00; font-family:Orbitron;'>⚗️ ANALISA TSAI TETES</h2>", unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="hero-container" style="display:block;">', unsafe_allow_html=True)
            cx, cy = st.columns(2)
            with cx:
                vol_titran = st.number_input("Volume Titran (ml)", value=22.5, format="%.1f")
                f_fehling = st.number_input("Faktor Fehling", value=0.979, format="%.3f")
                analisa_jam = st.selectbox("Analisa Jam", options=list_jam)
                hasil_kali = vol_titran * f_fehling
                konversi_tabel = hitung_interpolasi(hasil_kali, data_tsai); tsai_final = konversi_tabel / 4
                st.warning(f"Hasil Titran x Faktor: {hasil_kali:.3f}"); st.info(f"Koreksi Tabel: {konversi_tabel:.2f}")

                if st.button("🚀 SIMPAN KE EXCEL", key="btn_tsai", use_container_width=True):
                    client = init_connection()
                    if client:
                        try:
                            sh = client.open("KKKB_250711"); worksheet = sh.worksheet("INPUT")
                            tanggal = datetime.datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%Y-%m-%d")
                            worksheet.append_row([tanggal, analisa_jam, "TSAI", vol_titran, f_fehling, tsai_final])
                            st.success(f"Data TSAI jam {analisa_jam} Berhasil Disimpan! ✅")
                        except Exception as e: st.error(f"Gagal: {e}")
            with cy:
                st.markdown(f'<div class="card-result" style="border-color:#ffcc00; background:rgba(255,204,0,0.1); padding:50px;"><h1 style="color:#ffcc00; font-size:60px; font-family:Orbitron; margin:0;">{tsai_final:.3f}</h1><p style="color:white;">% TSAI TETES</p></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # --- ANALISA ICUMSA GULA ---
    elif st.session_state.analisa_type == 'icumsa':
        st.markdown("<h2 style='text-align:center; color:#00d4ff; font-family:Orbitron;'>💎 ANALISA ICUMSA GULA</h2>", unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="hero-container" style="display:block;">', unsafe_allow_html=True)
            cx, cy = st.columns(2)
            with cx:
                abs_icumsa = st.number_input("Absorbansi (Abs)", value=0.149, format="%.3f")
                brix_icumsa = st.number_input("% Brix Gula", value=49.44, format="%.2f")
                analisa_jam = st.selectbox("Analisa Jam", options=list_jam)
                bj_icumsa = hitung_interpolasi(brix_icumsa, data_bj)
                icumsa_res = (abs_icumsa * 100000) / (brix_icumsa * 1 * bj_icumsa) if brix_icumsa > 0 else 0
                st.info(f"🔍 BJ Terdeteksi: {bj_icumsa:.5f}")

                if st.button("🚀 SIMPAN KE EXCEL", key="btn_icumsa", use_container_width=True):
                    client = init_connection()
                    if client:
                        try:
                            sh = client.open("KKKB_250711"); worksheet = sh.worksheet("INPUT")
                            tanggal = datetime.datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%Y-%m-%d")
                            worksheet.append_row([tanggal, analisa_jam, "Icumsa", brix_icumsa, abs_icumsa, icumsa_res])
                            st.success(f"Data Icumsa jam {analisa_jam} Berhasil Disimpan! ✅")
                        except Exception as e: st.error(f"Gagal: {e}")
            with cy:
                st.markdown(f'<div class="card-result" style="border-color:#00d4ff; background:rgba(0,212,255,0.1); padding:50px;"><h1 style="color:#00d4ff; font-size:60px; font-family:Orbitron; margin:0;">{icumsa_res:.2f}</h1><p style="color:white; margin:0;">IU (ICUMSA UNIT)</p></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔙 KEMBALI KE MENU PILIHAN", key="back_sub", use_container_width=True):
        st.session_state.page = 'pilih_analisa'; st.rerun()
