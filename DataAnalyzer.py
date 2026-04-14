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
        self.df.columns = ["date_raw","type_raw","category_raw","amount_raw","content"]

        self.df["date_str"] = self.df["date_raw"].str.replace(r"[^\d]", "-", regex=True)
        self.df["date_dt"] = pd.to_datetime(self.df["date_str"], errors="coerce")
        self.df["year"] = self.df["date_dt"].dt.year
        self.df["month"] = self.df["date_dt"].dt.month

        self.df["type_str"] = self.df["type_raw"].str.strip().str.replace(" ", "", regex=False).str.lower()
        self.df["type_map"] = self.df["type_str"].str.replace({
            'income':'수입','refund':'수입','expense':'지출'})
        
        self.df["category_str"] = self.df["category_raw"].str.strip().str.replace(" ", "", regex=False).str.lower()
        self.df["category_map"] = self.df["category_str"].str.replace({
            'food':'식비','cafe':'카페','shopping':'쇼핑',
            'bonus':'급여','salary':'급여',
            'transport':'교통'})
        
        self.df["amount_str"] = self.df["amount_raw"].str.replace(r"[^\d]","",regex=True)
        self.df["amount_num"] = pd.to_numeric(self.df["amount_str"],errors="coerce")
    
    def get_analysis_data(self):
        analysis_data = self.df[["date_dt","year","month","type_map",
                            "category_map","amount_num","content"]].copy()
        analysis_data = analysis_data.rename(
                            columns=
                                {"date_dt":"date", "type_map":"type", 
                                "category_map":"category", "amount_num":"amount"})
        
        return analysis_data
    
    def filter_by_month(self,month):
        analysis_data = self.get_analysis_data()
        filtered_data = analysis_data[analysis_data["month"]==month]

        return filtered_data
    
    def summary_by_month(self,month):
        filtered_data = self.filter_by_month(month)
        summary_data = filtered_data.groupby("type")[["amount"]].sum()

        return summary_data
    
    def summary_by_category_type(self):
        analysis_data = self.get_analysis_data()
        summary_data = analysis_data.groupby(["category", "type"])[["amount"]].sum()

        return summary_data

    def summary_by_category(self, type):
        analysis_data = self.get_analysis_data()
        filtered_data = analysis_data[analysis_data["type"] == type]
        summary_data = filtered_data.groupby("category")[["amount"]].sum()

        return summary_data
    
    def get_top_n_by_type(self, type_name, n):
        analysis_data = self.get_analysis_data()
        top_data = (
            analysis_data[analysis_data["type"]==type_name]
            .sort_values(by="amount",ascending=False)
            .head(n)
            )
        return top_data




da = DataAnalyzer()
da.load_data('messy_expense_data.csv')
da.preprocess_data()
print(da.get_top_n_by_type("지출",5))


