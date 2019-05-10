from pathlib import Path
import os
import random
import numpy as np

import torch
import torch.nn as nn
from torch import optim
import torch.nn.functional as F

def load_files(load_dir):

    files = os.listdir(load_dir)

    for i in range(len(files)):
        files[i] = os.path.join(load_dir,files[i])
    return files

def create_dataset(files, val_data_amount=0.3, sequence_max_length=30, step=3):
    """ Creates a dataset and splits it into training and validation data.
    Returns the training and validation datasets as well as the enumerations.
    @TODO maybe save the datasets to a folder instead of returning them
    """
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

    val_samples = int(val_data_amount*len(sequences))

    #Split the dataset into training and validation data

    sequences = np.array(sequences)
    np.random.shuffle(sequences)

    t_seqs = sequences[:val_samples]
    v_seqs = sequences[val_samples:]
    
    print("Split the dataset into ",len(t_seqs), " training samples and ", len(v_seqs), " validation samples.")

    return t_seqs, v_seqs, notes_indices, indices_notes


class Encoder(nn.Module):
    def __init__(self, dictionary_size, hidden_size):
        """
        Args:
          dictionary_size (int): Size of dictionary in the source language.
          hidden_size (int): Size of the hidden state.
        """
        super(Encoder, self).__init__()
        self.hidden_size = hidden_size
        self.embedding = nn.Embedding(dictionary_size, hidden_size)
        self.gru = nn.GRU(input_size=hidden_size, hidden_size=hidden_size)

    def forward(self, input_seq, hidden):
        """
        Args:
          input_seq (tensor):  Tensor of words (word indices) of the input sentence. The shape is
                               [seq_length, batch_size] with batch_size = 1.
          hidden (tensor):    The state of the GRU (shape [1, batch_size, hidden_size] with batch_size=1).

        Returns:
          output (tensor): Output of the GRU (shape [seq_length, 1, hidden_size]).
          hidden (tensor): New state of the GRU (shape [1, batch_size, hidden_size] with batch_size=1).
        """
        batch_size = input_seq.size(1)
        assert batch_size == 1, "Encoder can process only one sequence at a time."
        
        # YOUR CODE HERE
        embedded = self.embedding(input_seq)
        outputs, hidden = self.gru(embedded, hidden)

        return outputs, hidden

    def init_hidden(self):
        return torch.zeros(1, 1, self.hidden_size, device=device)

if __name__ == '__main__':
    """This is the stuff that should be done through the notebook, rest can be called I guess
    """

    data_dir = '/home/peter/classy/data/'
    complete_dir = os.path.join(data_dir,'composers/notewise/piano_solo/note_range38/sample_freq12/bach')
    train_path = os.path.join(data_dir,'train/')
    test_path = os.path.join(data_dir,'test/')

    val_data_amount = 0.3 #Rest will be training data

    print('The complete directory from where the files are loaded is ', complete_dir)

    files = load_files(complete_dir)
    print('Loaded %d files' % len(files))

    t_seqs, v_seqs, notes_indices, indices_notes = create_dataset(files, val_data_amount)

    skip_training = False
    device = torch.device("cpu")

hidden_size = 20
test_encoder = Encoder(dictionary_size=10, hidden_size=hidden_size).to(device)
