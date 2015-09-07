#from inc import *
from os import listdir
import json

#mainFunc.addCommand('triviabot', 'triviabot', 'start')
#mainFunc.addcommand('question', 'triviabot', 'question')
#mainFunc.addcommand('hint', 'triviabot', 'hint')


class triviabot:
	def __init__(self):
		instance = False
		#this is the list of question files
		qfiles = listdir('./triviabot_questions')
		question = ''
		answer = ''
		hints = []
		#dict of nicks and number of hints gotten per current question
		hinters = {}

	def start(self):
		self.question()
		self._generatehints()
	
	def question(self):
		'''Get a question and its answer from a json files
		should be made random such that questions in a json file are random'''
		qfile = random.choice(self.qfiles)
		j = json.load(qfile)
		self.question = j['question']
		self.answer = ['answer']

	def _generatehints(self):
		num = len(self.answer)
		self.hints = []
		firsthint = self.answer[0] + ('*'*(len(self.answer)-1))
		self.hints.append(firsthint)
		lasthint = firsthint
		while num > 1:
			idxs = [yield i for i,lts in enumerate(lasthint) if ltr == '*']
			idx = random.choice(idxs)
			lasthint[idx] = self.answer[indx]
			hints.append(lasthint)

trvbot = triviabot()		
trvbot.start()

def question(line, irc):
	global 	trvbot
	message, username, msgto = ircFunc.ircMessage(line)
	ircFunc.ircSay('#Evilquiz', trvbot.question, irc)
	ircFunc.ircSay(msgto, ('Hint: '+('*'*trvbot.answer)), irc)

def hint(line, irc):
	global trvbot
	try:
		message, username, msgto = ircFunc.ircMessage(line)
		if trvbot.hints:
			message, username, msgto = ircFunc.ircMessage(line)
			if username in trvbot.hinters:
				trvbot.hinters[username] += 1
			else:
				trvbot.hinters[username] = 1
			hint = trvbot.hints[0]
			trvbot.hints = trvbot.hints[1:]
			ircFunc.ircSay(msgto, ('Hint: {}'.format(hint)))
		else:
			ircFunc.ircSay(msgto, "No more hints, answer is: {}".format(trvbot.answer), irc)
			trvbot.question()
			question(line, irc)
	except IndexError:
		pass
def answer(line, irc):
	global trvbot
	message, username, msgto = ircFunc.ircMessage(line)
	if message == trvbot.answer:
		


if __name__ == '__main__':
	tr = triviabot()
	print tr.question()
		
