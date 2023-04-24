import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import io
import wave
from spectrogram import *
from spectrogram import *

def uniform_range_mode_apply_filters(data, sample_rate, freq_range, slider_values):
    # Calculate the number of samples in the data
    n_samples = len(data)

    # Compute the Fourier transform of the data
    data_ft = np.fft.rfft(data)

    # Create an array of frequencies for each frequency bin
    freqs = np.fft.rfftfreq(n_samples, d=1/sample_rate)

    # Initialize an empty array to store the modified frequency components
    modified_freqs = np.zeros_like(data_ft)

    # Apply the frequency filters to the data
    for i in range(10):
        # Determine the frequency range for the current slider
        min_freq = i * (freq_range / 10)
        max_freq = (i + 1) * (freq_range / 10)

        # Determine the indices of the frequency components within the current range
        freq_indices = np.where((freqs >= min_freq) & (freqs < max_freq))[0]

        # Apply the current slider value to the frequency components within the current range
        slider_value = slider_values[i]
        modified_freqs[freq_indices] = slider_value * data_ft[freq_indices]

    return modified_freqs,freqs



def uniform_range_mode(uploaded_file,color):
    # Check if a file was uploaded
    if uploaded_file is not None:
        # Load the file data
        sample_rate, data = wavfile.read(uploaded_file)

        # Calculate the frequency range of the signal
        freq_range = sample_rate / 2

        # Calculate the frequency range for each slider
        slider_range = freq_range / 10

        # Create an empty list to store the slider values
        slider_values = []

       # Create a slider for each frequency range
        for i in range(10):
            # Calculate the start and end frequency of this range
            start_freq = i * slider_range
            end_freq = (i + 1) * slider_range

            # Create a slider with the start and end frequencies
            slider = st.sidebar.slider(f"Frequency Range {i+1}", int(start_freq), int(end_freq), int(start_freq))

            # Append the slider value to the list of slider values
            slider_values.append(slider)
        
        
        # Apply the frequency filters to the signal
        modified_freqs,freqs = uniform_range_mode_apply_filters(data, sample_rate, freq_range, slider_values)

        # Compute the inverse Fourier transform to get the modified audio signal
        modified_data = np.fft.irfft(modified_freqs)
        
        # Compute the inverse Fourier transform of the modified frequency components
        reconstructed_signal = np.fft.irfft(modified_freqs)

        # Create a plot of the reconstructed signal
        fig, ax = plt.subplots(1, 1, figsize=(8, 4))
        ax.plot(reconstructed_signal,color=color, linewidth=1.5, linestyle='-')
        ax.set_xlabel("Time (samples)", fontsize=12)
        ax.set_ylabel("Amplitude", fontsize=12)
        ax.set_title("Reconstructed Signal", fontsize=12)
        st.pyplot(fig)

        # Create an audio player widget
        with io.BytesIO() as wav_file:
            wav_writer = wave.open(wav_file, "wb")
            wav_writer.setnchannels(1)
            wav_writer.setsampwidth(2)
            wav_writer.setframerate(sample_rate)
            wav_writer.writeframes(modified_data)
            wav_writer.close()
            st.audio(wav_file.getvalue(), format='audio/wav')

        plot_spectrogram(sample_rate, modified_data, freqs)