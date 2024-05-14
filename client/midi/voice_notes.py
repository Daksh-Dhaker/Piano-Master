import pygame.mixer


def _midi_to_note(midi_number):
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    octave = (midi_number // 12) - 1
    note = note_names[midi_number % 12]
    return note + str(octave)


class VoiceNote:
    def __init__(self):
        self.d = {}
        notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        for i in range(9):
            for j in range(len(notes)):
                note_name = notes[j] + str(i)
                self.d[note_name] = pygame.mixer.Sound(f"assets/{note_name}.mp3")

    def play_note(self, midi_number):
        self.d[_midi_to_note(midi_number)].play()
