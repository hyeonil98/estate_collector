from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import insert

from models import Base, RegionCode



def initialize_engine(echo=False, create_schema=False):
    # 아이디 비밀번호 secret 으로 설정
    engine = create_engine(
        "mysql+pymysql://:!@database-1.cleosac8ya6g.ap-northeast-2.rds.amazonaws.com:3306/estatedb?charset=utf8mb4",
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