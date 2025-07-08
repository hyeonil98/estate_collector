from lxml import etree
import requests

from db_utils import upsert_post, upsert_real_estate, fetch_filtered_table_data_with_like_multi_like
from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_last_6_months():
    now = datetime.now()
    result = []

    for i in range(6, -1, -1):  # 6개월 전부터 현재까지 (총 7개)
        date = now - relativedelta(months=i)
        result.append(date.strftime("%Y%m"))

    return result

def parse_item_to_model(item_dict):
    contract_term = item_dict.get("contractTerm", "").strip()
    contract_start = ""
    contract_end = ""
    if "~" in contract_term:
        parts = contract_term.split("~")
        contract_start = parts[0].strip()
        contract_end = parts[1].strip()

    return {
        "build_year": int(item_dict.get("buildYear", 0)),
        "contract_start": contract_start,
        "contract_end": contract_end,
        "contract_type": item_dict.get("contractType", ""),
        "deal_day": int(item_dict.get("dealDay", 0)),
        "deal_month": int(item_dict.get("dealMonth", 0)),
        "deal_year": int(item_dict.get("dealYear", 0)),
        "deposit": int(item_dict.get("deposit", 0).replace(",", "")),
        "exclu_use_ar": float(item_dict.get("excluUseAr", 0.0)),
        "floor": int(item_dict.get("floor", 0)),
        "house_type": item_dict.get("houseType", ""),
        "jibun": item_dict.get("jibun", ""),
        "mhouse_nm": item_dict.get("mhouseNm", ""),
        "monthly_rent": int(item_dict.get("monthlyRent", 0)),
        "pre_deposit": item_dict.get("preDeposit", "").strip(),
        "pre_monthly_rent": item_dict.get("preMonthlyRent", "").strip(),
        "sgg_cd": item_dict.get("sggCd", ""),
        "umd_nm": item_dict.get("umdNm", ""),
        "use_rrright": item_dict.get("useRRRight", "").strip()
    }


def get_real_estate_info(LAWD_CD, DEAL_YMD):
    url = "http://apis.data.go.kr/1613000/RTMSDataSvcRHRent/getRTMSDataSvcRHRent?serviceKey=gqgCiTBY%2FOzh3gKUuVZHqIiL1tYT0oRma1NwX6frkysuY%2FEgLn4nSgRWDqGMM8YbTslnVrSfmE3D7n4iapQ%2BqQ%3D%3D"
    params = {
        "LAWD_CD"  : LAWD_CD,
        "DEAL_YMD" : DEAL_YMD
    }
    response = requests.get(url, params=params)
    # 2. XML 파싱
    root = etree.fromstring(response.content)

    # 모든 <item> 요소 추출
    items = root.xpath(".//item")
    parsed_items = []
    for item in items:
        raw = {}
        for element in item.iterchildren():
            tag = element.tag
            text = element.text.strip() if element.text else ""
            raw[tag] = text

        model_data = parse_item_to_model(raw)
        print(f"model_data: {model_data}")
        parsed_items.append(model_data)
        upsert_real_estate(model_data)

if __name__ == '__main__':
    filters = {}
    region_codes = set()
    get_6_month = get_last_6_months()

    like_filters = {
        "locatadd_nm": ["서울%", "경기%"]  # 두 개 이상 LIKE 조건
    }

    rows = fetch_filtered_table_data_with_like_multi_like(
        "region_codes", filters, like_filters
    )

    for month in get_6_month:
        for row in rows:
            region_code = row["region_cd"]
            region_codes.add(region_code[:5])

            for region_code in region_codes:
                get_real_estate_info(region_code, month)