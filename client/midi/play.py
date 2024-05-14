import mido
import time
from client.midi.voice_notes import VoiceNote
import threading
import pygame


def get_midi_file_events(midi_file):
    events = []
    cur_time = 0
    for msg in mido.MidiFile(midi_file):
        if not msg.is_meta:
            if msg.type == "note_on":
                events.append(["on", msg.note, cur_time * 1000])
                cur_time += msg.time
                events.append(["off", msg.note, cur_time * 1000])
    return events


class MidiNarrator(VoiceNote):
    def __init__(self, slow, narrate_name=True, narrate_note=False, midi_out=None):
        super().__init__()
        self.midi_events = []
        self.stop = False
        self.slow = slow
        if narrate_note:
            self.midi_out = midi_out
        self.narrate_note = narrate_note
        self.narrate_name = narrate_name

    def _play(self):
        raise NotImplementedError

    def play(self):
        self.t = threading.Thread(target=self._play, daemon=True)
        self.t.start()

    def stop_playback(self):
        self.stop = True

    def is_playing(self):
        return self.t.is_alive()


class MidiFileNarrator(MidiNarrator):
    def __init__(
        self, midi_file, slow, narrate_name=True, narrate_note=False, midi_out=None
    ):
        super().__init__(slow, narrate_name, narrate_note, midi_out)
        self.midi_file = midi_file

    def _play(self):
        file = mido.MidiFile(self.midi_file)
        for msg in file:
            if not msg.is_meta:
                time.sleep(msg.time * self.slow)
                if self.stop:
                    break
                if msg.type == "note_on" and msg.velocity > 0:
                    if self.narrate_name and self.narrate_note:
                        self.play_note(msg.note)
                        self.midi_out.note_on(msg.note, 100)
                    elif self.narrate_note:
                        self.midi_out.note_on(msg.note, 100)
                    else:
                        self.play_note(msg.note)
                elif msg.type == "note_off":
                    self.midi_out.note_off(msg.note)

        time.sleep(0.5)


class MidiEventNarrator(MidiNarrator):
    def __init__(
        self, midi_arr, slow, narrate_name=True, narrate_pitch=False, midi_out=None
    ):
        super().__init__(slow, narrate_name, narrate_pitch, midi_out)
        self.midi_arr = midi_arr
        self.slow = slow

    def _play(self):
        if len(self.midi_arr) == 0:
            return
        delay = self.midi_arr[0][2]
        new_arr = []
        for elem in self.midi_arr:
            temp = elem[2]
            elem[2] = elem[2] - delay
            delay = temp
            new_arr.append(elem)
        for event_type, note, delay in self.midi_arr:
            time.sleep((delay * self.slow) / 1000)
            if not self.stop:
                if event_type == "on":
                    self.midi_out.note_on(note, 100)
                elif event_type == "off":
                    self.midi_out.note_off(note)

        time.sleep(0.5)
