import streamlit as st
import numpy as np
import pandas as pd
import time

st.set_page_config(page_title="Aalto-laboratorio", layout="wide")

# Alustetaan muuttujat session_stateen
if 'run' not in st.session_state:
    st.session_state.run = False
if 'frame' not in st.session_state:
    st.session_state.frame = 0

st.title("🌊 Aalto-laboratorio")

# Ohjauspaneeli
st.sidebar.header("⚙️ Ohjauspaneeli")

def toggle_run():
    st.session_state.run = not st.session_state.run

st.sidebar.button('▶️ Käynnistä / ⏸️ Pysäytä', on_click=toggle_run)

v1 = st.sidebar.slider("Taajuus 1", 0.1, 10.0, 1.95)
c1 = st.sidebar.selectbox("Väri 1", ['blue', 'green', 'teal', 'cyan'], index=0)

st.sidebar.divider()

v2 = st.sidebar.slider("Taajuus 2", 0.1, 10.0, 2.82)
c2 = st.sidebar.selectbox("Väri 2", ['red', 'magenta', 'orange', 'gold'], index=0)

speed = st.sidebar.slider("Päivitysviive (s)", 0.01, 0.20, 0.05)

col1, col2 = st.columns(2)
m1 = col1.empty()
m2 = col2.empty()
placeholder = st.empty()

t = np.linspace(0, 2 * np.pi, 200)

# ANIMAATIO-LOGIIKKA
if st.session_state.run:
    # Lasketaan aallot nykyisellä framella
    offset = st.session_state.frame * 0.1
    y1 = np.sin(v1 * (t + offset))
    y2 = np.sin(v2 * (t + offset))
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
        'height': 450
    }, use_container_width=True)
    
    # Kasvatetaan framea ja nukutaan hetki
    st.session_state.frame += 1
    time.sleep(speed)
    # TÄMÄ PAKOTTAA UUDELLEENLATAUKSEN
    st.rerun()

else:
    # Kun animaatio on seis, näytetään staattinen kuva Vega-Litellä (jotta värit pysyvät)
    y1_s = np.sin(v1 * t)
    y2_s = np.sin(v2 * t)
    df_s = pd.DataFrame({'x': t, 'Aalto 1': y1_s, 'Aalto 2': y2_s, 'Summa': y1_s + y2_s})
    df_sm = df_s.melt('x', var_name='Aalto', value_name='y')
    
    placeholder.vega_lite_chart(df_sm, {
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
