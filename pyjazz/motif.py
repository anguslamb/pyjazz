from pyjazz.note import Note

class Motif:
    def __init__(self, notes: list[Note], length: int, chords: list[str]):
        self.notes = notes
        #TODO enforce that actual motif length <= length
        self.length = length
        self.chords = chords

    def __getitem__(self, i: int) -> Note:
        return self.notes[i]

    @property
    def low(self) -> int:
        return min(note.pitch for note in self.notes)
    
    @property
    def high(self) -> int:
        return max(note.pitch for note in self.notes)

    def transpose(self, interval: int) -> None:
        for note in self.notes:
            note.transpose(interval)

    def move(self, interval: int) -> None:
        for note in self.notes:
            note.move(interval)

#TODO use quality objects here rather than chord strings?
MAJ7_UP = Motif(
    [
        Note(0, 0, 0.5),
        Note(4, 0.5, 0.5),
        Note(7, 1, 0.5),
        Note(11, 1.5, 0.5),
    ],
    2,
    ["MAJ7"]
)

MAJ7_DOWN = Motif(
    [
        Note(11, 0, 0.5),
        Note(7, 0.5, 0.5),
        Note(4, 1, 0.5),
        Note(0, 1.5, 0.5),
    ],
    2,
    ["MAJ7"]
)

MAJ7_UP_9 = Motif(
    [
        Note(4, 0, 0.5),
        Note(7, 0.5, 0.5),
        Note(11, 1, 0.5),
        Note(14, 1.5, 0.5),
    ],
    2,
    ["MAJ7"]
)

MAJ7_DOWN_9 = Motif(
    [
        Note(14, 0, 0.5),
        Note(11, 0.5, 0.5),
        Note(7, 1, 0.5),
        Note(4, 1.5, 0.5),
    ],
    2,
    ["MAJ7"]
)


DOM7_UP = Motif(
    [
        Note(0, 0, 0.5),
        Note(4, 0.5, 0.5),
        Note(7, 1, 0.5),
        Note(10, 1.5, 0.5),
    ],
    2,
    ["DOM7"]
)

DOM7_DOWN = Motif(
    [
        Note(10, 0, 0.5),
        Note(7, 0.5, 0.5),
        Note(4, 1, 0.5),
        Note(0, 1.5, 0.5),
    ],
    2,
    ["DOM7"]
)

DOM7_UP_9 = Motif(
    [
        Note(4, 0, 0.5),
        Note(7, 0.5, 0.5),
        Note(10, 1, 0.5),
        Note(14, 1.5, 0.5),
    ],
    2,
    ["DOM7"]
)

DOM7_DOWN_9 = Motif(
    [
        Note(14, 0, 0.5),
        Note(10, 0.5, 0.5),
        Note(7, 1, 0.5),
        Note(4, 1.5, 0.5),
    ],
    2,
    ["DOM7"]
)


MIN7_UP = Motif(
    [
        Note(0, 0, 0.5),
        Note(3, 0.5, 0.5),
        Note(7, 1, 0.5),
        Note(10, 1.5, 0.5),
    ],
    2,
    ["MIN7"]
)

MIN7_DOWN = Motif(
    [
        Note(10, 0, 0.5),
        Note(7, 0.5, 0.5),
        Note(3, 1, 0.5),
        Note(0, 1.5, 0.5),
    ],
    2,
    ["MIN7"]
)

MIN7_UP_9 = Motif(
    [
        Note(3, 0, 0.5),
        Note(7, 0.5, 0.5),
        Note(10, 1, 0.5),
        Note(14, 1.5, 0.5),
    ],
    2,
    ["MIN7"]
)

MIN7_DOWN_9 = Motif(
    [
        Note(14, 0, 0.5),
        Note(10, 0.5, 0.5),
        Note(7, 1, 0.5),
        Note(3, 1.5, 0.5),
    ],
    2,
    ["MIN7"]
)


MIN7B5_UP = Motif(
    [
        Note(0, 0, 0.5),
        Note(3, 0.5, 0.5),
        Note(6, 1, 0.5),
        Note(10, 1.5, 0.5),
    ],
    2,
    ["MIN7B5"]
)

MIN7B5_DOWN = Motif(
    [
        Note(10, 0, 0.5),
        Note(6, 0.5, 0.5),
        Note(3, 1, 0.5),
        Note(0, 1.5, 0.5),
    ],
    2,
    ["MIN7B5"]
)

MIN7B5_UP_9 = Motif(
    [
        Note(3, 0, 0.5),
        Note(6, 0.5, 0.5),
        Note(10, 1, 0.5),
        Note(13, 1.5, 0.5),
    ],
    2,
    ["MIN7B5"]
)

MIN7B5_DOWN_9 = Motif(
    [
        Note(13, 0, 0.5),
        Note(10, 0.5, 0.5),
        Note(6, 1, 0.5),
        Note(3, 1.5, 0.5),
    ],
    2,
    ["MIN7B5"]
)

MAJ_TRANE_UP = Motif(
    [
        Note(0, 0, 0.5),
        Note(2, 0.5, 0.5),
        Note(4, 1, 0.5),
        Note(7, 1.5, 0.5),
    ],
    2,
    ["MAJ7", "DOM7"]
)

MAJ_TRANE_DOWN = Motif(
    [
        Note(7, 0, 0.5),
        Note(4, 0.5, 0.5),
        Note(2, 1, 0.5),
        Note(0, 1.5, 0.5),
    ],
    2,
    ["MAJ7", "DOM7"]
)

MIN_TRANE_UP = Motif(
    [
        Note(0, 0, 0.5),
        Note(2, 0.5, 0.5),
        Note(3, 1, 0.5),
        Note(7, 1.5, 0.5),
    ],
    2,
    ["MIN7"]
)

MIN_TRANE_DOWN = Motif(
    [
        Note(7, 0, 0.5),
        Note(3, 0.5, 0.5),
        Note(2, 1, 0.5),
        Note(0, 1.5, 0.5),
    ],
    2,
    ["MIN7"]
)

DIM_TRANE_UP = Motif(
    [
        Note(0, 0, 0.5),
        Note(1, 0.5, 0.5),
        Note(3, 1, 0.5),
        Note(6, 1.5, 0.5),
    ],
    2,
    ["MIN7B5", "DIM7"]
)

DIM_TRANE_DOWN = Motif(
    [
        Note(6, 0, 0.5),
        Note(3, 0.5, 0.5),
        Note(1, 1, 0.5),
        Note(0, 1.5, 0.5),
    ],
    2,
    ["MIN7B5", "DIM7"]
)

motifs = [
    MAJ7_UP, MAJ7_DOWN, DOM7_UP, DOM7_DOWN, MIN7_UP, MIN7_DOWN, MIN7B5_UP, MIN7B5_DOWN,
    MAJ7_UP_9, MAJ7_DOWN_9, DOM7_UP_9, DOM7_DOWN_9, MIN7_UP_9, MIN7_DOWN_9, MIN7B5_UP_9, MIN7B5_DOWN_9,
    MAJ_TRANE_UP, MAJ_TRANE_DOWN, MIN_TRANE_UP, MIN_TRANE_DOWN, DIM_TRANE_UP, DIM_TRANE_DOWN
    ]
