DO
$$
    DECLARE
        parentId BIGINT;
    BEGIN
        -- 菜单 SQL
        INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible,
                              status, perms, icon, create_by, create_time, update_by, update_time, remark)
        VALUES ('交易研究记录', '3', '1', 'record', 'trd_trade_record/record/index', 1, 0, 'C', '0', '0',
                'trd_trade_record:record:list', '#', 'admin', CURRENT_TIMESTAMP, '', NULL, '交易研究记录菜单')
        RETURNING menu_id INTO parentId;

        -- 按钮 SQL
        INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible,
                              status, perms, icon, create_by, create_time, update_by, update_time, remark)
        VALUES ('交易研究记录查询', parentId, '1', '#', '', 1, 0, 'F', '0', '0', 'trd_trade_record:record:query', '#',
                'admin', CURRENT_TIMESTAMP, '', NULL, '');

        INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible,
                              status, perms, icon, create_by, create_time, update_by, update_time, remark)
        VALUES ('交易研究记录新增', parentId, '2', '#', '', 1, 0, 'F', '0', '0', 'trd_trade_record:record:add', '#',
                'admin', CURRENT_TIMESTAMP, '', NULL, '');

        INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible,
                              status, perms, icon, create_by, create_time, update_by, update_time, remark)
        VALUES ('交易研究记录修改', parentId, '3', '#', '', 1, 0, 'F', '0', '0', 'trd_trade_record:record:edit', '#',
                'admin', CURRENT_TIMESTAMP, '', NULL, '');

        INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible,
                              status, perms, icon, create_by, create_time, update_by, update_time, remark)
        VALUES ('交易研究记录删除', parentId, '4', '#', '', 1, 0, 'F', '0', '0', 'trd_trade_record:record:remove', '#',
                'admin', CURRENT_TIMESTAMP, '', NULL, '');

        INSERT INTO sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible,
                              status, perms, icon, create_by, create_time, update_by, update_time, remark)
        VALUES ('交易研究记录导出', parentId, '5', '#', '', 1, 0, 'F', '0', '0', 'trd_trade_record:record:export', '#',
                'admin', CURRENT_TIMESTAMP, '', NULL, '');
    END
$$;
