from DataAnalyzer import DataAnalyzer


da = DataAnalyzer()
da.load_data("messy_expense_data_large.csv")
da.preprocess_data()
invalid =  da.find_invalid_rows()
invalid_view = invalid[["date_raw","type_raw","amount_raw","category_raw","content"]]
da.save_data(da.df,"debugging_data.csv")
# print(da.df.loc[da.df["amount_raw"].str.contains("천"),"amount_num"])
# print(da.df["amount_str"])
# print(invalid_view)
# print(da.df["date_dt"])
# print(da.get_view_data())
# print(da.df.iloc[14])

# print(f"전체 행 수 : {len(da.df)}")
# print(f"정상 행 수: {len(da.get_view_data())}")
# print(f"실패 행 수: {len(invalid_view)}")

