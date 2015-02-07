# coding:utf8
from __future__ import division
import math


def floor(n):
    return int(math.floor(n))


mark_l = ['END', 'MEASURE', 'HAKU', 'TEMPO', 'PLAY']
note_c = {'16': '0', '11': '1', '12': '2', '13': '3', '14': '4', '15': '5', '18': '6', '19': '7', '21': '8',
          '22': '9', '23': '10', '24': '11', '25': '12', '28': '13', '29': '14', '26': '15'}


def add_mark(marks, time, mark_type, data):
    if time not in marks:
        marks[time] = [[], [], [], [], []]
    marks[time][mark_type].append(data)


class Measure:
    def __init__(self, bms_b, start_time, start_bpm, need_tempo=False, is_end=False, debug=False, bar=0):
        self.bar = bar
        self.debug = debug
        self.start_time = start_time
        self.start_bpm = start_bpm
        self.need_tempo = need_tempo
        self.is_end = is_end
        self.end_time = 0
        self.eve = ''
        # marks array with a initial MEASURE, key is beat position
        self.marks = {0: [[], [0], [], [], []]}
        self.marks_eve = {}
        self.beats = 4
        bms_lines = bms_b.strip().split('\n')
        # first manual tempo
        if need_tempo:
            self.marks[0][3].append(start_bpm)
        # noinspection PyBroadException
        try:
            # change beats
            if bms_lines[0][4:6] == '02':
                self.beats = int(self.beats * float(bms_lines[0][7:]))
                del bms_lines[0]
            # change bpm
            if bms_lines[0][4:6] == '03':
                bpm_l = bms_lines[0][7:]
                bpm_s = [bpm_l[i:i + 2] for i in range(0, len(bpm_l), 2)]
                bpm_len = len(bpm_s)
                for bpm_i in range(0, bpm_len):
                    if bpm_s[bpm_i] != '00':
                        time = bpm_i / bpm_len
                        add_mark(self.marks, time, 3, int(bpm_s[bpm_i], 16))
                del bms_lines[0]
            # change bpms
            if bms_lines[0][4:6] == '08':
                bpm_l = bms_lines[0][7:]
                bpm_s = [bpm_l[i:i + 2] for i in range(0, len(bpm_l), 2)]
                bpm_len = len(bpm_s)
                for bpm_i in range(0, bpm_len):
                    if bpm_s[bpm_i] != '00':
                        time = bpm_i / bpm_len
                        add_mark(self.marks, time, 3, int(bpms[bpm_s[bpm_i]]))
                del bms_lines[0]
        except:
            pass
        # haku
        for beat in range(0, self.beats):
            time = beat / self.beats
            add_mark(self.marks, time, 2, 0)
        # play
        for bms_line in bms_lines:
            note_id = bms_line[4:6]
            notes_l = bms_line[7:]
            notes = [notes_l[i:i + 2] for i in range(0, len(notes_l), 2)]
            notes_n = len(notes)
            for note_i in range(0, notes_n):
                if not notes[note_i] == '00':
                    time = note_i / notes_n
                    add_mark(self.marks, time, 4, note_c[note_id])

    # transform to eve
    def transform(self):
        current_t = 0
        last_beat = 0
        current_bpm = self.start_bpm
        for beat in sorted(self.marks.keys()):
            current_t += (beat - last_beat) * 60 * 1200 / current_bpm * (self.beats / 4)
            for act_i in range(0, 5):
                for v in self.marks[beat][act_i]:
                    # print(current_t + self.start_time)
                    if act_i == 3:
                        add_mark(self.marks_eve, floor(current_t + self.start_time), act_i,
                                 int(60 * 1000000 / v))
                        current_bpm = v
                    else:
                        add_mark(self.marks_eve, floor(current_t + self.start_time), act_i, str(v))
            last_beat = beat
        self.start_time += current_t + (1 - last_beat) * 60 * 1200 / current_bpm * (self.beats / 4)
        self.start_bpm = current_bpm

    # print in eve format
    def print_eve(self):
        eve_b = ''
        for time in sorted(self.marks_eve):
            for act in range(0, 5):
                for v in self.marks_eve[time][act]:
                    if debug:
                        if act == 1:
                            eve_l = ','.join(
                                [str(time).rjust(8), mark_l[act].ljust(8), str(v).rjust(8),
                                 str(self.bar-1).rjust(3, '0').rjust(8)])+','
                        else:
                            eve_l = ','.join(
                                [str(time).rjust(8), mark_l[act].ljust(8), str(v).rjust(8),
                                 ''.rjust(8)])+','
                    else:
                        eve_l = ','.join([str(time).rjust(8), mark_l[act].ljust(8), str(v).rjust(8)])
                    eve_b += eve_l + '\n'
        return eve_b


if __name__ == '__main__':
    debug = True
    filename = 'test'
    is_header = True
    bpm = 0
    bpms = {}
    bms_f = open(filename + '.bms', 'r')
    eve_f = open(filename + '.eve', 'w')
    bar_count = 0
    bms_b = ''
    current_time = 0
    need_tempo = True
    for line in bms_f:
        if not line.isspace():
            if is_header:
                if 'MAIN DATA FIELD' in line:
                    is_header = False
                if line.startswith('#BPM '):
                    bpm = int(line[5:])
                elif line.startswith('#BPM'):
                    bpms[line.split(' ')[0][4:]] = line.split(' ')[1].strip()
                    # print(bpms)
            else:
                if line.startswith('#'):
                    while not line.startswith('#' + str(bar_count).rjust(3, '0')):
                        bar_count += 1
                        e = Measure(bms_b, current_time, bpm, need_tempo, debug=debug, bar=bar_count)
                        e.transform()
                        current_time = e.start_time
                        bpm = e.start_bpm
                        eve_f.write(e.print_eve())
                        need_tempo = False
                        bms_b = ''
                    bms_b += line
    bar_count += 1
    e = Measure(bms_b, current_time, bpm, need_tempo, debug=debug, bar=bar_count)
    e.transform()
    eve_f.write(e.print_eve())
    eve_f.close()
    bms_f.close()


