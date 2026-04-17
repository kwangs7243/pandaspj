from src.DataAnalyzer import DataAnalyzer
from src.ExpenseAnalyzer import ExpenseAnalyzer

def run():
    da = DataAnalyzer()
    da.load_data("data/raw/data.csv")
    da.preprocess_data()

    ea = ExpenseAnalyzer(da.get_analysis_data())

    result = ea.get_view_data(da.get_analysis_data())
    print(result)

if __name__ == "__main__":
    run()