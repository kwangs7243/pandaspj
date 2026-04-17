import pandas as pd
class ExpenseAnalyzer:
    def __init__(self,data:pd.DataFrame):
        self.df = data

    def get_view_data(self,data,sort_by="date",order="desc"):
        view_data = data[["date","type","category","amount","content"]]
        view_data:pd.DataFrame = view_data.sort_values(by=sort_by,ascending=(order == "asc"))
        return view_data
#======================================조회 기능===========================================

    # 년,월 조회
    def filter_by_year_month(self,year,month):
        analysis_data = self.df
        filtered_data : pd.DataFrame  = analysis_data[((analysis_data["year"]==year) &
                                                        (analysis_data["month"]==month))]

        return filtered_data
    
    # 기간 조회
    def filter_by_date_range(self,start_date, end_date):
        analysis_data = self.df
        filtered_data = (analysis_data[(analysis_data["date"] >= start_date  ) &
                                       (analysis_data["date"] <= end_date)])
        return filtered_data
    # 카테고리 조회
    def filter_by_category(self,category_name):
        analysis_data = self.df
        filtered_data = analysis_data[analysis_data["category"]==category_name]

        return filtered_data
    
    # 타입 조회
    def filter_by_type(self,type_name):
        analysis_data = self.df
        filtered_data = analysis_data[analysis_data["type"]==type_name]

        return filtered_data
#======================================조회 기능===========================================

    # 타입별 top n위까지 데이터생성
    def get_top_n_by_type(self, type_name, n):
        analysis_data = self.df
        filtered_data : pd.DataFrame = analysis_data[analysis_data["type"]==type_name]
        top_data  = (
            filtered_data
            .sort_values(by="amount",ascending=False)
            .head(n)
            )
        top_data = self.get_view_data(top_data)

        return top_data

    # 키워드 검색 
    def filter_by_keyword(self, keyword=""):
        keyword = keyword.strip()
        analysis_data = self.df
        if not keyword:
            return self.get_view_data(analysis_data)
        
        filtered_data = analysis_data[analysis_data["content"].str.contains(keyword,na=False)]
        filtered_data = filtered_data.sort_values(by="date")
        filtered_data = self.get_view_data(filtered_data)

        return filtered_data

    # 년,월 요약데이터 (수입 지출 총액 요약) 저장시 인덱스 True
    def summary_by_year_month(self,year,month):
        analysis_data = self.df
        filtered_data : pd.DataFrame  = analysis_data[((analysis_data["year"]==year) &
                                                        (analysis_data["month"]==month))]
        summary_data = filtered_data.groupby("type")[["amount"]].sum()

        return summary_data

    # 카테고리,타입 요약 (카테고리 ,타입별 총액) 저장시 인덱스 True
    def summary_by_category_type(self):
        analysis_data = self.df
        summary_data = analysis_data.groupby(["category", "type"])[["amount"]].sum()
        summary_data = summary_data.sort_values(by="type")

        return summary_data

    # 카테고리 요약 (카테고리별 총액) 저장시 인덱스 True
    def summary_by_category(self, type_name):
        analysis_data = self.df
        filtered_data : pd.DataFrame = analysis_data[analysis_data["type"] == type_name]
        summary_data = filtered_data.groupby("category")[["amount"]].sum()
        summary_data = summary_data.sort_values(by="amount", ascending=False)

        return summary_data
