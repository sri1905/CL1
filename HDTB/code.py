import sys

if __name__ == "__main__" :
	
	with open(sys.argv[1]) as f :
		alllines = f.readlines()
	
	all_sent = []
	curr_sent = []

	for line in alllines :
		if line == "\n" :
			all_sent.append(curr_sent)
			curr_sent = []
		else :
			curr_sent.append(line.split())

	
	relation_dict = {}

	for sent in all_sent :
		position_list = []
		for i,token in enumerate(sent) :
			if token[3] == 'v' :
				position_list.append(token[0])
				if token[1] not in relation_dict :
					relation_dict[token[1]] = []
		for i,token in enumerate(sent) :
			if token[-4] in position_list :
				if token[-3][0] =='k' and len(token[-3]) == 2:
					relation_dict[sent[int(token[-4])-1][1]].append((token[1],token[-3]))


	print("############## ALL RELATIONS #################")
	for key,value in relation_dict.items() :
		print(key," --- > ",value)
		print("\n")

	seen = []
	for i in all_sent :
		for l in i:
			if l[-3] not in seen :
				seen.append(l[-3])

	print("###### ALL RELATION KINDS #########")
	print(seen)
	print(len(seen))
