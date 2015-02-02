__author__ = 'Epix'


def main():
    min=350
    plays = {}
    for i in range(0, 16):
        plays[str(i)] = []
    # print(plays)
    f_eve = open('sample1.eve', 'r')
    for line in f_eve:
        if 'PLAY' in line:
            line_s = line.split(',')
            plays[line_s[2].strip()].append(line_s[0].strip())
    print(plays)
    for i in range(0, 16):
        play=plays[str(i)]
        for j in range(1, len(play)):
            if int(play[j])-int(play[j-1])<min:
                print play[j]


if __name__ == '__main__':
    main()
