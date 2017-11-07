# CS 6320 - Natural Language Processing
# Group Project
#
# Task 2:
#       Create a shallow NLP pipeline.
#
# Authors:
#       Stephen Blystone (smb032100@utdallas.edu)
#       Amit Gupta (axg162930@utdallas.edu)
#       Deepan Verma (dxv160430@utdallas.edu)
#
# Teamname:
#       GASBDV (General Anakin Skywalker Becomes Darth Vader)
import os
import sys
import argparse
import nltk
from nltk.tokenize import sent_tokenize

# For Testing Purposes.
### DO NOT MAKE CHANGES TO TESTING VARIABLE HERE ###
### ONLY MAKE CHANGES FROM COMMAND-LINE OPTIONS ###
DEBUG = False  # True/False.

# Get directory of executable files are located in relative to python file.
execDir = os.path.dirname(os.path.realpath(__file__))

# Variable to hold training data location.  Can change via command-line parameter.
trainingDataDir = os.path.join(execDir, "TrainingData")


def printDebugMsg(text):
    """Used for printing debug messages."""
    if DEBUG:
        print(text)


def segmentIntoSentences(article):
    """Segment article into sentences using NLTK.

    Input:
        -article: article to segment.
    Output:
        -list of sentences.
    """
    outputSentences = sent_tokenize(article)

    printDebugMsg("article is {}".format(article))
    printDebugMsg("outputSentences are {}".format(outputSentences))

    return outputSentences


def tokenizeIntoWords(sentence):
    """Tokenize sentence into words using NLTK.

    Input:
        -sentence: sentence to tokenize.
    Output:
        -list of words.
    """
    outputWords = nltk.word_tokenize(sentence)

    printDebugMsg("sentence is {}".format(sentence))
    printDebugMsg("words are {}".format(outputWords))

    return outputWords


def indexIntoSOLR(args):
    """"""
    pass


def queryFromSOLR(args):
    """"""
    pass


def readTrainingData():
    """Read the Training Data.
    Training Data Directory is stored in the trainingDataDir variable.

    Calls the nlpPipelineHelper for each article in directory.
    """
    numFiles = 0
    numWords = 0
    for trainFile in os.listdir(trainingDataDir):
        currFile = open(os.path.join(trainingDataDir, trainFile), 'r')
        currFileData = currFile.read()
        # Call the pipeline for each article.
        nlpPipelineHelper(currFileData, indexQueryFlag="query")

        numFiles += 1
        numWords += len(tokenizeIntoWords(currFileData))

    printDebugMsg("Found {} Files in Training Data Directory.".format(numFiles))
    printDebugMsg("Found {} Words in Training Data.".format(numWords))


def nlpPipelineHelper(Input, indexQueryFlag):
    """Helper function for the NLP Pipeline.
    This is where the main part of the pipeline happens.

    INPUT:
        -Input: either user input or article input.
        -indexQueryFlag: Flag to determine if we need
                to index into SOLR, or query from SOLR.
    """
    # Segment into sentences.
    sentences = segmentIntoSentences(Input)
    for sentence in sentences:
        # Tokenize sentences into words.
        words = tokenizeIntoWords(sentence)

        # Select whether to index words into SOLR or query from SOLR.
        if indexQueryFlag == "index":
            indexIntoSOLR(words)
        elif indexQueryFlag == "query":
            queryFromSOLR(words)
        else:
            print("INVALID indexQueryFlag")
            sys.exit(1)


def nlpPipeline(indexQueryFlag, userInput=None):
    """NLP Pipeline.

    Input:
        -indexQueryFlag: Flag to determine if we need
                to index into SOLR, or query from SOLR.
        -userInput: Sentence if user input; otherwise None.
    """
    if indexQueryFlag == "index":
        readTrainingData()
    elif indexQueryFlag == "query":
        # For testing.
        # userInput = "Hello World. How are you today? I am fine. Thank you."
        nlpPipelineHelper(userInput, indexQueryFlag)


def runAlgorithm(args):
    """Main function that runs the Algorithm"""
    # Parse arguments
    parser = argparse.ArgumentParser(description='Task 2: Create a Shallow NLP Pipeline.')
    parser.add_argument('--debug', required=False, action="store_true",
                        help="Enable to print Debug Messages.")
    parser.add_argument('--trainData', required=False,
                        action="store_true", help="Train on the Corpus.")
    parser.add_argument('--dataLocation', required=False,
                        help="Training Data location if not default.")
    parser.add_argument('--userInput', required=False, help="Sentence to test on.")
    args = parser.parse_args()

    if (not args.trainData) and (not args.userInput):
        print("ERROR: You must type either --trainData and/or --userInput flags.  Exiting...")
        sys.exit(1)

    # Set global debug flag.
    if args.debug:
        global DEBUG
        DEBUG = True

    # Update trainingDataDir if user specified directory.
    if args.dataLocation:
        global trainingDataDir
        trainingDataDir = args.dataLocation
        # Confirm that user inputted directory exists and is a directory.
        if not os.path.exists(trainingDataDir):
            print("ERROR: {} does not exist. Exiting...".format(trainingDataDir))
            sys.exit(1)
        elif not os.path.isdir(trainingDataDir):
            print("ERROR: {} is not a directory. Exiting...".format(trainingDataDir))
            sys.exit(1)

    # Finished parsing command-line options.
    printDebugMsg("Finished with argument parsing.")

    # Training Data means we need to index into SOLR.
    if args.trainData:
        nlpPipeline("index")

    # User input means we need to query from SOLR.
    if args.userInput:
        nlpPipeline("query", userInput=args.userInput)


if __name__ == "__main__":
    runAlgorithm(sys.argv[1:])
