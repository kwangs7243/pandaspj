import pandas as pd
class ExpenseAnalyzer:
    def __init__(self,data:pd.DataFrame):
        self.df = data

    def get_view_data(self,data,sort_by="date",order="desc"):
        view_data = data[["date","type","category","amount","content"]]
        view_data:pd.DataFrame = view_data.sort_values(by=sort_by,ascending=(order == "asc"))
        return view_data
#======================================조회 기능===========================================

    # 년,월별 조회
    def filter_by_year_month(self,year,month):
        analysis_data = self.df
        filtered_data = analysis_data[((analysis_data["year"]==year) &
                                        (analysis_data["month"]==month))]

        return filtered_data
    
    # 기간별 조회
    def filter_by_date_range(self,start_date, end_date):
        analysis_data = self.df
        start_date = pd.to_datetime(start_date,"%Y-%m-%d")
        end_date = pd.to_datetime(end_date,"%Y-%m-%d")
        filtered_data = (
            analysis_data[(analysis_data["date"] >= start_date  ) &
                            (analysis_data["date"] <= end_date)]
                        )
        
        return filtered_data
    
    # 타입 조회
    def filter_by_type(self,type_name):
        analysis_data = self.df
        filtered_data = analysis_data[analysis_data["type"]==type_name]

        return filtered_data
    
    # 카테고리별 조회
    def filter_by_category(self,category_name):
        analysis_data = self.df
        filtered_data = analysis_data[analysis_data["category"]==category_name]

        return filtered_data
    
    # 최소금액이상 조회
    def filter_by_min_amount(self,min_amount):
        analysis_data = self.df
        filtered_data = analysis_data[analysis_data["amount"] >= min_amount]

        return filtered_data
    
    # 키워드 조회 
    def filter_by_keyword(self, keyword=""):
        keyword = keyword.strip()
        analysis_data = self.df
        if not keyword:
            return self.get_view_data(analysis_data)
        
        filtered_data = analysis_data[analysis_data["content"].str.contains(keyword,na=False)]

        return filtered_data
#======================================조회 기능===========================================

#======================================요약 기능===========================================
    # 전체요약
    def summary_total(self):
        analysis_data = self.df

        summary_data = analysis_data.groupby("type")["amount"].sum()

        total_imcome = summary_data["수입"]
        total_expense = summary_data["지출"]
        net_income = total_imcome - total_expense

        summary_total_data = pd.Series(
            {
            "총수입" : total_imcome,
            "총지출" : total_expense,
            "순수익" : net_income}
            )

        return summary_total_data
    
    # 월별 수입,지출 순이익 요약
    def summary_by_month(self):
        analysis_data = self.df
        # summary_data = analysis_data.pivot_table(
        #     index="month",columns="type",values="amount",aggfunc="sum")
        # 월별 수입/지출 합계를 피벗 테이블 형태로 요약
        # pivot_table은 집계와 형태 변환을 한 번에 처리할 수 있어서
        # 단순 요약표를 만들 때 편하다.
        # 다만 복잡한 집계나 후처리가 많아지면 groupby + agg + unstack 방식이 더 유연하다.
        summary_data = (
            analysis_data.groupby(["year_month","type"])["amount"]
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
    def summary_by_year_month(self,year,month):
        summary_data = self.summary_by_month()
        target = pd.Period(f"{year}-{month:02d}",freq="M")

        return summary_data.loc[[target]]
                # type              수입       지출       순이익
                # year_month
                # 2025-01     25710000  1504400  24205600

    # 카테고리별 요약
    def summary_by_category(self,type_name=None):
        analysis_data = self.df
        summary_data = analysis_data.groupby("category")["amount"].sum()
        if type_name is not None:
            return summary_data.loc[[type_name]]

        return summary_data

    # 카테고리별 건수 요약
    def summary_count_by_category(self):
        analysis_data = self.df
        summary_data = analysis_data.groupby("category")["amount"].count()

        return summary_data
#======================================요약 기능===========================================