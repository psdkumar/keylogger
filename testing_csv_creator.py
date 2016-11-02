from data_framer import TestingDataFramer
import os

tdf = TestingDataFramer()
tdf.get_all_paths(os.path.join(os.getcwd(), "Testing"))
tdf.extract_data()
tdf.make_dataframe()
tdf.make_csv()