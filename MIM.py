import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import io
import wave
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
        sliders['Piano'] = st.sidebar.slider('Piano', 26, 4186, 26)
        sliders['Guitar'] = st.sidebar.slider('Guitar', 82, 1175, 82)
        sliders['Bass'] = st.sidebar.slider('Bass', 41, 262, 41)
        sliders['Drums'] = st.sidebar.slider('Drums', 28, 20000,28)
        sliders['Strings'] = st.sidebar.slider('Strings', 196, 2637, 196)
        sliders['Synth'] = st.sidebar.slider('Synth', 27, 4186, 27)


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
            # Extract the minimum and maximum frequency values for the current instrument
            fmin, fmax = freq_range
            # Find the indices of the frequency bins within the specified range
            idx_min = np.argmin(np.abs(freqs - fmin))
            idx_max = np.argmin(np.abs(freqs - fmax))

            # Set the values of the frequency components outside the range to zero
            modified_freqs[idx_min:idx_max] = sliders[instrument] * data_ft[idx_min:idx_max]

        # Compute the inverse Fourier transform to get the modified audio signal
        modified_data = np.fft.irfft(modified_freqs)


        # Plot the modified audio signal
        fig, ax = plt.subplots(1,1,figsize=(8, 4))
        ax.plot(time, modified_data, color=color, linewidth=1.5, linestyle='-')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Amplitude')
        st.pyplot(fig)

        # Create an audio player widget
        with io.BytesIO() as wav_file:
            wav_writer = wave.open(wav_file, "wb")
            wav_writer.setnchannels(1)
            wav_writer.setsampwidth(2)
            wav_writer.setframerate(sample_rate)
            wav_writer.writeframes(modified_data    )
            wav_writer.close()
            st.audio(wav_file.getvalue(), format='audio/wav')

        # Plot the spectrogram of the modified audio signal
        plot_spectrogram(sample_rate, modified_data, freqs)