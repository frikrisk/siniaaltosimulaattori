import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# 1. Sivun asetukset
st.set_page_config(page_title="Aalto-laboratorio", layout="wide")

# Alustetaan Play/Pause-tila muistiin, jos sitä ei vielä ole
if 'run_animation' not in st.session_state:
    st.session_state.run_animation = False

# Otsikko
st.title("🌊 Siniaaltojen simulaattori")

# 2. Ohjauspaneeli sivupalkissa
st.sidebar.header("⚙️ Ohjauspaneeli")

# Play/Pause-painike
if st.sidebar.button('▶️ Käynnistä / ⏸️ Pysäytä'):
    st.session_state.run_animation = not st.session_state.run_animation

v1 = st.sidebar.slider("Aallonpituus 1", 0.1, 10.0, 1.948)
color1 = st.sidebar.selectbox("Väri 1", ['blue', 'green', 'cyan', 'teal'])

st.sidebar.divider()

v2 = st.sidebar.slider("Aallonpituus 2", 0.1, 10.0, 2.822)
color2 = st.sidebar.selectbox("Väri 2", ['red', 'magenta', 'orange', 'gold'])

# 3. Mittaristot (Kojelauta)
col1, col2, col3 = st.columns(3)
metric1 = col1.empty()
metric2 = col2.empty()
metric3 = col3.empty()

# 4. Paikka kuvaajalle
plot_spot = st.empty()

# Valmistellaan data
t = np.linspace(0, 2 * np.pi, 1000)

# 5. Animaatio-looppi
# Jos animaatio on päällä, pyöritetään looppia. Jos ei, piirretään vain staattinen kuva.
if st.session_state.run_animation:
    try:
        for frame in range(1000):
            # Jos käyttäjä painaa nappia uudelleen kesken loopin, se ei pysähdy heti,
            # mutta tämä tarkistus auttaa reagoimaan nopeammin:
            if not st.session_state.run_animation:
                break
                
            offset = frame * 0.1
            
            # Päivitetään mittarit
            metric1.metric("Aalto 1 Taajuus", f"{v1:.2f} Hz")
            metric2.metric("Aalto 2 Taajuus", f"{v2:.2f} Hz")
            metric3.metric("Animaatio-frame", frame)

            # Luodaan kuvaaja
            fig, ax = plt.subplots(figsize=(10, 5))
            y1 = np.sin(v1 * (t + offset))
            y2 = np.sin(v2 * (t + offset))
            
            ax.plot(t, y1, color=color1, lw=2, label='Aalto 1')
            ax.plot(t, y2, color=color2, lw=2, label='Aalto 2')
            ax.plot(t, y1 + y2, color='black', ls='--', lw=2, label='Summa')
            
            ax.set_ylim(-2.5, 2.5)
            ax.grid(True, alpha=0.3)
            ax.legend(loc='upper right')
            
            # Piirretään
            plot_spot.pyplot(fig)
            plt.close(fig)
            
            # 0.05s on "sweet spot" sulavuuden ja vakauden välillä
            time.sleep(0.05)
            
    except Exception as e:
        pass
else:
    # Staattinen kuva, kun animaatio on pysäytetty
    metric1.metric("Aalto 1 Taajuus", f"{v1:.2f} Hz", delta="PYSÄYTETTY", delta_color="inverse")
    metric2.metric("Aalto 2 Taajuus", f"{v2:.2f} Hz", delta="PYSÄYTETTY", delta_color="inverse")
    metric3.metric("Tila", "Tauko")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(t, np.sin(v1 * t), color=color1, lw=2)
    ax.plot(t, np.sin(v2 * t), color=color2, lw=2)
    ax.plot(t, np.sin(v1 * t) + np.sin(v2 * t), color='black', ls='--', lw=2)
    ax.set_ylim(-2.5, 2.5)
    ax.grid(True, alpha=0.3)
    plot_spot.pyplot(fig)
    plt.close(fig)
    st.info("Klikkaa 'Käynnistä' sivupalkista aloittaaksesi animaation.")
