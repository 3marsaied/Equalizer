import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import io
import wave
import scipy.signal as signal
from scipy import signal
from spectrogram import *

def vowels_mode(uploaded_file, color):
    if uploaded_file:
        # Load the WAV file data
        sample_rate, data = wavfile.read(uploaded_file)

        # Define the center frequencies and bandwidths for each vowel
        vowel_centers = {'a': 730, 'e': 660, 'i': 500, 'o': 450, 'u': 325}
        vowel_bandwidths = {'a': 50, 'e': 70, 'i': 40, 'o': 70, 'u': 50}

        # Create an empty list to store the slider values
        slider_values = []

        # Create a slider for each vowel
        for vowel in vowel_centers:
            # Calculate the start and end frequencies of the vowel band
            start_freq = vowel_centers[vowel] - vowel_bandwidths[vowel]
            end_freq = vowel_centers[vowel] + vowel_bandwidths[vowel]

        # Create a slider with the start and end frequencies
        slider = st.sidebar.slider(f"{vowel.capitalize()} ({start_freq}-{end_freq} Hz)", start_freq, end_freq, (start_freq + end_freq) // 2, 1)

        # Append the slider value to the list of slider values
        slider_values.append(slider)

        # Apply the frequency filters to the signal
        # Define filter order and type
        filter_order = 2
        filter_type = 'bandpass'

        # Calculate the frequency range for each slider
        slider_range = sample_rate / 2 / 10

        # Create an array of filter cutoff frequencies based on slider values
        filter_freqs = np.zeros(10)
        for i, slider_value in enumerate(slider_values):
            filter_freqs[i] = slider_value

        # Apply filters to the signal
        filtered_data_ft = np.fft.rfft(data)
        for i in range(10):
            # Calculate the filter coefficients
            filter_low = filter_freqs[i] - slider_range / 2
            filter_high = filter_freqs[i] + slider_range / 2
            filter_low_norm = filter_low / (sample_rate / 2)
            filter_high_norm = filter_high / (sample_rate / 2)
            b, a = signal.butter(filter_order, [filter_low_norm, filter_high_norm], btype=filter_type)

            # Apply the filter
            filtered_data_ft = signal.lfilter(b, a, filtered_data_ft)

        # Compute the inverse Fourier transform of the modified frequency components
        filtered_data = np.fft.irfft(filtered_data_ft)

        # Normalize the filtered data
        filtered_data = filtered_data / np.max(np.abs(filtered_data))

        # Create a time axis
        time = np.linspace(0, len(filtered_data) / sample_rate, len(filtered_data))

        # Create a plot
        fig, ax = plt.subplots(1, 1, figsize=(8, 4))
        ax.plot(time, filtered_data, color=color, linewidth=1.5, linestyle='-')

        # Set the plot title and labels
        ax.set_title("Filtered WAV file")
        ax.set_xlabel("Time (s)", fontsize=12)
        ax.set_ylabel("Amplitude", fontsize=12)

        # Display the plot
        st.pyplot(fig)

        # Create an audio player widget for the filtered data
        with io.BytesIO() as wav_file:
            wav_writer = wave.open(wav_file, "wb")
            wav_writer.setnchannels(1)
            wav_writer.setsampwidth(2)
            wav_writer.setframerate(sample_rate)
            wav_writer.writeframes(data)
            wav_writer.close()
            st.audio(wav_file.getvalue(), format='audio/wav')
