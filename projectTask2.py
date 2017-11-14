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
import re
import sys
import json
import argparse
import nltk
#from mysolr import Solr
import pysolr
import codecs
import requests
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
    #                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             sentence = re.sub(r'\W', ' ',sentence)
    outputWords = nltk.word_tokenize(sentence)

    printDebugMsg("sentence is {}".format(sentence))
    printDebugMsg("words are {}".format(outputWords))

    return outputWords




def createIndex(words, doc_id, sentence_id):
    """Takes in words, doc_id and sentence_id.
    Uses doc_id and sentence_id together constitute the key.
    Each word gets indexed with its doc_id and sentence_id.

    INPUT:
        -words:         List of words of a sentence from a Document.
        -doc_id:        Document No. of the word.
        -sentence_id:   Sentence No. of the word.

    OUTPUT:
        -solr_index:    Dictionary containing index of every word in a sentence.

    """

    word_num = 0
    solr_index = {}
    solr_index["id"]="D{}S{}".format(doc_id,sentence_id)
    for word in words:
        word_num += 1
        #if word_num != 78 :
        solr_index["W{}".format(word_num)] = word
        #print(solr_index)

    return solr_index

def indexIntoSOLR(documents_index_list):
    """Adds list of indices of sentences from all docs to SOLR.
    """
    # Setup a Solr instance. The timeout is optional.
    solr = pysolr.Solr('http://localhost:8983/solr/mycore', timeout=10)
    # session = requests.Session()
    # solr = Solr('http://localhost:8983/solr/mycore1/')
    doc_count = 0
    for document in documents_index_list:
        #try:
        #print(document)

        # solr.add([
        #
        # ])
        #document = json.loads(str(document))
        # with open('./jsonFiles/data{}.json'.format(doc_count), 'w') as outfile:
        #     json.dump(document, outfile, indent=4)
        #
        # #document = json.dumps(document)
        # with open('./jsonFiles/data{}.json'.format(doc_count)) as fp:
        #     d = json.load(fp)
        # print(type(d))
        # print(d)

        print("done")
        try:
            solr.add([document])
        except Exception:
            print("can't index this document")
        doc_count+=1
        print(doc_count)
    #print(documents_index_list)
    #solr.search('I')

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
    # Create a list containing index of every document in the directory.
    documents_index_list = []
    for trainFile in os.listdir(trainingDataDir):
        # currFile = open(os.path.join(trainingDataDir, trainFile), 'r')
        # currFileData = currFile.read()


        with codecs.open(os.path.join(trainingDataDir, trainFile), "r",encoding='utf-8', errors='ignore') as currFile:
            currFileData = currFile.read()


        numFiles += 1
        numWords += len(tokenizeIntoWords(currFileData))

        # Call the pipeline for each article.

        #nlpPipelineHelper(currFileData, indexQueryFlag="query", numFiles)
        sentences_index_list = nlpPipelineHelper(currFileData, numFiles, indexQueryFlag="index")
        #print(sentences_index_list)

        # append sentence indices of a document to the documents_index_list
        documents_index_list.extend(sentences_index_list)

        #

        if numFiles%100==0:
            print(numFiles)

    print("Adding list to SOLR...")

    #print(documents_index_list)
    indexIntoSOLR(documents_index_list)



    printDebugMsg("Found {} Files in Training Data Directory.".format(numFiles))
    printDebugMsg("Found {} Words in Training Data.".format(numWords))


def nlpPipelineHelper(Input, doc_id, indexQueryFlag):
    """Helper function for the NLP Pipeline.
    This is where the main part of the pipeline happens.

    INPUT:
        -Input:                 either user input or article input.
        -indexQueryFlag:        Flag to determine if we need
                                to index into SOLR, or query from SOLR.
        -doc_id:                Document id, or numFiles from `def readTrainingData()`.

    OUTPUT:
        -sentences_index_list:  List of index of every sentence in a Document.
    """
    # Segment into sentences.
    sentences = segmentIntoSentences(Input)
    sentence_id = 0
    # Create a list containing index of every sentence in a Document.
    sentences_index_list = []
    for sentence in sentences:
        sentence_id += 1
        # Tokenize sentences into words.
        words = tokenizeIntoWords(sentence)

        # Select whether to index words into SOLR or query from SOLR.
        if indexQueryFlag == "index":

            # Create solr index for one sentence
            solrIndex = createIndex(words, doc_id, sentence_id)

            #pysolr.Solr.add(solrIndex)

            #print("index added")

            # Add solr index of that sentence to a list
            sentences_index_list.append(solrIndex)

        elif indexQueryFlag == "query":
            queryFromSOLR(words)
        else:
            print("INVALID indexQueryFlag")
            sys.exit(1)

    return sentences_index_list

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
