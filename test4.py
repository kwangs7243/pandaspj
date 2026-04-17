from DataAnalyzer import DataAnalyzer
from ExpenseAnalyzer import ExpenseAnalyzer
import datetime as dt
da = DataAnalyzer()


da.load_data("messy_expense_data_large.csv")
da.preprocess_data()
data = da.get_analysis_data()
ea = ExpenseAnalyzer(data)
# print(ea.get_view_data(ea.df))
a = dt.datetime.strptime("2025-01-01","%Y-%m-%d")
b = dt.datetime.strptime("2025-01-20","%Y-%m-%d")
print(ea.filter_by_date_range(a,b))
# print(ea.df.columns)
# print(ea.df.dtypes)
# print(ea.df["date"].head())
# print(type(a), type(b))
