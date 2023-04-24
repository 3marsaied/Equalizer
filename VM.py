import streamlit as st
import wave
import struct
import math
import matplotlib.pyplot as plt
import io
from spectrogram import *

def vowel_mode(uploaded_file,color):
    # Load the audio file
    audio = wave.open(uploaded_file, 'rb')
    sample_rate = audio.getframerate()
    num_frames = audio.getnframes()

    # Define the frequencies of the vowel components
    freq_a = 730
    freq_e = 660
    freq_i = 540
    freq_o = 300
    freq_u = 3000

    # Read audio data
    signal = []
    for i in range(num_frames):
        data = audio.readframes(1)
        sample = struct.unpack('<h', data)[0]
        signal.append(sample)

    # Create 5 sliders for the vowel components
    max_amp_a = max(signal)
    max_amp_e = max(signal)
    max_amp_i = max(signal)
    max_amp_o = max(signal)
    max_amp_u = max(signal)
    slider_a = st.sidebar.slider("A", min_value=0, max_value=max_amp_a, step=1, value=int(max_amp_a/2))
    slider_e = st.sidebar.slider("E", min_value=0, max_value=max_amp_e, step=1, value=int(max_amp_e/2))
    slider_i = st.sidebar.slider("I", min_value=0, max_value=max_amp_i, step=1, value=int(max_amp_i/2))
    slider_o = st.sidebar.slider("O", min_value=0, max_value=max_amp_o, step=1, value=int(max_amp_o/2))
    slider_u = st.sidebar.slider("U", min_value=0, max_value=max_amp_u, step=1, value=int(max_amp_u/2))

    # Calculate the time axis and frequency axis
    time = [float(i)/sample_rate for i in range(num_frames)]
    freqs = [float(i)*sample_rate/num_frames for i in range(num_frames//2)]

    # Fourier Transform
    spectrum = []
    for f in range(num_frames//2):
        freq = freqs[f]
        amplitude = 0
        for i in range(num_frames):
            amplitude += signal[i]*math.cos(2*math.pi*freq*time[i])
        spectrum.append(amplitude)

    # Modify the amplitude of the specified frequency components using sliders
    spectrum[freqs.index(freq_a)] *= slider_a/max_amp_a
    spectrum[freqs.index(freq_e)] *= slider_e/max_amp_e
    spectrum[freqs.index(freq_i)] *= slider_i/max_amp_i
    spectrum[freqs.index(freq_o)] *= slider_o/max_amp_o
    spectrum[freqs.index(freq_u)] *= slider_u/max_amp_u

    # Inverse Fourier Transform
    signal_new = []
    for i in range(num_frames):
        sample = 0
        for f in range(num_frames//2):
            freq = freqs[f]
            amplitude = spectrum[f]
            sample += amplitude*math.cos(2*math.pi*freq*time[i])
        signal_new.append(sample)

    # Plot the modified audio signal
    fig, ax = plt.subplots(1,1,figsize=(8, 4))
    ax.plot(time, signal_new, color=color, linewidth=1.5, linestyle='-')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    st.pyplot(fig)

    # Create an audio player widget
    with io.BytesIO() as wav_file:
        wav_writer = wave.open(wav_file, "wb")
        wav_writer.setnchannels(1)
        wav_writer.setsampwidth(2)
        wav_writer.setframerate(sample_rate)
        wav_writer.writeframes(struct.pack('<' + 'h'*len(signal_new), *signal_new))
        wav_writer.close()
        st.audio(wav_file.getvalue(), format='audio/wav')

    # Plot the spectrogram of the modified audio signal
    plot_spectrogram(sample_rate, signal_new, freqs)