# coding:utf8

def bms_b2eve_b(bms_b, start_time, bpm, need_tempo=False, is_end=False):
    mark_l = ['END', 'MEASURE', 'HAKU', 'TEMPO', 'PLAY']
    note_c = {'16': '0', '11': '1', '12': '2', '13': '3', '14': '4', '15': '5', '18': '6', '19': '7', '21': '8',
              '22': '9', '23': '10', '24': '11', '25': '12', '28': '13', '29': '14', '26': '15'}
    bms_lines = bms_b.split('\n')
    eve_a = {int(start_time): [[], [0], [], [], []]}
    eve_b = ''
    beats = 4
    if bms_lines[0][4:6] == '02':
        beats = 3
        bms_lines.remove(0)
    if bms_lines[0][4:6] == '03':
        bpm_l = bms_lines[7:]
        bpm_s = [bpm_l[i:i + 2] for i in range(0, len(bpm_l), 2)]
        for bpm_i in range(0, len(bpms)):
            time = int
        bms_lines.remove(0)
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
                eve_l = ','.join([str(time).rjust(8), mark_l[act_i].ljust(8), str(v).rjust(8)])
                eve_b += eve_l + '\n'

    # print notes
    return eve_b


if __name__ == '__main__':
    filename = 'sample1'
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
                    print(bpms)
            else:
                if line.startswith('#'):
                    while not line.startswith('#' + str(bar_count).rjust(3, '0')):
                        bar_count += 1
                        eve_f.write(bms_b2eve_b(bms_b, current_time, bpm))
                        need_tempo = False
                        bms_b = ''
                        current_time += 60 * 1200 / bpm
                    bms_b += line
    eve_f.close()
    bms_f.close()


