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


	def get_all_paths(self,true_dir,false_dir,test_dir):

		self.home_dir = os.getcwd()
		self.tft_dirs = [true_dir,false_dir,test_dir]
		self.tft_filepaths = [[],[],[]]

		#directories = ["Primary_features", "Secondary_features_down", "Secondary_features_up", "Teritiary_features"]
		directories = ["Primary_features", "Teritiary_features"]
		for i,tft_dir in enumerate(self.tft_dirs):
			for directory in directories :
				# Test Files
				tft_features_dir = os.path.join(tft_dir, directory)
				tft_file_search = os.path.join(tft_features_dir, '*.txt')
				self.tft_filepaths[i].extend(glob.glob(tft_file_search))


	def extract_data(self):

		tmp_tft_filepaths = [[],[],[]]
		tft_filepath = ['','','']
		self.tft_filename = [[],[],[]]
		tft_content = [[],[],[]]
		self.tft_data = [[],[],[]]
		self.tft_mean = [[],[],[]]
		self.tft_size = [[],[],[]]
		k =0
		for i,test_filepath in enumerate(self.tft_filepaths[2]) :
			tmp_filepath = []
			tmp_filepath.append(os.path.join(os.getcwd(),"true",os.path.basename(os.path.dirname(test_filepath)),os.path.basename(test_filepath)))
			tmp_filepath.append(os.path.join(os.getcwd(),"false",os.path.basename(os.path.dirname(test_filepath)),os.path.basename(test_filepath)))

			if tmp_filepath[0] in self.tft_filepaths[0] and tmp_filepath[1] in self.tft_filepaths[1] :
				tft_filepath[0] = tmp_filepath[0]
				tft_filepath[1] = tmp_filepath[1]
				tft_filepath[2] = test_filepath

				tmp_tft_filepaths[0].append(tft_filepath[0])
				tmp_tft_filepaths[1].append(tft_filepath[1])

				tft_file = []
				for p in range(0,3) :
					tft_file.append(open(tft_filepath[p], 'r'))

				tmp = ""
				if "_down" in test_filepath :
					tmp = "down_"
				elif "_up" in test_filepath :
					tmp = "up_"

				for p in range(0,3) :
					self.tft_filename[p].append(tmp + os.path.splitext(os.path.basename(tft_filepath[p]))[0])
					tft_content[p] = tft_file[p].readlines()
					tft_file[p].close()
					self.tft_data[p].append(tft_content[p])

				for p in range(0,3) :
					for j,val in enumerate(self.tft_data[p][k]) :
						self.tft_data[p][k][j] = float(self.tft_data[p][k][j])

				for p in range(0,3) :
					self.tft_mean[p].append(round(np.mean(self.tft_data[p][k]),6))
					self.tft_size[p].append(len(tft_content[p]))

				k += 1
			else:
				i -= 1
				tmp_tft_filepaths[2].append(test_filepath)

		for tmp_test_filepath in tmp_tft_filepaths[2] :
			self.tft_filepaths[2].remove(tmp_test_filepath)

		for p in range(0,2):
			self.tft_filepaths[p] = tmp_tft_filepaths[p]

		# print self.tft_filepaths[0]


	def make_dataframe(self):
		self.tft_max_size = []
		self.tft_min_size = []
		tft_filepath = ['','','']
		self.tft_dic = [{},{},{}]
		self.tft_dframe = ['','','']

		for p in range(0,3):
			self.tft_max_size.append(max(self.tft_size[p]))
			self.tft_min_size.append(min(self.tft_size[p]))

		self.tft_max_size[0]= 50
		self.tft_max_size[1]= 50

		for p in range(0,3):
			for i,tft_filepath[p] in enumerate(self.tft_filepaths[p]):
				if self.tft_size[p][i] < self.tft_max_size[p] :
					for j in range(self.tft_size[p][i],self.tft_max_size[p]):
						self.tft_data[p][i].append(self.tft_mean[p][i])
				else :
					self.tft_data[p][i] = self.tft_data[p][i][0:self.tft_max_size[0]]
				self.tft_dic[p][self.tft_filename[p][i]] = self.tft_data[p][i]


		self.tft_dic[0]["zzzzzz"] = [1] * self.tft_max_size[0]
		#print self.tft_dic[0]
		self.tft_dframe[0] = pd.DataFrame(self.tft_dic[0])
		#self.tft_dframe[0].insert(len(self.tft_filename[0]),"user",[1] * self.tft_max_size[0])
		self.tft_dic[1]["zzzzzz"] = [0] * self.tft_max_size[1]
		self.tft_dframe[1] = pd.DataFrame(self.tft_dic[1])
		self.tft_dic[2]["zzzzzz"] = [0] * self.tft_max_size[2]
		self.tft_dframe[2] = pd.DataFrame(self.tft_dic[2])
		#print self.tft_dframe[0]
		#print self.tft_dframe[1]

	def make_csv(self):

		train_data = pd.concat([self.tft_dframe[0],self.tft_dframe[1]])
		test_data = self.tft_dframe[2]

		train_data.to_csv(os.path.join(self.tft_dirs[2], "train_data.csv") ,sep=',' ,index=False ,header=False)
		test_data.to_csv(os.path.join(self.tft_dirs[2], "test_data.csv") ,sep=',' ,index=False ,header=False)

		#with open(os.path.join(self.tft_dirs[2], "train_data.csv"))


	def get_columns(self) :
		return self.tft_filename[0]

