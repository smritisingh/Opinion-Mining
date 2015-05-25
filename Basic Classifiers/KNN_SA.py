from math import log, sqrt
from porter import PorterStemmer

#read in positive and negative lines from files, and stopwords (useless words)
poslines= open(r'rt-polarity.pos', 'r').read().splitlines()
neglines= open(r'rt-polarity.neg', 'r').read().splitlines()
stopwords= open(r'stopwords.txt', 'r').read().splitlines()

#there is a total of 5331 positives and negatives.
#lets take first N as training set, and leave rest for validation
#N= 4800
#N = 4265
N = 3730
poslinesTrain= poslines[:N]
neglinesTrain= neglines[:N]
poslinesTest= poslines[N:]
neglinesTest= neglines[N:]

#create the train set and the test set by attaching labels to text to form a
#list of tuples (sentence, label). Labels are 1 for positive, -1 for negative
#if you don't get this look up list comprehensions in Python
trainset= [(x,1) for x in poslinesTrain] + [(x,-1) for x in neglinesTrain]
testset= [(x,1) for x in poslinesTest] + [(x,-1) for x in neglinesTest]

#initialize the stemmer object for (optional) stemming later
stemmer= PorterStemmer()

def getwords(sentence):
    """
    this method returns important words from a sentence as list
    you can comment/uncomment lines as you experiment with the results
    """
    
    w= sentence.split()
    
    #remove all things that are 1 or 2 characters long (punctuation)
    w= [x for x in w if len(x)>2]
    
    #get rid of all stop words
    w= [x for x in w if not x in stopwords]
    
    #stem each word
    w= [stemmer.stem(x,0,len(x)-1) for x in w]
    
    #add bigrams
    #w= w + [w[i]+' '+w[i+1] for i in range(len(w)-1)]
    
    #get rid of duplicates by converting to set and back to list
	#this works because sets dont contain duplicates
    w= list(set(w))
    
    return w #imp words

#compute frequency of every word in the train set. We will want common words
#to count for less in our later analysis. Also while we're at it,
#build an array of processed words called trainfeatures for training reviews.
freq={}
trainfeatures= []
for line,label in trainset: #for every sentence and its label
    words= getwords(line)
    for word in words: #for every word in the sentence
        freq[word]= freq.get(word, 0) + 1
    trainfeatures.append((words, label))
    
#evaluate the test set
Ntr= len(trainset)
wrong=0 #will store number of misslassifications
for line,label in testset: #for each review in test set
    
    testwords= getwords(line)
    
    #we will store distances to all train reviews in this list as tuples
    #of (score, label). Later, we will sort by score and look at the labels
    results=[]
    
    #go over every review in train set and compute similarity
    for trainwords, trainlabel in trainfeatures:
        
        #find all words in common between these two sentences
        commonwords= [x for x in trainwords if x in testwords]
        
        #accumulate score for all overlaps. Common words count for less
		#and we achieve this by dividing by their frequency
        #the log() function squashes things down so that infrequent words
        #dont count for TOO much.
        score= 0.0
        for word in commonwords:
            score += log(Ntr/freq[word])
        
        results.append((score, trainlabel))
        
    #sort all similarities by their score, descending
    results.sort(reverse=True)
    
    #look at top 5 results and do a majority vote (i.e. this is 5-NN classifier)
    toplab= [x[1] for x in results[:5]] #extract top 5 labels
    numones= toplab.count(1) #count number of ones
    numnegones= toplab.count(-1) #and negative ones
    prediction= 1
    if numnegones>numones: prediction=-1 #majority vote
    
    if prediction!=label:
        wrong+=1
        print 'ERROR: %s #1=%d #-1=%d' % (line, numones, numnegones)
    else:
        print 'CORRECT: %s #1=%d #-1=%d' % (line, numones, numnegones)

#print the error rate
print 'Accuracy rate is %f' % (1-(1.0*wrong/len(testset)),)

