<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="主键ID" prop="id">
        <el-input
            v-model="queryParams.id"
            placeholder="请输入主键ID"
            clearable
            style="width: 240px"
            @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="关键位，例如 PDH / PDL / PWH" prop="keyPoint">
        <el-input
            v-model="queryParams.keyPoint"
            placeholder="请输入关键位，例如 PDH / PDL / PWH"
            clearable
            style="width: 240px"
            @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="多空：B=Buy，S=Sell" prop="direction">
        <el-input
            v-model="queryParams.direction"
            placeholder="请输入多空：B=Buy，S=Sell"
            clearable
            style="width: 240px"
            @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="信号：顶分型 / pinbar / 吞没" prop="signal">
        <el-input
            v-model="queryParams.signal"
            placeholder="请输入信号：顶分型 / pinbar / 吞没"
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
      <el-form-item label="回撤25入场" prop="retrace25Result">
        <el-input
            v-model="queryParams.retrace25Result"
            placeholder="请输入回撤25入场"
            clearable
            style="width: 240px"
            @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="回撤38.2入场" prop="retrace382Result">
        <el-input
            v-model="queryParams.retrace382Result"
            placeholder="请输入回撤38.2入场"
            clearable
            style="width: 240px"
            @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="回撤50入场" prop="retrace50Result">
        <el-input
            v-model="queryParams.retrace50Result"
            placeholder="请输入回撤50入场"
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
            type="primary"
            plain
            icon="Plus"
            @click="handleAdd"
            v-hasPermi="['trd_trade_record:record:add']"
        >新增
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
            type="success"
            plain
            icon="Edit"
            :disabled="single"
            @click="handleUpdate"
            v-hasPermi="['trd_trade_record:record:edit']"
        >修改
        </el-button>
      </el-col>
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
      <el-table-column label="主键ID" align="center" prop="id"/>
      <el-table-column label="主键ID" align="center" prop="id"/>
      <el-table-column label="关键位，例如 PDH / PDL / PWH" align="center" prop="keyPoint"/>
      <el-table-column label="多空：B=Buy，S=Sell" align="center" prop="direction"/>
      <el-table-column label="信号：顶分型 / pinbar / 吞没" align="center" prop="signal"/>
      <el-table-column label="收盘入场" align="center" prop="closeEntryResult"/>
      <el-table-column label="回撤25入场" align="center" prop="retrace25Result"/>
      <el-table-column label="回撤38.2入场" align="center" prop="retrace382Result"/>
      <el-table-column label="回撤50入场" align="center" prop="retrace50Result"/>
      <el-table-column label="R后推保本：1.5" align="center" prop="moveToBreakevenAtR"/>
      <el-table-column label="备注" align="center" prop="remark"/>
      <el-table-column label="扩展JSON字段" align="center" prop="extra"/>
      <el-table-column label="创建时间" align="center" prop="createdAt"/>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)"
                     v-hasPermi="['trd_trade_record:record:edit']">修改
          </el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)"
                     v-hasPermi="['trd_trade_record:record:remove']">删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination
        v-show="total>0"
        :total="total"
        v-model:page="queryParams.pageNum"
        v-model:limit="queryParams.pageSize"
        @pagination="getList"
    />

    <!-- 添加或修改交易研究记录对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="recordRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item v-if="renderField(true, true)" label="关键位，例如 PDH / PDL / PWH" prop="keyPoint">
          <el-input v-model="form.keyPoint" placeholder="请输入关键位，例如 PDH / PDL / PWH"/>
        </el-form-item>
        <el-form-item v-if="renderField(true, true)" label="多空：B=Buy，S=Sell" prop="direction">
          <el-input v-model="form.direction" placeholder="请输入多空：B=Buy，S=Sell"/>
        </el-form-item>
        <el-form-item v-if="renderField(true, true)" label="信号：顶分型 / pinbar / 吞没" prop="signal">
          <el-input v-model="form.signal" placeholder="请输入信号：顶分型 / pinbar / 吞没"/>
        </el-form-item>
        <el-form-item v-if="renderField(true, true)" label="收盘入场" prop="closeEntryResult">
          <el-input v-model="form.closeEntryResult" placeholder="请输入收盘入场"/>
        </el-form-item>
        <el-form-item v-if="renderField(true, true)" label="回撤25入场" prop="retrace25Result">
          <el-input v-model="form.retrace25Result" placeholder="请输入回撤25入场"/>
        </el-form-item>
        <el-form-item v-if="renderField(true, true)" label="回撤38.2入场" prop="retrace382Result">
          <el-input v-model="form.retrace382Result" placeholder="请输入回撤38.2入场"/>
        </el-form-item>
        <el-form-item v-if="renderField(true, true)" label="回撤50入场" prop="retrace50Result">
          <el-input v-model="form.retrace50Result" placeholder="请输入回撤50入场"/>
        </el-form-item>
        <el-form-item v-if="renderField(true, true)" label="备注" prop="remark">
          <el-input v-model="form.remark" type="textarea" placeholder="请输入内容"/>
        </el-form-item>

      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="cancel">取 消</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="Record">
import {listRecord, getRecord, delRecord, addRecord, updateRecord} from "@/api/trd_trade_record/record";

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

/** 新增按钮操作 */
function handleAdd() {
  reset();
  open.value = true;
  title.value = "添加交易研究记录";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _id = row.id || ids.value;
  getRecord(_id).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改交易研究记录";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["recordRef"].validate(valid => {
    if (valid) {
      if (form.value.id != null) {
        updateRecord(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addRecord(form.value).then(response => {
          proxy.$modal.msgSuccess("新增成功");
          open.value = false;
          getList();
        });
      }
    }
  });
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