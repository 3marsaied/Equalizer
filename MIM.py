import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import io
import wave
import scipy.signal as signal
from scipy import signal
from spectrogram import *

def musical_instruments_mode(uploaded_file, color):
    # Check if a file was uploaded
    if uploaded_file is not None:
        # Load the file data
        sample_rate, data = wavfile.read(uploaded_file)

        # Calculate the duration of the file
        duration = len(data) / sample_rate

        # Create a time axis
        time = np.linspace(0, duration, len(data))


        # Create sliders for each musical instrument
        sliders = {}
        sliders['Piano'] = st.sidebar.slider('Piano', 0.0, 1.0, 1.0, 0.1)
        sliders['Guitar'] = st.sidebar.slider('Guitar', 0.0, 1.0, 1.0, 0.1)
        sliders['Bass'] = st.sidebar.slider('Bass', 0.0, 1.0, 1.0, 0.1)
        sliders['Drums'] = st.sidebar.slider('Drums', 0.0, 1.0, 1.0, 0.1)
        sliders['Strings'] = st.sidebar.slider('Strings', 0.0, 1.0, 1.0, 0.1)
        sliders['Synth'] = st.sidebar.slider('Synth', 0.0, 1.0, 1.0, 0.1)

        # Create a dictionary of frequency ranges for each musical instrument
        freq_ranges = {
            'Piano': (26, 4186),
            'Guitar': (82, 1175),
            'Bass': (41, 262),
            'Drums': (20, 20000),
            'Strings': (196, 2637),
            'Synth': (27, 4186)
        }

        # Calculate the number of samples in the data
        n_samples = len(data)

        # Compute the Fourier transform of the data
        data_ft = np.fft.rfft(data)

        # Create an array of frequencies for each frequency bin
        freqs = np.fft.rfftfreq(n_samples, d=1/sample_rate)

        # Initialize an empty array to store the modified frequency components
        modified_freqs = np.zeros_like(data_ft)

        # Apply the frequency filters to the data
        for instrument, freq_range in freq_ranges.items():
            # Determine the indices of the frequency components within the current range
            freq_indices = np.where((freqs >= freq_range[0]) & (freqs < freq_range[1]))[0]

            # Apply the current slider value to the frequency components within the current range
            slider_value = sliders[instrument]
            modified_freqs[freq_indices] = data_ft[freq_indices] * slider_value
            # Compute the inverse Fourier transform of the modified frequency components
            modified_data = np.fft.irfft(modified_freqs)

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
            