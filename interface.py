import pickle
import matplotlib.pyplot as plt

k_s = pickle.load(open('pickles/k.p','rb'))
Korder = {}# position and the k_
for k in k_s:
	Korder[k_s[k]]=k

count = pickle.load(open('pickles/ArgsCount.p','rb')) #counts of k given a verb
dep = pickle.load(open('pickles/dependents.p','rb')) #dependent children given a verb

word = raw_input('\nInput the verb - ')

upper_limit = max(count[word])

plt.plot(count[word])
#plt.axis([0,22,0,22])
plt.show()

print "\nNecessary Arguments - ",
for i in range(len(count[word])):
	val = count[word][i]
	if val and val>=upper_limit-10:
		print Korder[i],

print '\n\nAll related words -: '
for i in dep[word]:
	print i[0]+' : '+i[1]

