import pandas as pd

class ExpenseAnalyzer:
    """
    전처리된 가계부 데이터를 조회, 요약, 순위 형태로 분석하는 클래스.
    """

    def __init__(self,data:pd.DataFrame):
        """
        분석에 사용할 데이터프레임을 저장한다.
        """
        self.df = data

    def get_view_data(self,data:pd.DataFrame,sort_by:str="date",order:str="desc"):
        """
        화면에 보여줄 기본 컬럼만 선택해 정렬하여 반환한다.
        """
        view_data = data[["date","type","category","amount","content"]]
        view_data = view_data.sort_values(by=sort_by,ascending=(order == "asc"))
        return view_data

#======================================외부 호출 ===========================================
    #======================================조회 ===========================================

    def filter_by_year_month(self,year:int,month:int) -> pd.DataFrame:
        """
        해당 연도와 월의 데이터만 반환한다.
        """
        return self._filter_by_year_month(data=self.df, year=year, month=month)

    def filter_by_date_range(self,start_date:pd.Timestamp, end_date:pd.Timestamp) -> pd.DataFrame:
        """
        시작일과 종료일 사이의 데이터만 반환한다.
        """
        return self._filter_by_date_range(data=self.df, start_date=start_date, end_date=end_date)

    def filter_by_type(self,type_name:str) -> pd.DataFrame:
        """
        해당 타입(수입/지출)의 데이터만 반환한다.
        """
        return self._filter_by_type(data=self.df, type_name=type_name)

    def filter_by_category(self,category_name:str) -> pd.DataFrame:
        """
        해당 카테고리의 데이터만 반환한다.
        """
        return self._filter_by_category(data=self.df, category_name=category_name)

    def filter_by_min_amount(self,min_amount:int) -> pd.DataFrame:
        """
        지정한 금액 이상인 데이터만 반환한다.
        """
        return self._filter_by_min_amount(data=self.df, min_amount=min_amount)

    def filter_by_keyword(self, keyword:str="") -> pd.DataFrame:
        """
        내용에 키워드가 포함된 데이터만 반환한다.
        키워드가 비어 있으면 전체 데이터를 반환한다.
        """
        keyword = keyword.strip()
        if not keyword:
            return self.df
        return self._filter_by_keyword(data=self.df, keyword=keyword)


    #======================================조회 ===========================================

#======================================외부 호출 ===========================================




