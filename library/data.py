from datetime import datetime
import pandas as pd


def DATE_PARSE(date): return datetime.strptime(date, "%Y年%m月%d日")


def get_data(ISIN, FUND):
    """
    Args:
        ISIN str: see https://www.jasdec.com/reading/itmei.php
        FUND str: see https://www.morningstar.co.jp/FundData/DetailSearchResult.do?mode=1
    """
    BASEURL = "https://toushin-lib.fwg.ne.jp/FdsWeb/FDST030000/csv-file-download?"
    ISINcd = "isinCd="+ISIN
    FUNDcd = "associFundCd="+FUND
    DOWNURL = BASEURL+ISINcd+"&"+FUNDcd

    df = pd.read_csv(DOWNURL, engine="python", encoding="shift-jis",
                     index_col="年月日", parse_dates=True, date_parser=DATE_PARSE)
    return df


def join_data(df_part, df_join, KEYWORD, str_date, end_date):
    df_part_fil = df_part.loc[(df_part.index >= str_date) & (
        df_part.index <= end_date), :]
    df_part_fil = df_part_fil.rename(columns={"基準価額(円)": KEYWORD})[[KEYWORD]]
    df_join = pd.merge(df_join, df_part_fil, left_index=True, right_index=True,
                       how="inner") if df_join is not None else df_part_fil
    return df_join
