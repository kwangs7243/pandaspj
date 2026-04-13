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
    def __init__(self):
        self.df = None

    def load_data(self,file_path):
        self.df = pd.read_csv(file_path)
    
    def preprocess_data(self):
        pass




