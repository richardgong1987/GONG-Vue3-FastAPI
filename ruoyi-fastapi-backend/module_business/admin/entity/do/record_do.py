from sqlalchemy import Numeric, Text, BigInteger, JSONB, DateTime, String, Column

from config.database import Base


class TrdTradeRecord(Base):
    """
    交易研究记录表
    """

    __tablename__ = 'trd_trade_record'
    __table_args__ = {'comment': '交易研究记录表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment='主键ID')
    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment='主键ID')
    key_point = Column(String, nullable=True, comment='关键位，例如 PDH / PDL / PWH')
    direction = Column(String, nullable=True, comment='多空：B=Buy，S=Sell')
    signal = Column(String, nullable=True, comment='信号：顶分型 / pinbar / 吞没')
    close_entry_result = Column(String, nullable=True, comment='收盘入场')
    retrace_25_result = Column(String, nullable=True, comment='回撤25入场')
    retrace_382_result = Column(String, nullable=True, comment='回撤38.2入场')
    retrace_50_result = Column(String, nullable=True, comment='回撤50入场')
    move_to_breakeven_at_r = Column(Numeric, nullable=True, comment='R后推保本：1.5')
    remark = Column(Text, nullable=True, comment='备注')
    extra = Column(JSONB, nullable=True, comment='扩展JSON字段')
    created_at = Column(DateTime, primary_key=True, nullable=False, comment='创建时间')



