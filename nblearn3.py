import os
import re
import fnmatch
import sys

def search_files(directory='.', extension=''):

    matches = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, extension):
            if 'README' not in filename:
                matches.append(os.path.join(root, filename))
    return matches


txtfiles = search_files(directory=sys.argv[1], extension="*.txt")


# Count of documents in class
posfilecnt = 0
negfilecnt = 0
truthfilecnt = 0
decfilecnt = 0
filecnt = len(txtfiles)

for filename in txtfiles:
    if 'positive' in filename:
        posfilecnt += 1
    elif 'negative' in filename:
        negfilecnt += 1

    if 'truthful' in filename:
        truthfilecnt += 1
    elif 'deceptive' in filename:
        decfilecnt += 1

prob_pos = posfilecnt/filecnt
prob_neg = negfilecnt/filecnt
prob_truth = truthfilecnt/filecnt
prob_dec = decfilecnt/filecnt


# Class dictionary
classes = {}
# Word-count dictionary
word_dict = {}
#List of all preprocessed all_words
words = []


for filename in txtfiles:
    file = open(filename, 'r')
    text = file.read()
    file.close()
    words = re.split(r'\W+', text)
    words = [word.lower() for word in words]
    # TODO: remove punctuation

    #list of classes
    classlist = []
    if 'positive' in filename:
        classlist.append('positive')
    elif 'negative' in filename:
        classlist.append('negative')

    if 'truthful' in filename:
        classlist.append('truthful')
    elif 'deceptive' in filename:
        classlist.append('deceptive')

#for positive-negative class
    for word in words:
        if word != '':
            if classlist[0] not in classes:
                    classes[classlist[0]] = {word: 1}
            else:
                word_dict = classes[classlist[0]]
                if word not in word_dict:
                    word_dict[word] = 1
                    classes[classlist[0]] = word_dict
                else:
                    word_dict[word] += 1
                    classes[classlist[0]] = word_dict

#for truthful-deceptive class
    for word in words:
         if word != '':
            if classlist[1] not in classes:
                    classes[classlist[1]] = {word: 1}
            else:
                word_dict = classes[classlist[1]]
                if word not in word_dict:
                    word_dict[word] = 1
                    classes[classlist[1]] = word_dict
                else:
                    word_dict[word] += 1
                    classes[classlist[1]] = word_dict


# count total number of words in each class
positive_words = 0
for k in classes['positive']:
    positive_words += classes['positive'][k]


negative_words = 0
for k in classes['negative']:
    negative_words += classes['negative'][k]


truthful_words = 0
for k in classes['truthful']:
    truthful_words += classes['truthful'][k]


deceptive_words = 0
for k in classes['deceptive']:
    deceptive_words += classes['deceptive'][k]

#count of vocabulary
vocabulary = []
for k in classes['positive']:
    if k not in vocabulary:
        vocabulary.append(k)
for k in classes['negative']:
    if k not in vocabulary:
        vocabulary.append(k)
for k in classes['truthful']:
    if k not in vocabulary:
        vocabulary.append(k)
for k in classes['deceptive']:
    if k not in vocabulary:
        vocabulary.append(k)

vocab = len(vocabulary)

# probability of word given class P(word|class)

word_given_pos = 0
word_given_neg = 0
word_given_truth = 0
word_given_dec = 0
probabilities = {}

#creating a dictionary of probabilities with add one smoothing
for word in vocabulary:
    if word in classes['positive']:
        word_given_pos = (classes['positive'][word] + 1) /(positive_words + vocab)
        probabilities[word] = [word_given_pos]
    else:
        probabilities[word] = [1 / (positive_words + vocab)]

    if word in classes['negative']:
        word_given_neg = (classes['negative'][word] + 1) /(negative_words + vocab)
        probabilities[word].append(word_given_neg)
    else:
        probabilities[word].append(1 / (negative_words + vocab))

    if word in classes['truthful']:
        word_given_truth = (classes['truthful'][word] + 1) /(truthful_words + vocab)
        probabilities[word].append(word_given_truth)
    else:
        probabilities[word].append(1 / (truthful_words + vocab))

    if word in classes['deceptive']:
        word_given_dec = (classes['deceptive'][word] + 1) /(deceptive_words + vocab)
        probabilities[word].append(word_given_dec)
    else:
        probabilities[word].append(1 / (deceptive_words + vocab))



#writing into the text file
output = open ('nbmodel.txt' , 'w')
output.write('Probability_of_classes' + '\t' + str(prob_pos) + '\t' + str(prob_neg) + '\t' + str(prob_truth) + '\t' + str(prob_dec) + '\n')
for word in vocabulary:
    output.write(word + '\t' + str(probabilities[word][0]) + '\t' + str(probabilities[word][1]) + '\t' + str(probabilities[word][2]) + '\t' + str(probabilities[word][3]) + '\n')

output.close
