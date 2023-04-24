import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal
import matplotlib.colors as colors
from matplotlib.animation import FuncAnimation
import io
import wave
import streamlit_vertical_slider  as svs


st.set_page_config(
    page_title="Equalizer",
    page_icon="./icons/equalizer.png",
    layout = "wide",
    initial_sidebar_state="expanded"
)

st.write("<p style='font-size:38px; text-align: center;'><b>Welcome to our website</b></p>", unsafe_allow_html=True)

def plot_spectrogram(uploaded_file):
    # Check if a file was uploaded
    if uploaded_file is not None:
        # Load the file data
        sample_rate, data = wavfile.read(uploaded_file)

        # Calculate the duration of the file
        duration = len(data) / sample_rate

        # Create a plot
        fig, ax = plt.subplots(1, 1, figsize=(8, 4))

        # Normalize the values in the spectrogram array
        spectrogram, freqs, bins, im = ax.specgram(data, Fs=sample_rate, cmap='viridis')

        # Set x and y limits of the spectrogram plot
        ax.set_xlim([0, duration])
        ax.set_ylim([0, max(freqs)])

        # Set the labels for the plot
        ax.set_xlabel("Time (s)", fontsize=12)
        ax.set_ylabel("Frequency (Hz)", fontsize=12)
        ax.set_title("Spectrogram", fontsize=12)

        # Display the plot
        st.pyplot(fig)



def plot_wav_file(uploaded_file, color):
    # Check if a file was uploaded
    if uploaded_file is not None:
        # Load the file data
        sample_rate, data = wavfile.read(uploaded_file)

        # Calculate the duration of the file
        duration = len(data) / sample_rate

        # Create a time axis
        time = np.linspace(0, duration, len(data))

        # Create a plot
        fig, ax = plt.subplots(1,1,figsize=(8, 4))
        ax.plot(time, data, color=color, linewidth=1.5, linestyle='-')

        # Set the plot title and labels
        ax.set_title("Uploaded WAV file")
        ax.set_xlabel("Time (s)", fontsize=12)
        ax.set_ylabel("Amplitude", fontsize=12)
        
        # Display the plot
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
        
        # plotting the spectrogram
        plot_spectrogram(uploaded_file)


def apply_filters(data, sample_rate, freq_range, slider_values):
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

    return modified_freqs


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
            slider = st.sidebar.slider(f"Frequency Range {i+1}", int(start_freq), int(end_freq), int((start_freq + end_freq) / 2))

            # Append the slider value to the list of slider values
            slider_values.append(slider)
        
        
        # Apply the frequency filters to the signal
        modified_freqs = apply_filters(data, sample_rate, freq_range, slider_values)

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
            wav_writer.writeframes(data)
            wav_writer.close()
            st.audio(wav_file.getvalue(), format='audio/wav')

        # Create a plot of the spectrogram
        fig, ax = plt.subplots(1, 1, figsize=(8, 4))
        # Normalize the values in the spectrogram array
        spectrogram, freqs, bins, im = ax.specgram(data, Fs=sample_rate, cmap='viridis')
        # Set x and y limits of the spectrogram plot
        ax.set_xlim([0, len(data)/sample_rate])
        ax.set_ylim([0, freq_range])
        # Set the labels for the plot
        ax.set_xlabel("Time (s)", fontsize=12)
        ax.set_ylabel("Frequency (Hz)", fontsize=12)
        ax.set_title("Spectrogram", fontsize=12)
        # Display the plot
        st.pyplot(fig)



# Divide the page into two columns
leftCol, rightCol = st.columns((1, 1), gap="small")

# uploading the files
uploadedFile = st.sidebar.file_uploader("Choose a CSV file1 📂 ")
color1 = st.sidebar.color_picker('Pick signal1 color', '#7B19E0')
color2 = st.sidebar.color_picker('Pick signal2 color', '#194AE0')
import streamlit as st

# Define the options for the dropdown menu
options = ['-','Uniform Range Mode', 'Vowels Mode', 'Musical Instruments Mode','Biological Signal Abnormalities']

# Add a dropdown menu to the sidebar
selected_option = st.sidebar.selectbox('Select an option:', options)

# Display the selected option
st.sidebar.write('You selected:', selected_option)

with leftCol:

    plot_wav_file(uploadedFile,color1)

with rightCol:
    if selected_option == "Uniform Range Mode":
        uniform_range_mode(uploadedFile,color2)

