# 전체 데이터 확인
# 특정 월 데이터만 보기
# 월별 수입/지출 요약
# 카테고리별 지출 합계
# 가장 큰 지출 5개 보기
# 키워드 검색
# 분석 결과 저장
import pandas as pd
class DataAnalyzer():
    # 객체생성
    def __init__(self):
        self.df = None

    # 데이터를 로드했는지 확인 => 아닐경우 오류 발생시키기
    def _check_loaded(self):
        if self.df is None:
            raise RuntimeError("먼저 load_data()를 실행해야 합니다.")

    # 데이터를 전처리했는지 확인 => 아닐경우 오류발생시키기 (누락된 컬럼명 같이 안내 디버깅 좋음)
    def _check_preprocessed(self):
        self._check_loaded()
        required_columns = ["date_dt", "year", "month", "type_map", "category_map", "amount_num"]
        missing_columns = [col for col in required_columns if col not in self.df.columns]
        if missing_columns:
            raise RuntimeError("먼저 preprocess_data()를 실행해야 합니다."
                               f"누락된 컬럼 : {missing_columns}")

    # CSV 불러오기
    #  파일경로를 받아서 파일 읽기 => 데이터프레임으로 처리됨 na_values : 잘못들어온값을 NaN으로 치환해줌
    def load_data(self,file_path):
        self.df = pd.read_csv(file_path,encoding="utf-8-sig",na_values=["not_available"])

    # 데이터 전처리
    # self.df["amount"] = self.df["amount"].str.strip().str.strip("원").str.strip("-").str.replace(",","",regex=False)
    # ↪ 이런 메서드채이닝 보단 정규식패턴으로 처리하는게 좀더 실무스타일
    # [^\d] 정규식패턴중하나 [] = or, ^ : not , \d : 숫자(0~9) => 숫자가아닌패턴을 찾는다
    # 전처리 과정을 컬럼으로 남겨서 원본 => 중간 => 결과 이런흐름을 확인할수있는 습관을 들여야한다
    def preprocess_data(self):
        self._check_loaded()
        df = self.df
        
        df.columns = ["date_raw","type_raw","category_raw","amount_raw","content"]

        df["date_str"] = df["date_raw"].str.replace(r"[^\d]", "-", regex=True)
        df["date_dt"] = pd.to_datetime(df["date_str"], errors="coerce")
        df["year"] = df["date_dt"].dt.year
        df["month"] = df["date_dt"].dt.month

        df["type_str"] = df["type_raw"].str.strip().str.replace(" ", "", regex=False).str.lower()
        df["type_map"] = df["type_str"].replace({
            'income':'수입','refund':'수입','expense':'지출'})
        
        df["category_str"] = df["category_raw"].str.strip().str.replace(" ", "", regex=False).str.lower()
        df["category_map"] = df["category_str"].replace({
            'food':'식비','cafe':'카페','shopping':'쇼핑',
            'bonus':'급여','salary':'급여',
            'transport':'교통'})

        df["amount_str"] = df["amount_raw"].str.replace(r"[^\d]","",regex=True)
        df["amount_num"] = pd.to_numeric(df["amount_str"],errors="coerce")

    # 전처리 실패항목 체크하기
    def find_invalid_rows(self):
        df = self.df
        date_invalid = df["date_dt"].isna()
        type_invalid = ~df["type_map"].isin(["수입","지출"]) | df["type_map"].isna()
        amount_invalid = df["amount_num"].isna()
        category_invalid = df["category_map"].isna()
        content_invalid = df["content"].isna()
        invalid_mask = date_invalid | type_invalid | amount_invalid | category_invalid | content_invalid

        return df[invalid_mask]

    # 분석용 데이터 생성
    def get_analysis_data(self):
        self._check_preprocessed()

        analysis_data = self.df[["date_dt","year","month","type_map",
                            "category_map","amount_num","content"]].copy()
        analysis_data = analysis_data.rename(
                            columns=
                                {"date_dt":"date", "type_map":"type", 
                                "category_map":"category", "amount_num":"amount"})
        
        analysis_data = analysis_data.dropna(axis=0)

        return analysis_data
    
    # 출력용 데이터 생성
    def get_view_data(self):
        analysis_data = self.get_analysis_data()
        view_data = analysis_data[["date", "type", "category", "amount", "content"]]

        return view_data
    
    # 년,월 필터 데이터
    def filter_by_year_month(self,year,month):
        analysis_data = self.get_analysis_data()
        filtered_data : pd.DataFrame  = analysis_data[(analysis_data["year"]==year) & (analysis_data["month"]==month)]
        filtered_data = filtered_data.sort_values(by="date")

        return filtered_data
    
    # 년,월 요약데이터 (수입 지출 총액 요약) 저장시 인덱스 True
    def summary_by_year_month(self,year,month):
        filtered_data = self.filter_by_year_month(year,month)
        summary_data = filtered_data.groupby("type")[["amount"]].sum()

        return summary_data
    
    # 카테고리,타입 요약 (카테고리 ,타입별 총액) 저장시 인덱스 True
    def summary_by_category_type(self):
        analysis_data = self.get_analysis_data()
        summary_data = analysis_data.groupby(["category", "type"])[["amount"]].sum()
        summary_data = summary_data.sort_values(by="type")

        return summary_data
    
    # 카테고리 요약 (카테고리별 총액) 저장시 인덱스 True
    def summary_by_category(self, type_name):
        analysis_data = self.get_analysis_data()
        filtered_data : pd.DataFrame = analysis_data[analysis_data["type"] == type_name]
        summary_data = filtered_data.groupby("category")[["amount"]].sum()
        summary_data = summary_data.sort_values(by="amount", ascending=False)

        return summary_data
    
    # 타입별 top n위까지 데이터생성
    def get_top_n_by_type(self, type_name, n):
        analysis_data : pd.DataFrame = self.get_analysis_data()
        filtered_data : pd.DataFrame = analysis_data[analysis_data["type"]==type_name]
        top_data = (
            filtered_data
            .sort_values(by="amount",ascending=False)
            .head(n)
            )
        
        return top_data
    
    # 키워드 검색 
    def filter_by_keyword(self, keyword=""):
        keyword = keyword.strip()
        analysis_data = self.get_analysis_data()
        if not keyword:
            return analysis_data
        filtered_data = analysis_data[analysis_data["content"].str.contains(keyword,na=False)]
        filtered_data = filtered_data.sort_values(by="date")

        return filtered_data

    # 데이터 저장
    def save_data(self,data : pd.DataFrame,file_path,index=False):
        data.to_csv(file_path, index=index, encoding="utf-8-sig")



