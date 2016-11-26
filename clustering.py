import random
import numpy 
import sys
import operator
import scipy.linalg
import scipy
import pickle
from scipy.spatial import distance
from collections import Counter



NO_OF_CLUSTERS = 50

def d_mean(clusters):
	one = 1
	two = 1
	min_dist = 90000000000000000000000
	for i in range(len(clusters)) :
		for j in range(i+1,len(clusters)) :
			a = numpy.mean(clusters[i])
			b = numpy.mean(clusters[j])
			dist = distance.euclidean(a,b)
			if dist < min_dist :
				min_dist = dist
				one = i
				two = j
	return one,two

def d_min(clusters):
	
	one = 4
	two = 4
	min_dist = 90000000000000000000000

	for i in range(len(clusters)) :
		for j in range(i+1,len(clusters)) :
			cluster1 = clusters[i]
			cluster2 = clusters[j]
			for point1 in cluster1 :
				for point2 in cluster2:
					if point1 == point2 :
						print("SHIT HAPPENED")
						sys.exit()
					dist = distance.sqeuclidean(point1,point2)
					if dist < min_dist :
						min_dist = dist
						one = i
						two = j

	return one,two



def agglomerative_clustering(data,no_of_clusters):
	c = len(data.keys())
	clusters = []
	for point in data.keys() :
		temp = []
		temp.append(point)
		clusters.append(temp)
	# print(clusters)
	# print(len(clusters))
	while c > no_of_clusters :
		# print(len(clusters))
		# one,two = random.sample(range(len(clusters)), 2)
		one,two = d_mean(clusters)
		clusters[one] = clusters[one] + clusters[two]
		del clusters[two]
		c -= 1
	# print(len(clusters))
	count = 0
	for i in clusters :
		count = count + len(i)
	# print(count)

	return clusters


def kernel_K_means(data,no_of_clusters,kernel):
	data_points = []
	for point in data.keys() :
		data_points.append(point)

	data_dict = {}
	for i, point in enumerate(data_points) :
		data_dict[point] = i

	# one_vectors = [ [ 0 for j in range(no_of_clusters)] for i in range(len(data_points)) ] 
	means = [ [data_points[i]] for i in random.sample(range(len(data_points)), no_of_clusters) ]


	if kernel == "rbf" :

		distance_matrix = distance.cdist(data_points,data_points, 'sqeuclidean')
		s = 1000
		rbf_kernel_matrix = scipy.exp(-1*(distance_matrix ** 2) /( s ** 2))

	elif kernel == "polynomial" :
		c = 2
		d = 5
		poly_kernel_matrix = [[[] for i in range(len(data_points))] for j in range(len(data_points)) ]
		for i, point1 in enumerate(data_points) :
			for j,point2 in enumerate(data_points) :
				poly_kernel_matrix[i][j] = (numpy.array(point1).T.dot(numpy.array(point2)) + c) ** d
		poly_kernel_matrix = numpy.array(poly_kernel_matrix)
		# print(poly_kernel_matrix.shape)


	flag = True

	count = 0
	while flag == True and count < 10:
		# print(count)
		for point in data_points :
			prev_means = means[:]
			min_dist = 90000000000000000
			min_j = 0
			for j,cluster in enumerate(means) :
				
				if kernel == "rbf" :
					first_term = rbf_kernel_matrix[data_dict[point]][data_dict[point]]
				elif kernel == "polynomial" :
					first_term = poly_kernel_matrix[data_dict[point]][data_dict[point]]
				
				temp_sum = 0
				for po in cluster :
					if kernel == "rbf" :
						temp_sum = temp_sum + rbf_kernel_matrix[data_dict[point]][data_dict[po]]
					elif kernel == "polynomial" :
						temp_sum = temp_sum + poly_kernel_matrix[data_dict[point]][data_dict[po]]
				if len(cluster) == 0 :
					second_term = 0
				else :
					second_term = 2 * temp_sum / len(cluster)

				temp_sum = 0
				for po1 in cluster :
					for po2 in cluster :
						if po1 != po2 :
							if kernel == "rbf" :
								temp_sum = temp_sum + rbf_kernel_matrix[data_dict[po1]][data_dict[po2]]
							elif kernel == "polynomial" :
								temp_sum = temp_sum + poly_kernel_matrix[data_dict[po1]][data_dict[po2]]
				if len(cluster) == 0 :
					third_term = 0
				else :
					third_term = temp_sum / (len(cluster) **2)

				dist = first_term - second_term + third_term
				if dist < min_dist :
					min_dist = dist
					min_j = j
			for i,f in enumerate(means) :
				if point in f :
					means[i].remove(point)
			means[min_j].append(point)

		if prev_means == means :
			flag = True
		count +=1
	return means





def K_means_clustering(data,no_of_clusters):
	
	data_points = []
	for point in data.keys() :
		data_points.append(point)

	one_vectors = [ [ 0 for j in range(no_of_clusters)] for i in range(len(data_points)) ] 
	means = [ data_points[i] for i in random.sample(range(len(data_points)), no_of_clusters) ]

	theta = 1
	while theta > 0.000000000000000000001 :
		for i,point in enumerate(data_points) :
			min_dist = 90000000000000000
			min_j = 0
			for j,mean in enumerate(means) :
				dist = distance.euclidean(point,mean) ** 2
				if dist < min_dist :
					min_dist = dist
					min_j = j
			one_vectors[i][min_j] = 1

		prev_means = means[:]
		new_means = []	
		for j,mean in enumerate(means) :

			numerator = tuple([0 for r in range(len(mean))])
			denominator = 0
			for i,point in enumerate(data_points) :
				numerator = tuple(map(sum,zip(numerator,tuple([one_vectors[i][j] * valu for valu in point]))))
				denominator += one_vectors[i][j]
				
			new_means.append(tuple([val/denominator for val in numerator]) )
		means = new_means[:]

		mean_diff = []

		for y,mean in enumerate(new_means) :
			dist = distance.euclidean(new_means[y],prev_means[y])
			mean_diff.append(dist)

		theta = max(mean_diff)

	clusters = [ [] for i in range(no_of_clusters)]
	for i,vec in enumerate(one_vectors) :
		for j,value in enumerate(vec) :
			if value == 1 :
				clusters[j].append(data_points[i])
	return clusters


def get_data():

	# no_of_clusters = NO_OF_CLUSTERS
	no_of_clusters = int(input("Enter the no of clusters : "))
	data = {}
	counts = pickle.load(open('pickles/ArgsCount.p','rb'))
	for key,value in counts.items() :
		data[tuple(value)] = key

	return data,no_of_clusters


if __name__=="__main__" :

	data,no_of_clusters = get_data()

	# for key,val in data.items() :
	# 	print(key," : ",val)
	# 	print(" ")
	# print(no_of_clusters)

	# print("######### AGGLOMERATIVE CLUSTERING ####################")
	# clusters = agglomerative_clustering(data,no_of_clusters)

	print("######## K_MEANS CLUSTERING ##########################")
	clusters = K_means_clustering(data,no_of_clusters)

	# print("######### KERNEL K_MEANS CLUSTERING ##########################")
	# clusters = kernel_K_means(data,no_of_clusters,"rbf")

	for cluster in clusters :
		listt = []
		for point in cluster :
			listt.append(data[point])
		print(listt , "\n")
	print(len(clusters))
