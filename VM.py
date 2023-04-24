import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import io
import wave
from scipy.fft import fft, fftfreq, fftshift
from spectrogram import *


def vowel_mode(uploaded_file,color):
    # Load the audio file
    sample_rate, data = wavfile.read(uploaded_file)

    # Define the frequencies of the vowel components
    freq_a = 730
    freq_e = 660
    freq_i = 540
    freq_o = 300
    freq_u = 3000
    freq_aa = 1200
    freq_ee = 2700
    freq_ii = 2250
    freq_oo = 500
    freq_uu = 1000

    # Create 10 sliders for the vowel components
    st.sidebar.markdown("## Vowels Mode")
    slider_a = st.sidebar.slider("A", min_value=0.0, max_value=1.0, step=0.01, value=1.0)
    slider_e = st.sidebar.slider("E", min_value=0.0, max_value=1.0, step=0.01, value=1.0)
    slider_i = st.sidebar.slider("I", min_value=0.0, max_value=1.0, step=0.01, value=1.0)
    slider_o = st.sidebar.slider("O", min_value=0.0, max_value=1.0, step=0.01, value=1.0)
    slider_u = st.sidebar.slider("U", min_value=0.0, max_value=1.0, step=0.01, value=1.0)
    slider_aa = st.sidebar.slider("AA", min_value=0.0, max_value=1.0, step=0.01, value=1.0)
    slider_ee = st.sidebar.slider("EE", min_value=0.0, max_value=1.0, step=0.01, value=1.0)
    slider_ii = st.sidebar.slider("II", min_value=0.0, max_value=1.0, step=0.01, value=1.0)
    slider_oo = st.sidebar.slider("OO", min_value=0.0, max_value=1.0, step=0.01, value=1.0)
    slider_uu = st.sidebar.slider("UU", min_value=0.0, max_value=1.0, step=0.01, value=1.0)

    # Apply the vowel mode to the data
    freqs = fftfreq(len(data)) * sample_rate
    data_fft = fft(data)

    data_fft[int(freq_a)] *= slider_a
    data_fft[int(freq_e)] *= slider_e
    data_fft[int(freq_i)] *= slider_i
    data_fft[int(freq_o)] *= slider_o
    data_fft[int(freq_u)] *= slider_u
    data_fft[int(freq_aa)] *= slider_aa
    data_fft[int(freq_ee)] *= slider_ee
    data_fft[int(freq_ii)] *= slider_ii
    data_fft[int(freq_oo)] *= slider_oo
    data_fft[int(freq_uu)] *= slider_uu

    time = np.arange(len(data))/float(sample_rate)

    # Inverse transform to get the modified audio data
    modified_data = np.real(np.fft.ifft(data_fft))

    # Create a plot of the modified data
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
    ax.plot(time, modified_data, color=color, linewidth=1.5, linestyle='-')

    # Set the plot title and labels
    ax.set_title("Modified WAV file")
    ax.set_xlabel("Time (s)", fontsize=12)
    ax.set_ylabel("Amplitude", fontsize=12)
    st.pyplot(fig)

    # Create an audio player widget
    with io.BytesIO() as wav_file:
        wav_writer = wave.open(wav_file, "wb")
        wav_writer.setnchannels(1)
        wav_writer.setsampwidth(2)
        wav_writer.setframerate(sample_rate)
        wav_writer.writeframes(data)
        wav_writer.close()
        st.audio(wav_file.getvalue(), format='audio/wav')

        plot_spectrogram(sample_rate, data)
