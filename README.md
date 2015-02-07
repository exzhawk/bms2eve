# bms2eve utility
## requirements
python 2.x
## basic usage
        python bms2eve.py <filename>
which <filename> stands for the filename your bms filename.
NOTICE <filename> here DOES NOT contain extension name(bms), if you have a sample.bms, just input "sample".
## debug mode
change "debug = False" to "debug = True" in bms2eve.py to enable debug mode. Extra information(currently the measure number) will be written.
use eve_check.py to check if two PLAYs are too close
        python eve_check.py <filename>
filename is same as above
<filename>_check.eve will be generated to show problem line with a "X"
to modify threshold or mark, change "min_gap" and "mark" in eve_check.py

