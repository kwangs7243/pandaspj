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
    def filter_by_year_month(self,year:int,month:int) -> pd.DataFrame:
        """
        연,월 조회
        요청받은 연 월에 해당하는 행들을 df형태로 반환하는 메서드
        전처리된 데이터의 연,월 컬럼은 dt.year, dt.month로 처리된 컬럼이므로 
        해당메서드의 매개변수 year,month는 정수형으로 보내야함
        """
        filtered_data = self.df[((self.df["year"]==year) &
                                        (self.df["month"]==month))]

        return filtered_data
    
    # 기간별 조회
    def filter_by_date_range(self,start_date:pd.Timestamp, end_date:pd.Timestamp) -> pd.DataFrame:
        """
        기간별 조회
        요청받은 시작,끝 날짜사이에 해당하는 행들을 df형태로 반환하는 메서드
        전처리된 데이터의 date 컬럼은 pd.to_datetime 으로 처리된 컬럼이므로
        해당메서드의 매개변수 start_date,end_date은 datetime 객체로 보내야함
        """
        filtered_data = (
            self.df[(self.df["date"] >= start_date  ) &
                            (self.df["date"] <= end_date)]
                        )
        
        return filtered_data
    
    # 타입 조회
    def filter_by_type(self,type_name:str) -> pd.DataFrame:
        """
        타입 조회
        요청받은 수입 또는 지출에 해당하는 행들을 df형태로 반환하는 메서드
        전처리된 데이터의 type 컬럼은 문자열 수입 또는 지출만 허용하여 처리된 컬럼이므로
        해당메서드의 매개변수 type_name은 수입 또는 지출 이라는 문자열로 보내야함
        """
        filtered_data = self.df[self.df["type"]==type_name]

        return filtered_data
    
    # 카테고리별 조회
    def filter_by_category(self,category_name:str) -> pd.DataFrame:
        """
        카테고리 조회
        요청받은 카테고리에 해당하는 행들을 df형태로 반환하는 메서드
        전처리된 데이터의 category 컬럼은 문자열로만 구성되어있으므로
        해당메서드는 매개변수 category_name은 문자열로 보내야함
        """
        filtered_data = self.df[self.df["category"]==category_name]

        return filtered_data
    
    # 최소금액이상 조회
    def filter_by_min_amount(self,min_amount:int) -> pd.DataFrame:
        """
        최소금액이상 조회
        요청받은 금액이상에 해당하는 행들을 df형태로 반환하는 메서드
        전처리된 데이터의 amount 컬럼은 정수형으로만 구성되어있으므로
        해당메서드의 매개변수 min_amount는 정수형으로 보내야함
        """
        filtered_data = self.df[self.df["amount"] >= min_amount]

        return filtered_data
    
    # 키워드 조회 
    def filter_by_keyword(self, keyword:str="") -> pd.DataFrame:
        """
        키워드 조회
        요정받은 키워드가 속해있는 행들을 df형태로 반환하는 메서드
        전처리된 데이터의 content 컬럼은 문자열로만 구성되어있으므로
        해당메서드의 매개변수 keyword는 문자열로 보내야함
        """
        keyword = keyword.strip()
        if not keyword:
            return self.df
        
        filtered_data = self.df[self.df["content"].str.contains(keyword,na=False)]

        return filtered_data
#======================================조회 기능===========================================

#======================================요약 기능===========================================
    # 전체요약
    def summary_total(self) -> pd.DataFrame:
        """
        전체 요약
        총수입,총지출,순이익 컬럼으로 요약하여 df형태로 반환하는 메서드
        """
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
    def summary_by_month(self) -> pd.DataFrame:
        """
        월별 요약
        월별 수입,지출 순이익 컬럼으로 요약하여 df형태로 반환하는 메서드
        """
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
    def summary_by_year_month(self,year:int,month:int) -> pd.DataFrame:
        """
        연,월 요약
        요청받은 연월에 해당하는 행들을 요약하여 df형태로 반환하는 메서드
        전처리된 데이터의 year_month 컬럼은 pd.Period(freq="M")으로 처리된 컬럼이므로
        메서드내에서 Period 객체로 변환을 위해 
        해당메서드의 매개변수 year, month는 정수형으로 보내야함
        """
        summary_data = self.summary_by_month()
        target = pd.Period(year=year, month=month ,freq="M")

        return summary_data.loc[[target]]
                # type              수입       지출       순이익
                # year_month
                # 2025-01     25710000  1504400  24205600

    # 카테고리별 요약
    def summary_by_category_type(self,type_name:str=None) -> pd.DataFrame:
        """
        카테고리 요약
        요청받은 수입 또는 지출(매개변수가없을시 둘 다)별 카테고리를 요약하여 df형태로 반환하는 메서드
        전처리된 데이터의 type 컬럼은 문자열 수입 또는 지출만 허용하여 처리된 컬럼이므로
        해당메서드는 매개변수 type_name은 수입 또는 지출 이라는 문자열로 보내야함
        """
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
    def summary_count_by_category(self) -> pd.Series:
        """
        카테고리 건수 요약
        카테고리별 건수로 이루어진 시리즈를 반환하는 메서드
        """
        summary_data = self.df.groupby("category").size()

        return summary_data
#======================================요약 기능===========================================


#======================================순위 기능===========================================
    # 타입별 상위 N개
    def get_top_n_by_type(self,type_name:str, n:int) -> pd.DataFrame:
        """
        타입별 상위 N개
        요청받은 수입 또는 지출 의 금액상위 n개의 행을 df형태로 반환하는 메서드
        전처리된 데이터의 type 컬럼은 문자열 수입 또는 지출만 허용하여 처리된 컬럼이고
        처리시 .head 메서드의 인자로 n을 보내기 떄문에
        해당메서드의 매개변수 type_name은 수입 또는 지출 이라는 문자열,
        n은 정수형으로 보내야함
        """
        top_data = (
            self.df[self.df["type"] == type_name]
            .sort_values(by="amount", ascending=False)
            .head(n)
            )
        
        return top_data

    # 카테고리별 상위 N개
    def get_top_n_by_category(self,category_name:str, n:int) -> pd.DataFrame:
        """
        카테고리별 상위 N개
        요청받은 카테고리 의 금액상위 n개의 행을 df형태로 반환하는 메서드
        전처리된 데이터의 category 컬럼은 문자열로만 구성되어있고
        처리시 .head 메서드의 인자로 n을 보내기 떄문에
        해당메서드의 매개변수 category_name은 문자열,
        n은 정수형으로 보내야함
        """
        top_data = (
            self.df[self.df["category"] == category_name]
            .sort_values(by="amount", ascending=False)
            .head(n)
            )
        
        return top_data
    
    # 전체 상위 N개
    def get_top_n_overall(self, n:int) -> pd.DataFrame:
        """
        전체 상위 N개
        전체 데이터에서 금액상위 n개의 행을 df형태로 반환하는 메서드
        처리시 .head 메서드의 인자로 n을 보내기 떄문에
        해당메서드의 매개변수 n은 정수형으로 보내야함
        """
        top_data = self.df.sort_values(by="amount", ascending=False).head(n)

        return top_data
#======================================순위 기능===========================================
