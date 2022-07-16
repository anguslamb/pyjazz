class Song:

    def __init__(self, chords, repeats):
        self.chords = chords
        self.repeats = repeats
        self.song_length = sum(x[1] for x in self.chords)
        self.total_length = self.song_length * self.repeats

        self.chord_starts_stops = [[chord, 0, 0] for chord, _ in self.chords]
        for i in range(1, len(self.chords)):
            self.chord_starts_stops[i][1] = self.chord_starts_stops[i-1][1] + self.chords[i-1][1]
            
        for i in range(len(self.chords)):
            self.chord_starts_stops[i][2] = self.chord_starts_stops[i][1] + self.chords[i][1]

    def get_current_chord(self, time):
        time = time % self.song_length
        return(next(i[0] for i in self.chord_starts_stops if time < i[2]))

    def get_duration_remaining(self, time):
        time = time % self.song_length
        return(next(i[2]-time for i in self.chord_starts_stops if time < i[2]))
