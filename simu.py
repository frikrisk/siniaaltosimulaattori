import streamlit as st
import numpy as np
import pandas as pd
import time

st.set_page_config(page_title="SinCos-simulaatio", layout="wide")

if 'run' not in st.session_state:
    st.session_state.run = False

# Uusi hieno otsikkosi
# st.title("𓂃🌊∿ SinCos+summa-simulaatio𓈉")
st.title("𓈉 SinCos+summa-simulaatio𓈉 ")

# --- OHJAUSPANEELI ---
if st.sidebar.button('▶️ Käynnistä / ⏸️ Pysäytä'):
    st.session_state.run = not st.session_state.run

v1 = st.sidebar.slider("Taajuus 1 (Sini)", 0.1, 10.0, 1.95)

st.sidebar.divider()

# Lisätty valinta: Sini vai Kosini
aaltomuoto2 = st.sidebar.radio("Aallon 2 muoto", ["Sini", "Kosini"], horizontal=True)
v2 = st.sidebar.slider(f"Taajuus 2 ({aaltomuoto2})", 0.1, 10.0, 2.82)

# Värivalinnat (aiemmin luomasi sanakirjan mukaan)
vari_vaihtoehdot = {"Sininen": "#0000FF", "Vihreä": "#00FF00", "Punainen": "#FF0000", "Oranssi": "#FFA500"}
c1 = vari_vaihtoehdot[st.sidebar.selectbox("Aallon 1 väri", list(vari_vaihtoehdot.keys()), index=0)]
c2 = vari_vaihtoehdot[st.sidebar.selectbox("Aallon 2 väri", list(vari_vaihtoehdot.keys()), index=2)]

speed = st.sidebar.slider("Päivitysviive (s)", 0.01, 0.20, 0.05)

placeholder = st.empty()
t = np.linspace(0, 2 * np.pi, 200)

# --- LASKENTA-LOGIIKKA FUNKTIONA ---
def laske_aallot(offset_val):
    y1 = np.sin(v1 * (t + offset_val))
    # Valitaan funktio radionapin perusteella
    if aaltomuoto2 == "Sini":
        y2 = np.sin(v2 * (t + offset_val))
    else:
        y2 = np.cos(v2 * (t + offset_val))
    return y1, y2, y1 + y2

# --- SUORITUS ---
if st.session_state.run:
    f = 0
    while st.session_state.run:
        y1, y2, y_sum = laske_aallot(f * 0.1)
        df = pd.DataFrame({'Aalto 1': y1, 'Aalto 2': y2, 'Summa-aalto': y_sum}, index=t)
        placeholder.line_chart(df, color=[c1, c2, "#000000"])
        f += 1
        time.sleep(speed)
else:
    y1, y2, y_sum = laske_aallot(0)
    df = pd.DataFrame({'Aalto 1': y1, 'Aalto 2': y2, 'Summa-aalto': y_sum}, index=t)
    placeholder.line_chart(df, color=[c1, c2, "#000000"])
    st.info("Simulaattori on tauolla")
