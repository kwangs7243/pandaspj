from DataAnalyzer import DataAnalyzer
da = DataAnalyzer()

da.load_data("messy_expense_data_xlarge.csv")
da.preprocess_data()

print(da.get_invalid_summary())

# invalid = da.find_invalid_rows()
# invalid = invalid[invalid["invalid_reason"].isin(["카테고리변환실패"])]
# data = invalid[["category_raw","category_str","category_map"]]
# # print(data)
# print(len(invalid["category_map"].unique()))
data = da.get_view_data(da.get_analysis_data())
da.save_data(data,"result.csv")

