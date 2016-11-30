import sys
import pickle
from collections import OrderedDict


class Verb():
	def __init__(self):

		self.verb_name = "null"
		self.arclabel = 'null'
		self.pos = []
		self.vib = []
		self.position = []
		self.count = 0

	def print_values(self):
		# print(self.verb_name)
		print(self.arclabel)
		print(self.pos)
		print(self.vib)
		print(self.position)
		print(self.count)
		

	def get_arclabel(self):
		return(self.arclabel)


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

	
	relation_dict = OrderedDict()

	for sent in all_sent :
		position_list = []
		for i,token in enumerate(sent) :
			if token[3] == 'v' :
				position_list.append(token[0])
				if token[2] not in relation_dict :
					relation_dict[token[2]] = []
		for i,token in enumerate(sent) :
			if token[-4] in position_list :
				if token[-3][0] =='k' :
					

					if relation_dict[sent[int(token[-4])-1][2]] is not [] :
						check_flag = False
						for ko in relation_dict[sent[int(token[-4])-1][2]] :
							if token[-3] == ko.get_arclabel() :
								ko.pos.append(token[3])
								ko.vib.append(token[5].split('|')[5].replace("vib-0"," ").replace("vib-"," "))
								if token[0] < token[-4]:
							 		ko.position.append("before")
								else :
									ko.position.append("after")
								ko.count += 1
								check_flag = True
								break

						if check_flag == False :
							temp_verb = Verb()
							temp_verb.verb_name = sent[int(token[-4])-1][2]
							temp_verb.arclabel = token[-3]
							temp_verb.pos.append(token[3])
							temp_verb.vib.append(token[5].split('|')[5].replace("vib-0"," ").replace("vib-"," "))
							temp_verb.count = 1
							if token[0] < token[-4]:
							 	temp_verb.position.append("before")
							else :
								temp_verb.position.append("after")

							relation_dict[sent[int(token[-4])-1][2]].append(temp_verb)



					else :
						temp_verb = Verb()
						temp_verb.verb_name = sent[int(token[-4])-1][2]
						temp_verb.arclabel = token[-3]
						temp_verb.pos.append(token[3])
						temp_verb.vib.append(token[5].split('|')[5].replace("vib-0"," ").replace("vib-"," "))
						temp_verb.count = 1
						if token[0] < token[-4]:
						 	temp_verb.position.append("before")
						else :
							temp_verb.position.append("after")

						relation_dict[sent[int(token[-4])-1][2]].append(temp_verb)



	print("############## ALL RELATIONS #################")
	for key,value in relation_dict.items() :
		print("Verb -> ",key)
		for i in value :
			i.print_values()
			print("\n")

	# seen = []
	# for i in all_sent :
	# 	for l in i:
	# 		if l[-3] not in seen :
	# 			if l[-3][0] =='k':
	# 				seen.append(l[-3])

	# print("###### ALL RELATION KINDS #########")
	# print (sorted(seen))
	# print (len(seen))

	# K_position = OrderedDict()
	# count = 0
	# for ks in sorted(seen) :
	# 	K_position[ks] = count
	# 	count += 1
	
	# count_keys = OrderedDict()
	# for keys in  relation_dict.keys() :
	# 	count_keys[keys] = [0] * len(seen)

	# for key,value in relation_dict.items():
	# 	for tuples in value :
	# 		count_keys[key][K_position[tuples[1]]] += 1
	
 
	# print("############## ALL COUNTS #################")
	# for key,value in count_keys.items() :
	# 	#key = key.decode('utf-8')
	# 	print (key," --- > ",value)
	# 	print("\n")
	# print (K_position)

	# pickle.dump(count_keys,open('pickles/ArgsCount.p','wb'))
	# pickle.dump(K_position,open('pickles/k.p','wb'))
	# pickle.dump(relation_dict,open('pickles/dependents.p','wb'))
