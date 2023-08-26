from typing import List, Tuple

from midiutil.MidiFile import MIDIFile
from abc import ABC
from pyjazz.song import Song
from random import choice, random
import logging
from pyjazz.motif import Motif
from pyjazz.chord import Chord
from functools import partial
from note import Note
logger = logging.getLogger(__name__)

class Performance(ABC):
    channel = 0
    def __init__(self, song: Song, note_range: tuple[int, int], volume: int = 100) -> None:
        self.song = song
        self.note_range = note_range
        self.volume = volume
        self.prev = None

    def write_to_midi(self, midi_file: MIDIFile, track: int) -> None:
        raise NotImplementedError


class MotifPerformance(Performance):
    def __init__(self, song: Song, note_range: tuple[int, int], motif_set: List[Motif], volume: int = 100) -> None:
        self.motif_set = motif_set
        super().__init__(song, note_range, volume)

        self.motifs = []  #TODO rename to distinguish from motif_set
        position = 0
        while position < self.song.total_length:
            chord = self.song.get_current_chord(position)
            duration = self.song.get_duration_remaining(position)
            motif = self._choose_motif(chord, duration).transpose(chord.root).move(position)
            self.motifs.append(motif)
            self.prev = motif
            position += motif.length

    
    def write_to_midi(self, midi_file: MIDIFile, track: int) -> None:
        for motif in self.motifs:
            for note in motif:
                midi_file.addNote(track, self.channel, note.pitch, note.position, note.duration, note.volume)

    def _get_valid_transpositions(self, motif: Motif) -> List[Motif]:
        valid_transpositions = []
        while motif.high <= self.note_range[1]:
            if motif.low >= self.note_range[0]:
                valid_transpositions.append(motif)
            motif = motif.transpose(12)
        return valid_transpositions
    
    @staticmethod
    def _distance(last_note: Note, motif: Motif) -> int:
        distance = abs(motif[0].pitch - last_note.pitch)
        if distance == 0:
            return 999
        logger.debug(f"distance {distance}")
        return distance
    
    def _choose_motif(self, chord: Chord, length: float) -> Motif:
        quality_str = chord.quality.name  # TODO use quality classes directly rather than strs
   
        chord_motifs = [m for m in self.motif_set if quality_str in m.chords and m.length <= length]

        valid_motifs = []
        for base_motif in chord_motifs:
            valid_motifs.extend(self._get_valid_transpositions(base_motif))
        if len(self.motifs) == 0:
            motif = choice(valid_motifs)
        else:
            last_note = self.motifs[-1][-1]  # last note of last motif
            sorted_motifs = sorted(valid_motifs, key=partial(self._distance, last_note))
            motif = choice([sorted_motifs[0], sorted_motifs[1], sorted_motifs[2]])

        return motif



class Comping(Performance):
    def __init__(self, song: Song, note_range: tuple[int, int], volume: int = 100) -> None:
        super().__init__(song, note_range, volume)
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

    def write_to_midi(self, midi_file: MIDIFile, track: int) -> None:
        position = 0
        for voicing, duration in self.chords:
            if random() < 0.2:
                position += 2/3
                duration -= 2/3
            for note in voicing:
                midi_file.addNote(track, self.channel, note + 48, position, duration, self.volume)
            position += duration


    @staticmethod
    def _voicing_distance(voicing1, voicing2):
        return abs(voicing1[-1] - voicing2[-1])

    def _choose_voicing(self, chord: Chord):
        if self.prev == None:
            voicing = choice(chord.voicings)
        else:
            voicing_distances = [(voicing, self._voicing_distance(voicing, self.prev)) for voicing in chord.voicings]
            voicing_distances.sort(key=lambda x: x[1])
            voicing = voicing_distances[0][0]

        return voicing


class Drums(Performance):
    channel = 9

    def write_to_midi(self, midi_file: MIDIFile, track:int) -> None:
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
                


            