#StephanieRojas
#02/08/2022
# Word Game with 3 levels:
#       1. Fruits
#       2. Animals 
#       3. Computer Parts    
# Choice:

# Create word lists

def menu():
    print("##################################################")
    print("||                   Welcome                    ||")
    print("||                    WORDLE                    ||")
    print("||            Prepare to be challenged!         ||")
    print("||                   1.Fruits                   ||")
    print("||                  2. Animals                  ||")
    print("||               3. Computer Parts              ||")
    print("||  Choose any category to recieve instructions ||")
    print("##################################################")
import os, random 
os.system('cls')
word=''
guess=''

def selectWord():
    global word
    fruits=["banana", "grapes", "waterMelon", "blueberries", 'apples', "blackberries",
    "papaya", 'oranges', 'tomatoes', 'mangoes','kiwis', 'strawberries']

#size= (len(fruits))
#randy=random.randint(0,size)
#print(randy)
#word=fruits[randy]
#print(word)

    word=random.choice(fruits)
def guessFunction():
    global guess
    check=True
    while check:
        try:
            guess=input("\nenter a letter to guess the word ")
            if guess.isalpha() and len(guess)==1:
                check=False
        except ValueError:
            print("only one letter please")
menu()
gameOn=True
tries=0
letterGuessed=""
while gameOn:
    selectWord()
    guessFunction()
    letterGuessed += guess #letterGuessed=letterGuessed + guess
    if guess not in word:
        tries +=1
        print(tries)# for testing delete when game is ready
    countLetter=0
    for letter in word:
        if letter in letterGuessed:
            print(letter, end=" ")
            countLetter +=1
        else:
            print("_", end=" " )
    if tries >6:
        print("\n Sorry run out of chances")
        #playGame() ask if they want to play again
    if countLetter == len(word):
        print ("\nyou guesses! ")
        #Calculate Score
        #playGame()

    
            