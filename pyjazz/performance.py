from typing import List, Tuple

from midiutil.MidiFile import MIDIFile
from abc import ABC
from pyjazz.chord import str_to_chord
from pyjazz.song import Song
from random import choice
import logging
from pyjazz.motif import motifs, Motif
from copy import deepcopy
from chord import Chord
logger = logging.getLogger(__name__)

class Performance(ABC):
    channel = 0
    def __init__(self, song: Song, volume: int = 100) -> None:
        self.song = song
        self.volume = volume
        self.prev = None

    def write_to_midi(self, midi_file, track) -> None:
        raise NotImplementedError

class Solo(Performance):
    def __init__(self, song: Song, volume: int = 100) -> None:
        super().__init__(song, volume)

        self.motifs = []
        position = 0
        while position < self.song.total_length:
            #TODO this fn should return a Chord object
            chord = str_to_chord(self.song.get_current_chord(position))
            motif = self._choose_motif(chord)
            #TODO remove implicit octave change in current chord root
            motif.transpose(chord.root)
            motif.move(position)
            self.motifs.append(motif)
            self.prev = motif
            position += motif.length

    
    def write_to_midi(self, midi_file, track) -> None:
        for motif in self.motifs:
            for note in motif:
                midi_file.addNote(track, self.channel, note.pitch, note.position, note.duration, note.volume)


    def _choose_note(self, chord):
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
    
    def _choose_motif(self, chord: Chord) -> Motif:
        quality_str = chord.quality.name
   
        #TODO find some way of returning new instances of a particular motif so that we don't have to copy here
        valid_motifs = [deepcopy(m) for m in motifs if quality_str in m.chords]
        for motif in valid_motifs:
            motif.transpose(12)
        octave_up_motifs = [deepcopy(m) for m in valid_motifs]
        #TODO make transpose, move etc classmethods that return a new, modified instance of the motif
        for motif in octave_up_motifs:
            motif.transpose(12)
        valid_motifs.extend(octave_up_motifs)
        motif = choice(valid_motifs)

        return motif


class Bassline(Performance):
    def __init__(self, song: Song, volume: int = 100) -> None:
        super().__init__(song, volume)
        self.notes = []
        position = 0
        while position < self.song.total_length:
            chord = self.song.get_current_chord(position)
            note = self._choose_note(chord)
            duration = 1  # can add method here for new policies
            self.notes.append((note, duration))
            self.prev = note
            position += duration
        
    def write_to_midi(self, midi_file, track) -> None:
        position = 0
        for note, duration in self.notes:
            midi_file.addNote(track, self.channel, note, position, duration, self.volume)
            position += duration

    def _choose_note(self, chord):
        chord = str_to_chord(chord)  # TODO factor into chord? define what these interfaces should be (chords/voicings etc)
        notes = [i-12 for i in chord.root_fifth] + chord.root_fifth

        if self.prev is None:
            note_choice = notes[0]
        else:
            note_distances = [(note, abs(note-self.prev)) for note in notes if abs(note-self.prev) != 0] 
            note_distances.sort(key=lambda x: x[1])
            note_choice= choice([note_distances[0][0], note_distances[1][0], note_distances[2][0]])
        return note_choice


class Comping(Performance):
    def __init__(self, song: Song, volume: int = 100) -> None:
        super().__init__(song, volume)
        self.chords = []
        position = 0
        while position < self.song.total_length:
            chord = self.song.get_current_chord(position)
            voicing = self._choose_voicing(chord)
            # TODO default to full length of chord
            duration = self.song.get_duration_remaining(position)  # can add method here for new policies
            self.chords.append((voicing, duration))
            self.prev = voicing
            position += duration

    def write_to_midi(self, midi_file, track) -> None:
        position = 0
        for voicing, duration in self.chords:
            for note in voicing:
                midi_file.addNote(track, self.channel, note, position, duration, self.volume)
            position += duration


    @staticmethod
    def _voicing_distance(voicing1, voicing2):
        return abs(voicing1[-1] - voicing2[-1])

    def _choose_voicing(self, chord):
        chord = str_to_chord(chord)  # TODO factor into chord? define what these interfaces should be (chords/voicings etc)
        if self.prev == None:
            voicing = choice(chord.voicings)
        else:
            voicing_distances = [(voicing, self._voicing_distance(voicing, self.prev)) for voicing in chord.voicings]
            voicing_distances.sort(key=lambda x: x[1])
            voicing = voicing_distances[0][0]

        return voicing


class Drums(Performance):
    channel = 9

    def write_to_midi(self, midi_file, track) -> None:
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
                


            