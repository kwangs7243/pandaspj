from DataAnalyzer import DataAnalyzer
import pandas as pd

da = DataAnalyzer()
da.load_data("messy_expense_data.csv")
da.preprocess_data()
da.find_invalid_rows()

# print(da.df)
# print(da.get_analysis_data())

# print(da.get_analysis_data().info())

# print(da.filter_by_year_month(2026,4)) 
# => 정렬필요 (date 기준으로)

# print(da.summary_by_year_month(2026,3)) 

# print(da.summary_by_category_type()) 
# => 정렬필요 (tpye으로 하는게 좋을듯)

# print(da.summary_by_category("수입"))   
# => 정렬필요 (amount 기준으로)

# print(da.get_top_n_by_type("수입",40).info())

# print(da.filter_by_keyword("바보")) 
# => 정렬필요 (date 기준으로)

# 전체적으로 원본 csv가 날짜별로 들어와있어서 정렬을 안해도 날짜순이지만 아닐경우를 대비해서 정렬필요성느낌

invalid =  da.find_invalid_rows()
invalid_view = invalid[["date_raw","type_raw","amount_raw","category_raw","content","invalid_reason"]]
print(invalid_view)

# print(f"전체 행 수 : {len(da.df)}")
# print(f"정상 행 수: {len(da.get_view_data())}")
# print(f"실패 행 수: {len(invalid_view)}")



