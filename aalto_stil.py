import streamlit as st
import numpy as np
import pandas as pd
import time

# 1. Sivun asetukset
st.set_page_config(page_title="Aalto-laboratorio", layout="wide")

# Alustetaan tilamuisti animaatiolle
if 'run_animation' not in st.session_state:
    st.session_state.run_animation = False

# Otsikko
st.title("🌊 Siniaaltojen simulaattori")

# 2. Ohjauspaneeli sivupalkissa
st.sidebar.header("⚙️ Ohjauspaneeli")

# Käynnistysnappi
if st.sidebar.button('▶️ Käynnistä / ⏸️ Pysäytä'):
    st.session_state.run_animation = not st.session_state.run_animation

# Aallon 1 säädöt
v1 = st.sidebar.slider("Aallonpituus 1", 0.1, 10.0, 1.95)
color1 = st.sidebar.selectbox("Väri 1", ['blue', 'green', 'cyan', 'teal'], index=0)

st.sidebar.divider()

# Aallon 2 säädöt
v2 = st.sidebar.slider("Aallonpituus 2", 0.1, 10.0, 2.82)
color2 = st.sidebar.selectbox("Väri 2", ['red', 'magenta', 'orange', 'gold'], index=0)

# Nopeuden hienosäätö (0.05 on hyvä perusarvo pilvessä)
speed = st.sidebar.slider("Päivitysviive (s)", 0.01, 0.20, 0.05)

# 3. Paikka kuvaajalle (tämä estää välkkymisen)
plot_spot = st.empty()

# Valmistellaan x-akselin pisteet (200 pistettä on optimaalinen nopeudelle)
t = np.linspace(0, 2 * np.pi, 200)

# 4. Animaatio-looppi
# 4. Animaatio-looppi
if st.session_state.run_animation:
    frame = 0
    while st.session_state.run_animation:
        offset = frame * 0.1
        
        # Lasketaan aallot
        y1 = np.sin(v1 * (t + offset))
        y2 = np.sin(v2 * (t + offset))
        y_sum = y1 + y2
        
        # Luodaan DataFrame ja muokataan se värejä varten
        df = pd.DataFrame({'x': t, 'Aalto 1': y1, 'Aalto 2': y2, 'Summa': y_sum})
        df_melted = df.melt('x', var_name='Aalto', value_name='y')
        
        # Piirretään Vega-Lite -kaavio
        plot_spot.vega_lite_chart(df_melted, {
            'mark': {'type': 'line', 'clip': True},
            'encoding': {
                'x': {'field': 'x', 'type': 'quantitative', 'scale': {'domain': [0, 6.28]}, 'title': 'Aika'},
                'y': {'field': 'y', 'type': 'quantitative', 'scale': {'domain': [-2.5, 2.5]}, 'title': 'Amplitudi'},
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
            'height': 450,
            'config': {'view': {'stroke': 'transparent'}}
        }, use_container_width=True)
        
        frame += 1
        time.sleep(speed)
else:
    # Viesti kun animaatio on pysäytetty
    plot_spot.info("Simulaattori on tauolla. Napsauta 'Käynnistä' sivupalkista nähdäksesi aallot liikkeessä.")
    
    # Piirretään staattinen kuva tauon ajaksi
    y1_static = np.sin(v1 * t)
    y2_static = np.sin(v2 * t)
    df_static = pd.DataFrame({'x': t, 'Aalto 1': y1_static, 'Aalto 2': y2_static, 'Summa': y1_static + y2_static})
    st.line_chart(df_static.set_index('x'))
