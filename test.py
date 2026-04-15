from dataanalyzer import DataAnalyzer
import pandas as pd

da = DataAnalyzer()
da.load_data("messy_expense_data.csv")
da.preprocess_data()
# print(da.get_analysis_data())
# print(da.get_analysis_data().info())
# print(da.filter_by_year_month(2026,4)) => 정렬필요 (date 기준으로)
# print(da.summary_by_year_month(2026,4)) => 정렬필요 (date 기준으로)
# print(da.summary_by_category_type()) => 정렬필요 (tpye으로 하는게 좋을듯)
# print(da.summary_by_category("바보"))   => 정렬필요 (date 기준으로)
# print(da.get_top_n_by_type("수입",40).info())
# print(da.filter_by_keyword("바보")) => 정렬필요 (date 기준으로)
# 전체적으로 원본 csv가 날짜별로 들어와있어서 정렬을 안해도 날짜순이지만 아닐경우를 대비해서 정렬필요성느낌
