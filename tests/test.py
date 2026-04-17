from src.DataAnalyzer import DataAnalyzer
from src.ExpenseAnalyzer import ExpenseAnalyzer
from main import run
#  python -m tests.test
da = DataAnalyzer()
da.load_data("data/raw/realistic_expense_1000.csv")
da.preprocess_data()
ea = ExpenseAnalyzer(da.get_analysis_data())

print(da.get_invalid_summary())