import music21
'''
This code is inspired by Christine McLeavys midi encoder
https://github.com/mcleavey/musical-neural-net/blob/master/data/midi-to-encoding.py
'''

def translate_piece(path):
    sample_freq = 12
    note_range = 62
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

def main(path):
    translate_piece(path)
    return

if __name__ == "__main__":
    path = '../data/midi/Bach/Bwv1080\ The\ Art\ Of\ Fugue/Canon\ Fugue\ n1.mid'
    main(path)
