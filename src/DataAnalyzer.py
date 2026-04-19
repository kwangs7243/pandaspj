import pandas as pd


class DataAnalyzer:
    """
    CSV 데이터를 불러와 전처리하고,
    분석에 사용할 수 있는 형태로 정리하는 클래스.
    """

    def __init__(self):
        """
        원본 데이터와 기본 설정값을 준비한다.
        """
        self.df = None
        self.valid_types = ["수입", "지출"]

    def _check_loaded(self):
        """
        데이터가 로드되었는지 확인한다.
        """
        if self.df is None:
            raise RuntimeError("먼저 load_data()를 실행해야 합니다.")

    def _check_preprocessed(self):
        """
        전처리에 필요한 컬럼이 준비되었는지 확인한다.
        """
        self._check_loaded()
        required_columns = ["date_dt", "year", "month", "type_map", "category_str", "amount_num"]
        missing_columns = [col for col in required_columns if col not in self.df.columns]
        if missing_columns:
            raise RuntimeError(
                "먼저 preprocess_data()를 실행해야 합니다."
                f"누락된 컬럼 : {missing_columns}"
            )

    def load_data(self, file_path):
        """
        CSV 파일을 읽어 원본 데이터프레임으로 저장한다.
        """
        self.df = pd.read_csv(file_path, encoding="utf-8-sig", na_values=["not_available"])

    def preprocess_data(self):
        """
        날짜, 타입, 카테고리, 금액 컬럼을 분석용으로 전처리한다.
        """
        self._check_loaded()
        df = self.df

        df.columns = ["date_raw", "type_raw", "category_raw", "amount_raw", "content"]

        df["date_parts"] = df["date_raw"].str.findall(r"\d+")
        df["date_str"] = df["date_parts"].str.join("-")
        df["date_dt"] = pd.to_datetime(df["date_str"], errors="coerce", format="mixed")
        df["year"] = df["date_dt"].dt.year
        df["month"] = df["date_dt"].dt.month
        df["year_month"] = df["date_dt"].dt.to_period("M")

        df["type_str"] = df["type_raw"].str.strip().str.replace(" ", "", regex=False).str.lower()
        df["type_map"] = df["type_str"].replace({
            "income": "수입", "refund": "수입", "bonus": "수입", "용돈": "수입", "입금": "수입",
            "allowance": "수입", "salary": "수입", "수익": "수입", "payback": "수입",
            "expense": "지출", "출금": "지출", "buy": "지출", "used": "지출",
            "payment": "지출", "spend": "지출", "other": "지출"
        })

        df["category_str"] = df["category_raw"].str.strip().str.replace(" ", "", regex=False)

        is_man = df["amount_raw"].str.contains("만")
        is_chun = df["amount_raw"].str.contains("천")
        df["amount_parts"] = df["amount_raw"].str.findall(r"\d+")
        df["amount_str"] = df["amount_parts"].str.join("")
        df["amount_num"] = pd.to_numeric(df["amount_str"], errors="coerce")
        df.loc[is_man, "amount_num"] = df.loc[is_man, "amount_num"] * 10000
        df.loc[is_chun, "amount_num"] = df.loc[is_chun, "amount_num"] * 1000

    def find_invalid_rows(self):
        """
        전처리에 실패한 행만 모아서 반환한다.
        """
        self._check_preprocessed()
        df = self.df.copy()

        date_invalid = df["date_dt"].isna()
        type_invalid = ~df["type_map"].isin(self.valid_types) | df["type_map"].isna()
        amount_invalid = df["amount_num"].isna()
        category_invalid = (df["category_str"].str.strip() == "") | (df["category_str"].isna())
        content_invalid = df["content"].isna()

        df["invalid_reason"] = ""
        df.loc[date_invalid, "invalid_reason"] = "날짜변환실패"
        df.loc[(type_invalid) & (df["invalid_reason"] == ""), "invalid_reason"] = "타입변환실패"
        df.loc[(amount_invalid) & (df["invalid_reason"] == ""), "invalid_reason"] = "금액변환실패"
        df.loc[(category_invalid) & (df["invalid_reason"] == ""), "invalid_reason"] = "카테고리내용없음"
        df.loc[(content_invalid) & (df["invalid_reason"] == ""), "invalid_reason"] = "내용없음"

        invalid_mask = date_invalid | type_invalid | amount_invalid | category_invalid | content_invalid
        return df[invalid_mask]

    def get_invalid_summary(self):
        """
        전처리 성공/실패 결과를 요약해서 반환한다.
        """
        self._check_preprocessed()

        analysis_data = self.get_analysis_data()
        invalid_df = self.find_invalid_rows()

        invalid_summary = {
            "전체 행 수": len(self.df),
            "성공 행 수": len(analysis_data),
            "실패 행 수": len(invalid_df),
        }

        if invalid_summary["전체 행 수"] == 0:
            invalid_summary["성공률"] = "계산불가"
        else:
            invalid_summary["성공률"] = (
                invalid_summary["성공 행 수"] / invalid_summary["전체 행 수"]
            ) * 100

        invalid_summary["실패사유"] = {
            "날짜변환실패": int(invalid_df["invalid_reason"].eq("날짜변환실패").sum()),
            "타입변환실패": int(invalid_df["invalid_reason"].eq("타입변환실패").sum()),
            "금액변환실패": int(invalid_df["invalid_reason"].eq("금액변환실패").sum()),
            "카테고리내용없음": int(invalid_df["invalid_reason"].eq("카테고리내용없음").sum()),
            "내용없음": int(invalid_df["invalid_reason"].eq("내용없음").sum()),
        }

        return invalid_summary

    def get_analysis_data(self):
        """
        전처리 결과에서 분석에 사용할 정상 데이터만 반환한다.
        """
        self._check_preprocessed()

        analysis_data = self.df[
            ["date_dt", "year", "month", "year_month", "type_map", "category_str", "amount_num", "content"]
        ].copy()

        analysis_data = analysis_data.rename(columns={
            "date_dt": "date",
            "type_map": "type",
            "category_str": "category",
            "amount_num": "amount"
        })

        analysis_data = analysis_data.dropna(axis=0)
        analysis_data = analysis_data[analysis_data["type"].isin(self.valid_types)]

        return analysis_data

    def save_data(self, data: pd.DataFrame, file_path, index=False):
        """
        데이터프레임을 CSV 파일로 저장한다.
        """
        data.to_csv(file_path, index=index, encoding="utf-8-sig")



