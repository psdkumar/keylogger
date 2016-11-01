from data_framer import DataFramer
import os

df = DataFramer()
df.get_all_paths(os.path.join(os.getcwd(), "Testing"))
df.extract_data()
df.make_dataframe()
df.make_csv()