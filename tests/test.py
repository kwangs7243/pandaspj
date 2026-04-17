from src.DataAnalyzer import DataAnalyzer
from src.ExpenseAnalyzer import ExpenseAnalyzer
#  python -m tests.test
da = DataAnalyzer()
da.preprocess_data()
ea = ExpenseAnalyzer(da.get_analysis_data())

print(ea.get_view_data(da.get_analysis_data()))