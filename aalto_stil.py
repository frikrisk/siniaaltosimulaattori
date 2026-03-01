import streamlit as st
import numpy as np
import pandas as pd
import time

# 1. Sivun asetukset
st.set_page_config(page_title="Aalto-laboratorio", layout="wide")

if 'run_animation' not in st.session_state:
    st.session_state.run_animation = False

st.title("🌊 Siniaaltojen simulaattori (Optimoitu)")

# 2. Ohjauspaneeli
st.sidebar.header("⚙️ Ohjauspaneeli")
if st.sidebar.button('▶️ Käynnistä / ⏸️ Pysäytä'):
    st.session_state.run_animation = not st.session_state.run_animation

v1 = st.sidebar.slider("Aallonpituus 1", 0.1, 10.0, 1.95)
v2 = st.sidebar.slider("Aallonpituus 2", 0.1, 10.0, 2.82)

# 3. Mittaristot
col1, col2 = st.columns(2)
metric1 = col1.empty()
metric2 = col2.empty()

# 4. Paikka kuvaajalle
plot_spot = st.empty()

# Valmistellaan data (300 pistettä riittää sulavuuteen)
t = np.linspace(0, 2 * np.pi, 300)

if st.session_state.run_animation:
    frame = 0
    while st.session_state.run_animation:
        offset = frame * 0.1
        
        y1 = np.sin(v1 * (t + offset))
        y2 = np.sin(v2 * (t + offset))
        y_sum = y1 + y2
        
        # Luodaan DataFrame, jonka Streamlit osaa piirtää nopeasti
        df = pd.DataFrame({
            'Aalto 1': y1,
            'Aalto 2': y2,
            'Summa': y_sum
        }, index=t)
        
        # Päivitetään mittarit ja kuvaaja
        metric1.metric("Aalto 1", f"{v1:.2f} Hz")
        metric2.metric("Aalto 2", f"{v2:.2f} Hz")
        
        # st.line_chart on huomattavasti nopeampi kuin plt.pyplot()
        plot_spot.line_chart(df)
        
        frame += 1
        time.sleep(0.03) # Pienempi viive, koska line_chart on nopeampi
        
        # Streamlit tarvitsee pienen tauon säädinten tarkistamiseen
        if frame % 100 == 0:
             # Tämä auttaa sovellusta pysymään responsiivisena
             pass
else:
    plot_spot.info("Klikkaa 'Käynnistä' aloittaaksesi animaation.")
