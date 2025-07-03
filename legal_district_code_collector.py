from datetime import datetime
from pydoc import locate

import requests
import pandas as pd

from db_utils import upsert_post

# 기본 설정
base_url = "http://apis.data.go.kr/1741000/StanReginCd/getStanReginCdList"
service_key = "gqgCiTBY%2FOzh3gKUuVZHqIiL1tYT0oRma1NwX6frkysuY%2FEgLn4nSgRWDqGMM8YbTslnVrSfmE3D7n4iapQ%2BqQ%3D%3D"
page = 1
num_rows = 1000

# URL 조립


# 요청
while True:
    url = (
        f"{base_url}?serviceKey={service_key}"
        f"&type=json&pageNo={page}&numOfRows={num_rows}"
    )

    response = requests.get(url)
    data = response.json()
    if "StanReginCd" not in data:
        print("❌ StanReginCd 키 없음. 전체 응답 출력:")
        print(data)
    try:
        rows = data["StanReginCd"][1]["row"]

        for r in rows:
            parsed = {
                "region_cd": r["region_cd"],
                "sido_cd": r["sido_cd"],
                "sgg_cd": r["sgg_cd"],
                "umd_cd": r["umd_cd"],
                "ri_cd": r["ri_cd"],
                "locatjumin_cd": r["locatjumin_cd"],
                "locatjijuk_cd": r["locatjijuk_cd"],
                "locatadd_nm": r["locatadd_nm"],
                "locat_order": r["locat_order"],
                "locat_rm": r["locat_rm"],
                "locathigh_cd": r["locathigh_cd"],
                "locallow_nm": r["locallow_nm"],
                "adpt_de": None
            }

            if r["adpt_de"]:
                try:
                    parsed["adpt_de"] = datetime.strptime(r["adpt_de"], "%Y%m%d").date()
                except ValueError:
                    pass
            print(f"{parsed}")
            upsert_post(parsed)
    except Exception as e:
        print(f"exception: {e}")
        break
    page += 1
