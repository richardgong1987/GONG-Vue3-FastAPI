<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="created_at" prop="createdAt">
        <el-date-picker
          v-model="queryParams.createdAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择created_at"
          clearable
          style="width: 240px"
        />
      </el-form-item>
      <el-form-item label="creator" prop="creator">
        <el-input
          v-model="queryParams.creator"
          placeholder="请输入creator"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="updater" prop="updater">
        <el-input
          v-model="queryParams.updater"
          placeholder="请输入updater"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="deleted_at" prop="deletedAt">
        <el-date-picker
          v-model="queryParams.deletedAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择deleted_at"
          clearable
          style="width: 240px"
        />
      </el-form-item>
      <el-form-item label="番号" prop="laptopCode">
        <el-input
          v-model="queryParams.laptopCode"
          placeholder="请输入番号"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="ライセンスキー" prop="officeLicense">
        <el-input
          v-model="queryParams.officeLicense"
          placeholder="请输入ライセンスキー"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="Microsoft Account" prop="microsoftAccount">
        <el-input
          v-model="queryParams.microsoftAccount"
          placeholder="请输入Microsoft Account"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="PRODUCT_ID" prop="productId">
        <el-input
          v-model="queryParams.productId"
          placeholder="请输入PRODUCT_ID"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="SKU_ID" prop="skuId">
        <el-input
          v-model="queryParams.skuId"
          placeholder="请输入SKU_ID"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="LICENSE_NAME" prop="licenseName">
        <el-input
          v-model="queryParams.licenseName"
          placeholder="请输入LICENSE_NAME"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="LICENSE_DESCRIPTION" prop="licenseDescription">
        <el-input
          v-model="queryParams.licenseDescription"
          placeholder="请输入LICENSE_DESCRIPTION"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="BETA_EXPIRATION" prop="betaExpiration">
        <el-input
          v-model="queryParams.betaExpiration"
          placeholder="请输入BETA_EXPIRATION"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="LICENSE_STATUS" prop="licenseStatus">
        <el-select v-model="queryParams.licenseStatus" placeholder="请选择LICENSE_STATUS" clearable style="width: 240px">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item>
      <el-form-item label="status" prop="status">
        <el-select v-model="queryParams.status" placeholder="请选择status" clearable style="width: 240px">
          <el-option label="请选择字典生成" value="" />
        </el-select>
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
          v-hasPermi="['laptops:laptops:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['laptops:laptops:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['laptops:laptops:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['laptops:laptops:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="laptopsList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="id" align="center" prop="id" />
      <el-table-column label="id" align="center" prop="id" />
      <el-table-column label="id" align="center" prop="id" />
      <el-table-column label="created_at" align="center" prop="createdAt" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.createdAt, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="created_by" align="center" prop="createdBy" />
      <el-table-column label="creator" align="center" prop="creator" />
      <el-table-column label="updated_at" align="center" prop="updatedAt" />
      <el-table-column label="updated_by" align="center" prop="updatedBy" />
      <el-table-column label="updater" align="center" prop="updater" />
      <el-table-column label="deleted_by" align="center" prop="deletedBy" />
      <el-table-column label="deleted_at" align="center" prop="deletedAt" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.deletedAt, '{y}-{m}-{d}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="番号" align="center" prop="laptopCode" />
      <el-table-column label="ライセンスキー" align="center" prop="officeLicense" />
      <el-table-column label="Microsoft Account" align="center" prop="microsoftAccount" />
      <el-table-column label="PRODUCT_ID" align="center" prop="productId" />
      <el-table-column label="SKU_ID" align="center" prop="skuId" />
      <el-table-column label="LICENSE_NAME" align="center" prop="licenseName" />
      <el-table-column label="LICENSE_DESCRIPTION" align="center" prop="licenseDescription" />
      <el-table-column label="BETA_EXPIRATION" align="center" prop="betaExpiration" />
      <el-table-column label="LICENSE_STATUS" align="center" prop="licenseStatus" />
      <el-table-column label="status" align="center" prop="status" />
      <el-table-column label="remark" align="center" prop="remark" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['laptops:laptops:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['laptops:laptops:remove']">删除</el-button>
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

    <!-- 添加或修改laptop管理对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="laptopsRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item v-if="renderField(true, true)" label="created_at" prop="createdAt">
        <el-date-picker clearable
          v-model="form.createdAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择created_at">
        </el-date-picker>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="creator" prop="creator">
        <el-input v-model="form.creator" placeholder="请输入creator" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="updater" prop="updater">
        <el-input v-model="form.updater" placeholder="请输入updater" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="deleted_at" prop="deletedAt">
        <el-date-picker clearable
          v-model="form.deletedAt"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="请选择deleted_at">
        </el-date-picker>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="番号" prop="laptopCode">
        <el-input v-model="form.laptopCode" placeholder="请输入番号" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="ライセンスキー" prop="officeLicense">
        <el-input v-model="form.officeLicense" placeholder="请输入ライセンスキー" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="Microsoft Account" prop="microsoftAccount">
        <el-input v-model="form.microsoftAccount" placeholder="请输入Microsoft Account" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="PRODUCT_ID" prop="productId">
        <el-input v-model="form.productId" placeholder="请输入PRODUCT_ID" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="SKU_ID" prop="skuId">
        <el-input v-model="form.skuId" placeholder="请输入SKU_ID" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="LICENSE_NAME" prop="licenseName">
        <el-input v-model="form.licenseName" placeholder="请输入LICENSE_NAME" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="LICENSE_DESCRIPTION" prop="licenseDescription">
        <el-input v-model="form.licenseDescription" placeholder="请输入LICENSE_DESCRIPTION" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="BETA_EXPIRATION" prop="betaExpiration">
        <el-input v-model="form.betaExpiration" placeholder="请输入BETA_EXPIRATION" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="LICENSE_STATUS" prop="licenseStatus">
        <el-radio-group v-model="form.licenseStatus">
          <el-radio label="请选择字典生成" value="" />
        </el-radio-group>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="status" prop="status">
        <el-radio-group v-model="form.status">
          <el-radio label="请选择字典生成" value="" />
        </el-radio-group>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="remark" prop="remark">
        <el-input v-model="form.remark" placeholder="请输入remark" />
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

<script setup name="Laptops">
import { listLaptops, getLaptops, delLaptops, addLaptops, updateLaptops } from "@/api/laptops/laptops.js";

const { proxy } = getCurrentInstance();

const laptopsList = ref([]);
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
    createdAt: null,
    creator: null,
    updater: null,
    deletedAt: null,
    laptopCode: null,
    officeLicense: null,
    microsoftAccount: null,
    productId: null,
    skuId: null,
    licenseName: null,
    licenseDescription: null,
    betaExpiration: null,
    licenseStatus: null,
    status: null,
  },
  rules: {
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询laptop管理列表 */
function getList() {
  loading.value = true;
  listLaptops(queryParams.value).then(response => {
    laptopsList.value = response.rows;
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
    id: null,
    createdAt: null,
    createdBy: null,
    creator: null,
    updatedAt: null,
    updatedBy: null,
    updater: null,
    deletedBy: null,
    deletedAt: null,
    laptopCode: null,
    officeLicense: null,
    microsoftAccount: null,
    productId: null,
    skuId: null,
    licenseName: null,
    licenseDescription: null,
    betaExpiration: null,
    licenseStatus: null,
    status: null,
    remark: null,
  };
  proxy.resetForm("laptopsRef");
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
  title.value = "添加laptop管理";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _id = row.id || ids.value;
  getLaptops(_id).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改laptop管理";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["laptopsRef"].validate(valid => {
    if (valid) {
      if (form.value.id != null) {
        updateLaptops(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addLaptops(form.value).then(response => {
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
  proxy.$modal.confirm('是否确认删除laptop管理编号为"' + _ids + '"的数据项？').then(function() {
    return delLaptops(_ids);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('laptops/laptops/export', {
    ...queryParams.value
  }, `laptops_${new Date().getTime()}.xlsx`);
}

/** 是否渲染字段 */
function renderField(insert, edit) {
  return form.value.id == null ? insert : edit;
}

getList();
</script>