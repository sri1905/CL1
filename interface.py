import sys
import pickle
import numpy as np
import matplotlib.pyplot as plt

c = pickle.load(open('pickles/ArgsCount.p','rb')) #counts of k given a verb
dep = pickle.load(open('pickles/dependents.p','rb')) #dependent children given a verb
k = pickle.load(open('pickles/k.p','rb'))
Korder = {}# position and the k_
for ks in k:
	Korder[k[ks]]=ks

word = raw_input('\nInput the verb - ')
factor = input('Factor to cutoff - ')

upper_limit = max(c[word])
total = len(k)+3

x = np.arange(0,total,1)
kas = np.array([0]+k.keys()+[len(k)+1,len(k)+2])
plt.xticks(x,kas)

plt.title('Frequency of Karakas')
plt.xlabel('Karakas')
plt.ylabel('Frequency')

plt.axis([0,len(k)+2,-2,max(c[word])+2])
plt.grid(True)
plt.plot([None]+c[word],'ro')

cutoff = factor*max(c[word])

print ("\nNecessary Arguments - "),
for i in range(len(c[word])):
	val = c[word][i]
	if val and val>=cutoff:
		print (Korder[i]),

print ('\n\nAll related words -: ')
for i in dep[word]:
	print ('\t\t'+i[0]+' : '+i[1])

plt.show()