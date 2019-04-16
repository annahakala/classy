import music21
'''
This code is inspired by Christine McLeavys midi encoder
https://github.com/mcleavey/musical-neural-net/blob/master/data/midi-to-encoding.py
'''

def translate_piece(path):

    #Create music 21 midifile object
    mf = music21.midi.MidiFile()

    #Test if the file is corrupted
    try:
        mf.open(path)
        mf.read()
        mf.close()
    except:
        print("Skipping file: " + str(path) + " has bad formatting.")
        return

    #Try to translate the file to music21 stream
    try:
        midi_stream=music21.midi.translate.midiFileToStream(mf)
    except:
        print("Skipping file: translation of " + (str(path))+ " failed")
        return
