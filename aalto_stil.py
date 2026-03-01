import streamlit as st
import numpy as np
import pandas as pd
import time

# 1. Sivun asetukset
st.set_page_config(page_title="Aalto-laboratorio", layout="wide")

# Alustetaan animaation tila
if 'run_animation' not in st.session_state:
    st.session_state.run_animation = False

st.title("🌊 Siniaaltojen simulaattori")

# 2. Ohjauspaneeli sivupalkissa
st.sidebar.header("⚙️ Ohjauspaneeli")

if st.sidebar.button('▶️ Käynnistä / ⏸️ Pysäytä'):
    st.session_state.run_animation = not st.session_state.run_animation

# Aaltojen säädöt - nämä muuttujat (color1, color2) täytyy olla olemassa alempana!
v1 = st.sidebar.slider("Aallonpituus 1", 0.1, 10.0, 1.95)
color1 = st.sidebar.selectbox("Väri 1", ['blue', 'green', 'cyan', 'teal'], index=0)

st.sidebar.divider()

v2 = st.sidebar.slider("Aallonpituus 2", 0.1, 10.0, 2.82)
color2 = st.sidebar.selectbox("Väri 2", ['red', 'magenta', 'orange', 'gold'], index=1)

speed = st.sidebar.slider("Päivitysviive (s)", 0.01, 0.20, 0.05)

# Paikka kuvaajalle
plot_spot = st.empty()
t = np.linspace(0, 2 * np.pi, 200)

# 3. Animaatio ja logiikka
if st.session_state.run_animation:
    frame = 0
    while st.session_state.run_animation:
        offset = frame * 0.1
        y1 = np.sin(v1 * (t + offset))
        y2 = np.sin(v2 * (t + offset))
        y_sum = y1 + y2
        
        # Luodaan data
        df = pd.DataFrame({'x': t, 'Aalto 1': y1, 'Aalto 2': y2, 'Summa': y_sum})
        df_melted = df.melt('x', var_name='Aalto', value_name='y')
        
        # Piirretään Vega-Lite (Streamlitin nopein tapa)
        plot_spot.vega_lite_chart(df_melted, {
            'mark': {'type': 'line', 'clip': True},
            'encoding': {
                'x': {'field': 'x', 'type': 'quantitative', 'scale': {'domain': [0, 6.28]}},
                'y': {'field': 'y', 'type': 'quantitative', 'scale': {'domain': [-2.5, 2.5]}},
                'color': {
                    'field': 'Aalto', 
                    'type': 'nominal',
                    'scale': {
                        'domain': ['Aalto 1', 'Aalto 2', 'Summa'],
                        'range': [color1, color2, 'black']
                    }
                },
                'strokeDash': {
                    'field': 'Aalto',
                    'type': 'nominal',
                    'scale': {
                        'domain': ['Aalto 1', 'Aalto 2', 'Summa'],
                        'range': [,,]
                    }
                }
            },
            'height': 450
        }, use_container_width=True)
        
        frame += 1
        time.sleep(speed)
else:
    plot_spot.info("Simulaattori on tauolla. Käynnistä animaatio sivupalkista.")
    # Staattinen kuvaaja tauon ajaksi
    y1_s = np.sin(v1 * t)
    y2_s = np.sin(v2 * t)
    df_s = pd.DataFrame({'x': t, 'Aalto 1': y1_s, 'Aalto 2': y2_s, 'Summa': y1_s + y2_s})
    plot_spot.line_chart(df_s.set_index('x'))
