from song import Song

giant_steps = [("BMaj7", 2), ("D7", 2), ("GMaj7", 2), ("Bb7", 2), ("EbMaj7", 4), ("AMin7", 2), ("D7", 2), 
        ("GMaj7", 2), ("Bb7", 2), ("EbMaj7", 2), ("F#7", 2), ("BMaj7", 4), ("FMin7", 2), ("Bb7", 2), 
        ("EbMaj7", 4), ("AMin7", 2), ("D7", 2), ("GMaj7", 4), ("C#Min7", 2), ("F#7", 2), 
        ("BMaj7", 4), ("FMin7", 2), ("Bb7", 2), ("EbMaj7", 4), ("C#Min7", 2), ("F#7", 2), 
]

song = Song(giant_steps, 2)

assert song.chord_starts_stops == [['BMaj7', 0, 2], ['D7', 2, 4], ['GMaj7', 4, 6], ['Bb7', 6, 8], ['EbMaj7', 8, 12], 
['AMin7', 12, 14], ['D7', 14, 16], ['GMaj7', 16, 18], ['Bb7', 18, 20], ['EbMaj7', 20, 22], ['F#7', 22, 24], 
['BMaj7', 24, 28], ['FMin7', 28, 30], ['Bb7', 30, 32], ['EbMaj7', 32, 36], ['AMin7', 36, 38], ['D7', 38, 40], 
['GMaj7', 40, 44], ['C#Min7', 44, 46], ['F#7', 46, 48], ['BMaj7', 48, 52], ['FMin7', 52, 54], ['Bb7', 54, 56], 
['EbMaj7', 56, 60], ['C#Min7', 60, 62], ['F#7', 62, 64]]

assert song.song_length == 64
assert song.total_length == 64 * 2

assert song.get_current_chord(0.5) == 'BMaj7'
assert song.get_current_chord(2) == 'D7'
assert song.get_current_chord(40.1) == 'GMaj7'

assert song.get_current_chord(64 + 0.5) == 'BMaj7'
assert song.get_current_chord(64 + 2) == 'D7'
assert song.get_current_chord(64 + 40.1) == 'GMaj7'

assert song.get_duration_remaining(0.5) == 1.5
assert song.get_duration_remaining(2) == 2
assert song.get_duration_remaining(41) == 3.0