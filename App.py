import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import io
import wave
from spectrogram import *
from URM import *
from BIM import *
from MIM import *
from VM import *

st.set_page_config(
    page_title="Equalizer",
    page_icon="./icons/equalizer.png",
    layout = "wide",
    initial_sidebar_state="expanded"
)

st.write("<p style='font-size:38px; text-align: center;'><b>Welcome to our website</b></p>", unsafe_allow_html=True)


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
        plot_spectrogram(sample_rate,data)


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
    if selected_option == "vowels Mode":
        vowels_mode(uploadedFile,color2)
    if selected_option == "Musical Instruments Mode":
        musical_instruments_mode(uploadedFile,color2)
    if selected_option == "Biological Instruments Mode":
        if uploadedFile:
            apply_abnormalities(uploadedFile,color2)