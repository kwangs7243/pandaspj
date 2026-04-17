import pandas as pd
from DataAnalyzer import DataAnalyzer
da = DataAnalyzer()
class ExpenseAnalyzer:

    def get_view_data(self,data):
        view_data = data[["date","type","category","amount","content"]]
        return view_data

        # 년,월 필터 데이터
    def filter_by_year_month(self,year,month):
        analysis_data = da.get_analysis_data()
        filtered_data : pd.DataFrame  = analysis_data[((analysis_data["year"]==year) &
                                                        (analysis_data["month"]==month))]
        filtered_data = filtered_data.sort_values(by="date")
        filtered_data = self.get_view_data(filtered_data)

        return filtered_data
    
    
    # 타입별 top n위까지 데이터생성
    def get_top_n_by_type(self, type_name, n):
        analysis_data : pd.DataFrame = da.get_analysis_data()
        filtered_data : pd.DataFrame = analysis_data[analysis_data["type"]==type_name]
        top_data = (
            filtered_data
            .sort_values(by="amount",ascending=False)
            .head(n)
            )
        top_data = self.get_view_data(top_data)

        return top_data
    
    # 키워드 검색 
    def filter_by_keyword(self, keyword=""):
        keyword = keyword.strip()
        analysis_data = da.get_analysis_data()
        if not keyword:
            return self.get_view_data(analysis_data)
        
        filtered_data = analysis_data[analysis_data["content"].str.contains(keyword,na=False)]
        filtered_data = filtered_data.sort_values(by="date")
        filtered_data = self.get_view_data(filtered_data)

        return filtered_data

    # 년,월 요약데이터 (수입 지출 총액 요약) 저장시 인덱스 True
    def summary_by_year_month(self,year,month):
        analysis_data = da.get_analysis_data()
        filtered_data : pd.DataFrame  = analysis_data[((analysis_data["year"]==year) &
                                                        (analysis_data["month"]==month))]
        summary_data = filtered_data.groupby("type")[["amount"]].sum()

        return summary_data
    
    # 카테고리,타입 요약 (카테고리 ,타입별 총액) 저장시 인덱스 True
    def summary_by_category_type(self):
        analysis_data = da.get_analysis_data()
        summary_data = analysis_data.groupby(["category", "type"])[["amount"]].sum()
        summary_data = summary_data.sort_values(by="type")

        return summary_data
    
    # 카테고리 요약 (카테고리별 총액) 저장시 인덱스 True
    def summary_by_category(self, type_name):
        analysis_data = da.get_analysis_data()
        filtered_data : pd.DataFrame = analysis_data[analysis_data["type"] == type_name]
        summary_data = filtered_data.groupby("category")[["amount"]].sum()
        summary_data = summary_data.sort_values(by="amount", ascending=False)

        return summary_data
