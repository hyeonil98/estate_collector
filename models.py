from sqlalchemy import Column, Integer, String, Text, UniqueConstraint, Date
from sqlalchemy.ext.declarative import declarative_base

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