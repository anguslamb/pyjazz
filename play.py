from midiutil.MidiFile import MIDIFile
from pathlib import Path
from pyjazz.song import Song
from pyjazz.performance import MotifPerformance, Comping, Performance, Drums
from pyjazz.motif import motifs, bass_motifs
from pyjazz.instrument import Instrument
from typing import List
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def create_midi_file(tempo: int, instruments: List[Instrument]) -> MIDIFile:
    mf = MIDIFile(numTracks=len(instruments)) 
    for i, instrument in enumerate(instruments):
        mf.addTrackName(track=i, time=0, trackName=instrument.name)
        mf.addTempo(track=i, time=0, tempo=tempo)
        logger.info(f'changing track {i} to program {instrument.program}')
        mf.addProgramChange(tracknum=i, channel=0, time=0, program=instrument.program)
    return mf

         
#TODO make functions return a modified mf rather than modifying in-place
def perform(mf: MIDIFile, performances: List[Performance]):
    for i, performance in enumerate(performances):
        performance.write_to_midi(mf, i)

if __name__ == "__main__":
    N_REPEATS = 2
    OUTPUT_DIR = Path(__file__).parent / "outputs"
    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

    song = Song.from_json("songs/giant_steps.json", repeats=N_REPEATS)

    output_path = OUTPUT_DIR / (song.name + ".mid")

    #TODO pass the song to the performance automatically
    #TODO couple the instruments and performances in an enclosing class/tuple
    instruments = [
        Instrument("piano", 0), 
        Instrument("saxophone", 66), 
        Instrument("bass", 33),
        Instrument("drums", 0)
    ]

    performances = [
        Comping(song, (20,60)), 
        MotifPerformance(song, (40,80), motifs), 
        MotifPerformance(song, (8+12,35+12), bass_motifs), 
        Drums(song, (-1,-1))]

    mf = create_midi_file(tempo=song.tempo, instruments=instruments)
    perform(mf, performances)

    with open(output_path, 'wb') as outf:
        mf.writeFile(outf)
