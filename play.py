from midiutil.MidiFile import MIDIFile
from pathlib import Path
from pyjazz.song import Song
from pyjazz.performance import Solo, Bassline, Comping, Performance
from pyjazz.instrument import Instrument
from typing import List

def create_midi_file(tempo: int, instruments: List[Instrument]) -> MIDIFile:
    mf = MIDIFile(numTracks=len(instruments)) 
    for i, instrument in enumerate(instruments):
        mf.addTrackName(track=i, time=0, trackName=instrument.name)
        mf.addTempo(track=i, time=0, tempo=tempo)
        mf.addProgramChange(tracknum=i, channel=i, time=0, program=instrument.program)
    return mf

         
#TODO make functions return a modified mf rather than modifying in-place
def perform(mf: MIDIFile, performances: List[Performance]):
    for i, performance in enumerate(performances):
        performance.play(mf, i, i)

if __name__ == "__main__":
    GIANT_STEPS = [("BMaj7", 2), ("D7", 2), ("GMaj7", 2), ("Bb7", 2), ("EbMaj7", 4), ("AMin7", 2), ("D7", 2), 
            ("GMaj7", 2), ("Bb7", 2), ("EbMaj7", 2), ("F#7", 2), ("BMaj7", 4), ("FMin7", 2), ("Bb7", 2), 
            ("EbMaj7", 4), ("AMin7", 2), ("D7", 2), ("GMaj7", 4), ("C#Min7", 2), ("F#7", 2), 
            ("BMaj7", 4), ("FMin7", 2), ("Bb7", 2), ("EbMaj7", 4), ("C#Min7", 2), ("F#7", 2), 
    ]

    AUTUMN_LEAVES = [
        ("AMin7", 4), ("D7", 4), ("GMaj7", 4), ("CMaj7", 4),
        ("F#Min7b5", 4), ("B7", 4), ("EMin7", 8)
        ]

    N_REPEATS = 2
    TEMPO = 120

    OUTPUT_DIR = Path(__file__).parent / "outputs"
    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
    OUTPUT_FILENAME = "out.mid"
    OUTPUT_PATH = OUTPUT_DIR / OUTPUT_FILENAME

    song = Song(AUTUMN_LEAVES, repeats=4)

    #TODO pass the song to the performance automatically
    instruments = [
        Instrument("piano", 0), 
        Instrument("saxophone", 66), 
        Instrument("bass", 33)
    ]

    performances = [Comping(song), Solo(song), Bassline(song)]

    mf = create_midi_file(tempo=TEMPO, instruments=instruments)
    perform(mf, performances)

    with open(OUTPUT_PATH, 'wb') as outf:
        mf.writeFile(outf)