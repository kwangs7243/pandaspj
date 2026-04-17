import pandas as pd
class DataAnalyzer():
    # 객체생성 (데이터프레임을 담을 객체, 타입허용값, 카테고리허용값)
    def __init__(self):
        self.df = None
        self.valid_types = ["수입", "지출"]

    # 데이터를 로드했는지 확인 => 아닐경우 오류 발생시키기
    def _check_loaded(self):
        if self.df is None:
            raise RuntimeError("먼저 load_data()를 실행해야 합니다.")

    # 데이터를 전처리했는지 확인 => 아닐경우 오류발생시키기 (누락된 컬럼명 같이 안내 디버깅 좋음)
    def _check_preprocessed(self):
        self._check_loaded()
        required_columns = ["date_dt", "year", "month", "type_map", "category_str", "amount_num"]
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

        df["date_parts"] = df["date_raw"].str.findall(r"\d+")
        df["date_str"] = df["date_parts"].str.join("-")
        df["date_dt"] = pd.to_datetime(df["date_str"], errors="coerce", format="mixed")
        df["year"] = df["date_dt"].dt.year
        df["month"] = df["date_dt"].dt.month
#         [       '용돈',        '출금',       'buy',      'used', 'allowance',   'incomee',
#               'unknown',    'salary',        '수익',   'payment',     'spend',        '??',
#          nan,    'expnse',   'payback',     'other',        '입금']
        df["type_str"] = df["type_raw"].str.strip().str.replace(" ", "", regex=False).str.lower()
        df["type_map"] = df["type_str"].replace({
            'income':'수입','refund':'수입','bonus':'수입','용돈':'수입','입금':'수입',
            'allowance':'수입', 'salary':'수입','수익':'수입','payback':'수입',
            'expense':'지출','출금':'지출','buy':'지출','used':'지출',
            'payment':'지출','spend':'지출','other':'지출'})

        df["category_str"] = df["category_raw"].str.strip().str.replace(" ", "", regex=False)

        is_MAN = df["amount_raw"].str.contains("만")
        is_CHUN = df["amount_raw"].str.contains("천")
        df["amount_parts"] = df["amount_raw"].str.findall(r"\d+")
        df["amount_str"] = df["amount_parts"].str.join("")
        df["amount_num"] = pd.to_numeric(df["amount_str"],errors="coerce")
        df.loc[is_MAN,"amount_num"] = df.loc[is_MAN,"amount_num"] * 10000
        df.loc[is_CHUN,"amount_num"] = df.loc[is_CHUN,"amount_num"] * 1000

    # 전처리 실패항목 체크하기
    def find_invalid_rows(self):
        self._check_preprocessed()
        df = self.df.copy()
        valid_types = self.valid_types

        date_invalid = df["date_dt"].isna()
        type_invalid = ~df["type_map"].isin(valid_types) | df["type_map"].isna()
        amount_invalid = df["amount_num"].isna()
        category_invalid = (
            (df["category_str"].str.strip() == "") | 
            (df["category_str"].isna())
                            )
        content_invalid = df["content"].isna()

        df["invalid_reason"] = ""
        df.loc[date_invalid,"invalid_reason"] = "날짜변환실패"
        df.loc[(type_invalid) & (df["invalid_reason"]==""), "invalid_reason"] = "타입변환실패"
        df.loc[(amount_invalid) & (df["invalid_reason"]==""), "invalid_reason"] = "금액변환실패"
        df.loc[(category_invalid) & (df["invalid_reason"]==""), "invalid_reason"] = "카테고리내용없음"
        df.loc[(content_invalid) & (df["invalid_reason"]==""), "invalid_reason"] = "내용없음"

        invalid_mask = date_invalid | type_invalid | amount_invalid | category_invalid | content_invalid

        return df[invalid_mask]
    
    # 전처리 결과 요약
    def get_invalid_summary(self):
        self._check_preprocessed()

        invalid_summary = {}
        
        analysis_data = self.get_analysis_data()
        invalid_df = self.find_invalid_rows()

        invalid_summary["전체 행 수"] = len(self.df)
        invalid_summary["성공 행 수"] = len(analysis_data)
        invalid_summary["실패 행 수"] = len(invalid_df)
        
        if invalid_summary["전체 행 수"] == 0 :
            invalid_summary["성공률"] = "계산불가"
        else:
            invalid_summary["성공률"] = (invalid_summary["성공 행 수"]/ invalid_summary["전체 행 수"]) * 100

        invalid_summary["실패사유"] = {
                                        "날짜변환실패": 0,
                                        "타입변환실패": 0,
                                        "금액변환실패": 0,
                                        "카테고리내용없음": 0,
                                        "내용없음": 0
                                    }
        for key in invalid_summary["실패사유"]:
            invalid_summary["실패사유"][key] = int(invalid_df["invalid_reason"].isin([key]).sum())

        return invalid_summary
    
    # 분석용 데이터 생성
    def get_analysis_data(self):
        self._check_preprocessed()
        valid_types = self.valid_types

        analysis_data : pd.DataFrame = self.df[["date_dt","year","month","type_map",
                            "category_str","amount_num","content"]].copy()
        
        analysis_data = analysis_data.rename(
                            columns=
                                {"date_dt":"date", "type_map":"type", 
                                "category_str":"category", "amount_num":"amount"})
        
        analysis_data = analysis_data.dropna(axis=0)

        analysis_data = analysis_data[analysis_data["type"].isin(valid_types)]

        return analysis_data
    
    

    
    # 데이터 저장
    def save_data(self,data : pd.DataFrame,file_path,index=False):
        data.to_csv(file_path, index=index, encoding="utf-8-sig")



