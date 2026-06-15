<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="80px">
      <el-form-item label="关键位" prop="keyPoint">
        <el-input
            v-model="queryParams.keyPoint"
            placeholder="请输入关键位"
            clearable
            style="width: 240px"
            @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="多空" prop="direction">
        <el-input
            v-model="queryParams.direction"
            placeholder="请输入多空"
            clearable
            style="width: 240px"
            @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="信号" prop="signal">
        <el-input
            v-model="queryParams.signal"
            placeholder="请输入信号"
            clearable
            style="width: 240px"
            @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="收盘入场" prop="closeEntryResult">
        <el-input
            v-model="queryParams.closeEntryResult"
            placeholder="请输入收盘入场"
            clearable
            style="width: 240px"
            @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
            type="danger"
            plain
            icon="Delete"
            :disabled="multiple"
            @click="handleDelete"
            v-hasPermi="['trd_trade_record:record:remove']"
        >删除
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
            type="warning"
            plain
            icon="Download"
            @click="handleExport"
            v-hasPermi="['trd_trade_record:record:export']"
        >导出
        </el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="recordList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center"/>
      <el-table-column label="ID" align="center" prop="id"/>
      <el-table-column label="关键位" align="center" prop="keyPoint"/>
      <el-table-column label="多空" align="center" prop="direction"/>
      <el-table-column label="信号" align="center" prop="signal"/>
      <el-table-column label="收盘入场" align="center" prop="closeEntryResult"/>
      <el-table-column label="回撤25入场" align="center" prop="retrace25Result"/>
      <el-table-column label="回撤38.2入场" align="center" prop="retrace382Result"/>
      <el-table-column label="回撤50入场" align="center" prop="retrace50Result"/>
      <el-table-column label="R后推保本" align="center" prop="moveToBreakevenAtR"/>
      <el-table-column label="备注" align="center" prop="remark"/>
      <el-table-column label="创建时间" align="center" prop="createdAt"/>
    </el-table>

    <pagination
        v-show="total>0"
        :total="total"
        v-model:page="queryParams.pageNum"
        v-model:limit="queryParams.pageSize"
        @pagination="getList"
    />
  </div>
</template>

<script setup name="Record">
import {delRecord, listRecord} from "@/api/trd_trade_record/record";

const {proxy} = getCurrentInstance();

const recordList = ref([]);
const open = ref(false);
const loading = ref(true);
const showSearch = ref(true);
const ids = ref([]);
const single = ref(true);
const multiple = ref(true);
const total = ref(0);
const title = ref("");

const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    id: null,
    keyPoint: null,
    direction: null,
    signal: null,
    closeEntryResult: null,
    retrace25Result: null,
    retrace382Result: null,
    retrace50Result: null,
    moveToBreakevenAtR: null,
    remark: null,
    extra: null,
  },
  rules: {}
});

const {queryParams, form, rules} = toRefs(data);

/** 查询交易研究记录列表 */
function getList() {
  loading.value = true;
  listRecord(queryParams.value).then(response => {
    recordList.value = response.rows;
    total.value = response.total;
    loading.value = false;
  });
}

/** 取消按钮 */
function cancel() {
  open.value = false;
  reset();
}

/** 表单重置 */
function reset() {
  form.value = {
    id: null,
    keyPoint: null,
    direction: null,
    signal: null,
    closeEntryResult: null,
    retrace25Result: null,
    retrace382Result: null,
    retrace50Result: null,
    moveToBreakevenAtR: null,
    remark: null,
    extra: null,
    createdAt: null,
  };
  proxy.resetForm("recordRef");
}

/** 搜索按钮操作 */
function handleQuery() {
  queryParams.value.pageNum = 1;
  getList();
}

/** 重置按钮操作 */
function resetQuery() {
  proxy.resetForm("queryRef");
  handleQuery();
}

/** 多选框选中数据  */
function handleSelectionChange(selection) {
  ids.value = selection.map(item => item.id);
  single.value = selection.length != 1;
  multiple.value = !selection.length;
}

/** 删除按钮操作 */
function handleDelete(row) {
  const _ids = row.id || ids.value;
  proxy.$modal.confirm('是否确认删除交易研究记录编号为"' + _ids + '"的数据项？').then(function () {
    return delRecord(_ids);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {
  });
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('trd_trade_record/record/export', {
    ...queryParams.value
  }, `record_${new Date().getTime()}.xlsx`);
}

/** 是否渲染字段 */
function renderField(insert, edit) {
  return form.value.id == null ? insert : edit;
}

getList();
</script>