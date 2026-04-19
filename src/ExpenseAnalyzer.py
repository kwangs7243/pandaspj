import pandas as pd
class ExpenseAnalyzer:
    def __init__(self,data:pd.DataFrame):
        self.df = data

    def get_view_data(self,data:pd.DataFrame,sort_by:str="date",order:str="desc"):
        view_data = data[["date","type","category","amount","content"]]
        view_data = view_data.sort_values(by=sort_by,ascending=(order == "asc"))
        return view_data
#======================================조회 기능===========================================

    # 년,월별 조회
    def filter_by_year_month(self,year:int,month:int):
        filtered_data = self.df[((self.df["year"]==year) &
                                        (self.df["month"]==month))]

        return filtered_data
    
    # 기간별 조회
    def filter_by_date_range(self,start_date:pd.Timestamp, end_date:pd.Timestamp):
        filtered_data = (
            self.df[(self.df["date"] >= start_date  ) &
                            (self.df["date"] <= end_date)]
                        )
        
        return filtered_data
    
    # 타입 조회
    def filter_by_type(self,type_name:str):
        filtered_data = self.df[self.df["type"]==type_name]

        return filtered_data
    
    # 카테고리별 조회
    def filter_by_category(self,category_name:str):
        filtered_data = self.df[self.df["category"]==category_name]

        return filtered_data
    
    # 최소금액이상 조회
    def filter_by_min_amount(self,min_amount:int):
        filtered_data = self.df[self.df["amount"] >= min_amount]

        return filtered_data
    
    # 키워드 조회 
    def filter_by_keyword(self, keyword:str=""):
        keyword = keyword.strip()
        if not keyword:
            return self.df
        
        filtered_data = self.df[self.df["content"].str.contains(keyword,na=False)]

        return filtered_data
#======================================조회 기능===========================================

#======================================요약 기능===========================================
    # 전체요약
    def summary_total(self):
        summary_data = self.df.pivot_table(columns="type", values="amount", aggfunc="sum", fill_value=0)
        summary_data = summary_data.rename(
                            columns={
                                "수입" : "총수입",
                                "지출" : "총지출"
                            }
                        )
        summary_data["순이익"] = summary_data["총수입"] - summary_data["총지출"]

        return summary_data
                # type          총수입       총지출        순이익
                # amount  336224000  25285000  310939000
    
    # 월별 수입,지출 순이익 요약
    def summary_by_month(self):
        # summary_data = self.df.pivot_table(
        #     index="month",columns="type",values="amount",aggfunc="sum")
        # 월별 수입/지출 합계를 피벗 테이블 형태로 요약
        # pivot_table은 집계와 형태 변환을 한 번에 처리할 수 있어서
        # 단순 요약표를 만들 때 편하다.
        # 다만 복잡한 집계나 후처리가 많아지면 groupby + agg + unstack 방식이 더 유연하다.
        summary_data = (
            self.df.groupby(["year_month","type"])["amount"]
            .sum()
            .unstack(fill_value=0)
            .reindex(columns=["수입","지출"],fill_value=0)
            )
        summary_data["순이익"] = summary_data["수입"] - summary_data["지출"]
        

        return summary_data
                # type              수입       지출       순이익
                # year_month
                # 2025-01     25710000  1504400  24205600
                # 2025-02     21616000  1305500  20310500

    # 특정 년,월 별 요약
    def summary_by_year_month(self,year:int,month:int):
        summary_data = self.summary_by_month()
        target = pd.Period(year=year, month=month ,freq="M")

        return summary_data.loc[[target]]
                # type              수입       지출       순이익
                # year_month
                # 2025-01     25710000  1504400  24205600

    # 카테고리별 요약
    def summary_by_category_type(self,type_name:str=None):
        summary_data = (
            self.df.groupby(["category","type"])["amount"]
            .sum()
            .unstack(fill_value=0)
            .reindex(columns=["수입","지출"],fill_value=0)
            )
        if type_name is not None:
            return summary_data[[type_name]]

        return summary_data

    # 카테고리별 건수 요약
    def summary_count_by_category(self):
        summary_data = self.df.groupby("category").size()

        return summary_data
#======================================요약 기능===========================================


#======================================순위 기능===========================================
    # 타입별 상위 N개
    def get_top_n_by_type(self,type_name:str, n:int):
        top_date = self.df.groupby


