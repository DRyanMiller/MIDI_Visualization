# MIDI_Visualization
Function for visualizing MIDI files from the MAESTRO dataset

# Explanation of Script and Data
This Python script is a function for visualizing MIDI data from the MAESTRO dataset. The MAESTRO dataset contains over 200 hours of piano performances from the International Piano-e-Competition. Participants in the competition perform on Yamaha Disklaviers, acoustic pianos that can also capture and playback Musical Instrument Digital Interface (MIDI) data. The MAESTRO dataset contains MIDI data from contestant performances as well as audio recordings of the performances.

Detailed instructions on how the script works can be found at 

# Using the Function
Below using this function, you will need to download the MIDI data from the [MAESTRO dataset website](https://magenta.tensorflow.org/datasets/maestro). Once the data is downloaded, you must choose a file to use. The following section outlines how to select a piece.

# Choosing a file
To choose a file to visualize, execute the following code in your Python environment. 

```import pandas as pd
files = pd.read_csv('https://storage.googleapis.com/magentadata/datasets/maestro/v2.0.0/maestro-v2.0.0.csv')
```

Once the CSV is read into Python, the following commands can be used to identify the composers in the dataset and the titles of the compositions, respectively

```files.canonical_composer.unique()
files.canonical_title.unique()
```

Once you have identified the piece you wish to visualize, you will need to locate the name of the MIDI file. Below is sample code for locating the MIDI file name for a performance of Mozart's Sonata in D Major.


```mozart_df = files[files.canonical_composer=='Wolfgang Amadeus Mozart']
mozart_df.canonical_title.unique()
mozart_sonataDMaj = mozart_df[mozart_df.canonical_title=='Sonata in D Major K576']
mozart_sonataDMaj.midi_filename.iloc[0]
```

The last step before creating your visualization is to create a string object with the path to the file name. Assign the string to the object file_name. Below is an example:

```file_path = "/Users/username/Desktop/maestro-v2.0.0/"
file_name = file_path + mozart_sonataDMaj.midi_filename.iloc[0]
```

# Calling the Function and Options
To call the function, simply open the script and give the following command:

```MAESTRO_midi_graph(file_name)
```

The MAESTRO_midi_graph function has several options that may be specified. The full function call is listed below.

```MAESTRO_midi_graph(file_name, plot_type='jointplot', axes_=False, 
                       palette='icefire', gridsize=88, figwidth=20, 
                       figheight=10)
```

The only plot types currently supported are 'jointplot' and 'kdeplot'. The axes_ option turns on and off the axis labels, tick labels, and marginal plots. The palette option can be set to any Seaborn supported palette. The gridsize changes the size of the hexagons in the jointplot. Figwidth and figheight set the width and height of the plot, respectively. 

