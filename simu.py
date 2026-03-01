import streamlit as st
import numpy as np
import pandas as pd
import time

st.set_page_config(page_title="Aalto-simulaattori", layout="wide")

if 'run' not in st.session_state:
    st.session_state.run = False

st.title("🌊 Aalto-laboratorio")

if st.sidebar.button('▶️ Käynnistä / ⏸️ Pysäytä'):
    st.session_state.run = not st.session_state.run

v1 = st.sidebar.slider("Taajuus 1", 0.1, 10.0, 2.0)
v2 = st.sidebar.slider("Taajuus 2", 0.1, 10.0, 3.0)

t = np.linspace(0, 2 * np.pi, 200)
placeholder = st.empty()

if st.session_state.run:
    f = 0
    while st.session_state.run:
        off = f * 0.1
        y1, y2 = np.sin(v1*(t+off)), np.sin(v2*(t+off))
        df = pd.DataFrame({'x': t, 'A1': y1, 'A2': y2, 'Sum': y1+y2})
        # Käytetään Streamlitin omaa nopeaa kaaviota ilman värisäätöjä virheen välttämiseksi
        placeholder.line_chart(df.set_index('x'))
        f += 1
        time.sleep(0.05)
else:
    placeholder.info("Paina Käynnistä")
