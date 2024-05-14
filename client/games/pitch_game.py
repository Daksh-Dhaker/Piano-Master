from client.games.base_game import MidiGame
from client.utils.score import calc_score
import random
import pygame
import client.midi.play as play


class PitchGame(MidiGame):
    def __init__(self, note_length, narrate_pitch=False, narrate_name=True):
        self.notes = self.generate_random_midi_notes(12, note_length)
        super().__init__(self.notes, note_length, narrate_pitch, narrate_name)

    def generate_random_midi_notes(self, num_notes, note_length):
        delay = note_length
        notes = []
        for _ in range(num_notes):
            note = random.randint(12, 115)
            notes.append(["on", note, 1000 * delay])
            notes.append(["off", note, 1000 * (delay + note_length / 2)])
            delay += note_length
        return notes

    def initialise_narrator(self, narrate_pitch, narrate_name):
        self.midi_narrator = play.MidiEventNarrator(
            self.midi_source,
            self.note_length,
            narrate_name,
            narrate_pitch,
            midi_out=self.midi_output,
        )

    def get_score_array(self):
        d = 0
        score = []
        for note, _, delay in self.notes:
            score += [note, d]
            d += delay
        return score

    def stop(self):
        pygame.midi.quit()
        pygame.mixer.music.pause()
        self.midi_narrator.stop_playback()
        return calc_score(self.cur_events, self.get_score_array(), self.note_length)
