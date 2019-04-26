# classy

## Classy project
Classy is a neural network that uses RNN:s to generate classical music.

The project is done as a part of the Deep Learning course at Aalto University and is inspired by Christine Mcleavys Musical Neural net https://github.com/mcleavey/musical-neural-net

## Quick start
* Install the dependencies in requirements.txt e.g. by running
>> pip install -r requirements.txt

* Set the environment paths for music21 if you want to view scores and play music directly from music21 (optional)
* Scrape a lot of midis e.g. by using classicalarchives and BeautifulSoup. I created a script for it, see the section "Get midis"
* Encode the midis into text format, see Midi encoding section

## Get started with music 21
Music21 is used to decode and encode midis
https://web.mit.edu/music21/doc/usersGuide/usersGuide_02_notes.html#usersguide-02-notes

To play midi files you need to set the path to your midi-player e.g.
>> environment.set('midiPath', '/usr/bin/timidity')

To view scores install a software e.g. musescore and set the path e.g.
>> environment.set('musicxmlPath', '/usr/bin/musescore')

## Get midis
A list of links to midis are genereated Classicalarchives with midi_parser/get_midi_links.py and then downloaded with the command
>> cat midi_links | xargs wget

## Midi encoding
We use Christine Mcleacys midi-to-encoding.py to make the midis readable.

The midi-encoder creates several encoded versions of the same midi with slightly different encoding depending on the sampling frequency and the note ranges.

### Chord- and notewise
We can represent the midis in two ways, either by representing each timestep as a chord that defines which notes are played at that instance. e.g. p00000000002000000000000000200202000000000000000000000000000000. This is called **chordwise.**

The **notewise** representation defines start and stop times for each note and pause respectively. e.g. p40 wait6 p28 p32 wait5 endp40

### Sampling frequency
Sampling frequency defines how many samples are taken per quarter note. The higher frequency the more accurate the text representation will be.

### Note range
The range from lowest to highest note. If a note in the midi is too high or too low it will get transposed one octave up or down.

See this link for an in-depth explanation https://github.com/mcleavey/musical-neural-net/blob/master/data/README.md

## How to play midis
The easiest solution seems to be to install timidity



## TODO
### Done
* Script to scrape midis (24.4.)
* Encode midis to text-format (24.4.)
### Not Done
* Decode text-format back to midis
* Look into how to implement the RNN
* Clean up readme/documentation
