# CS 6320 - Natural Language Processing
# Group Project
#
# Task 3:
#       Create a deep NLP pipeline.
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
import pysolr
import codecs
from nltk.tokenize import sent_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn

# For Testing Purposes.
### DO NOT MAKE CHANGES TO TESTING VARIABLE HERE ###
### ONLY MAKE CHANGES FROM COMMAND-LINE OPTIONS ###
DEBUG = False  # True/False.

# Get directory of executable files are located in relative to python file.
execDir = os.path.dirname(os.path.realpath(__file__))

# Variable to hold training data location.  Can change via command-line parameter.
trainingDataDir = os.path.join(execDir, "TrainingData")

# Setup a Solr instance. The timeout is optional.
solr = pysolr.Solr('http://localhost:8983/solr/part3core', timeout=10)


# Flags for query variables and their scores.
# Higher scores put more weight on those search terms.
# Default all to 1 for now.
# Can use these flags to automate testing later.
SENTENCE_FLAG = True
SENTENCE_SCORE = 1
LEMMA_FLAG = True
LEMMA_SCORE = 1
STEM_FLAG = True
STEM_SCORE = 1
POSTAG_FLAG = True
POSTAG_SCORE = 1
HYPERNYM_FLAG = True
HYPERNYM_SCORE = 1
HYPONYM_FLAG = True
HYPONYM_SCORE = 1
MERONYM_FLAG = True
MERONYM_SCORE = 1
HOLONYM_FLAG = True
HOLONYM_SCORE = 1


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
    # sentence = re.sub(r'\W', ' ',sentence)
    outputWords = nltk.word_tokenize(sentence)

    printDebugMsg("sentence is {}".format(sentence))
    printDebugMsg("words are {}".format(outputWords))

    return outputWords


def lemmatizeWords(words):
    """Lemmatize words using NLTK.

    Input:
        -list of words
    Output:
        -list of lemmatized words.
    """
    wordnet_lemmatizer = WordNetLemmatizer()
    lemmatizedWords = []
    for word in words:
        lemmatizedWords.append(wordnet_lemmatizer.lemmatize(word))

    printDebugMsg("Lemmatized words are {}".format(lemmatizedWords))

    return lemmatizedWords


def stemWords(words):
    """Stem the words using NLTK Porter Stemmer.

    Input:
        -list of words.
    Output:
        -list of stemmed words
    """
    porter_stemmer = PorterStemmer()
    stemmedWords = []
    for word in words:
        stemmedWords.append(porter_stemmer.stem(word))

    printDebugMsg("Stemmed words are {}".format(stemmedWords))

    return stemmedWords


def posTagWords(words):
    """POS Tag words using NLTK.

    Input:
        -list of words.
    Output:
        -list of POS-tagged words.
    """
    posTaggedWords = nltk.pos_tag(words)

    printDebugMsg("POS-Tagged Words are {}".format(posTaggedWords))

    return posTaggedWords


def syntacticParseAndExtractPhrases(sentence):
    """NOTE: Only have to do one of the following:
            1) Syntactic Parse And Extract Phrases.
            2) Head Words.
            3) Dependency Parse Relations As Features.

    This function performs syntactic parsing and extracting phrases.
    """
    pass


def headWords(words):
    """NOTE: Only have to do one of the following:
            1) Syntactic Parse And Extract Phrases.
            2) Head Words.
            3) Dependency Parse Relations As Features.

    This function extracts the head word from the sentence.
    """
    pass


def dependencyParseRelationsAsFeatures(words):
    """NOTE: Only have to do one of the following:
            1) Syntactic Parse And Extract Phrases.
            2) Head Words.
            3) Dependency Parse Relations As Features.

    This function performs dependency parse relations as features.
    """
    pass


def synsets(word):
    """Helper function for hypernym, hyponym, meronym, and holonym.

    Input:
        -word
    Output:
        -list of synsets.
    """
    listOfSynsets = wn.synsets(word)

    # printDebugMsg("Synsets are: {}".format(listOfSynsets))

    return listOfSynsets


