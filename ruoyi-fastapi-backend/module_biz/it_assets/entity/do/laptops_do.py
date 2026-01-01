from sqlalchemy import Column, String, DateTime, BigInteger, Identity

from config.database import Base


class BizLaptopManagement(Base):
    """
    laptop管理表
    """

    __tablename__ = 'biz_laptop_management'
    __table_args__ = {'comment': 'laptop管理'}

    id = Column(BigInteger, Identity(), primary_key=True, nullable=False, comment='id')
    created_at = Column(DateTime, nullable=True, comment='created_at')
    created_by = Column(BigInteger, nullable=False, comment='created_by')
    creator = Column(String, nullable=True, comment='creator')
    updated_at = Column(DateTime, nullable=False, comment='updated_at')
    updated_by = Column(BigInteger, nullable=False, comment='updated_by')
    updater = Column(String, nullable=True, comment='updater')
    deleted_by = Column(BigInteger, nullable=False, comment='deleted_by')
    deleted_at = Column(DateTime, nullable=True, comment='deleted_at')
    laptop_code = Column(String, nullable=True, comment='番号')
    office_license = Column(String, nullable=True, comment='ライセンスキー')
    microsoft_account = Column(String, nullable=True, comment='Microsoft Account')
    product_id = Column(String, nullable=True, comment='PRODUCT_ID')
    sku_id = Column(String, nullable=True, comment='SKU_ID')
    license_name = Column(String, nullable=True, comment='LICENSE_NAME')
    license_description = Column(String, nullable=True, comment='LICENSE_DESCRIPTION')
    beta_expiration = Column(String, nullable=True, comment='BETA_EXPIRATION')
    license_status = Column(String, nullable=True, comment='LICENSE_STATUS')
    status = Column(String, nullable=True, comment='status')
    remark = Column(String, nullable=True, comment='remark')
