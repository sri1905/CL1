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
				if token[-3][0] =='k' :
					relation_dict[sent[int(token[-4])-1][1]].append((token[1],token[-3]))


	print("############## ALL RELATIONS #################")
	for key,value in relation_dict.items() :
		print(key," --- > ",value)
		print("\n")

	seen = []
	for i in all_sent :
		for l in i:
			if l[-3] not in seen :
				if l[-3][0] =='k':
					seen.append(l[-3])

	print("###### ALL RELATION KINDS #########")
	print(sorted(seen))
	print(len(seen))

	K_position = {}
	count = 0
	for ks in sorted(seen) :
		K_position[ks] = count
		count += 1
	
	count_keys = {}
	for keys in  relation_dict.keys() :
		count_keys[keys] = [0] * len(seen)

	for key,value in relation_dict.items():
		for tuples in value :
			count_keys[key][K_position[tuples[1]]] += 1
	
 
	print("############## ALL COUNTS #################")
	for key,value in count_keys.items() :
		print(key," --- > ",value)
		print("\n")

	




