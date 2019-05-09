from pathlib import Path
import os

def load_files(load_dir):

    files = os.listdir(load_dir)

    for i in range(len(files)):
        files[i] = os.path.join(load_dir,files[i])
    return files

def create_dataset(files, sequence_max_length=30, step=3):
    dataset = []
    for file in files:
        f = open(file,'r')
        f = f.read().split()
        f = ['start'] + f + ['stop'] #Add start and stop to mark when a song starts or ends

        dataset += f

    notes = list(dict.fromkeys(dataset))
    print("Total amount of unique symbols: ", len(notes))

    notes_indices = dict((c, i) for i, c in enumerate(notes))
    indices_notes = dict((i, c) for i, c in enumerate(notes))

    for i in range(len(dataset)):
        dataset[i] = notes_indices[dataset[i]]

    sequences = []   
    next_notes = []
    for i in range(0, len(dataset) - sequence_max_length, step):
        sequences.append(dataset[i: i+sequence_max_length])
        next_notes.append(dataset[i + sequence_max_length])
    
    print("Generated ", len(sequences), "sequences")


if __name__ == '__main__':
    data_dir = '/home/peter/classy/data/'
    complete_dir = os.path.join(data_dir,'composers/notewise/piano_solo/note_range38/sample_freq12/bach')
    print('The complete directory from where the files are loaded is ', complete_dir)

    train_path = os.path.join(data_dir,'train/')
    test_path = os.path.join(data_dir,'test/')
    
    files = load_files(complete_dir)
    print('Loaded %d files' % len(files))

    create_dataset(files)