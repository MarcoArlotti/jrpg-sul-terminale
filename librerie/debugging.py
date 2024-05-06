
from art import art,text2art
#
from termcolor import colored
Art = text2art("one more",font='sub-zero',chr_ignore=True)
print(colored(Art,"blue"))