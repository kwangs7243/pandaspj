# CSV 불러오기
# 전체 데이터 확인
# 월별 수입/지출 요약
# 카테고리별 지출 합계
# 가장 큰 지출 5개 보기
# 특정 월 데이터만 보기
# 키워드 검색
# 분석 결과 저장
import pandas as pd
class DataAnalyzer():
    # 객체생성
    def __init__(self):
        self.df = None

    # 파일경로를 받아서 파일 읽기 => 데이터프레임으로 처리됨 na_values : 잘못들어온값을 NaN으로 치환해줌
    def load_data(self,file_path):
        self.df = pd.read_csv(file_path,encoding="utf-8-sig",na_values=["not_available"]) 

    # 데이터 전처리
    # self.df["amount"] = self.df["amount"].str.strip().str.strip("원").str.strip("-").str.replace(",","",regex=False)
    # ↪ 이런 메서드채이닝 보단 정규식패턴으로 처리하는게 좀더 실무스타일
    # [^\d] 정규식패턴중하나 [] = or, ^ : not , \d : 숫자(0~9) => 숫자가아닌패턴을 찾는다
    # 전처리 과정을 컬럼으로 남겨서 원본 => 중간 => 결과 이런흐름을 확인할수있는 습관을 들여야한다
    def preprocess_data(self):
        self.df.columns = ["date","type","category","amount","content"]
        self.df["type"] = self.df["type"].str.strip().str.replace(" ", "", regex=False).str.lower()
        self.df["type"] = self.df["type"].str.replace({
            'income':'수입','refund':'수입','expense':'지출'})
        self.df["category"] = self.df["category"].str.strip().str.replace(" ", "", regex=False).str.lower()
        self.df["category"] = self.df["category"].str.replace({
            'food':'식비','cafe':'카페','shopping':'쇼핑',
            'bonus':'급여','salary':'급여',
            'transport':'교통'})
        self.df["amount_str"] = self.df["amount"].str.replace(r"[^\d]","",regex=True)
        self.df["amount_num"] = pd.to_numeric(self.df["amount_str"],errors="coerce")


da = DataAnalyzer()
da.load_data('messy_expense_data.csv')
da.preprocess_data()
print(da.df[["amount","amount_str","amount_num"]])
print(da.df["amount_num"].agg(["count","mean","sum"]))

