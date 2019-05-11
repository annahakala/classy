from pathlib import Path
import os
import random
import numpy as np


def load_files(load_dir):

    files = os.listdir(load_dir)

    for i in range(len(files)):
        files[i] = os.path.join(load_dir,files[i])
    return files

def create_dataset(files, train_data_amount=0.7, sequence_max_length=30, step=3):
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

    dataset += [SOS_token, EOS_token]
    notes = list(dict.fromkeys(dataset))
    print("Total amount of unique symbols: ", len(notes))

    notes_indices = dict((c, i) for i, c in enumerate(notes))
    indices_notes = dict((i, c) for i, c in enumerate(notes))

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

    return t_seqs_input, t_seqs_target, v_seqs_input, v_seqs_target, notes_indices, indices_notes