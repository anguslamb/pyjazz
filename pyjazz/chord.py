from dataclasses import dataclass

@dataclass
class Quality:
    name: str
    voicings = []
    arpeggio = []


class Maj7(Quality):
    name = "MAJ7"
    voicings =  [(0, 4, 11, 14, 19), # A voicing
                 (0, 11, 16, 19, 26) # B voicing
    ]
    arpeggio = [0, 4, 7, 10]


class Dom7(Quality):
    name = "DOM7"
    voicings =  [(0, 4, 10, 14, 21), # A voicing
                 (0, 10, 16, 21, 26) # B voicing
    ]


class Min7(Quality):
    name = "MIN7"
    voicings =  [(0, 3, 10, 14, 19), # A voicing
                 (0, 10, 15, 19, 26) # B voicing
    ]


class Min7b5(Quality):
    name = "MIN7B5"
    voicings = [(0, 3, 10, 13, 18), # A voicing
                 (0, 10, 15, 18, 26) # B voicing
    ]


class Dim7(Quality):
    name = "DIM7"
    voicings = [(0, 3, 9, 14, 18), # A voicing
                 (0, 9, 15, 18, 26) # B voicing
    ]


class Chord:
    def __init__(self, root: int, quality: Quality):
        #0=A, 1=A# etc
        self.root = root
        self.quality = quality
 
        self.voicings = [tuple([self.root + interval for interval in voicing]) for voicing in quality.voicings]
        
    @classmethod
    def from_str(cls, chord: str) -> "Chord":
        root_str = chord[0]
        if chord[1] in ["b", "#"]:
            root_str += chord[1]
            quality_str = chord[2:]
        else:
            quality_str = chord[1:]
        
        note_str_to_int = {
            "A": 0, "A#": 1, "Bb": 1, "B": 2, "C":3, "C#":4, "Db":4, "D": 5, "D#":6, "Eb":6, "E":7, "F":8, "F#":9, 
            "Gb":9, "G":10, "G#":11, "Ab": 11}
        root = note_str_to_int[root_str]

        quality_str_to_class = {"MAJ7": Maj7, "MIN7": Min7, "DOM7": Dom7, "7": Dom7, "DIM7": Dim7, "MIN7B5": Min7b5}
        quality = quality_str_to_class[quality_str.upper()]
        return cls(root, quality)  