import music21


def writeMidi(stream, filename, output_folder):
    fp = stream.write('midi', fp=output_folder+str("/")+filename)
    return


def notewiseToStream(score, sample_freq, note_offset):
    speed = 1./sample_freq
    piano_notes = []
    time_offset = 0

    # Go through each note and determine its beginning and end and insert it to the music21 stream
    for i in range(len(score)):
        if score[i] in ["", " ", "<eos>", "<unk>"]:
            continue
        elif score[i][:3] == "end":
            continue
        elif score[i][:4] == "wait":
            time_offset += int(score[i][4:])
            continue
        # If the string is not empty, end or wait it has to be a note, now calculate the duration of this note and insert it to the stream
        else:
            duration = 1 # Duration has to be at least the minimum quantization
            has_end = False # If we don't find an end we will set a default duration
            note_string_len = len(score[i])

            for j in range(1,200):
                if i+j >= len(score): # We should not search outside the score or we get errors
                    break
                if score[i+j][:4] == "wait": # Add the length of a pause if we have one
                    duration += int(score[i+j][4:])
                if score[i+j][:3+note_string_len] == "end" + score[i] or score[i+j][:note_string_len] == score[i]:
                    has_end = True
                    break
            
            if not has_end:
                duration = 12
            
            
            try:
                new_note = music21.note.Note(int(score[i][1:])+note_offset)
                new_note.duration = music21.duration.Duration(duration*speed) # Duration depends on the sampling frequency (speed 1/f)
                new_note.offset = time_offset*speed # Set the position of the note in the stream
                
                piano_notes.append(new_note)
            except:
                print("Unkown note: " + str(score[i]))
    piano = music21.instrument.fromString("Piano")
    piano_notes.insert(0,piano)
    piano_stream = music21.stream.Stream(piano_notes)
    return piano_stream


def encodeToMidi(score, sample_freq, note_offset, fname):
    m21_stream = notewiseToStream(score, sample_freq, note_offset)
    #m21_stream.show("midi")
    filename = "testfile.mid"
    output_folder="tests"
    writeMidi(m21_stream, filename, output_folder)
    return 

if __name__ == "__main__":
    f = open('../data/composers/notewise/piano_solo/note_range62/sample_freq12/bach/bwv805.txt','r')
    score = f.read().split(" ")
    f.close()
    sample_freq = 12
    note_offset = 33
    fname = "test"

    encodeToMidi(score, sample_freq, note_offset, fname)

    