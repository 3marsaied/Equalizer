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

        # Create a spectrogram
        freqs, times, spectrogram = signal.spectrogram(data, sample_rate)

        # Create a time axis
        time = np.linspace(0, duration, len(data))

        # Create a plot
        fig, ax = plt.subplots(1, 1)

        ax.plot(time, data, 'b-', linewidth=3)
        ax.grid()
        ax.set_facecolor(ax.get_facecolor())

        # Set the plot title and labels
        font1 = {'family': 'serif', 'color': 'white', 'size': 20}
        ax.set_xlabel("Time (s)", fontsize=12, fontdict=font1)
        ax.set_ylabel("Amplitude", fontsize=12, fontdict=font1)

        # Display the plot
        line = ax.plot(time, data, color=color, linewidth=3)[0]
        st.plotly_chart(fig, use_container_width=True)

        # Create an audio player widget
        with io.BytesIO() as wav_file:
            wav_writer = wave.open(wav_file, "wb")
            wav_writer.setnchannels(1)
            wav_writer.setsampwidth(2)
            wav_writer.setframerate(sample_rate)
            wav_writer.writeframes(data)
            wav_writer.close()
            st.audio(wav_file.getvalue(), format='audio/wav')

        
        # Define the function to update the plot in real-time
        def update_plot(frame):
            line.set_ydata(data[frame])
            return line,

        # Define the animation
        frames = len(data)
        interval = 1000 / sample_rate
        animation = FuncAnimation(fig, update_plot, frames=frames, interval=interval, blit=True)
        
        # plotting the spectrogram
        plot_spectrogram(uploaded_file)



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


if uploadedFile:
    st.write("<p style='font-size:20px;'>Adjust the parameters:</p>", unsafe_allow_html=True)
    cols = st.columns(10)

    for i in range(10):
        with cols[i%10]:
            st.write(f"<h3>Slider {i+1}</h3>", unsafe_allow_html=True)
            svs.vertical_slider(
            key=f"slider_{i}",
            default_value=50,
            min_value=0,
            max_value=100,
            step=1,
            slider_color="blue",
            track_color="lightgray",
            thumb_color="red",)