#read in positive and negative lines from files
poslines= open(r'rt-polarity.pos', 'r').read().splitlines()
neglines= open(r'rt-polarity.neg', 'r').read().splitlines()
 
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
#if you don't get this look up text comprehensions in Python
trainset= [(x,1) for x in poslinesTrain] + [(x,-1) for x in neglinesTrain]
testset= [(x,1) for x in poslinesTest] + [(x,-1) for x in neglinesTest]
 
#count the number of occurances of each word in positives and negatives
poswords={} #this dictionary will store counts for every word in positives
negwords={} #and negatives
for line,label in trainset: #for every sentence and its label
    for word in line.split(): #for every word in the sentence
         
        #increment the counts for this word based on the label
        #the .get(x, 0) method returns the current count for word 
        #x, of 0 if the word is not yet in the dictionary
        if label==1: poswords[word]= poswords.get(word, 0) + 1
        else: negwords[word]= negwords.get(word, 0) + 1
             
             
#evaluate the test set
wrong=0 #will store number of misslassifications
for line,label in testset:
     
    totpos, totneg= 0.0, 0.0
    for word in line.split():
         
        #get the (+1 smooth'd) number of counts this word occurs in each class
        #smoothing is done in case this word isnt in train set, so that there 
        #is no danger in dividing by 0 later when we do a/(a+b)
        #it's a trick: we are basically artifically inflating the counts by 1.
        a= poswords.get(word,0.0) + 1.0
        b= negwords.get(word,0.0) + 1.0
         
        #increment our score counter for each class, based on this word
        totpos+= a/(a+b)
        totneg+= b/(a+b)
         
    #create prediction based on the counter values
    prediction=1
    if totneg>totpos: prediction=-1
     
    if prediction!=label:
        wrong+=1
        print 'ERROR: posscore=%.2f negscore=%.2f' % (totpos, totneg)
    else:
        print 'CORRECT: posscore=%.2f negscore=%.2f' % (totpos, totneg)
 
#print the error rate
print 'Accuracy rate is %f ' % (1-(1.0*wrong/len(testset)),)
