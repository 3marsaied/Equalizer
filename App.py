import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal
import matplotlib.colors as colors


st.set_page_config(
    page_title="Equalizer",
    page_icon="./icons/equalizer.png",
    layout = "wide",
    initial_sidebar_state="expanded"
)

st.write("<p style='font-size:38px; text-align: center;'><b>Welcome to our website</b></p>", unsafe_allow_html=True)
# plt.style.use('bmh')

def plot_wav_file(uploaded_file,color):
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
       
        # Create the figure and axes objects
        fig2, ax2 = plt.subplots(figsize=(8, 4))

        # Normalize the values in the spectrogram array
        norm = colors.Normalize(vmin=spectrogram.min(), vmax=spectrogram.max())


        ax.plot(time, data, 'b-', linewidth=3)
        ax.grid()
        ax.set_facecolor(ax.get_facecolor())
        # Set the plot title and labels
        font1 = {'family':'serif','color':'white','size':20}
        ax.set_xlabel("Time (s)", fontsize=12, fontdict=font1)
        ax.set_ylabel("Amplitude", fontsize=12, fontdict=font1)
        
        # Display the plot
        ax.plot(time,data,color=color,linewidth=3)
        st.plotly_chart(fig,use_container_width=True)
        

        # Plot the spectrogram with the normalized values
        ax2.pcolormesh(times, freqs, spectrogram, cmap='viridis', norm=norm)

        ax2.set_facecolor('white')
        ax2.set_ylabel("Frequency (Hz)", fontsize=12)
        ax2.set_xlabel("Time (s)", fontsize=12)
        ax2.set_title("Spectrogram", fontsize=12)
        ax2.grid()

        # Display the plot
        st.pyplot(fig2)



# Divide the page into two columns
leftCol, rightCol = st.columns((1, 1), gap="small")

    
# Divide the page into 4 containers (rows)
row1 = st.container()
row2 = st.container()
row3 = st.container()
row4 = st.container()

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

