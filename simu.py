import streamlit as st
import numpy as np
import pandas as pd
import time

st.set_page_config(page_title="Aalto-laboratorio", layout="wide")

if 'run' not in st.session_state:
    st.session_state.run = False

st.title("🌊 Aalto-laboratorio")

# 1. Ohjauspaneeli sivupalkissa
st.sidebar.header("⚙️ Ohjauspaneeli")

if st.sidebar.button('▶️ Käynnistä / ⏸️ Pysäytä'):
    st.session_state.run = not st.session_state.run

v1 = st.sidebar.slider("Taajuus 1", 0.1, 10.0, 1.95)
c1 = st.sidebar.selectbox("Väri 1", ['blue', 'green', 'teal', 'cyan'], index=0)

st.sidebar.divider()

v2 = st.sidebar.slider("Taajuus 2", 0.1, 10.0, 2.82)
c2 = st.sidebar.selectbox("Väri 2", ['red', 'magenta', 'orange', 'gold'], index=0)

speed = st.sidebar.slider("Päivitysviive (s)", 0.01, 0.20, 0.05)

# 2. Luodaan paikkamerkit, jotka pysyvät vakioina (ei hyppimistä)
col1, col2 = st.columns(2)
m1 = col1.empty()
m2 = col2.empty()
chart_placeholder = st.empty()

t = np.linspace(0, 2 * np.pi, 200)

# 3. Animaatio-fragmentti (Päivittää vain sisällön, ei koko sivua)
@st.fragment
def run_animation():
    frame = 0
    while st.session_state.run:
        offset = frame * 0.1
        y1 = np.sin(v1 * (t + offset))
        y2 = np.sin(v2 * (t + offset))
        y_sum = y1 + y2
        
        # Päivitetään mittarit
        m1.metric("Aalto 1", f"{v1:.2f} Hz")
        m2.metric("Aalto 2", f"{v2:.2f} Hz")
        
        # Data
        df = pd.DataFrame({'x': t, 'Aalto 1': y1, 'Aalto 2': y2, 'Summa': y_sum})
        df_m = df.melt('x', var_name='Aalto', value_name='y')
        
        # Piirto Vega-Litellä ilman hyppimistä
        chart_placeholder.vega_lite_chart(df_m, {
            'mark': {'type': 'line', 'clip': True},
            'encoding': {
                'x': {'field': 'x', 'type': 'quantitative', 'scale': {'domain': [0, 6.28]}},
                'y': {'field': 'y', 'type': 'quantitative', 'scale': {'domain': [-2.5, 2.5]}},
                'color': {
                    'field': 'Aalto', 
                    'type': 'nominal',
                    'scale': {
                        'domain': ['Aalto 1', 'Aalto 2', 'Summa'],
                        'range': [c1, c2, 'black']
                    }
                },
                'strokeDash': {
                    'field': 'Aalto',
                    'type': 'nominal',
                    'scale': {
                        'domain': ['Aalto 1', 'Aalto 2', 'Summa'],
                        'range': [[0,0], [0,0], [5,5]]
                    }
                }
            },
            'height': 450,
            'config': {'autosize': {'type': 'fit', 'contains': 'padding'}}
        }, use_container_width=True)
        
        frame += 1
        time.sleep(speed)

# 4. Suoritus
if st.session_state.run:
    run_animation()
else:
    # Staattinen näkymä tauolla
    m1.metric("Aalto 1", f"{v1:.2f} Hz")
    m2.metric("Aalto 2", f"{v2:.2f} Hz")
    y1_s = np.sin(v1 * t)
    y2_s = np.sin(v2 * t)
    df_s = pd.DataFrame({'x': t, 'Aalto 1': y1_s, 'Aalto 2': y2_s, 'Summa': y1_s + y2_s})
    df_sm = df_s.melt('x', var_name='Aalto', value_name='y')
    chart_placeholder.vega_lite_chart(df_sm, {
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
        'height': 450
    }, use_container_width=True)
    st.info("Paina Käynnistä-painiketta sivupalkista.")
