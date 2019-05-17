from pathlib import Path
import os
import random
import numpy as np
import pickle

SOS_token="SOS"
EOS_token="EOS"

def load_files(load_dir):

    files = os.listdir(load_dir)

    for i in range(len(files)):
        files[i] = os.path.join(load_dir,files[i])
    return files

def generate_dictionaries(files, SOS_token="SOS", EOS_token="EOS"):
    ''' Creates a dictionary of notes to indices and vice versa
    Args:
    files (list): A list locations of files with notes to index
    SOS_token (string): The start of sequence token
    EOS_token (string): The end of sequence token
    
    Returns:
    notes_indices (dict): Mapping from notes to indices
    indices_notes (dict): Mapping from indices to notes
    '''
    ni_dir = "dicts/notes_indices.pickle"
    in_dir = "dicts/indices_notes.pickle"

    if os.path.exists(ni_dir) or os.path.exists(in_dir):
        overwrite = input("Warning: a dictionary with this name aldready exists, are you sure you want to wipe it? All models trained with the old dictioanry will be useless (yes/no)")
        if overwrite != "yes":
            return

    dataset = []
    for file in files:
        f = open(file,'r')
        f = f.read().split()
        #f = ['start'] + f + ['stop'] #Add start and stop to mark when a song starts or ends

        dataset += f

    dataset += [SOS_token, EOS_token]
    notes = list(dict.fromkeys(dataset))

    print("Total amount of unique symbols: ", len(notes))

    notes_indices = dict((c, i) for i, c in enumerate(notes))
    indices_notes = dict((i, c) for i, c in enumerate(notes))

    pickle_out_1 = open(ni_dir,'wb+')
    pickle_out_2 = open(in_dir,'wb+')

    pickle.dump(notes_indices, pickle_out_1)
    pickle.dump(indices_notes, pickle_out_2)

    pickle_out_1.close()
    pickle_out_2.close()

    return notes_indices, indices_notes

def create_dataset(files, ni_dict, in_dict, train_data_amount=0.7, sequence_max_length=30, step=3):
    """ Creates a dataset and splits it into training and validation data.
    Returns the training and validation datasets as well as the enumerations.
    @TODO maybe save the datasets to a folder instead of returning them
    """
    dataset = []
    for file in files:
        f = open(file,'r')
        f = f.read().split()
        #f = ['start'] + f + ['stop'] #Add start and stop to mark when a song starts or ends

        dataset += f

    pickle_in_1 = open(ni_dict,"rb")
    pickle_in_2 = open(in_dict,"rb")

    notes_indices = pickle.load(pickle_in_1)
    indices_notes = pickle.load(pickle_in_2)

    for i in range(len(dataset)):
        dataset[i] = notes_indices[dataset[i]]

    sequences = []   
    next_notes = []

    SOS_ind = notes_indices[SOS_token]
    EOS_ind = notes_indices[EOS_token]

    for i in range(0, len(dataset) - sequence_max_length, step):
        sequences.append([SOS_ind] + dataset[i: i+sequence_max_length] + [EOS_ind])
        next_notes.append([SOS_ind, dataset[i + sequence_max_length], EOS_ind])

    print("Generated ", len(sequences), "sequences")

    t_samples = int(train_data_amount*len(sequences))

    #Split the dataset into training and validation data

    sequences = np.array(sequences)
    np.random.shuffle(sequences)

    t_seqs_input = sequences[:t_samples]
    t_seqs_target = next_notes[:t_samples]

    v_seqs_input = sequences[t_samples:]
    v_seqs_target = next_notes[t_samples:]
    
    print("Split the dataset into ",len(t_seqs_input), " training samples and ", len(v_seqs_input), " validation samples.")

    return t_seqs_input, t_seqs_target, v_seqs_input, v_seqs_target