#StephanieRojas
#01/31/2022
# Strings array of characters 
# Has many functions
import os
import random
os.system ('cls')
myName= "Stephanie Rojas"
myStatement= """ My name is 
so nice because 
blah blah blagggg

Whatever 
ever"""
print ("My last name begins with " +myName[10])
print(myStatement)
if "blah" in myStatement:
    print('true')
print('expert' not in myStatement)

print ("My last name begins with " +myName[10 ])
print(myStatement)
if 'blah' in myStatement:
    print('true')
print('expert' not in myStatement) 
# find () will return the index of the character you are looking for(first instance)
INDEX=myName.find(" ")
print(INDEX)
#finding the length of your word
wordLen= len(myName)
print(wordLen) #your last index is len-1
#For loop in range 0 to limit
for i in range(wordLen-1):
    if "a" in myName[i]:
        print(i, end=", ")
print("")
print("done")
myStatement= myStatement.upper() #make all letter uppercase
print(myStatement)
# letter=input("Dear user, please give us a nice letter")
# print("Thank you, the letter is "+ letter)
# if letter in myStatement:
#     print ("GREAT")

check=True
while check: 
    letter=input("Dear user, please give us a nice letter")
#alpha is a function that makes sure the input is only letter
    if len(letter)>1 or not letter.isalpha():
        print("BAd")
    else:
        check=False
print("ready play game") 
