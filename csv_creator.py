from data_framer import DataFramer
import os

df = DataFramer()
df.get_all_paths(os.getcwd())
df.extract_data()
df.make_dataframe()
df.make_csv()