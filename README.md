# Project
NLP Project

Running the program:
- You can always run the program with the "-h" flag to get help and see what arguments are available.
Example:
python projectTask2.py -h
usage: projectTask2.py [-h] [--debug] [--trainData]
                       [--dataLocation DATALOCATION] [--userInput USERINPUT]

Task 2: Create a Shallow NLP Pipeline.

optional arguments:
  -h, --help            show this help message and exit
  --debug               Enable to print Debug Messages.
  --trainData           Train on the Corpus.
  --dataLocation DATALOCATION
                        Training Data location if not default.
  --userInput USERINPUT
                        Sentence to test on.
                        


Example of running the program with user input:
python projectTask2.py --debug --userInput "This is a test sentence. How do you do? This is a third sentence."


Example of running the program to train based on the corpus:
python projectTask2.py --debug --trainData


Example of running the program with user input AND also training based on the corpus:
python projectTask2.py --debug --userInput "This is a test sentence. How do you do? This is a third sentence." --trainData




REQUIREMENTS:
The training data must be located in a folder called "TrainingData" located in the same folder as projectTask2.py.
