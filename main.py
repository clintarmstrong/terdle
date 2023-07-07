import contextlib
import requests
import json
from rich.console import Console
from string import ascii_letters, ascii_uppercase
console = Console()
score = 0

def getPossStr():
	possibles=[]
	for letter in ascii_uppercase:
		possibles.append(letter)
	return possibles
	
def getWord():
	api_url = "https://random-word-api.vercel.app/api?words=1&length=5&type=uppercase"
	response = requests.get(api_url)
	word = json.loads(response.text)
        
	return word[0]

def welcome():
	console.clear()
	console.rule("TERDLE")
	console.print("Try to guess our 5 letter word! You get 6 tries to guess correctly!")

def checkGuess(guess,answer,all_guesses,possibles):
	global score
	welcome()
	format_guess = []

	remaining_map = {}
	for i in range(0, len(answer)):
		if answer[i] == guess[i]:
			continue
		c = answer[i]
		remaining_map[c] = remaining_map.get(c, 0) + 1

	result = ''
	for i in range(0, len(answer)):
		if answer[i] == guess[i]:
			format = "bold white on green"
		elif remaining_map.get(guess[i], 0) > 0:
			format = "bold white on yellow"
			remaining_map[guess[i]] -= 1
		else:
			format = "bold white on #555555"
		
		format_guess.append(f"[{format}]{guess[i]}[/]")
		for num, letter in enumerate(getPossStr()):
			if letter == guess[i]:
				possibles[num] =  f"[{format}]{guess[i]}[/]"
		
	all_guesses.append(format_guess)
	console.print("Streak: ",score,justify="center")

	for i in all_guesses:
		console.print("".join(i),justify="center")
		
	console.print("\n" + "".join(possibles), justify="center")
	
def checkWin(right,answer):  
	global score
	if right == True:
		console.rule("\nThat is correct!")
		score = score + 1
	else:
		print("\nThe word was ",answer)
		console.rule("Better luck next time!")
		score = 0

def get_guess():
	guess = ''
	valid = False

	guess = input("Guess: ").upper()
	if len(guess)!=5:
		print("\nYour guess must contain exactly five letters")
		return get_guess()
	if not guess.isalpha():
		
		print("\nPlease, only use valid characters")
		return get_guess()
	return guess

def newRoundCheck():
	resp = input("\nWould you like to play another round?(Y or N): ")
	if resp == "y" or resp == "Y":
		main()
	elif resp == "n" or resp == "N":
		print("Thanks for playing!")
		return 0
	else:
		print("Please type valid option")
		newRoundCheck()

def main():
	possibles = getPossStr()
	right = False
	answer = getWord()
	num_guesses=7
	welcome()
	all_guesses = list()
	with contextlib.suppress(KeyboardInterrupt):
		for i in range(1,num_guesses):
		
			guess = get_guess()
			checkGuess(guess,answer,all_guesses,possibles)
			if guess == answer:
				right = True
				break

		checkWin(right,answer)
		newRoundCheck()

main()
