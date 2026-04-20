from src.DataAnalyzer import DataAnalyzer
from src.ExpenseAnalyzer import ExpenseAnalyzer
#  python -m tests.test
da = DataAnalyzer()
da.load_data("data/raw/realistic_expense_1000.csv")
da.preprocess_data()
ea = ExpenseAnalyzer(da.get_analysis_data())
data = ea.compare_months(target=(2025,2),base=(2025,1))
print(data)

