import streamlit as st
import numpy as np
import pandas as pd
import time

# Sivun perusasetukset
st.set_page_config(page_title="Aalto-laboratorio", layout="wide")

if 'run' not in st.session_state:
    st.session_state.run = False

st.title("🌊 Aalto-laboratorio")

# 1. Ohjauspaneeli
st.sidebar.header("⚙️ Ohjauspaneeli")

if st.sidebar.button('▶️ Käynnistä / ⏸️ Pysäytä'):
    st.session_state.run = not st.session_state.run

v1 = st.sidebar.slider("Taajuus 1", 0.1, 10.0, 1.95)
c1 = st.sidebar.selectbox("Väri 1", ['blue', 'green', 'teal', 'cyan'], index=0)
st.sidebar.divider()
v2 = st.sidebar.slider("Taajuus 2", 0.1, 10.0, 2.82)
c2 = st.sidebar.selectbox("Väri 2", ['red', 'magenta', 'orange', 'gold'], index=0)
speed = st.sidebar.slider("Päivitysviive (s)", 0.01, 0.20, 0.07)

# 2. Luodaan paikat, jotka pysyvät vakioina
m1, m2 = st.columns(2)
metric1 = m1.empty()
metric2 = m2.empty()
chart_spot = st.empty()

t = np.linspace(0, 2 * np.pi, 200)

# 3. Päivitysfunktio (estää koodin toiston)
def draw_plot(offset_val):
    y1 = np.sin(v1 * (t + offset_val))
    y2 = np.sin(v2 * (t + offset_val))
    y_sum = y1 + y2
    
    df = pd.DataFrame({'x': t, 'Aalto 1': y1, 'Aalto 2': y2, 'Summa': y_sum})
    df_m = df.melt('x', var_name='Aalto', value_name='y')
    
    chart_spot.vega_lite_chart(df_m, {
        'width': 'container',
        'height': 450,
        'mark': {'type': 'line', 'clip': True},
        'encoding': {
            'x': {'field': 'x', 'type': 'quantitative', 'scale': {'domain': [0, 6.28]}},
            'y': {'field': 'y', 'type': 'quantitative', 'scale': {'domain': [-2.5, 2.5]}},
            'color': {
                'field': 'Aalto', 
                'type': 'nominal',
                'scale': {'domain': ['Aalto 1', 'Aalto 2', 'Summa'], 'range': [c1, c2, 'black']}
            },
            'strokeDash': {
                'field': 'Aalto',
                'type': 'nominal',
                'scale': {'domain': ['Aalto 1', 'Aalto 2', 'Summa'], 'range': [[0,0], [0,0], [5,5]]}
            }
        },
        'config': {'autosize': {'type': 'none'}} # TÄMÄ estää hyppimisen
    }, use_container_width=True)

# 4. Animaation suoritus
if st.session_state.run:
    frame = 0
    while st.session_state.run:
        metric1.metric("Aalto 1", f"{v1:.2f} Hz")
        metric2.metric("Aalto 2", f"{v2:.2f} Hz")
        
        draw_plot(frame * 0.1)
        
        frame += 1
        time.sleep(speed)
else:
    # Staattinen tila
    metric1.metric("Aalto 1", f"{v1:.2f} Hz")
    metric2.metric("Aalto 2", f"{v2:.2f} Hz")
    draw_plot(0)
    st.info("Simulaattori on tauolla. Käynnistä animaatio sivupalkista.")
