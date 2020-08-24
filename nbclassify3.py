import os
import re
import fnmatch
import sys
import math

def search_files(directory='.', extension=''):

    matches = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, extension):
            if 'README' not in filename:
                matches.append(os.path.join(root, filename))
    return matches


txtfiles = search_files(directory=sys.argv[2], extension="*.txt")

#reading the text file into a dictionary
model = {}
openfile = open("nbmodel.txt",'r')
for line in openfile:
    field = line.strip().split('\t')
    probs = []
    word = field[0]
    probs.append(field[1])
    probs.append(field[2])
    probs.append(field[3])
    probs.append(field[4])
    model[word] = probs

results = {}
#reading the test file
for filename in txtfiles:
    # print(filename)
    file = open(filename, 'r')
    text = file.read()
    file.close()
    words = re.split(r'\W+', text)
    words = [word.lower() for word in words]

#Calculating and multiplying the probabilities of text|class

    pos_prob = 0
    neg_prob = 0
    truth_prob = 0
    dec_prob = 0
    for word in words:
        if word in model and word != '':
            pos_prob += math.log(float(model[word][0]))
            neg_prob += math.log(float(model[word][1]))
            truth_prob += math.log(float(model[word][2]))
            dec_prob += math.log(float(model[word][3]))

#Calculating probabilities of file|class

    prob_file_given_pos = math.log(float(model['Probability_of_classes'][0])) + pos_prob
    prob_file_given_neg = math.log(float(model['Probability_of_classes'][1])) + neg_prob
    prob_file_given_truth = math.log(float(model['Probability_of_classes'][2])) + truth_prob
    prob_file_given_dec = math.log(float(model['Probability_of_classes'][3])) + dec_prob

    if max(prob_file_given_truth,prob_file_given_dec) == prob_file_given_truth:
        label_a = 'truthful'
    else:
        label_a = 'deceptive'

    if max(prob_file_given_pos,prob_file_given_neg) == prob_file_given_pos:
        label_b = 'positive'
    else:
        label_b = 'negative'

# create a dictionary with key as filename and value as classifier result
    results[filename] = [label_a]
    results[filename].append(label_b)

# Write output to output file

output = open ('nboutput.txt' , 'w')

for filename in results:
    output.write(str(results[filename][0]) + '\t' + str(results[filename][1]) + '\t' + str(filename) + '\n')

output.close
