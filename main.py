from __future__ import division

__author__ = 'Epix'


def bms2eve(bms, eve):
    is_header = True
    bpm = 0

    bms_f = open(bms, 'r')
    eve_f = open(eve, 'w')
    bar_count = 0
    bms_b = ''
    current_time = 0
    need_tempo = True
    for line in bms_f:
        if not line.isspace():
            if is_header:
                if 'MAIN DATA FIELD' in line:
                    is_header = False
                if '#BPM' in line:
                    bpm = int(line[5:])
                    # print(bpm)
            else:
                if line.startswith('#'):
                    while not line.startswith('#' + str(bar_count).rjust(3, '0')):
                        bar_count += 1
                        eve_f.write(bms_b2eve_b(bms_b, current_time, bpm, need_tempo))
                        need_tempo = False
                        bms_b = ''
                        current_time += 60 * 1200 / bpm
                    bms_b += line
    eve_f.close()
    bms_f.close()


def bms_b2eve_b(bms_b, start_time, bpm, need_tempo=False, is_end=False, beats=4):
    mark_l = ['END', 'MEASURE', 'HAKU', 'TEMPO', 'PLAY']
    note_c = {'16': '0', '11': '1', '12': '2', '13': '3', '14': '4', '15': '5', '18': '6', '19': '7', '21': '8',
              '22': '9', '23': '10', '24': '11', '25': '12', '28': '13', '29': '14', '26': '15'}
    bms_lines = bms_b.split('\n')
    eve_a = {int(start_time): [[], [0], [], [], []]}
    eve_b = ''
    if need_tempo:
        eve_a[int(start_time)][3].append(int(60 * 1000000 / bpm))
    for beat in range(0, beats):
        time = int(start_time + beat * 60 * 1200 / bpm / 4)
        if time not in eve_a:
            eve_a[time] = [[], [], [], [], []]
        eve_a[time][2].append(0)
    for line in bms_lines:
        note_id = line[4:6]
        notes_l = line[7:]
        notes = [notes_l[i:i + 2] for i in range(0, len(notes_l), 2)]
        notes_n = len(notes)
        for note_i in range(0, notes_n):
            if not notes[note_i] == '00':
                time = int(start_time + note_i * 60 * 1200 / bpm / notes_n)
                if time not in eve_a:
                    eve_a[time] = [[], [], [], [], []]
                eve_a[time][4].append(note_c[note_id])
    for time in sorted(eve_a.keys()):
        for act_i in range(0, 5):
            for v in eve_a[time][act_i]:
                eve_l = ','.join([str(time).rjust(8),mark_l[act_i].ljust(8),str(v).rjust(8)])
                eve_b += eve_l + '\n'

    # print notes
    return eve_b


if __name__ == '__main__':
    bms2eve('sample1.bms', 'sample1.eve')