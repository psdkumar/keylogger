#!/usr/bin/python

import os
import glob
import pandas as pd
import numpy as np

dic = {}
filepaths = []
filename = []
data = []
mean = []
size = []

curr_dir = os.getcwd()
directories = ["Primary_features", "Secondary_features_down", "Secondary_features_up", "Teritiary_features"]
for directory in directories : 
	features_dir = os.path.join(curr_dir, directory)
	file_search = os.path.join(features_dir, '*.txt')	
	filepaths = glob.glob(file_search)
# print filepaths	

for i,filepath in enumerate(filepaths) :
	file = open(filepath, 'r')
	filename.append(os.path.splitext(os.path.basename(filepath))[0])
	content = file.readlines()
	file.close()
	data.append(content)
	size.append(len(content))
	# Calculating Mean
	data_sum = 0
	for j,val in enumerate(data[i]) :
		data[i][j] = float(data[i][j])
		data_sum += data[i][j]
	mean_data = data_sum / max(len(content),1) 
	mean.append(mean_data)

max_size = max(size)
min_size = min(size)

for i,filepath in enumerate(filepaths) :
	if size[i] < max_size :
		for j in range(size[i],max_size) :
			data[i].append(round(mean[i],6))
	dic[filename[i]] = data[i]		 

# print dic
df = pd.DataFrame(dic)
print df
df.to_csv("data.csv", sep='\t')