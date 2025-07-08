from sqlalchemy import Column, Integer, String, Text, UniqueConstraint, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import Float

Base = declarative_base()

class RegionCode(Base):
    __tablename__ = "region_codes"

    region_cd = Column(String(10), primary_key=True)
    sido_cd = Column(String(10))
    sgg_cd = Column(String(10))
    umd_cd = Column(String(10))
    ri_cd = Column(String(10))
    locatjumin_cd = Column(String(10))
    locatjijuk_cd = Column(String(10))
    locatadd_nm = Column(String(100))
    locat_order = Column(Integer)
    locat_rm = Column(String(100))
    locathigh_cd = Column(String(10))
    locallow_nm = Column(String(50))
    adpt_de = Column(Date)

    __table_args__ = (
        UniqueConstraint("region_cd", name="uq_region_cd"),
    )

class RealEstateDeal(Base):
    __tablename__ = "real_estate_deals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    build_year = Column(Integer)
    contract_start = Column(String(10))
    contract_end = Column(String(10))
    contract_type = Column(String(10))
    deal_day = Column(Integer)
    deal_month = Column(Integer)
    deal_year = Column(Integer)
    deposit = Column(Integer)
    exclu_use_ar = Column(Float)
    floor = Column(Integer)
    house_type = Column(String(20))
    jibun = Column(String(20))
    mhouse_nm = Column(String(50))
    monthly_rent = Column(Integer)
    pre_deposit = Column(String(20))
    pre_monthly_rent = Column(String(20))
    sgg_cd = Column(String(10))
    umd_nm = Column(String(20))
    use_rrright = Column(String(20))
