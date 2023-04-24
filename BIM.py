import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import io
import wave
from spectrogram import *

def apply_abnormalities(uploaded_file,color):
    
    sample_rate, data = wavfile.read(uploaded_file)
    time = np.arange(len(data))/float(sample_rate)

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

    with st.sidebar:
        arrhythmia_slider = st.sidebar.slider("Arrhythmia Magnitude", min_value=0, max_value=5)
        epilepsy_slider = st.sidebar.slider("Epilepsy Magnitude", min_value=0, max_value=10)
        hypertension_slider = st.sidebar.slider("Hypertension Magnitude", min_value=0, max_value=15)
        diabetes_slider = st.sidebar.slider("Diabetes Magnitude", min_value=0, max_value=25)
        sleep_apnea_slider = st.sidebar.slider("Sleep Apnea Magnitude", min_value=0, max_value=50)
        tachycardia_slider = st.sidebar.slider("Tachycardia Magnitude", min_value=0, max_value=70)
        asthma_slider = st.sidebar.slider("Asthma Magnitude", min_value=0, max_value=80)
        parkinsons_slider = st.sidebar.slider("Parkinson's Magnitude", min_value=0, max_value=100)
        multiple_sclerosis_slider = st.sidebar.slider("Multiple Sclerosis Magnitude", min_value=0, max_value=150)
        cancer_slider = st.sidebar.slider("Cancer Magnitude", min_value=0, max_value=200)

    arrhythmia_magnitude = arrhythmia_slider
    epilepsy_magnitude = epilepsy_slider
    hypertension_magnitude = hypertension_slider
    diabetes_magnitude = diabetes_slider
    sleep_apnea_magnitude = sleep_apnea_slider
    tachycardia_magnitude = tachycardia_slider
    asthma_magnitude = asthma_slider
    parkinsons_magnitude = parkinsons_slider
    multiple_sclerosis_magnitude = multiple_sclerosis_slider
    cancer_magnitude = cancer_slider

    # Compute the Fourier transform of the data
    data_ft = np.fft.rfft(data)

    # Create an array of frequencies for each frequency bin
    freqs = np.fft.rfftfreq(len(data), d=1/sample_rate)

    # Initialize an empty array to store the modified frequency components
    modified_freqs = np.zeros_like(data_ft)

    # Apply the abnormalities to the data
    arrhythmia_indices = np.where((freqs >= 1) &(freqs < 4))[0]
    modified_freqs[arrhythmia_indices] += arrhythmia_magnitude * slider_values[0]
    epilepsy_indices = np.where((freqs >= 5) &
                            (freqs < 20))[0]
    modified_freqs[epilepsy_indices] += epilepsy_magnitude * slider_values[1]

    hypertension_indices = np.where((freqs >= 20) &
                                 (freqs < 50))[0]
    modified_freqs[hypertension_indices] += hypertension_magnitude * slider_values[2]

    diabetes_indices = np.where((freqs >= 50) &
                             (freqs < 100))[0]
    modified_freqs[diabetes_indices] += diabetes_magnitude * slider_values[3]

    sleep_apnea_indices = np.where((freqs >= 100) &
                                (freqs < 200))[0]
    modified_freqs[sleep_apnea_indices] += sleep_apnea_magnitude * slider_values[4]

    tachycardia_indices = np.where((freqs >= 200) &
                                 (freqs < 400))[0]
    modified_freqs[tachycardia_indices] += tachycardia_magnitude * slider_values[5]

    asthma_indices = np.where((freqs >= 400) &
                            (freqs < 600))[0]
    modified_freqs[asthma_indices] += asthma_magnitude * slider_values[6]

    parkinsons_indices = np.where((freqs >= 600) &
                                 (freqs < 800))[0]
    modified_freqs[parkinsons_indices] += parkinsons_magnitude * slider_values[7]

    multiple_sclerosis_indices = np.where((freqs >= 800) &
                                        (freqs < 1000))[0]
    modified_freqs[multiple_sclerosis_indices] += multiple_sclerosis_magnitude * slider_values[8]

    cancer_indices = np.where(freqs >= 1000)[0]
    modified_freqs[cancer_indices] += cancer_magnitude * slider_values[9]

    # Inverse Fourier transform to get modified data
    modified_data = np.fft.irfft(modified_freqs)

    # Create a new wave file with the modified data
    modified_file = io.BytesIO()
    with wave.open(modified_file, 'wb') as wav:
        wav.setparams((1, 2, sample_rate, len(modified_data), 'NONE', 'not compressed'))
        wav.writeframes(np.array(modified_data * (2 ** 15 - 1), dtype=np.int16).tobytes())

    # Display the modified spectrogram
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
        wav_writer.writeframes(modified_data)
        wav_writer.close()
        st.audio(wav_file.getvalue(), format='audio/wav')

    plot_spectrogram(sample_rate, modified_data, freqs)
