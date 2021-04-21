#!/usr/bin/env python
# coding: utf-8


import parselmouth
import numpy as np
import streamlit as st
import pandas as pd
import plotly
import plotly.graph_objs as go
import plotly.offline as pyo
import plotly.express as px

st.title('Spectrogram')
#waveform = pd.DataFrame({"Amplitude": sound.values[0].T})
#st.line_chart(waveform)

# Load sound into Praat
sound = parselmouth.Sound("03-01-01-01-01-01-01.wav")

named_colorscales = px.colors.named_colorscales()

def draw_spectrogram(spectrogram, vmin, vmax):
    X, Y = spectrogram.x_grid(), spectrogram.y_grid()
    sg_db = 10 * np.log10(spectrogram.values)
    # Plot with plotly
    data = [go.Heatmap(x=X, y=Y, z=sg_db, zmin=vmin, zmax= vmax, colorscale=colours,)]
    layout = go.Layout(
        title='Spectrogram',
        yaxis=dict(title='Frequency (Hz)'),
        xaxis=dict(title='Time (s)'),
    )
    fig = go.Figure(data=data, layout=layout)
    st.plotly_chart(fig)


# Side Bar #######################################################
nyquist_frequency = int(sound.sampling_frequency/2)
maximum_frequency = st.sidebar.slider('Maximum frequency (Hz)', 5000, nyquist_frequency, 5500)

default_ix = named_colorscales.index('turbo')
colours = st.sidebar.selectbox(('Choose a colour pallete'), named_colorscales, index=default_ix)
dynamic_range = st.sidebar.slider('Dynamic Range (dB)', 10, 100, 75)
window_length = st.sidebar.slider('Window length (s)', 0.005, 0.05, 0.05)

# App ##################################################
# Load sound into Praat
sound = parselmouth.Sound("03-01-01-01-01-01-01.wav")
sound.pre_emphasize()

spectrogram = sound.to_spectrogram(window_length=window_length, maximum_frequency=maximum_frequency)
sg_db = 10 * np.log10(spectrogram.values)
vmin = sg_db.max() - dynamic_range
vmax = sg_db.max() #+ dynamic_range
draw_spectrogram(spectrogram, vmin, vmax)
