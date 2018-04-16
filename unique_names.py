import csv

#cases to handle:
#   -Middle Names
#   -Nicknames
#   -Typos
#The program won't handle cases with two or more of these cases
#For example countUniqueNames("Daniel","Cohen","Dam" (typo of "Dan"),"Cohen","Daniel Choen") = 2

#In the comments i'll repher the persons as followe:
#   Billind addres form = A
#   Shipping address form = B
#   Name on credit card = C

DEF_MISSES_ALLOWED_FOR_LAST_NAME = 2
DEF_MISSES_ALLOWED_FOR_FIRST_NAME = 2


def countUniqueNames(billFirstName, billLastName, shipFirstName, shipLastName, billNameOnCard):
    #taking care of misses of caps for example "Ori" and "ori" or "ORI"
    billFirstName = billFirstName.lower()
    billLastName = billLastName.lower()
    shipFirstName = shipFirstName.lower()
    shipLastName = shipLastName.lower()
    billNameOnCard = billNameOnCard.lower()

    if len(billNameOnCard.split(' ')) == 1:
        #Input error : name on card should look like this "<FirstName> <LastName>" or "<LastName> <FirstName>"
        return 0

    #the first can be the first name or the last name so i'll call it cardName1 and 2
    if len(billNameOnCard.split(' ')) == 3: #for example "Michael B Jordan"
        #i am assuming the card name will be in the following format :
        #<first name> <second name> <last name>
        cardName1 = billNameOnCard.split(' ')[0] + " " + billNameOnCard.split(' ')[1]
        cardName2 = billNameOnCard.split(' ')[2]
    else:
        cardName1 = billNameOnCard.split(' ')[0]
        cardName2 = billNameOnCard.split(' ')[1]
    
    uniqueNames = 1

    #are the middle names different? (assuming you can't make a typo for a single letter)
    if samePerson(billFirstName,billLastName,shipFirstName,shipLastName):
        #print "A is B"
        if samePerson(billFirstName,billLastName,cardName1,cardName2) or samePerson(billFirstName,billLastName,cardName2,cardName1):
            #print "A is C"
            return uniqueNames
        else:
            #print "A is not C"
            uniqueNames += 1
            return uniqueNames
    else:
        #print "A is not B"
        uniqueNames += 1
        if samePerson(shipFirstName,shipLastName,cardName1,cardName2) or samePerson(shipFirstName,shipLastName,cardName2,cardName1):
            #print "B is C"
            return uniqueNames
        else:
            #print "B is not C"
            if samePerson(billFirstName,billLastName,cardName1,cardName2) or samePerson(billFirstName,billLastName,cardName2,cardName1):
                #print "A is C"
                return uniqueNames
            else:
                #print "A is not C"
                uniqueNames += 1
                return uniqueNames


def samePerson(firstName1,lastName1,firstName2,lastName2):
    #There can't be a nickname to lastname
    if countMissMatches(lastName1, lastName2) > DEF_MISSES_ALLOWED_FOR_LAST_NAME:
        #Different last names -> different persons
        return False

    if len(firstName1.split(' ')) == len(firstName2.split(' ')) == 2:
        if firstName1.split(' ')[1] != firstName2.split(' ')[1]:
            #Different middle names -> different persons
            return False

    #ignoring middle names because they are the same (probably), or irrelevent (only one has middle name)
    firstName1 = firstName1.split(' ')[0]
    firstName2 = firstName2.split(' ')[0]

    #dealing with nicknames
    if not isNickName(firstName1, firstName2):
        #maybe the same name or a typo

        if countMissMatches(firstName1, firstName2) > DEF_MISSES_ALLOWED_FOR_FIRST_NAME:
            return False


    return True

def countMissMatches(str1, str2):
    #counting one time from the begining and one time from the end 
    #to take in count missing a letter ("Israeli" and "Isaeli" is the same but "r" is missing)
    missMatchesBegining = 0
    missMatchesEnd = 0

    for i in range(0, min(len(str1), len(str2))):
        if str1[i] != str2[i]:
            missMatchesBegining += 1
    
    missMatchesBegining += abs(len(str1)-len(str2))

    if len(str1) == len(str2):
        #no missed characters if the strings are the same length (probably)
        return missMatchesBegining

    for i in range(1, min(len(str1), len(str2)) + 1):
        if str1[-i] != str2[-i]:
            missMatchesEnd += 1
    
    missMatchesEnd += abs(len(str1)-len(str2))

    return abs(missMatchesBegining + missMatchesEnd - max(len(str1), len(str2)))


def isNickName(name1, name2):
    with open('nicknames.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            if (row[1][:-1].lower() == name1 and row[2].lower() == name2) or (row[1][:-1].lower() == name2 and row[2].lower() == name1):
                return True
    return False

def main():
    
    print "Alonzo Ball, Alonzo Ball, Alonzo Ball" #1 person, no typos, no nicknames, no middle names
    print countUniqueNames("Alonzo", "Ball", "Alonzo", "Ball", "Alonzo Ball")
    
    print "Alozo Ball, Alonzo Ball, Alonzo Ball" #1 person, 1 miss, no nicknames, no middle names
    print countUniqueNames("Alozo", "Ball", "Alonzo", "Ball", "Alonzo Ball")
    
    print "Alomzo Ball, Alonzo Ball, Alonzo Ball" #1 person, 1 typo, no nicknames, no middle names
    print countUniqueNames("Alomzo", "Ball", "Alonzo", "Ball", "Alonzo Ball")

    print "Alomso Ball, Alonzo Ball, Alonzo Ball" #1 person, 2 typos, no nicknames, no middle names
    print countUniqueNames("Alomso", "Ball", "Alonzo", "Ball", "Alonzo Ball")

    print "Aiomso Ball, Alonzo Ball, Alonzo Ball" #1 person, 3 typos, no nicknames, no middle names
    print countUniqueNames("Aiomso", "Ball", "Alonzo", "Ball", "Alonzo Ball")
    
    print "James Harden, Jamie Hardin, James Harden" #1 person, no typos, 1 nickname, no middle names
    print countUniqueNames("James", "Harden", "Jamie", "Harden", "James Harden")

    print "Alonzo A Ball, Alonzo Ball, Alonzo Ball" #1 person, no typos, no nicknames, 1 middle name
    print countUniqueNames("Alonzo A", "Ball", "Alonzo", "Ball", "Alonzo Ball")

    print "Michael J Jordan, Michael B Jordan, Michael J Jordan" #2 persons, no typos, no nicknames, 2 middle name
    print countUniqueNames("Michael J", "Jordan", "Michael B", "Jordan", "Michael J Jordan")

    print "Michael J Jordan, Michael B Jordan, Michael A Jordan" #3 persons, no typos, no nicknames, 3 middle name
    print countUniqueNames("Michael J", "Jordan", "Michael B", "Jordan", "Michael A Jordan")

    print "Mike Jordan, Micky Jordan, Michael J Jordan" #1 person, no typos, 2 nicknames, no middle names
    print countUniqueNames("Mike", "Jordan", "Micky", "Jordan", "Michael Jordan")

    print "Joe Jonas, Nick Jonas, Kevin Jonas" #3 persons, no typos, no nicknames, no middle names
    print countUniqueNames("Joe", "Jonas", "Nick", "Jonas", "Kevin Jonas")


main()