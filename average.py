import os 
#Stephanie Rojas
# 1/14/2022
# Declare variables, print variables, print type of data, 
# learn some operators

# this symbol is for comments, means the computer will ignore
# I want to clear my terminal
os.system('cls')
#Program is Average of 3 tests

#Declare and Assign values
test1=80
test2=76
test3=92 
Flag=False 

#to display things on the screen we use the function print()
# print(type(test1), type(test2), type(Flag))

#declare Sum to add tests symbol for addition is +
Sum = test1 + test2 + test3 
#Average we will divide ....        /
Average= Sum/3
print(Sum)
print(Average)

#I want to print    The average of 3 tests is " number here"
print("The average of 3 tests is", Average)

print("Test 1 =", test1, end=" ")
print("Test 2 =", test2)
print("The average of 3 tests is", Average)