def getHypernyms(words):
    """Get Hypernyms for all of the words.

    Input:
        -list of words.
    Output:
        -list of hypernyms.
    """
    listOfHypernyms = []

    for word in words:
        wordSynsets = synsets(word)
        for synset in wordSynsets:
            for hypernym in synset.hypernyms():
                listOfHypernyms.append(hypernym)

    printDebugMsg("Hypernyms are: {}".format(listOfHypernyms))

    return listOfHypernyms


def getHyponyms(words):
    """Get Hyponyms for all of the words.

    Input:
        -list of words.
    Output:
        -list of hyponyms.
    """
    listOfHyponyms = []

    for word in words:
        wordSynsets = synsets(word)
        for synset in wordSynsets:
            for hyponym in synset.hyponyms():
                listOfHyponyms.append(hyponym)

    printDebugMsg("Hyponyms are: {}".format(listOfHyponyms))

    return listOfHyponyms


def getMeronyms(words):
    """Get Meronyms for all of the words.

    Input:
        -list of words.
    Output:
        -list of meronyms.
    """
    listOfMeronyms = []

    for word in words:
        wordSynsets = synsets(word)
        for synset in wordSynsets:
            for meronym in synset.part_meronyms():
                listOfMeronyms.append(meronym)

    printDebugMsg("Meronyms are: {}".format(listOfMeronyms))

    return listOfMeronyms


def getHolonyms(words):
    """Get Holonyms for all of the words.

    Input:
        -list of words.
    Output:
        -list of holonyms.
    """
    listOfHolonyms = []

    for word in words:
        wordSynsets = synsets(word)
        for synset in wordSynsets:
            for holonym in synset.member_holonyms():
                listOfHolonyms.append(holonym)

    printDebugMsg("Meronyms are: {}".format(listOfHolonyms))

    return listOfHolonyms


def createIndex(sentence, words, lemmas, stems, posTags, hypernyms, hyponyms, meronyms, holonyms, doc_id, sentence_id):
    """Takes in words, doc_id and sentence_id.
    Uses doc_id and sentence_id together constitute the key.
    Each word gets indexed with its doc_id and sentence_id.

    INPUT:
        -words:         List of words of a sentence from a Document.
        -lemmas.
        -stemmed words.
        -POS-tagged words.
        -Hypernyms.
        -Hyponyms.
        -Meronyms.
        -Holonyms.
        -doc_id:        Document No. of the word.
        -sentence_id:   Sentence No. of the word.

    OUTPUT:
        -solr_index:    Dictionary containing index of every word in a sentence.

    """

    solr_index = {}
    solr_index["id"] = "D{}_S{}".format(doc_id, sentence_id)
    solr_index["sentence"] = sentence
    solr_index["lemmas"] = lemmas
    solr_index["stems"] = stems
    solr_index["posTags"] = posTags
    solr_index["hypernyms"] = hypernyms
    solr_index["hyponyms"] = hyponyms
    solr_index["meronyms"] = meronyms
    solr_index["holonyms"] = holonyms

    return solr_index


def indexIntoSOLR(documents_index_list):
    """Indexes the list of all the docs to SOLR,one
    document at a time.

    INPUT:
        -documents_index_list:  List of indices of all the documents.
    """

    doc_count = 0
    for document in documents_index_list:
        print("done")
        try:
            solr.add([document])
        except Exception:
            print("can't index this document")
        doc_count += 1
        print(doc_count)


