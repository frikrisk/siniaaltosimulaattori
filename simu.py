import streamlit as st
import numpy as np
import pandas as pd
import time

st.set_page_config(page_title="Aalto-laboratorio", layout="wide")

if 'run' not in st.session_state:
    st.session_state.run = False

st.title("🌊 Aalto-laboratorio")

if st.sidebar.button('▶️ Käynnistä / ⏸️ Pysäytä'):
    st.session_state.run = not st.session_state.run

v1 = st.sidebar.slider("Taajuus 1", 0.1, 10.0, 1.95)
v2 = st.sidebar.slider("Taajuus 2", 0.1, 10.0, 2.82)
speed = st.sidebar.slider("Päivitysviive (s)", 0.01, 0.20, 0.05)

col1, col2 = st.columns(2)
m1 = col1.empty()
m2 = col2.empty()
placeholder = st.empty()

t = np.linspace(0, 2 * np.pi, 200)

if st.session_state.run:
    f = 0
    while st.session_state.run:
        off = f * 0.1
        y1 = np.sin(v1 * (t + off))
        y2 = np.sin(v2 * (t + off))
        y_sum = y1 + y2
        
        m1.metric("Aalto 1", f"{v1:.2f} Hz")
        m2.metric("Aalto 2", f"{v2:.2f} Hz")
        
        df = pd.DataFrame({'x': t, 'Aalto 1': y1, 'Aalto 2': y2, 'Summa': y_sum})
        df_m = df.melt('x', var_name='Aalto', value_name='y')
        
        placeholder.vega_lite_chart(df_m, {
            'mark': {'type': 'line', 'clip': True},
            'encoding': {
                'x': {'field': 'x', 'type': 'quantitative', 'scale': {'domain': [0, 6.28]}},
                'y': {'field': 'y', 'type': 'quantitative', 'scale': {'domain': [-2.5, 2.5]}},
                'color': {
                    'field': 'Aalto', 
                    'type': 'nominal',
                    'scale': {
                        'domain': ['Aalto 1', 'Aalto 2', 'Summa'],
                        'range': ['blue', 'red', 'black']
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
        
        f += 1
        time.sleep(speed)
else:
    placeholder.info("Simulaattori on tauolla. Paina Käynnistä.")
    y1_s = np.sin(v1 * t)
    y2_s = np.sin(v2 * t)
    df_s = pd.DataFrame({'x': t, 'Aalto 1': y1_s, 'Aalto 2': y2_s, 'Summa': y1_s + y2_s})
    placeholder.line_chart(df_s.set_index('x'))
