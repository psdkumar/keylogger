#!/usr/bin/python

import os
import glob
import pandas as pd
import numpy as np


class DataFramer:

	def __init__(self):
		
		self.dic = {}
		self.filepaths = []
		self.filename = []
		self.data = []
		self.mean = []
		self.size = []
		self.df = pd.DataFrame()


	def get_all_paths(self):

		curr_dir = os.getcwd()
		directories = ["Primary_features", "Secondary_features_down", "Secondary_features_up", "Teritiary_features"]
		for directory in directories : 
			features_dir = os.path.join(curr_dir, directory)
			file_search = os.path.join(features_dir, '*.txt')	
			self.filepaths.extend(glob.glob(file_search))
		# print filepaths	
	

	def get_specific_paths(self, paths):

		self.filepaths = paths


	def extract_data(self):

		for i,filepath in enumerate(self.filepaths) :
			file = open(filepath, 'r')
			tmp = ""
			if "_down" in filepath :
				tmp = "down_"
			elif "_up" in filepath :
				tmp = "up_"
			self.filename.append(tmp + os.path.splitext(os.path.basename(filepath))[0])
			content = file.readlines()
			file.close()

			self.data.append(content)
			for j,val in enumerate(self.data[i]) :
				self.data[i][j] = float(self.data[i][j])
			self.mean.append(round(np.mean(self.data[i]),6))
			self.size.append(len(content))

	def make_dataframe(self):

		self.max_size = max(self.size)
		self.min_size = min(self.size)
		# print self.min_size,self.max_size,self.size

		for i,filepath in enumerate(self.filepaths) :
			if self.size[i] < self.max_size :
				for j in range(self.size[i],self.max_size) :
					self.data[i].append(self.mean[i])
			self.dic[self.filename[i]] = self.data[i]		 
		
		# print self.dic
		self.df = pd.DataFrame(self.dic)
		print self.df


	def make_csv(self):

		self.df.to_csv("data.csv", sep='\t')


if __name__ == '__main__':
	df = DataFramer()
	df.get_all_paths()
	df.extract_data()
	df.make_dataframe()
	df.make_csv()