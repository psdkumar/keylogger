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
length = []

curr_dir = os.getcwd()
directories = ["Primary_features", "Secondary_features_down", "Secondary_features_up", "Teritiary_features"]
# directories = ["Primary_features"]

for directory in directories : 
	features_dir = os.path.join(curr_dir, directory)
	file_search = os.path.join(features_dir, '*.txt')	
	filepaths = glob.glob(file_search)
# print filepaths	

# filepaths = ["/home/sai/Documents/keylogger/Primary_features/bracketleft.txt", "/home/sai/Documents/keylogger/Primary_features/1.txt"]
for i,filepath in enumerate(filepaths) :
	file = open(filepath, 'r')
	filename.append(os.path.splitext(os.path.basename(filepath))[0])
	content = file.readlines()
	file.close()
	data.append(content)
	length.append(len(content))
	
	# Calculating Mean
	data_sum = 0
	for j,val in enumerate(data[i]) :
		data[i][j] = float(data[i][j])
		data_sum += data[i][j]
	mean_data = data_sum / max(len(content),1) 
	mean.append(mean_data)

max_len = max(length)
for i,filepath in enumerate(filepaths) :
	if length[i] < max_len :
		for j in range(length[i],max_len) :
			data[i].append(round(mean[i],6))
	dic[filename[i]] = data[i]		 

# print dic
df = pd.DataFrame(dic)
print df

df.to_csv("data.csv", sep='\t')
