import os
import glob
import keylogger as kl
from data_framer import TestingDataFramer
import L_regressor as LR

def clean_testing_dir(directory) :
	contents = glob.glob(os.path.join(directory,'*'))
	if len(contents) > 0 :
		for content in contents :
			if os.path.isfile(content) :
				os.remove(content)
			else :
				clean_testing_dir(content)

def start_test() :
	#running keylogger
	print "type for 10 seconds......"
	kl.start_keylogger(10)

def create_final_CSVs() :
	tdf = TestingDataFramer()
	tdf.get_all_paths(os.path.join(os.getcwd(), "true"),os.path.join(os.getcwd(), "false"),os.path.join(os.getcwd(), "Testing"))
	tdf.extract_data()
	tdf.make_dataframe()
	tdf.make_csv()
	return tdf.get_columns()

if __name__ == '__main__':
	clean_testing_dir(os.path.join(os.getcwd(),"Testing"))
	start_test()
	columns = create_final_CSVs()
	columns.append("user")

	print columns

	LR.COLUMNS = columns
	LR.CONTINUOUS_COLUMNS = columns

	LR.train_and_eval()
