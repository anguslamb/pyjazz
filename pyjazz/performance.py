from typing import List, Tuple

from midiutil.MidiFile import MIDIFile
from abc import ABC
from pyjazz.chord import str_to_chord
from pyjazz.song import Song
from random import choice
import logging

logger = logging.getLogger(__name__)
class Performance(ABC):
    channel = 0
    def __init__(self, song: Song, volume: int = 100) -> None:
        self.song = song
        self.volume = volume
        self.prev = None

    def choose_note(self, chord):
        pass

    def play(self, midi_file, track):
        pass
class Solo(Performance):

    def choose_note(self, chord):
        chord = str_to_chord(chord)  # TODO factor into chord? define what these interfaces should be (chords/voicings etc)
        notes = []
        list(map(notes.extend, chord.voicings))
        notes = list(set(notes))
        # TODO separate arpeggio or something to give dense collection of all allowed notes for solo purposes
        # maybe add a get_candidate_notes() method that gets all viable notes in a permitted range?
        #notes = [note + 12 for note in notes]
        notes.extend([i+12 for i in notes])
        notes = list(set(notes))

        if self.prev is None:
            note_choice = choice(notes)
        else:
            note_distances = [(note, abs(note-self.prev)) for note in notes if abs(note-self.prev) != 0] 
            note_distances.sort(key=lambda x: x[1])
            note_choice= choice([note_distances[0][0], note_distances[1][0], note_distances[2][0]])
        return note_choice

    def play(self, midi_file, track):  # num_repeats could be factored into song
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
            self.prev = note
            position += duration

        position = 0
        for note, duration in solo:
            midi_file.addNote(track, self.channel, note, position, duration, self.volume)
            position += duration

class Bassline(Performance):

    def choose_note(self, chord):
        chord = str_to_chord(chord)  # TODO factor into chord? define what these interfaces should be (chords/voicings etc)
        notes = [i-12 for i in chord.root_fifth] + chord.root_fifth

        if self.prev is None:
            note_choice = notes[0]
        else:
            note_distances = [(note, abs(note-self.prev)) for note in notes if abs(note-self.prev) != 0] 
            note_distances.sort(key=lambda x: x[1])
            note_choice= choice([note_distances[0][0], note_distances[1][0], note_distances[2][0]])
        return note_choice

    def play(self, midi_file, track):  # num_repeats could be factored into song
        bassline = []
        position = 0
        while position < self.song.total_length:
            chord = self.song.get_current_chord(position)
            note = self.choose_note(chord)
            duration = 1  # can add method here for new policies
            bassline.append((note, duration))
            self.prev = note
            position += duration

        position = 0
        for note, duration in bassline:
            logger.debug(f"writing bass to track {track}")
            midi_file.addNote(track, self.channel, note, position, duration, self.volume)
            position += duration

class Comping(Performance):

    @staticmethod
    def voicing_distance(voicing1, voicing2):  #rename to voicing?
        return abs(voicing1[-1] - voicing2[-1])

    def choose_voicing(self, chord):
        chord = str_to_chord(chord)  # TODO factor into chord? define what these interfaces should be (chords/voicings etc)
        if self.prev == None:
            voicing = choice(chord.voicings)
        else:
            voicing_distances = [(voicing, self.voicing_distance(voicing, self.prev)) for voicing in chord.voicings]
            voicing_distances.sort(key=lambda x: x[1])
            voicing = voicing_distances[0][0]

        return voicing

    def play(self, midi_file, track):
        comping = []
        position = 0
        while position < self.song.total_length:
            chord = self.song.get_current_chord(position)
            voicing = self.choose_voicing(chord)
            # TODO default to full length of chord
            duration = self.song.get_duration_remaining(position)  # can add method here for new policies
            comping.append((voicing, duration))
            self.prev = voicing
            position += duration

        position = 0
        for voicing, duration in comping:
            for note in voicing:
                midi_file.addNote(track, self.channel, note, position, duration, self.volume)
            position += duration

class Drums(Performance):
    channel = 9
    def choose_note(self, chord):
        chord = str_to_chord(chord)  # TODO factor into chord? define what these interfaces should be (chords/voicings etc)
        notes = []
        list(map(notes.extend, chord.voicings))
        notes = list(set(notes))
        # TODO separate arpeggio or something to give dense collection of all allowed notes for solo purposes
        # maybe add a get_candidate_notes() method that gets all viable notes in a permitted range?
        #notes = [note + 12 for note in notes]
        notes.extend([i+12 for i in notes])
        notes = list(set(notes))

        if self.prev is None:
            note_choice = choice(notes)
        else:
            note_distances = [(note, abs(note-self.prev)) for note in notes if abs(note-self.prev) != 0] 
            note_distances.sort(key=lambda x: x[1])
            note_choice= choice([note_distances[0][0], note_distances[1][0], note_distances[2][0]])
        return note_choice

    def play(self, midi_file, track):  # num_repeats could be factored into song
        # Ride
        # TODO probably easiest to replace patterns with simple lists of (position, note, duration) tuples/dataclasses
        pattern = [1, 2/3, 1/3]
        note = 51
        position = 0
        for i in range(self.song.total_length // 2):
            position = i * 2  # snap to start of bar in case of accumulated floating point rounding errors
            for j, duration in enumerate(pattern):
                midi_file.addNote(track=track, channel=self.channel, pitch=note, time=position, duration=duration, volume=self.volume)
                # TODO remove this ugly hack
                if j == 0:
                    midi_file.addNote(track=track, channel=self.channel, pitch=35, time=position, duration=duration, volume=self.volume)
                elif j == 1:
                    midi_file.addNote(track=track, channel=self.channel, pitch=44, time=position, duration=duration, volume=self.volume)
                position += duration
                


            