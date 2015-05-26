# Class:     CSCI 490-B3
# Program:   Assignment 4
# Author:    Vivek Patel
# Z-number:  z1698694
# Date Due:  03/06/2015

# Purpose:   Run a comparison (Pearson r value) using a user selected movie and all other movies in the data file 
#            in order to determine the 20 most similar movies based on the movies ratings.             

# Execution: python3 hw4.py 

#!/usr/bin/python3

import sys
from math import sqrt
from math import pow
import functools 

#Function to compute Pearson R value
def computePearson(movie1, movie2, index):

	#Variables used in calculation
    stddev1 = 0
    stddev2 = 0
    rValue =  0
    sum = 0
	
    #Compute mean
    mean1 = functools.reduce(lambda x, y: x + y, movie1) / float(len(movie1)) 
    mean2 = functools.reduce(lambda x, y: x + y, movie2) / float(len(movie2)) 
		
	#Compute sum of (xi- mean)^2 for use in std deviation
    for num, num1 in zip(movie1, movie2):
        stddev1 += float(pow(num - mean1, 2))    
        stddev2 += float(pow(num1 - mean2, 2))

	#compute standard deviation
    stddev1 = sqrt(1/(len(movie1)-1) * stddev1)
    stddev2 = sqrt(1/(len(movie1)-1) * stddev2)
    
	#Compute sum of (Xi-mean)/stddev * (Yi - mean)/stddev
    for m1, m2 in zip(movie1, movie2):
        sum += (((m1 - mean1) / stddev1) * ((m2 - mean2) / stddev2))
	
	#Compute r value
    rValue = 1/((len(movie1)-1)) * sum
	
	#Add the r value with the movie index to the list of rvalues
    rValues.append((rValue, index))

#Function to print top 20 movies
def printMovies(rValuesList, index):

    #Line number counter
    line = 1;
	
    outString = ""
	
	#Sort the list by r value descending
    rValuesList.sort(key=lambda tup: tup[0], reverse=True)
	
	#Print blank lines for spacing
    print("")
    print("")
	
	#Print the user chosen movie
    print(index, ": ", movieNames[index])
	
	#Print headings
    print("")
    print(" Movie Name".ljust(70), "r Value".ljust(8))
	
	#If there are at least 20 movies
    if len(rValues) >= 21:
        
		#Print the top 20 movies
        for tuples in rValues[1:21]:
		
			#Print the movie name and rvalues
            print("{:3d}".format(line), " ", movieNames[tuples[1]].ljust(65), "{:5.3f}".format(tuples[0]))
        
            line += 1    		
    else:
	    #if there are not 20 movies indicate this
        print("Insufficient comparison movies")
		
#List to hold the individual lists of movie ratings
ratings = []

#List to hold movie names
movieNames = []

#List to hold pearson scores
pearsonScores = []

#List to hold ratings for similar reviewers
movieRatingsA = []
movieRatingsB = []

#List to hold r values
rValues = []

#Open the file of matrices
f = open("movie-matrix.txt", "r")

#Apend an empty list to the ratings and names so indexes start at 1
ratings.append("")
movieNames.append("")

#For each line in the file split it using the semicolon as a delimiter and store the generated list in the list of movies. 
for data in f.readlines():
    ratings.append(data.split(';'))
#close the file
f.close()

#Open the movie names file
f = open("movie-names.txt", "r")

#For each movie name split it based on the | and store only the name in the movieNames list
for data in f.readlines():
    number, name = data.split("|",1)
    movieNames.append(name.strip())

	
#Print the total number of movies and total reviewers\
print("")
print("Total number of movies: ".ljust(26), len(movieNames)-1)
print("Total number of reviewers: ".ljust(25), len(ratings[1])-1)
print("")
	
#String to hold user input
movieNumber = ""	

validInput = False	
	
#While the user input is not 1 or quit run the program
while movieNumber != 'q' or movieNumber != "quit":
    
    print("")
	
	#Reset valid input bool
    validInput = False
	
	#User input for the movie they want to use
    movieNumber = input('Enter a movie number 1-1682 (q or quit to exit): ')
    
	#If the user entered q or quit then exit the program
    if movieNumber == "q" or movieNumber == "quit":
        exit()	
	
	#While the user input in invalid
    while validInput == False:
        
		#If the user entered q or quit then exit
        if movieNumber == "q" or movieNumber == "quit":
            exit()	
		
		#Else if the user entered something non numeric re-prompt
        elif movieNumber.isdigit() == False:
            movieNumber = input('Enter a movie number 1-1682 (q or quit to exit): ')
		
        #Else if the user entered a digit out of range re-prompt		
        elif int(movieNumber) < 1 or int(movieNumber) > 1682: 
            movieNumber = input('Enter a movie number 1-1682 (q or quit to exit): ')
			
		#Else if the input was valid set validInput to true causing the loop to terminate
        elif movieNumber.isdigit == True and int(movieNumber) > 0 or int(movieNumber) < 1683:
             validInput = True
			
    #Convert movie number to an int
    movieNumber = int(movieNumber)
        
    #List set to the ratings for the user selected movie number
    movie1 = ratings[movieNumber]
    	
    #Create sub lists of only similar reviewer
    #Loop through all movies
    for index, movie2 in enumerate(ratings):
    
        #Loop through the ratings of both movies
        for rating1, rating2 in zip (movie1, movie2):
    
        	#If the rating is not null append the rating to the list
            if rating1 != '' and rating2 != '':
                movieRatingsA.append(rating1)
                movieRatingsB.append(rating2)
    			
        #If there are at least 10 ratings in the list
        if(len(movieRatingsA) >= 11):
            #Remove the /n from the list        
            movieRatingsA.pop()
            movieRatingsB.pop()
    		
    		#Convert the list into a list of ints
            movieRatingsA = [int(i) for i in movieRatingsA]
            movieRatingsB = [int(i) for i in movieRatingsB]
    
    		#Call the function to compute the pearson r values for the movies
            computePearson(movieRatingsA, movieRatingsB, index)
    	
    	#Clear out the list of ratings for the next movie
        movieRatingsA[:] = []
        movieRatingsB[:] = []
    
    #Print the 20 similar movies
    printMovies(rValues, movieNumber)
    rValues[:] = []
