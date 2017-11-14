# Project
NLP Project

Running the program:
- You can always run the program with the "-h" flag to get help and see what arguments are available.

Example:
<pre>
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
</pre>                        


Example of running the program with user input:<br />
<pre>python projectTask2.py --debug --userInput "This is a test sentence. How do you do? This is a third sentence."</pre>


Example of running the program to train based on the corpus:<br />
<pre>python projectTask2.py --debug --trainData</pre>


Example of running the program with user input AND also training based on the corpus:<br />
<pre>python projectTask2.py --debug --userInput "This is a test sentence. How do you do? This is a third sentence." --trainData</pre>

<br /><br />

<p>
  <b>REQUIREMENTS:</b><br />
  The training data must be located in a folder called "TrainingData" located in the same folder as projectTask2.py.
</p>

<br /><br />

### Setup Solr

1. Install Solr -v 7.1.0.
  * For mac: ``` $ brew install solr```
  * For Windows: Go to Mirror link [Solr](http://apache.mirrors.pair.com/lucene/solr/7.1.0)
    * Click on **solr-7.1.0.zip** link.

2. Start Solr
  * go to root folder of Solr.
    * For mac: ``` $ solr start -p 8983```
    * For Windows: ```bin\solr.cmd start```
  * Check status of Solr.
    * ```bin/solr status```, or
    * Go to ```http://localhost:8983/solr/```

3. Add Core
  * For mac: ``` $ solr create -c mycore```
  * For Windows: ```bin\solr.cmd create -c mycore```

4. ```$ pip3 install pysolr```

5. ```$ pip3 install codecs```

6. To start indexing, run the following command:</br>
<pre> $ python3 projectTask2.py --trainData </pre>

7. To query:</br>
<pre> $ python3 projectTask2.py --userInput "This is a test sentence. How do you do? This is a third sentence." </pre>
