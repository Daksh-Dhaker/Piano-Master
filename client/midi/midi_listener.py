import pygame
import threading
import time
import pygame.midi


class MidiListener:
    def __init__(self, duration):
        self.cur_events = []
        self.clock = pygame.time.Clock()
        self.duration = duration
        self.stop_listening = False
        self.initialise_midi()

    def initialise_midi(self):
        pygame.midi.init()
        self.input_id = pygame.midi.get_default_input_id()
        if self.input_id == -1:
            print("No MIDI input devices found.")
            exit()

        self.midi_input = pygame.midi.Input(self.input_id)
        print(
            f"MIDI Input: {pygame.midi.get_device_info(self.input_id)[1].decode('ascii')}"
        )
        self.output_id = 0
        for i in range(pygame.midi.get_count()):
            if pygame.midi.get_device_info(i)[1] == b"Microsoft MIDI Mapper":
                self.output_id = i
        self.midi_output = pygame.midi.Output(self.output_id)
        print(
            f"MIDI Output: {pygame.midi.get_device_info(self.output_id)[1].decode('ascii')}"
        )

    # TODO handle back delay error
    def handle_events(self):
        if self.midi_input.poll():
            midi_events = self.midi_input.read(10)
            midi_evs = pygame.midi.midis2events(midi_events, self.midi_input.device_id)
            for event in midi_evs:
                if event.type == pygame.midi.MIDIIN:
                    note, velocity = event.data1, event.data2
                    note_on = True if event.status // 16 == 9 else False
                    note_off = True if event.status // 16 == 8 else False
                    if note_on:
                        # self.midi_output.note_on(note, velocity)
                        self.cur_events.append(["on", note, event.timestamp])
                    elif note_off:
                        # self.midi_output.note_off(note)
                        self.cur_events.append(["off", note, event.timestamp])

    def is_listening(self):
        return not self.stop_listening

    def start(self):
        self.t = threading.Thread(target=self.count_down, daemon=True)
        self.t.start()

    def count_down(self):
        time.sleep(self.duration)
        self.stop_listening = True

    def stop(self):
        pygame.midi.quit()
        pygame.mixer.music.pause()
        # print(self.cur_events)
        # temp = calc_score(self.cur_events, reference, self.note_length)
        # print(temp)
        return self.cur_events
