import random, sys

class Madlib:
	def __init__(self, template):
		self.template = template
		self.blanks = []
		self.answers = {}
		self.answered = False
		self._populate_blanks()

	def _populate_blanks(self):
		copy = self.template
		while len(copy) > 2:
			left = copy.find('{')
			right = copy.find('}')
			if left < 0 and right < 0:
				break
			else:
				blank = copy[left+1:right]
				if blank not in self.blanks:
					self.blanks.append(blank)
			copy = copy[right+1:]

	def set_answers(self, answers):
		for blank in self.blanks:
			if blank not in answers:
				raise ValueError
		self.answers = answers
		self.answered = True

	def clear(self):
		self.answers = {}

	def render(self):
		if self.answered:
			return self.template.format(**self.answers)
		else:
			raise ValueError


class MadlibList:
	def __init__(self, file='madlibs.txt'):
		self.file = file

	def madlibs(self):
		with open(self.file, 'r') as file:
			madlibs = [Madlib(madlib) for madlib in file.read().split('\n\n')]
		return madlibs 


class Madlibber:
	def __init__(self, file='madlibs.txt'):
		self.file = file
		self.switch = { 
			'1': self.generate_madlib,
			'2': self.quit 
		}

	def print_menu(self):
		print()
		print("************************")
		print("* 1. Generate a Madlib *")
		print("* 2. Quit              *")
		print("************************")
		print()

	def quit(self):
		sys.exit()

	def get_option(self):
		option = ""
		while option not in self.switch:
			option = input("Choose an option: ")
			if option not in self.switch:
				print("Please choose option 1 or 2.")
			else:
				self.switch[option]()

	def get_input(self, blanks):
		answers = {}
		for blank in blanks:
			answer = input("Choose a/an {blank}: ".format(blank=blank.replace("_", " ")))
			answers[blank] = answer
		return answers


	def generate_madlib(self):
		with open(self.file, 'r') as file:
			madlibs = file.read().split('\n\n')
		madlib = Madlib(random.choice(madlibs))
		answers = self.get_input(madlib.blanks)
		
		print()
		print("----- New Madlib -----")
		print(madlib.render())
		print()

	def run(self):
		while True:
			self.print_menu()
			self.get_option()
