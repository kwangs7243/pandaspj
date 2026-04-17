from DataAnalyzer import DataAnalyzer


da = DataAnalyzer()
da.load_data("messy_expense_data_large.csv")
da.preprocess_data()
invalid = da.find_invalid_rows()
# print(da.df["category_map"].unique())

# print(invalid["invalid_reason"])
# da.save_data(invalid_filtered,"invalid_data.csv")
# da.save_data(da.get_view_data(),"view_data.csv")
# print(da.df.loc[da.df["amount_raw"].str.contains("천"),"amount_num"])
# print(da.df["amount_str"])
# print(invalid_view)
# print(da.df["date_dt"])
# print(da.get_view_data())
# print(da.df.iloc[14])
# print(da.get_view_data()["category"].unique())
# print(f"전체 행 수 : {len(da.df)}")
# print(f"정상 행 수: {len(da.get_view_data())}")
# print(f"실패 행 수: {len(invalid_view)}")
result = invalid[invalid["type_map"]=='기타']
print(da.get_invalid_summary())
print(result[["type_map","amount_num"]])