__author__ = 'Epix'


def main(filename):
    warning = []
    min = 300
    plays = {}
    for i in range(0, 16):
        plays[str(i)] = []
    # print(plays)
    f_eve = open(filename + '.eve', 'r')
    for line in f_eve:
        if 'PLAY' in line:
            line_s = line.split(',')
            plays[line_s[2].strip()].append(line_s[0].strip())
    # print(plays)
    for i in range(0, 16):
        play = plays[str(i)]
        for j in range(1, len(play)):
            if int(play[j]) - int(play[j - 1]) < min:
                warning.append(int(play[j]))
    print(sorted(warning))
    f_eve.close()
    f_eve = open(filename + '.eve', 'r')
    f_eve_check = open(filename + '_check.eve', 'w')
    for line in f_eve:
        if 'PLAY' in line:
            if int(line[0:8]) in warning:
                line = line[0:-1] + 'X\n'
        f_eve_check.write(line)


if __name__ == '__main__':
    main('test_v1')
