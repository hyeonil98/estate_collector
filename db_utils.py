from _ast import Dict
from typing import List

from sqlalchemy import create_engine, inspect, or_, and_, select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import Session
from typing_extensions import Any

from models import Base, RegionCode, RealEstateDeal


def initialize_engine(echo=False, create_schema=False):
    # 아이디 비밀번호 secret 으로 설정
    engine = create_engine(
        "mysql+pymysql://:@database-1.cleosac8ya6g.ap-northeast-2.rds.amazonaws.com:3306/estatedb?charset=utf8mb4",
        echo=echo,
        pool_size=5,
        max_overflow=2,
        pool_recycle=1800,
        pool_pre_ping=True
    )
    if create_schema:
        Base.metadata.create_all(engine)  # 최초 실행 시만 True로
    return engine


# 최초 1회만 True
engine = initialize_engine(create_schema=False)

def fetch_filtered_table_data_with_like_multi_like(
    table_name,
    filters,
    like_filters):
    """
    LIKE 조건에 리스트를 허용하여 서울%, 경기% 등 복수 조건 검색 지원
    """
    inspector = inspect(engine)
    session = Session(bind=engine)

    if table_name not in inspector.get_table_names():
        raise ValueError(f"'{table_name}' 테이블이 존재하지 않습니다.")

    table = Base.metadata.tables.get(table_name)
    if table is None:
        raise ValueError(f"'{table_name}' 테이블은 Base에 정의되어 있지 않습니다.")

    try:
        conditions = []

        # 일반 조건
        for key, value in filters.items():
            if key in table.c:
                conditions.append(table.c[key] == value)
            else:
                raise ValueError(f"'{key}' 컬럼이 없습니다.")

        # LIKE 조건
        if like_filters:
            for key, patterns in like_filters.items():
                if key in table.c:
                    like_conds = [table.c[key].like(p) for p in patterns]
                    conditions.append(or_(*like_conds))
                else:
                    raise ValueError(f"'{key}' 컬럼이 없습니다.")

        stmt = select(table).where(and_(*conditions))
        result = session.execute(stmt).mappings().all()
        return result

    finally:
        session.close()

def upsert_post(data):
    stmt = insert(RegionCode).values(**data)
    update_stmt = stmt.on_duplicate_key_update(
        sido_cd=stmt.inserted.sido_cd,
        sgg_cd=stmt.inserted.sgg_cd,
        umd_cd=stmt.inserted.umd_cd,
        ri_cd=stmt.inserted.ri_cd,
        locatjumin_cd=stmt.inserted.locatjumin_cd,
        locatjijuk_cd=stmt.inserted.locatjijuk_cd,
        locatadd_nm=stmt.inserted.locatadd_nm,
        locat_order=stmt.inserted.locat_order,
        locat_rm=stmt.inserted.locat_rm,
        locathigh_cd=stmt.inserted.locathigh_cd,
        locallow_nm=stmt.inserted.locallow_nm,
        adpt_de=stmt.inserted.adpt_de
    )
    with engine.begin() as conn:
        conn.execute(update_stmt)

def upsert_real_estate(data):
    stmt = insert(RealEstateDeal).values(**data)
    update_stmt = stmt.on_duplicate_key_update(
        mhouse_nm=stmt.inserted.mhouse_nm,
        monthly_rent=stmt.inserted.monthly_rent,
        pre_deposit=stmt.inserted.pre_deposit,
        pre_monthly_rent=stmt.inserted.pre_monthly_rent,
        sgg_cd=stmt.inserted.sgg_cd,
        umd_nm=stmt.inserted.umd_nm,
        use_rrright=stmt.inserted.use_rrright
    )
    with engine.begin() as conn:
        conn.execute(update_stmt)