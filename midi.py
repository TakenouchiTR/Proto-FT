from mido import Message, MidiFile, MidiTrack, MetaMessage
from pathlib import Path

# Helper function to get MIDI note number
def note_number(note):
    base_notes = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4,
                  'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9,
                  'A#': 10, 'B': 11}
    octave = int(note[-1])
    key = note[:-1]
    return 12 * (octave + 1) + base_notes[key]

# Chords for the progression: C – Am – F – G
chord_progression = [
    [('C2',), ('C3', 'E3', 'G3')],   # Boom-Chick: C
    [('A2',), ('A3', 'C4', 'E4')],   # Am
    [('F2',), ('F3', 'A3', 'C4')],   # F
    [('G2',), ('G3', 'B3', 'D4')]    # G
]

# Create a MIDI file
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

# Add tempo and instrument
track.append(MetaMessage('set_tempo', tempo=500000))  # 120 BPM
track.append(Message('program_change', program=0, time=0))  # Acoustic Grand Piano

# Time configuration
quarter_note_ticks = 480
time_between_chords = quarter_note_ticks * 2

# Write the boom-chick pattern (root on beat 1, chord on beat 2)
for root_notes, chord_notes in chord_progression:
    # Root (beat 1)
    for note in root_notes:
        track.append(Message('note_on', note=note_number(note), velocity=64, time=0))
    for note in root_notes:
        track.append(Message('note_off', note=note_number(note), velocity=64, time=quarter_note_ticks))

    # Chord (beat 2)
    for note in chord_notes:
        track.append(Message('note_on', note=note_number(note), velocity=64, time=0))
    for note in chord_notes:
        track.append(Message('note_off', note=note_number(note), velocity=64, time=quarter_note_ticks))

# Save the file
output_path = Path("/mnt/data/boom_chick_pattern.mid")
mid.save(output_path)

output_path
