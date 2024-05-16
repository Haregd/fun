#!/usr/bin/env python

from re import sub
import sys
import signal
from time import sleep
from date import datetime
import os



DIGIT_COLOR = "RED"
VOID_COLOR = "BLACK"
LETTER_COLOR = "YELLOW"
PUNCT_COLOR = "YELLOW"
PAD_WIDTH = 1


strings = {
	"0" : "######|##__##|##--##|##__##|######",
	"1" : "----##|--__##|----##|--__##|----##",
	"2" : "######|--__##|######|##__--|######",
	"3" : "######|--__##|######|--__##|######",
	"4" : "##--##|##__##|######|--__##|----##",
	"5" : "######|##__--|######|--__##|######",
	"6" : "######|##__--|######|##__##|######",
	"7" : "######|--__##|----##|--__##|----##",
	"8" : "######|##__##|######|##__##|######",
	"9" : "######|##__##|######|--__##|----##",
	"A" : "_AAAA_|AA__AA|AAAAAA|AA__AA|AA__AA",
	"B" : "AAAAA_|AA__AA|AAAAA_|AA__AA|AAAAAA",
	"C" : "_AAAA_|AA__AA|AA____|AA__AA|_AAAA_",
	"D" : "AAAAA_|AA__AA|AA__AA|AA__AA|AAAAA_",
	"E" : "AAAAAA|AA____|AAAAAA|AA____|AAAAAA",
	"F" : "AAAAAA|AA____|AAAA__|AA____|AA____",
	"G" : "_AAAA_|AA____|AA_AAA|AA__AA|_AAAA_",
	"H" : "AA__AA|AA__AA|AAAAAA|AA__AA|AA__AA",
	"I" : "AAAA|_AA_|_AA_|_AA_|AAAA",
	"J" : "___AAA|____AA|____AA|AA__AA|_AAAA_",
	"K" : "AA__AA|AA_AA_|AAAA__|AA_AA_|AA__AA",
	"L" : "AA____|AA____|AA____|AA____|AAAAAA",
	"M" : "AA___AA|AAA_AAA|AAAAAAA|AA_A_AA|AA___AA",
	"N" : "AA__AA|AAA_AA|AAAAAA|AA_AAA|AA__AA",
	"O" : "_AAAA_|AA__AA|AA__AA|AA__AA|_AAAA_",
	"P" : "AAAAAA|AA__AA|AAAAAA|AA____|AA____",
	"Q" : "_AAAA_|AA__AA|AA__AA|AA_AAA|_AAAA_",
	"R" : "AAAAA_|AA__AA|AAAAAA|AA_AA_|AA__AA",
	"S" : "_AAAAA|AA____|_AAAA_|____AA|AAAAA_",
	"T" : "AAAAAA|__AA__|__AA__|__AA__|__AA__",
	"U" : "AA__AA|AA__AA|AA__AA|AA__AA|_AAAA_",
	"V" : "AA__AA|AA__AA|AA__AA|_AAAA_|__AA__",
	"W" : "AA___AA|AA_A_AA|AAAAAAA|AAA_AAA|AA___AA",
	"X" : "AA__AA|_AAAA_|__AA__|_AAAA_|AA__AA",
	"Y" : "AA__AA|AA__AA|_AAAA_|__AA__|__AA__",
	"Z" : "AAAAAA|___AA_|__AA__|_AA___|AAAAAA",
	">" : "________|________|________|________|________",
	":" : "__|::|__|::|__",
	"," : "__|__|__|::|_:",
	"!" : "::|::|::|__|::",
	"." : "__|__|__|__|::",
	";" : "__|::|__|::|_:",
	" " : "__|__|__|__|__",
	"~" : "------|--__--|------|--__--|------"
}

colors = {
	"BLACK" : "0",
	"RED" : "1",
	"GREEN" : "2",
	"YELLOW" : "3",
	"BLUE" : "4",
	"MAGENTA" : "5",
	"CYAN" : "6",
	"WHITE" : "7"
}

DC = "\033[3" + colors[DIGIT_COLOR] + ";4" + colors[DIGIT_COLOR] + "m"
VC = "\033[9" + colors[VOID_COLOR] + ";10" + colors[VOID_COLOR] + "m"
LC = "\033[3" + colors[LETTER_COLOR] + ";4" + colors[LETTER_COLOR] + "m"
PC = "\033[3" + colors[PUNCT_COLOR] + ";4" + colors[PUNCT_COLOR] + "m"
NC = "\033[0m"


def clear():
	os.system('cls' if os.name=='nt' else 'printf "\Ec"')


def exit(signal, frame):
	print "\033[5B" + "\033[?25h", # move cursor below clock and make it reappear
        sys.exit(0)


def initializeStrings():
	for name, string in strings.iteritems():
		
		width = str(string.find("|"))

		string = sub("(#+)", DC + r"\1" + NC, string)	# colorize #'s in digit strings
		string = sub("(-+)", VC + r"\1" + NC, string)	# colorize -'s (void areas) in digit strings
		string = sub("(A+)", LC + r"\1" + NC, string)	# colorize A's in letter strings
		string = sub("(:+)", PC + r"\1" + NC, string)	# colorize :'s in puctuation strings
		string = sub("_", " ", string)			# replace _'s with spaces
		string = sub("\|", "\033[" + width + "D" + "\033[1B", string) + "\033[4A" # add cursor movement

		strings[name] = string


import fcntl, termios, struct
def terminalSize():
	h, w, hp, wp = struct.unpack('HHHH',
		fcntl.ioctl(0, termios.TIOCGWINSZ,
		struct.pack('HHHH', 0, 0, 0, 0)))
	return w, h


def drawClock():
	terminalSize_log = "0"
	while True:

		terminalSize_cur = terminalSize()
		if terminalSize_cur != terminalSize_log:
			terminalSize_log = terminalSize_cur
			clear()

		print "\033[0;0H" + "\033[?25l" # move cursor to 0,0 and hide it

		string = datetime.now().strftime("%I:%M:%S") # 12-hour clock
		if string[0] == "0":
			string = "~" + string[1:]
		#string = datetime.now().strftime("%H:%M:%S") # 24-hour clock
		print "",
		for i in list(string):
			print " " * PAD_WIDTH, 
			sys.stdout.write(strings[i])
		sys.stdout.flush()

		sleep((1000000 - datetime.now().microsecond) / 1000000.0)


signal.signal(signal.SIGINT, exit)
initializeStrings()
drawClock()
