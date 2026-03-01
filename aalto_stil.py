import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Aalto-laboratorio", layout="wide")

if 'run_animation' not in st.session_state:
    st.session_state.run_animation = False

st.title("🌊 Siniaaltojen simulaattori")

# --- Ohjauspaneeli ---
st.sidebar.header("⚙️ Ohjauspaneeli")
if st.sidebar.button('▶️ Käynnistä / ⏸️ Pysäytä'):
    st.session_state.run_animation = not st.session_state.run_animation

v1 = st.sidebar.slider("Aallonpituus 1", 0.1, 10.0, 1.95)
color1 = st.sidebar.selectbox("Väri 1", ['blue', 'green', 'cyan', 'teal'], index=0)

st.sidebar.divider()

v2 = st.sidebar.slider("Aallonpituus 2", 0.1, 10.0, 2.82)
color2 = st.sidebar.selectbox("Väri 2", ['red', 'magenta', 'orange', 'gold'], index=0)

# Nopeuden säätö lennosta
speed = st.sidebar.slider("Animaation nopeus", 0.01, 0.20, 0.05)

plot_spot = st.empty()
t = np.linspace(0, 2 * np.pi, 400) # 400 pistettä on hyvä kompromissi

# --- Animaatio-looppi ---
frame = 0
while st.session_state.run_animation:
    offset = frame * 0.1
    y1 = np.sin(v1 * (t + offset))
    y2 = np.sin(v2 * (t + offset))
    y_sum = y1 + y2

    # Luodaan Plotly-kuvaaja
    fig = go.Figure()
    
    # Aalto 1
    fig.add_trace(go.Scatter(x=t, y=y1, name='Aalto 1', line=dict(color=color1, width=2)))
    # Aalto 2
    fig.add_trace(go.Scatter(x=t, y=y2, name='Aalto 2', line=dict(color=color2, width=2)))
    # Summa (Katkoviivalla)
    fig.add_trace(go.Scatter(x=t, y=y_sum, name='Summa', line=dict(color='black', width=2, dash='dash')))

    fig.update_layout(
        ylim=dict(range=[-2.5, 2.5]),
        margin=dict(l=0, r=0, t=0, b=0),
        height=400,
        showlegend=True,
        xaxis=dict(gridcolor='lightgray'),
        yaxis=dict(gridcolor='lightgray'),
        plot_bgcolor='white'
    )

    plot_spot.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    frame += 1
    time.sleep(speed) # Käytetään sliderista tulevaa viivettä

# Jos animaatio ei ole päällä, näytetään ohje
if not st.session_state.run_animation:
    st.info("Simulaattori on pysäytetty. Käynnistä animaatio sivupalkista.")
