import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from spectrogram import *

def apply_abnormalities(uploaded_file,color):
    
    sample_rate, data = wavfile.read(uploaded_file)

    # Generate random slider values between 0 and 1 for each abnormality
    slider_values = np.random.rand(10)

    # Scale the slider values to the appropriate magnitudes for each abnormality
    slider_values[0] *= 5  # arrhythmia
    slider_values[1] *= 10  # epilepsy
    slider_values[2] *= 15  # hypertension
    slider_values[3] *= 25  # diabetes
    slider_values[4] *= 50  # sleep apnea
    slider_values[5] *= 70  # tachycardia
    slider_values[6] *= 80  # asthma
    slider_values[7] *= 100  # Parkinson's
    slider_values[8] *= 150  # multiple sclerosis
    slider_values[9] *= 200  # cancer
    # Set the magnitudes of the abnormalities
    arrhythmia_magnitude = slider_values[0]
    epilepsy_magnitude = slider_values[1]
    hypertension_magnitude = slider_values[2]
    diabetes_magnitude = slider_values[3]
    sleep_apnea_magnitude = slider_values[4]
    tachycardia_magnitude = slider_values[5]
    asthma_magnitude = slider_values[6]
    parkinsons_magnitude = slider_values[7]
    multiple_sclerosis_magnitude = slider_values[8]
    cancer_magnitude = slider_values[9]

    # Compute the Fourier transform of the data
    data_ft = np.fft.rfft(data)

    # Create an array of frequencies for each frequency bin
    freqs = np.fft.rfftfreq(len(data), d=1/sample_rate)

    # Initialize an empty array to store the modified frequency components
    modified_freqs = np.zeros_like(data_ft)

    # Apply the abnormalities to the data
    arrhythmia_indices = np.where((freqs >= 1) & (freqs < 4))[0]
    epilepsy_indices = np.where((freqs >= 5) & (freqs < 10))[0]
    hypertension_indices = np.where((freqs >= 10) & (freqs < 15))[0]
    diabetes_indices = np.where((freqs >= 20) & (freqs < 25))[0]
    sleep_apnea_indices = np.where((freqs >= 30) & (freqs < 40))[0]
    tachycardia_indices = np.where((freqs >= 40) & (freqs < 50))[0]
    asthma_indices = np.where((freqs >= 60) & (freqs < 70))[0]
    parkinsons_indices = np.where((freqs >= 80) & (freqs < 100))[0]
    multiple_sclerosis_indices = np.where((freqs >= 120) & (freqs < 140))[0]
    cancer_indices = np.where((freqs >= 200) & (freqs < 300))[0]

    modified_freqs[arrhythmia_indices] = arrhythmia_magnitude * data_ft[arrhythmia_indices]
    modified_freqs[epilepsy_indices] = epilepsy_magnitude * data_ft[epilepsy_indices]
    modified_freqs[hypertension_indices] = hypertension_magnitude * data_ft[hypertension_indices]
    modified_freqs[diabetes_indices] = diabetes_magnitude * data_ft[diabetes_indices]
    modified_freqs[sleep_apnea_indices] = sleep_apnea_magnitude * data_ft[sleep_apnea_indices]
    modified_freqs[tachycardia_indices] = tachycardia_magnitude * data_ft[tachycardia_indices]
    modified_freqs[asthma_indices] = asthma_magnitude * data_ft[asthma_indices]
    modified_freqs[parkinsons_indices] = parkinsons_magnitude * data_ft[parkinsons_indices]
    modified_freqs[multiple_sclerosis_indices] = multiple_sclerosis_magnitude * data_ft[multiple_sclerosis_indices]
    modified_freqs[cancer_indices] = cancer_magnitude * data_ft[cancer_indices]
    # Compute the inverse Fourier transform of the modified frequency components to obtain the modified audio data
    modified_data = np.fft.irfft(modified_freqs)

    # Save the modified audio data as a WAV file
    wavfile.write('modified_audio.wav', sample_rate, modified_data)

    # Plot the original and modified audio data
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
    ax.plot(modified_data, color=color, linewidth=1.5, linestyle='-')
    ax.set_title('Modified Audio Data')
    ax.set_xlabel("Time (s)", fontsize=12)
    ax.set_ylabel("Amplitude", fontsize=12)
    st.pyplot(fig)
    plt.show()