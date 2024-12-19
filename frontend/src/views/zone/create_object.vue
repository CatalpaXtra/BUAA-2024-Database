<template>
  <v-container class="page-container">
    <v-card class="create-container" title="补充评分对象" outlined>
      <v-row class="mb-4">
        <v-col cols="12">
          <v-card>
            <v-card-text>
              <v-file-input
                label="点击添加封面"
                prepend-icon="mdi-camera"
                type="file"
                ref="fileInput"
                accept="image/*"
                @change="handleFileUpload"
              ></v-file-input>
              <v-text-field
                v-model="object.name"
                label="请输入对象名称"
                hint="最多 24 字"
                max-length="24"
                outlined
                required
              ></v-text-field>
              
              <v-textarea
                v-model="object.description"
                label="简介"
                outlined
                rows="4"
              ></v-textarea>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
          <v-col cols="6">
            <v-btn @click="cancel" color="error" block>
              取消创建
            </v-btn>
          </v-col>
          <v-col cols="6">
            <v-btn @click="submitObject" color="success" block>
              提交创建
            </v-btn>
          </v-col>
        </v-row>
    </v-card>
  </v-container>
</template>

<script>
import api from '@/api/zone.js'
import { alert } from '@/store/alert.ts'

export default {
  data() {
    return {
      formData: new FormData(),
      object: {
        name: "", // 对象名称
        cover: null, // 对象封面
        description: "" // 对象简介
      },
      successDialog: false // 控制成功对话框
    };
  },
  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0];
      this.formData.append('graphic', file);
    },
    // 提交评分对象
    submitObject() {
      // 检查必填项
      if (this.formData.get('graphic') == null || !this.object.name || !this.object.description) {
        alert('请填写所有必填项！', 'warning');
        return console.log("请填写所有必填项！");
      }

      this.formData.append('name', this.object.name);
      this.formData.append('introduction', this.object.description);

      const zoneId = this.$route.query.zone_id;
      api.createObjectApi(this.formData, zoneId).then(res => {
        if (res.code === 200) {
          // 假设请求成功, 弹出成功对话框
          this.successDialog = true;
          alert(res.message, 'success');
          this.$router.push({ path: "/zones/zone_detail/",  query: { zone_id: zoneId } }); // 跳转到博客列表页
        }
        else {
          alert(res.message, 'error');
        }
      }).catch(error => {
        console.log(error)
      })
    },
    // 取消
    cancel() {
      this.$router.go(-1);
    },
    // 成功后跳转至专区
    redirectToZone() {
      this.successDialog = false;
      this.$router.push({ name: 'zoneDetail' }); // 这里跳转到具体的专区
    }
  }
};
</script>

<style scoped>

.v-card-title {
  font-weight: bold;
}

/* 用户信息卡片，将 v-card 置于页面中心 */
.create-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 16px;
  width: 80%;
}

/* 调整 v-card 长宽 */
.page-container {
  position: relative;
  width: 100%;
  height: 100%;
}
</style>
