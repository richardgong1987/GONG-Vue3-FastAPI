<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="番号" prop="laptopCode">
        <el-input
            v-model="queryParams.laptopCode"
            placeholder="请输入番号"
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
            v-hasPermi="['laptops:laptops:add']"
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
            v-hasPermi="['laptops:laptops:edit']"
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
            v-hasPermi="['laptops:laptops:remove']"
        >删除
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
            type="warning"
            plain
            icon="Download"
            @click="handleExport"
            v-hasPermi="['laptops:laptops:export']"
        >导出
        </el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="laptopsList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center"/>
      <el-table-column label="id" align="center" prop="id"/>
      <el-table-column label="番号" align="center" prop="laptopCode"/>
      <el-table-column label="ライセンスキー" width="155" align="center" prop="officeLicense"/>
      <el-table-column label="Microsoft Account" width="200" align="center" prop="microsoftAccount"/>
      <el-table-column label="PRODUCT_ID" width="300" align="center" prop="productId"/>
      <el-table-column label="SKU_ID" align="center" width="300" prop="skuId"/>
      <el-table-column label="LICENSE_NAME" width="300" align="center" prop="licenseName"/>
      <el-table-column label="LICENSE_DESCRIPTION" width="300" align="center" prop="licenseDescription"/>
      <el-table-column label="BETA_EXPIRATION" width="300" align="center" prop="betaExpiration"/>
      <el-table-column label="LICENSE_STATUS" width="300" align="center" prop="licenseStatus"/>
      <el-table-column label="status" width="200" align="center" prop="status"/>
      <el-table-column label="remark" width="300" align="center" prop="remark"/>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)"
                     v-hasPermi="['laptops:laptops:edit']">修改
          </el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)"
                     v-hasPermi="['laptops:laptops:remove']">删除
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

    <!-- 添加或修改laptop管理对话框 -->
    <el-dialog :title="title" v-model="open" width="1200px" append-to-body>
      <el-form ref="laptopsRef" :model="form" :rules="rules" label-width="180px">
        <el-form-item v-if="renderField(true, true)" label="番号" prop="laptopCode">
          <el-input v-model="form.laptopCode" placeholder="请输入番号"/>
        </el-form-item>
        <el-form-item v-if="renderField(true, true)" label="ライセンスキー" prop="officeLicense">
          <el-input v-model="form.officeLicense" placeholder="请输入ライセンスキー"/>
        </el-form-item>
        <el-form-item v-if="renderField(true, true)" label="Microsoft Account" prop="microsoftAccount">
          <el-input v-model="form.microsoftAccount" placeholder="请输入Microsoft Account"/>
        </el-form-item>
        <el-form-item v-if="renderField(true, true)" label="PRODUCT_ID" prop="productId">
          <el-input v-model="form.productId" placeholder="请输入PRODUCT_ID"/>
        </el-form-item>
        <el-form-item v-if="renderField(true, true)" label="SKU_ID" prop="skuId">
          <el-input v-model="form.skuId" placeholder="请输入SKU_ID"/>
        </el-form-item>
        <el-form-item v-if="renderField(true, true)" label="LICENSE_NAME" prop="licenseName">
          <el-input v-model="form.licenseName" placeholder="请输入LICENSE_NAME"/>
        </el-form-item>
        <el-form-item v-if="renderField(true, true)" label="LICENSE_DESCRIPTION" prop="licenseDescription">
          <el-input v-model="form.licenseDescription" placeholder="请输入LICENSE_DESCRIPTION"/>
        </el-form-item>
        <el-form-item v-if="renderField(true, true)" label="BETA_EXPIRATION" prop="betaExpiration">
          <el-input v-model="form.betaExpiration" placeholder="请输入BETA_EXPIRATION"/>
        </el-form-item>
        <el-form-item v-if="renderField(true, true)" label="remark" prop="remark">
          <el-input v-model="form.remark" placeholder="请输入remark"/>
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
import {listLaptops, getLaptops, delLaptops, addLaptops, updateLaptops} from "@/api/laptops/laptops.js";

const {proxy} = getCurrentInstance();

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
  rules: {}
});

const {queryParams, form, rules} = toRefs(data);

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
  proxy.$modal.confirm('是否确认删除laptop管理编号为"' + _ids + '"的数据项？').then(function () {
    return delLaptops(_ids);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {
  });
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