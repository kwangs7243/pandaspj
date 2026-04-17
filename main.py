from src.DataAnalyzer import DataAnalyzer
from src.ExpenseAnalyzer import ExpenseAnalyzer

da = DataAnalyzer()
da.preprocess_data()
ea = ExpenseAnalyzer(da.get_analysis_data())