def queryFromSOLR(words, lemmas, stems, posTags, hypernyms, hyponyms, meronyms, holonyms):
    """Takes in words and match each word against the SOLR indices.

    INPUT:
        -words: List of tokenized sentences.
        -lemmas.
        -stemmed words.
        -POS-tagged words.
        -Hypernyms.
        -Hyponyms.
        -Meronyms.
        -Holonyms.
    """
    resultCounter = 1

    # NOTE: If you search with all words separated by space surrounded by ( ),
    # then SOLR will look for those words in the sentence in any order.

    # Build search query.
    searchQuery = ""

    if SENTENCE_FLAG:
        searchQuery += "sentence:({})^{} ".format(" ".join(words), SENTENCE_SCORE)

    if LEMMA_FLAG:
        searchQuery += "lemmas:({})^{} ".format(" ".join(lemmas), LEMMA_SCORE)

    if STEM_FLAG:
        searchQuery += "stems:({})^{} ".format(" ".join(stems), STEM_SCORE)

    if POSTAG_FLAG:
        posTagList = [str(x) for x in posTags]
        searchQuery += "posTags:({})^{} ".format(" ".join(posTagList), POSTAG_SCORE)

    if HYPERNYM_FLAG:
        hypernymList = [str(x) for x in hypernyms]
        searchQuery += "hypernyms:({})^{} ".format(" ".join(hypernymList), HYPERNYM_SCORE)

    if HYPONYM_FLAG:
        hyponymList = [str(x) for x in hyponyms]
        searchQuery += "hyponyms:({})^{} ".format(" ".join(hyponymList), HYPONYM_SCORE)

    if MERONYM_FLAG:
        meronymList = [str(x) for x in meronyms]
        searchQuery += "meronyms:({})^{} ".format(" ".join(meronymList), MERONYM_SCORE)

    if HOLONYM_FLAG:
        holonymList = [str(x) for x in holonyms]
        searchQuery += "holonyms:({})^{} ".format(" ".join(holonymList), HOLONYM_SCORE)

    # Verify that at least one thing is being queried.
    if len(searchQuery) == 0:
        print("ERROR: Nothing specified to search. Exiting...")
        sys.exit(1)

    printDebugMsg("searchQuery is {}".format(searchQuery))

    # Search.
    results = solr.search(searchQuery)

    # Print results.
    for result in results:
        print("{}\t{}\t{}\n".format(resultCounter, result['id'], result['sentence']))
        # printDebugMsg("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(resultCounter, result['id'], result['sentence'], result[
        #               'lemmas'], result['stems'], result['posTags'], result['hypernyms'], result['hyponyms'], result['meronyms'], result['holonyms']))
        resultCounter += 1


def readTrainingData(indexQueryFlag):
    """Read the Training Data.
    Training Data Directory is stored in the trainingDataDir variable.

    Calls the nlpPipelineHelper for each article in directory.
    """
    numFiles = 0
    numWords = 0
    # Create a list containing index of every document in the directory.
    documents_index_list = []
    for trainFile in os.listdir(trainingDataDir):
        # Reads the file text as utf-8 coded text and ignores that can't be read.
        with codecs.open(os.path.join(trainingDataDir, trainFile), "r", encoding='utf-8', errors='ignore') as currFile:
            currFileData = currFile.read()

        numFiles += 1
        numWords += len(tokenizeIntoWords(currFileData))

        # Call the pipeline for each article.

        # nlpPipelineHelper(currFileData, indexQueryFlag="query", numFiles)
        sentences_index_list = nlpPipelineHelper(currFileData, indexQueryFlag, numFiles)
        # print(sentences_index_list)

        # append sentence indices of a document to the documents_index_list
        documents_index_list.extend(sentences_index_list)

        if numFiles % 100 == 0:
            print(numFiles)

    print("Adding list to SOLR...")

    # print(documents_index_list)
    indexIntoSOLR(documents_index_list)

    printDebugMsg("Found {} Files in Training Data Directory.".format(numFiles))
    printDebugMsg("Found {} Words in Training Data.".format(numWords))


def nlpPipelineHelper(Input, indexQueryFlag=None, doc_id=None,):
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
        lemmas = lemmatizeWords(words)
        stems = stemWords(words)
        posTags = posTagWords(words)
        # TODO: Add in one of the OR functions (head word, etc.).
        hypernyms = getHypernyms(words)
        hyponyms = getHyponyms(words)
        meronyms = getMeronyms(words)
        holonyms = getHolonyms(words)

        # Select whether to index words into SOLR or query from SOLR.
        if indexQueryFlag == "index":

            # Create solr index for one sentence
            solrIndex = createIndex(sentence, words, lemmas, stems, posTags,
                                    hypernyms, hyponyms, meronyms, holonyms, doc_id, sentence_id)

            # Add solr index of that sentence to a list
            sentences_index_list.append(solrIndex)

        elif indexQueryFlag == "query":
            queryFromSOLR(words, lemmas, stems, posTags, hypernyms, hyponyms, meronyms, holonyms)
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
        readTrainingData(indexQueryFlag)
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