#======================================내부 계산 ===========================================

    #======================================조회 기능===========================================
    def _filter_by_year_month(self,data:pd.DataFrame,year:int,month:int) -> pd.DataFrame:

        return data[(data["year"]==year) & (data["month"]==month)]


    def _filter_by_date_range(self,data:pd.DataFrame, start_date:pd.Timestamp, end_date:pd.Timestamp) -> pd.DataFrame:
        
        return data[(data["date"] >= start_date) & (data["date"] <= end_date)]

    def _filter_by_type(self,data:pd.DataFrame, type_name:str) -> pd.DataFrame:
        
        return data[data["type"]==type_name]

    def _filter_by_category(self,data:pd.DataFrame, category_name:str) -> pd.DataFrame:
        
        return data[data["category"]==category_name]

    def _filter_by_min_amount(self,data:pd.DataFrame, min_amount:int) -> pd.DataFrame:
        
        return data[data["amount"] >= min_amount]

    def _filter_by_keyword(self,data:pd.DataFrame, keyword:str="") -> pd.DataFrame:
        
        return data[data["content"].str.contains(keyword,na=False)]

    #======================================조회 기능===========================================

    #======================================요약 기능===========================================

    def summary_total(self) -> pd.DataFrame:
        """
        전체 데이터를 총수입, 총지출, 순이익으로 요약해 반환한다.
        """
        summary_data = self.df.pivot_table(columns="type", values="amount", aggfunc="sum", fill_value=0)
        summary_data.columns = ["총수입","총지출"]
        summary_data["순이익"] = summary_data["총수입"] - summary_data["총지출"]
        return summary_data

    def summary_by_month(self) -> pd.DataFrame:
        """
        월별 수입, 지출, 순이익을 요약해 반환한다.
        """
        summary_data = (
            self.df.groupby(["year_month","type"])["amount"]
            .sum()
            .unstack(fill_value=0)
            .reindex(columns=["수입","지출"],fill_value=0)
        )
        summary_data["순이익"] = summary_data["수입"] - summary_data["지출"]
        return summary_data

    def summary_by_year_month(self,year:int,month:int) -> pd.DataFrame:
        """
        특정 연도와 월의 수입, 지출, 순이익을 요약해 반환한다.
        """
        summary_data = self.summary_by_month()
        target = pd.Period(year=year, month=month ,freq="M")
        return summary_data.loc[[target]]

    def summary_by_category_type(self,type_name:str=None) -> pd.DataFrame:
        """
        카테고리별 금액을 타입 기준으로 요약해 반환한다.
        타입을 지정하면 해당 타입만 반환한다.
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

    def summary_count_by_category(self) -> pd.Series:
        """
        카테고리별 데이터 개수를 반환한다.
        """
        return self.df.groupby("category").size()

    #======================================요약 기능===========================================

    #======================================순위 기능===========================================

    def get_top_n_by_type(self,type_name:str, n:int) -> pd.DataFrame:
        """
        해당 타입에서 금액이 큰 상위 n개 데이터를 반환한다.
        """
        return (
            self.df[self.df["type"] == type_name]
            .sort_values(by="amount", ascending=False)
            .head(n)
        )

    def get_top_n_by_category(self,category_name:str, n:int) -> pd.DataFrame:
        """
        해당 카테고리에서 금액이 큰 상위 n개 데이터를 반환한다.
        """
        return (
            self.df[self.df["category"] == category_name]
            .sort_values(by="amount", ascending=False)
            .head(n)
        )

    def get_top_n_overall(self, n:int) -> pd.DataFrame:
        """
        전체 데이터에서 금액이 큰 상위 n개를 반환한다.
        """
        return self.df.sort_values(by="amount", ascending=False).head(n)

    #======================================순위 기능===========================================


    #======================================비교 기능===========================================

    def compare_months(self,base:tuple[int,int],target:tuple[int,int]) -> pd.DataFrame:
        """
        타겟 월과 기준 월을 비교하여 증감, 증감률을 반환한다.
        """
        base_year,base_month = base
        target_year,target_month = target

        base_df = self.summary_by_year_month(year=base_year,month=base_month).T
        target_df = self.summary_by_year_month(year=target_year,month=target_month).T

        compare_data = pd.concat([base_df,target_df], axis=(1))
        base_col,target_col = compare_data.columns

        compare_data["증감"] = compare_data[target_col] - compare_data[base_col]
        compare_data["증감률"] = (
            compare_data["증감"] / compare_data[base_col].replace(0, pd.NA) * 100
            ).round(2).fillna(0)

        return compare_data
    
    def compare_category_between_months(self,category:str,base:tuple[int,int],target:tuple[int,int]) -> pd.DataFrame:
        """
        특정 카테고리에 대해 두 달 비교
        """
        filtered_data = self.filter_by_category(category_name=category)

        base_year,base_month = base
        target_year,target_month = target

        base_peroid = pd.Period(year=base_year, month=base_month, freq="M")
        target_peroid = pd.Period(year=target_year, month=target_month, freq="M")

        base_df = (
            filtered_data[filtered_data["year_month"]==base_peroid]
            .groupby(["category","year_month","type"])["amount"]
            .sum()
            .unstack(fill_value=0)
            .reindex(columns=["수입","지출"], fill_value=0)
            ).T
        
        target_df = (
            filtered_data.loc[filtered_data["year_month"]==target_peroid]
            .groupby(["category","year_month","type"])["amount"]
            .sum()
            .unstack(fill_value=0)
            .reindex(columns=["수입","지출"], fill_value=0)
            ).T 

        compare_data = pd.concat([base_df,target_df], axis=1)

        return compare_data
    #======================================비교 기능===========================================

#======================================내부계산===========================================






