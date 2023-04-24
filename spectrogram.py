import streamlit as st
import matplotlib.pyplot as plt


def plot_spectrogram(sample_rate, data):
         
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
