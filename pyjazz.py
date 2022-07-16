from typing import List, Tuple

from midiutil.MidiFile import MIDIFile

from chord import str_to_chord
from song import Song

# create your MIDI object
mf = MIDIFile(3) 
track = 0
solo_track = 1
solo_channel = 1
bass_track = 2
bass_channel = 2

tempo = 240
time = 0 
mf.addTrackName(track, time, "Sample Track")
mf.addTempo(track, time, tempo)

mf.addTrackName(solo_track, time, "Solo Track")
mf.addTempo(solo_track, time, tempo)

mf.addTrackName(bass_track, time, "Bass Track")
mf.addTempo(bass_track, time, tempo)

mf.addProgramChange(tracknum=1, channel=1, time=0, program=66)
mf.addProgramChange(tracknum=2, channel=2, time=0, program=33)

channel = 0
volume = 100

from random import choice

class Solo:

    def __init__(self, song):
        self.song = song
        self.prev_note = None

    def choose_note(self, chord):
        chord = str_to_chord(chord)  # TODO factor into chord? define what these interfaces should be (chords/voicings etc)
        notes = []
        list(map(notes.extend, chord.voicings)) # need list here to make it actually evaluate?
        notes = list(set(notes))
        # TODO separate arpeggio or something to give dense collection of all allowed notes for solo purposes
        # maybe add a get_candidate_notes() method that gets all viable notes in a permitted range?
        #notes = [note + 12 for note in notes]
        notes.extend([i+12 for i in notes])
        notes = list(set(notes))

        if self.prev_note is None:
            note_choice = choice(notes)
        else:
            note_distances = [(note, abs(note-self.prev_note)) for note in notes if abs(note-self.prev_note) != 0] 
            note_distances.sort(key=lambda x: x[1])
            note_choice= choice([note_distances[0][0], note_distances[1][0], note_distances[2][0]])
        return note_choice

    def play_solo(self, midi_file, solo_track, solo_channel):  # num_repeats could be factored into song
        solo = []
        position = 0
        while position < self.song.total_length:
            chord = self.song.get_current_chord(position)
            note = self.choose_note(chord)
            if position // 2 == 0:
                duration = 0.5
            else:
                duration = choice([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 2])  # can add method here for new policies
            #duration = choice([0.25, 0.5, 0.75, 1])
            solo.append((note, duration))
            self.prev_note = note
            position += duration

        position = 0
        for note, duration in solo:
            midi_file.addNote(solo_track, solo_channel, note, position, duration, volume)
            position += duration

class Bassline:

    def __init__(self, song):
        self.song = song
        self.prev_note = None

    def choose_note(self, chord):
        chord = str_to_chord(chord)  # TODO factor into chord? define what these interfaces should be (chords/voicings etc)
        notes = [i-12 for i in chord.root_fifth] + chord.root_fifth

        if self.prev_note is None:
            note_choice = notes[0]
        else:
            note_distances = [(note, abs(note-self.prev_note)) for note in notes if abs(note-self.prev_note) != 0] 
            note_distances.sort(key=lambda x: x[1])
            note_choice= choice([note_distances[0][0], note_distances[1][0], note_distances[2][0]])
        return note_choice

    def play_bassline(self, midi_file, bass_track, bass_channel):  # num_repeats could be factored into song
        bassline = []
        position = 0
        while position < self.song.total_length:
            chord = self.song.get_current_chord(position)
            note = self.choose_note(chord)
            duration = 1  # can add method here for new policies
            bassline.append((note, duration))
            self.prev_note = note
            position += duration

        position = 0
        for note, duration in bassline:
            midi_file.addNote(bass_track, bass_channel, note, position, duration, volume)
            position += duration

class Comping:

    def __init__(self, song):
        self.song = song
        self.prev_voicing = None

    @staticmethod
    def voicing_distance(voicing1, voicing2):  #rename to voicing?
        return abs(voicing1[-1] - voicing2[-1])

    def choose_voicing(self, chord):
        chord = str_to_chord(chord)  # TODO factor into chord? define what these interfaces should be (chords/voicings etc)
        if self.prev_voicing == None:
            voicing = choice(chord.voicings)
        else:
            voicing_distances = [(voicing, self.voicing_distance(voicing, self.prev_voicing)) for voicing in chord.voicings]
            voicing_distances.sort(key=lambda x: x[1])
            voicing = voicing_distances[0][0]

        return voicing

    def play_comping(self, midi_file, comping_track, comping_channel):
        comping = []
        position = 0
        while position < self.song.total_length:
            chord = self.song.get_current_chord(position)
            voicing = self.choose_voicing(chord)
            # TODO default to full length of chord
            duration = self.song.get_duration_remaining(position)  # can add method here for new policies
            comping.append((voicing, duration))
            self.prev_voicing = voicing
            position += duration

        position = 0
        for voicing, duration in comping:
            for note in voicing:
                midi_file.addNote(comping_track, comping_channel, note, position, duration, volume)
            position += duration
         
    
