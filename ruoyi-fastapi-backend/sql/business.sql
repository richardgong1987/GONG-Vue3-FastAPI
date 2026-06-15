CREATE TABLE trd_trade_record
(
    id                     BIGSERIAL PRIMARY KEY,
    key_point              VARCHAR(20),
    direction              VARCHAR(20),
    signal                 VARCHAR(50),
    close_entry_result     VARCHAR(20),
    retrace_25_result      VARCHAR(20),
    retrace_382_result     VARCHAR(20),
    retrace_50_result      VARCHAR(20),
    move_to_breakeven_at_r NUMERIC(10, 2),
    remark                 TEXT,
    extra                  jsonb,
    created_at             timestamptz NOT NULL DEFAULT NOW()
);

COMMENT
ON TABLE trd_trade_record IS '交易研究记录表';

COMMENT
ON COLUMN trd_trade_record.id
    IS '主键ID';

COMMENT
ON COLUMN trd_trade_record.key_point
    IS '关键位，例如 PDH / PDL / PWH';

COMMENT
ON COLUMN trd_trade_record.direction
    IS '多空：B=Buy，S=Sell';

COMMENT
ON COLUMN trd_trade_record.signal
    IS '信号：顶分型 / pinbar / 吞没';

COMMENT
ON COLUMN trd_trade_record.close_entry_result
    IS '收盘入场';

COMMENT
ON COLUMN trd_trade_record.retrace_25_result
    IS '回撤25入场';

COMMENT
ON COLUMN trd_trade_record.retrace_382_result
    IS '回撤38.2入场';

COMMENT
ON COLUMN trd_trade_record.retrace_50_result
    IS '回撤50入场';

COMMENT
ON COLUMN trd_trade_record.move_to_breakeven_at_r
    IS 'R后推保本：1.5';

COMMENT
ON COLUMN trd_trade_record.remark
    IS '备注';

COMMENT
ON COLUMN trd_trade_record.extra
    IS '扩展JSON字段';

COMMENT
ON COLUMN trd_trade_record.created_at
    IS '创建时间';