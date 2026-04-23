
from src.DataAnalyzer import DataAnalyzer
from src.ExpenseAnalyzer import ExpenseAnalyzer
import pandas as pd
da = DataAnalyzer()
da.load_data("data/raw/realistic_expense_1000.csv")
da.preprocess_data()
ea = ExpenseAnalyzer(da.get_analysis_data())
df = ea.compare_months(base=(2025,1),target=(2025,2))
print(df)