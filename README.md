# classy

## Get started with music 21
https://web.mit.edu/music21/doc/usersGuide/usersGuide_02_notes.html#usersguide-02-notes

To play midi files you need to set the path to your midi-player e.g.
>> environment.set('midiPath', '/usr/bin/timidity')

To view scores install a software e.g. musescore and set the path e.g.
>> environment.set('musicxmlPath', '/usr/bin/musescore')

## Get midis
A list of links to midis are genereated Classicalarchives with midi_parser/get_midi_links.py and then downloaded with the command >> cat midi_links | xargs wget

## Encode midis
We use Christine Mcleacys midi-to-encoding.py to make the midis readable.
