
import random, os
os.system('cls')

# Today we are learning try and except, functions, elif

# Let's make menu a function key word def
def menu():

    print('###########W############################')
    print('#          Guess A Number Menu         #')
    print('#                                      #')
    print('#         1.  Choices 1-10             #')
    print('#         2.  Choices 1-50             #')
    print('#         3.  Choices 1-100            #')
    print('#           Select your choice         #')
    print('######################################  ')
#Checking for correct user input

menu() #calling the function menu 
check=True
while check:
    try:
        choice=int(input("Choice: "))
        if choice>0 and choice<4: 
            check=False
        else:
            print("please enter only a number from 1-2")
    except ValueError:
        print("Sorry, wrong choice, please enter 1 to 3 only")

if choice == 1:
    myNumber= random.randint(1,10)
    Level=10
elif choice == 2:
    myNumber= random.randint(1,50)
    Level=50
elif choice == 3:
    myNumber= random.randint(1,100)
    Level=100
print(choice)
GameOn=True
while(GameOn):
    userGuess=int(input("give me a number from 1 to "+str(Level)))
    if myNumber ==userGuess:
        print("You guessed it!")
        GameOn=False
    else:
        print("good luck next time", myNumber)
print("The number to guess was " + str(myNumber))
os.system('cls')
menu()