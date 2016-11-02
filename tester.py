import os
import keylogger as kl
from data_framer import TestingDataFramer

def start_test() :
    #running keylogger
    print "type for 10 seconds......"
    kl.start_keylogger(10)

def create_final_CSVs() :
	tdf = TestingDataFramer()
	tdf.get_all_paths(os.path.join(os.getcwd(), "Testing"))
	tdf.extract_data()
	tdf.make_dataframe()
	tdf.make_csv()

if __name__ == '__main__':
    start_test()
    create_final_CSVs()



