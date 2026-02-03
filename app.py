# --- UPDATE DI BAGIAN CSS ---
st.markdown(f"""
    <style>
    /* ... (style lainnya tetep sama) ... */

    .partner-box {{ 
        background: white; 
        padding: 15px 30px !important;
        border-radius: 15px; 
        display: flex !important; 
        flex-direction: row !important;
        align-items: center !important; 
        justify-content: center !important;
        gap: 30px !important; 
        
        /* INI KUNCINYA: Kita paksa lebar minimalnya jauh lebih panjang */
        min-width: 600px !important; 
        width: auto !important;
        overflow: visible !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.5);
    }}
    
    .partner-box img {{ 
        height: 40px !important; /* Kita gedein dikit logonya */
        width: auto !important;
        flex-shrink: 0 !important; /* Biar logo gak kegencet */
        object-fit: contain !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- UPDATE DI BAGIAN RENDER_HEADER ---
@st.fragment
def render_header():
    # Gue ubah rasionya jadi [4, 1] biar kolom logo dapet jatah lebih luas
    h1, h2 = st.columns([4, 1]) 
    with h1:
        # Gunakan file lokal jika ada, jika tidak gunakan URL backup
        src_kb = f"data:image/png;base64,{l_kb}" if l_kb else url_bumn_backup
        
        html_logos = f'''
        <div class="partner-box">
            <img src="{src_kb}" style="margin-right: 10px;">
            <img src="data:image/png;base64,{l_sgn if l_sgn else ''}">
            <img src="data:image/png;base64,{l_ptpn if l_ptpn else ''}">
            <img src="data:image/png;base64,{l_lpp if l_lpp else ''}">
        </div>
        '''
        st.markdown(html_logos, unsafe_allow_html=True)
    
    # ... (sisanya sama) ...
