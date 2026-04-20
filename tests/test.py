from src.DataAnalyzer import DataAnalyzer
from src.ExpenseAnalyzer import ExpenseAnalyzer
import pandas as pd
#  python -m tests.test
da = DataAnalyzer()
da.load_data("data/raw/realistic_expense_1000.csv")
da.preprocess_data()
ea = ExpenseAnalyzer(da.get_analysis_data())
aa = pd.Period(year=2025,month=1,freq="M")
data = ea.compare_category_between_months(category="카페",base=(2025,1),target=(2025,2))
print(data)