giant_steps_chords = [("BMaj7", 2), ("D7", 2), ("GMaj7", 2), ("Bb7", 2), ("EbMaj7", 4), ("AMin7", 2), ("D7", 2), 
        ("GMaj7", 2), ("Bb7", 2), ("EbMaj7", 2), ("F#7", 2), ("BMaj7", 4), ("FMin7", 2), ("Bb7", 2), 
        ("EbMaj7", 4), ("AMin7", 2), ("D7", 2), ("GMaj7", 4), ("C#Min7", 2), ("F#7", 2), 
        ("BMaj7", 4), ("FMin7", 2), ("Bb7", 2), ("EbMaj7", 4), ("C#Min7", 2), ("F#7", 2), 
]

autumn_leaves_chords = [
    ("AMin7", 4), ("D7", 4), ("GMaj7", 4), ("CMaj7", 4),
    ("F#Min7b5", 4), ("B7", 4), ("EMin7", 8)
    ]


giant_steps = Song(giant_steps_chords, repeats=2)

def perform(song, mf):
    comping_track = 0  #TODO these are defined at the top, pass them as args?
    comping_channel = 0
    comping = Comping(song)
    comping.play_comping(mf, comping_track, comping_channel)

    solo_track = 1  
    solo_channel = 1
    solo = Solo(song)
    solo.play_solo(mf, solo_track, solo_channel)

    bass_track = 2 
    bass_channel = 2
    bassline = Bassline(song)
    bassline.play_bassline(mf, bass_track, bass_channel)

perform(giant_steps, mf)

with open("output.mid", 'wb') as outf:
    mf.writeFile(outf)

# def play_song(song: List[Tuple[str, int]], num_repeats=2):
#     curr_time = 0
#     prev_voicing = None
#     prev_note = None
#     prev_bass_note = None
#     for _ in range(num_repeats):
#         for (chord_str, duration) in song:
#             chord = str_to_chord(chord_str)
#             prev_voicing = play_chord(chord, curr_time, duration, prev_voicing)
#             prev_note = play_solo(chord, curr_time, duration, note_length=0.5, prev_note=prev_note)
#             prev_bass_note = play_bassline(chord, curr_time, duration, note_length=1, prev_note=prev_bass_note)
#             curr_time += duration


   

# def play_chord(chord, time, duration, prev_voicing=None):
#     if prev_voicing == None:
#         voicing = choice(chord.voicings)
#     else:
#         voicing_distances = [(voicing, chord_distance(voicing, prev_voicing)) for voicing in chord.voicings]
#         voicing_distances.sort(key=lambda x: x[1])
#         voicing = voicing_distances[0][0]
        
#     for note in voicing:
#         mf.addNote(track, channel, note, time, duration, volume)
#     return voicing


# def play_solo(chord, start_time, duration, note_length=0.5, prev_note=None):
#     notes = []
#     list(map(notes.extend, chord.voicings)) # need list here to make it actually evaluate?
#     notes = list(set(notes))
#     # TODO separate arpeggio or something to give dense collection of all allowed notes for solo purposes
#     # maybe add a get_candidate_notes() method that gets all viable notes in a permitted range?
#     #notes = [note + 12 for note in notes]
#     notes.extend([i+12 for i in notes])
#     notes = list(set(notes))
#     solo = []
#     num_notes = int(duration//note_length)
#     for _ in range(num_notes):
#         if prev_note == None:
#             note_choice = choice(notes)
#         else:
#             note_distances = [(note, abs(note-prev_note)) for note in notes if abs(note-prev_note) != 0] 
#             note_distances.sort(key=lambda x: x[1])
#             note_choice= choice([note_distances[0][0], note_distances[1][0], note_distances[2][0]])
#             #can you use walrus to assign for conditional target in list comp?
#         solo.append(note_choice)
#         prev_note = note_choice
#     for idx, note in enumerate(solo):
#         time = start_time + (note_length * idx)
#         note_duration = 0.5
#         mf.addNote(solo_track, solo_channel, note, time, note_duration, volume)
#     return prev_note
   
# def play_bassline(chord, start_time, duration, note_length=1, prev_note=None):
#     notes = [i-12 for i in chord.root_fifth] + chord.root_fifth
#     bassline = []
#     num_notes = int(duration//note_length)
#     for _ in range(num_notes):
#         if prev_note == None:
#             note_choice = notes[0]
#         else:
#             note_distances = [(note, abs(note-prev_note)) for note in notes if abs(note-prev_note) != 0] 
#             note_distances.sort(key=lambda x: x[1])
#             note_choice= choice([note_distances[0][0], note_distances[1][0]])
#         bassline.append(note_choice)
#         prev_note = note_choice
#     for idx, note in enumerate(bassline):
#         time = start_time + (note_length * idx)
#         note_duration = 0.5
#         mf.addNote(bass_track, bass_channel, note, time, note_duration, volume)
#     return prev_note
    