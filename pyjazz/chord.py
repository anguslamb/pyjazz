from dataclasses import dataclass

@dataclass
class Quality:
    name: str
    voicings = []
    arpeggio = []
    root_fifth = []

class Maj7(Quality):
    name = "MAJ7"
    voicings =  [(0, 4, 11, 14, 19), # A voicing
                 (0, 11, 16, 19, 26) # B voicing
    ]
    arpeggio = [0, 4, 7, 10]
    root_fifth = [0, 7]
class Dom7(Quality):
    name = "DOM7"
    voicings =  [(0, 4, 10, 14, 21), # A voicing
                 (0, 10, 16, 21, 26) # B voicing
    ]
    root_fifth = [0, 7]

class Min7(Quality):
    name = "MIN7"
    voicings =  [(0, 3, 10, 14, 19), # A voicing
                 (0, 10, 15, 19, 26) # B voicing
    ]
    root_fifth = [0, 7]

class Min7b5(Quality):
    name = "MIN7B5"
    voicings = [(0, 3, 10, 13, 18), # A voicing
                 (0, 10, 15, 18, 26) # B voicing
    ]
    root_fifth = [0, 6]

class Dim7(Quality):
    name = "DIM7"
    voicings = [(0, 3, 9, 14, 18), # A voicing
                 (0, 9, 15, 18, 26) # B voicing
    ]
    root_fifth = [0, 6]


class Chord:
    def __init__(self, root: int, quality: Quality):
        #0=A, 1=A# etc
        #TODO: note class?

        # Start from A octave below middle C
        self.root = 45 + root
        self.quality = quality
 
        self.voicings = [tuple([self.root + interval for interval in voicing]) for voicing in quality.voicings]
        self.root_fifth = [self.root + interval for interval in quality.root_fifth]
        
def str_to_chord(chord: str) -> Chord:
    root_str = chord[0]
    if chord[1] in ["b", "#"]:
        root_str += chord[1]
        quality_str = chord[2:]
    else:
        quality_str = chord[1:]
    
    note_str_to_int = {"A": 0, "A#": 1, "Bb": 1, "B": 2, "C":3, "C#":4, "Db":4, "D": 5, "D#":6, "Eb":6, "E":7, "F":8, "F#":9, "Gb":9, "G":10, "G#":11, "Ab": 11}
    root = note_str_to_int[root_str]

    quality_str_to_class = {"MAJ7": Maj7, "MIN7": Min7, "DOM7": Dom7, "7": Dom7, "DIM7": Dim7, "MIN7B5": Min7b5}
    quality = quality_str_to_class[quality_str.upper()]
    return Chord(root, quality)  