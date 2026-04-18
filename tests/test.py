from src.DataAnalyzer import DataAnalyzer
from src.ExpenseAnalyzer import ExpenseAnalyzer
import datetime as dt
#  python -m tests.test
da = DataAnalyzer()
da.load_data("data/raw/realistic_expense_1000.csv")
da.preprocess_data()
ea = ExpenseAnalyzer(da.get_analysis_data())
# a = dt.datetime.strptime("")
data = ea.filter_by_date_range("2025-01-01","2025-03-01")
print(ea.get_view_data(data,order="asc"))
