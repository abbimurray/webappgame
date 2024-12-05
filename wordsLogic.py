from collections import Counter

#importDBcm

creds = {
    "user": "words4user",
    "password": "words4passwd",
    "host": "localhost",
    "database": "words4DB",
}

#logic 
#1: check wordtocheck is made up of letters in sourceword
def check_sourceword_letters(sourceword, wordtocheck):
    """This function checks that the letters in the "wordtocheck" are in the "sourceword".returns true if letters in wordtocheck are in sourceword"""
    for letter in wordtocheck:
        if letter not in sourceword:
            return False
    return True

#2: check too many letters used 
def check_too_many_letters(sourceword, wordtocheck):
    """Ensures you haven't used too many of the letters in the sourceword. Returns True if there are no letters overused"""
    source_counter = Counter(sourceword) 
    word_counter = Counter(wordtocheck) 

    for letter in word_counter:
        # Compare the counts of each letter
        if word_counter[letter] > source_counter.get(letter, 0):
            return False  #False if any letter is overused
    return True  

#3: check if the word exists in a dictionary
def is_it_a_real_word(wordtocheck):
    """Returns True if the "wordtocheck" is a real word, i.e., it exists within words-huge.This check will also """
    wordtocheck = wordtocheck.lower() #convert to lowercase
    filepath="static/words-huge"
    try:
        with open(filepath, "r") as file:
            for line in file:
                word = line.strip().lower()  #read word, strip whitespace, and convert to lowercase
                if len(word) >= 4 and word == wordtocheck: #only check words that are at least 4 letters long
                    return True 
        return False  
    except FileNotFoundError:
        print(f"Error: The file at '{filepath}' was not found.")
        return False

#check that there are seven words enteredentered_seven_words("bill till sill real seal ability list")   # returns True.
#4: count seven words
def entered_seven_words(wordlist):
    """Returns true if there are seven words entered"""
    if isinstance(wordlist, str):    #split string into list of words
        wordlist = wordlist.split()
    if len(wordlist) >= 7:
        return True  #7 or more words
    else:
        return False #less than 7

#returns the number of words in the wordslist
def how_many_words(wordslist):
    """Returns the number of words in the submitted "wordslist" string."""
    if isinstance(wordslist, str):      #split string into list of words
        wordslist = wordslist.split()
    
    return len(wordslist)

#5: words all have 4 letters or more
def min_word_length(wordslist):
    """
    Returns True if all words in 'wordslist' have at least 4 letters, otherwise
    Returns False
    """
    if isinstance(wordslist, str):
        wordslist = wordslist.split()
    
    # Check each word's length
    for word in wordslist:
        if len(word) < 4:
            return False  
    return True 

#6: check for duplicates 
def check_for_duplicates(wordslist):
    """Returns True is the "wordslist" contains any duplicates, otherwise False."""
    if isinstance(wordslist, str):     #split string into list of words
        wordslist = wordslist.split()
         
    wordslist = [word.lower() for word in wordslist] #lowercase as this game is not case sensitive
    #using a set to check for duplicates
    #see if the number of words is different from the number of unique words
    if len(wordslist) != len(set(wordslist)):
        return True  #duplicates
    else:
        return False  #no duplicates

#7: none of the words are in sourceword
def includes_sourceword(sourceword, wordslist):
    """Returns True if any one of the words in the "wordslist" are the same as the "sourceword", otherwise
    returns False."""
    if isinstance(wordslist, str):
        wordslist = wordslist.split()
    
    sourceword = sourceword.lower()   #convert to lowercase
    wordslist = [word.lower() for word in wordslist]
    
    #see if sourceword is in wordslist
    if sourceword in wordslist:
        return True
    else:
        return False


def validate_wordlist(sourceword, wordlist):
    """
    Validates the wordlist based on the following rules:
    1. Words are valid if:
       - Method #1 (check_sourceword_letters) returns True
       - Method #2 (check_too_many_letters) returns True
       - Method #3 (is_it_a_real_word) returns True
       - Method #4 (entered_seven_words) returns True
       - Method #5 (min_word_length) returns True
       - Method #6 (check_for_duplicates) returns False
       - Method #7 (includes_sourceword) returns False

    Returns True if all the rules are satisfied, otherwise False.
    """
    
    if isinstance(wordlist, str):
        words = wordlist.split()
    else:
        return False

    # Rule 1: All words are made up of letters in sourceword
    if not all(check_sourceword_letters(sourceword, word) for word in words):
        print("Failed Rule 1: Words contain letters not in the sourceword.")
        #failures.append("Failed Rule 1: Words contain letters not in the sourceword.")
        return False

    # Rule 2: No overuse of letters
    if not all(check_too_many_letters(sourceword, word) for word in words):
        print("Failed Rule 2: Words overuse letters from the sourceword.")
        #failures.append("Failed Rule 2: Words overuse letters from the sourceword.")
        return False

    # Rule 3: All words exist in the dictionary
    if not all(is_it_a_real_word(word) for word in words):
        print("Failed Rule 3: Some words are not valid dictionary words.")
        #failures.append("Failed Rule 3: Some words are not valid dictionary words.")
        return False

    # Rule 4: Check for at least 7 words
    if not entered_seven_words(wordlist):
        print("Failed Rule 4: Less than 7 words entered.")
        #failures.append("Failed Rule 4: Less than 7 words entered.")
        return False

    # Rule 5: All words are 4 letters or more
    if not min_word_length(wordlist):
        print("Failed Rule 5: Some words are shorter than 4 letters.")
        #failures.append("Failed Rule 5: Some words are shorter than 4 letters.")
        return False

    # Rule 6: No duplicate words
    if check_for_duplicates(wordlist):
        print("Failed Rule 6: Duplicate words are present.")
        #failures.append("Failed Rule 6: Duplicate words are present.")
        return False

    # Rule 7: None of the words should match the sourceword
    if includes_sourceword(sourceword, wordlist):
        print("Failed Rule 7: Sourceword is included in the wordlist.")
        #failures.append("Failed Rule 7: Sourceword is included in the wordlist.")
        return False

    # All checks passed
    print("Validation passed all rules.")
    return True
    #return failures

