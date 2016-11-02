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
		self.dframe = pd.DataFrame()


	def get_all_paths(self,this_dir):

		self.curr_dir = this_dir
		directories = ["Primary_features", "Secondary_features_down", "Secondary_features_up", "Teritiary_features"]
		for directory in directories : 
			features_dir = os.path.join(self.curr_dir, directory)
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
		
		self.dic["user"] = [0] * self.max_size
		self.dframe0 = pd.DataFrame(self.dic)
		self.dic["user"] = [1] * self.max_size
		self.dframe1 = pd.DataFrame(self.dic)
		print self.dframe0


	def make_csv(self):

		self.dframe0.to_csv(os.path.join(self.curr_dir, "data_0.csv"), sep='\t')
		self.dframe1.to_csv(os.path.join(self.curr_dir, "data_1.csv"), sep='\t')


class TestingDataFramer:

	def __init__(self):
		# Train Variables
		self.train_dic = {}
		self.train_filepaths = []
		self.train_filename = []
		self.train_data = []
		self.train_mean = []
		self.train_size = []
		self.train_dframe = pd.DataFrame()
		# Test Variables
		self.test_dic = {}
		self.test_filepaths = []
		self.test_filename = []
		self.test_data = []
		self.test_mean = []
		self.test_size = []
		self.test_dframe = pd.DataFrame()


	def get_all_paths(self,this_dir):

		self.home_dir = os.getcwd()
		self.test_dir = this_dir
		directories = ["Primary_features", "Secondary_features_down", "Secondary_features_up", "Teritiary_features"]
		for directory in directories : 
			# Test Files
			test_features_dir = os.path.join(self.test_dir, directory)
			test_file_search = os.path.join(test_features_dir, '*.txt')	
			self.test_filepaths.extend(glob.glob(test_file_search))

			# Train Files
			train_features_dir = os.path.join(self.home_dir, directory)
			train_file_search = os.path.join(train_features_dir, '*.txt')	
			self.train_filepaths.extend(glob.glob(train_file_search))

		# print self.test_filepaths
		# print self.train_filepaths	
	

	def get_specific_paths(self, paths):

		self.filepaths = paths


	def extract_data(self):

		tmp_train_filepaths = []
		for i,test_filepath in enumerate(self.test_filepaths) :
			tmp_filepath = os.path.join(os.getcwd(),os.path.basename(os.path.dirname(test_filepath)),os.path.basename(test_filepath))
			if tmp_filepath in self.train_filepaths :
				train_filepath = tmp_filepath
				tmp_train_filepaths.append(tmp_filepath)
				test_file = open(test_filepath, 'r')
				train_file = open(train_filepath, 'r')

				tmp = ""
				if "_down" in test_filepath :
					tmp = "down_"
				elif "_up" in test_filepath :
					tmp = "up_"

				self.test_filename.append(tmp + os.path.splitext(os.path.basename(test_filepath))[0])
				self.train_filename.append(tmp + os.path.splitext(os.path.basename(train_filepath))[0])
			
				test_content = test_file.readlines()
				train_content = train_file.readlines()
				
				test_file.close()
				train_file.close()

				self.test_data.append(test_content)
				self.train_data.append(train_content)
				
				for j,val in enumerate(self.test_data[i]) :
					self.test_data[i][j] = float(self.test_data[i][j])
				for j,val in enumerate(self.train_data[i]) :
					self.train_data[i][j] = float(self.train_data[i][j])

				self.test_mean.append(round(np.mean(self.test_data[i]),6))
				self.train_mean.append(round(np.mean(self.train_data[i]),6))
				
				self.test_size.append(len(test_content))
				self.train_size.append(len(train_content))
			else :
				self.test_filepaths.remove(test_filepath)
		self.train_filepaths = tmp_train_filepaths

	def make_dataframe(self):
		
		self.test_max_size = max(self.test_size)
		self.train_max_size = max(self.train_size)
		
		self.test_min_size = min(self.test_size)
		self.train_min_size = min(self.train_size)
		
		# print self.test_min_size,self.test_max_size,self.test_size
		# print self.train_min_size,self.train_max_size,self.train_size

		for i,test_filepath in enumerate(self.test_filepaths) :
			if self.test_size[i] < self.test_max_size :
				for j in range(self.test_size[i],self.test_max_size) :
					self.test_data[i].append(self.test_mean[i])
			self.test_dic[self.test_filename[i]] = self.test_data[i]

		for i,train_filepath in enumerate(self.train_filepaths) :
			if self.train_size[i] < self.train_max_size :
				for j in range(self.train_size[i],self.train_max_size) :
					self.train_data[i].append(self.train_mean[i])
			self.train_dic[self.train_filename[i]] = self.train_data[i]		 
		
		self.test_dic["user"] = [0] * self.test_max_size
		self.test_dframe0 = pd.DataFrame(self.test_dic)
		self.test_dic["user"] = [1] * self.test_max_size
		self.test_dframe1 = pd.DataFrame(self.test_dic)
		print self.test_dframe0

		self.train_dic["user"] = [0] * self.train_max_size
		self.train_dframe0 = pd.DataFrame(self.train_dic)
		self.train_dic["user"] = [1] * self.train_max_size
		self.train_dframe1 = pd.DataFrame(self.train_dic)
		print self.train_dframe0


	def make_csv(self):

		self.test_dframe0.to_csv(os.path.join(self.test_dir, "test_data_0.csv"), sep='\t')
		self.test_dframe1.to_csv(os.path.join(self.test_dir, "test_data_1.csv"), sep='\t')

		self.train_dframe0.to_csv(os.path.join(self.test_dir, "train_data_0.csv"), sep='\t')
		self.train_dframe1.to_csv(os.path.join(self.test_dir, "train_data_1.csv"), sep='\t')