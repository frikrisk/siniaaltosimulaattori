import streamlit as st
import numpy as np
import pandas as pd
import time

# 1. Sivun asetukset
st.set_page_config(page_title="Aalto-laboratorio", layout="wide")

if 'run' not in st.session_state:
    st.session_state.run = False

st.title("🌊 Aalto-laboratorio")

# 2. Värien määrittely sanakirjana
vari_vaihtoehdot = {
    "Sininen": "#0000FF",
    "Vihreä": "#00FF00",
    "Turkoosi": "#008080",
    "Punainen": "#FF0000",
    "Violetti": "#FF00FF",
    "Oranssi": "#FFA500"
}

# 3. Ohjauspaneeli sivupalkissa
if st.sidebar.button('▶️ Käynnistä / ⏸️ Pysäytä'):
    st.session_state.run = not st.session_state.run

v1 = st.sidebar.slider("Taajuus 1", 0.1, 10.0, 1.95)
c1_nimi = st.sidebar.selectbox("Aallon 1 väri", list(vari_vaihtoehdot.keys()), index=0)
c1 = vari_vaihtoehdot[c1_nimi]

st.sidebar.divider()

v2 = st.sidebar.slider("Taajuus 2", 0.1, 10.0, 2.82)
c2_nimi = st.sidebar.selectbox("Aallon 2 väri", list(vari_vaihtoehdot.keys()), index=3) # Oletuksena punainen
c2 = vari_vaihtoehdot[c2_nimi]

speed = st.sidebar.slider("Päivitysviive (s)", 0.01, 0.20, 0.05)

# 4. Paikanvaraus elementeille
col1, col2 = st.columns(2)
m1 = col1.empty()
m2 = col2.empty()
placeholder = st.empty()

t = np.linspace(0, 2 * np.pi, 200)

# 5. Animaatio ja logiikka
if st.session_state.run:
    f = 0
    while st.session_state.run:
        off = f * 0.1
        y1 = np.sin(v1 * (t + off))
        y2 = np.sin(v2 * (t + off))
        y_sum = y1 + y2
        
        m1.metric("Aalto 1", f"{v1:.2f} Hz")
        m2.metric("Aalto 2", f"{v2:.2f} Hz")
        
        df = pd.DataFrame({
            'Aalto 1': y1, 
            'Aalto 2': y2, 
            'Summa': y_sum
        }, index=t)
        
        placeholder.line_chart(df, color=[c1, c2, "#000000"])
        
        f += 1
        time.sleep(speed)
else:
    # Staattinen näkymä tauolla (käyttää samoja värejä)
    m1.metric("Aalto 1", f"{v1:.2f} Hz")
    m2.metric("Aalto 2", f"{v2:.2f} Hz")
    
    y1_s = np.sin(v1 * t)
    y2_s = np.sin(v2 * t)
    y_sum_s = y1_s + y2_s
    
    df_s = pd.DataFrame({
        'Aalto 1': y1_s, 
        'Aalto 2': y2_s, 
        'Summa': y_sum_s
    }, index=t)
    
    placeholder.line_chart(df_s, color=[c1, c2, "#000000"])
    st.info("Simulaattori on tauolla. Säädä taajuuksia ja värejä tai käynnistä animaatio.")
