<template>
  <v-container class="page-container" color="grey lighten-4">
    <!-- 评分专区创建表单 -->
    <v-card class="create-container" title="创建专区" outlined>
      <v-form ref="form" v-model="valid" lazy-validation>
        <!-- 添加封面 -->
        <v-row>
          <v-col cols="12">
            <v-file-input
              label="点击添加封面"
              prepend-icon="mdi-camera"
              type="file"
              ref="fileInput"
              accept="image/*"
              @change="handleFileUpload"
            ></v-file-input>
          </v-col>
        </v-row>


        <v-text-field
          v-model="zoneTitle"
          label="输入评分主题"
          hint="最多 12 字"
          max-length="12"
          outlined
          required
        ></v-text-field>


        <!-- 输入评分简介 -->

        <v-textarea
          v-model="zoneIntroduction"
          label="输入评分简介"
          outlined
          rows="4"
        ></v-textarea>


        <!-- 添加评分对象 -->
        <v-card v-if="objects.length === 0" color="secondary" variant="flat" class="mx-auto" @click="openObjectDialog">
          <v-card-item>
            <div>
              <v-row align="center">
                <v-col cols="auto">
                  <v-icon>mdi-plus-box-multiple</v-icon>
                </v-col>
                <v-col cols="auto">
                  <div class="text-h6 mb-1">添加评分对象（不得少于 3 个）</div>
                </v-col>
              </v-row>
              <div class="text-caption">
                添加 3 个及以上评分对象，才能获得更多打分哦~
              </div>
            </div>
          </v-card-item>
        </v-card>

        <v-container v-else>
          <v-row>
            <v-col cols="auto">
              <p>全部评分对象</p>
            </v-col>
          </v-row>

          <!-- 评分对象列表 -->
          <v-row>
            <v-col v-for="(object, index) in objects" :key="index" cols="12">
              <v-card>
                <v-row>
                  <v-col cols="auto" class="ml-1">
                    <v-img :src="getImageUrl(object.cover)" alt="object cover" aspect-ratio="1" style="width: 80px" />
                  </v-col>
                  <v-col>
                    <v-card-title>{{ object.name }}</v-card-title>
                    <v-card-subtitle>{{ object.description || '无简介' }}</v-card-subtitle>
                  </v-col>
                  <!-- 删除按钮 -->
                  <v-col cols="auto" class="d-flex justify-center align-center" style="delete-icon">
                    <v-icon @click="removeObject(index)">mdi-trash-can</v-icon>
                  </v-col>
                </v-row>
              </v-card>
            </v-col>
          </v-row>

          <!-- 添加评分对象按钮 -->
          <v-row>
            <v-col cols="12">
              <v-btn @click="openObjectDialog" block class="text-center">
                继续添加
              </v-btn>
            </v-col>
          </v-row>
        </v-container>

        <!-- 提交按钮 -->
        <v-row>
          <v-col cols="6">
            <v-btn @click="goBack" color="error" block>
              取消创建
            </v-btn>
          </v-col>
          <v-col cols="6">
            <v-btn @click="submitForm" color="success" block :disabled="!valid || objects.length < 3">
              提交创建
            </v-btn>
          </v-col>
        </v-row>
      </v-form>

      <!-- 评分对象对话框 -->
      <v-dialog v-model="dialog" max-width="500px">
        <v-card>
          <v-card-title class="headline">添加评分对象</v-card-title>
          <v-card-text>
            <v-text-field
              v-model="newObject.name"
              label="请输入对象名称"
              hint="最多 24 字"
              max-length="24"
              outlined
              required
            ></v-text-field>
            <v-file-input
              v-model="newObject.cover"
              label="添加对象封面"
              accept="image/*"
              prepend-icon="mdi-camera"
              outlined
            ></v-file-input>
            <v-textarea v-model="newObject.description" label="简介" outlined required rows="4"></v-textarea>
          </v-card-text>
          <v-card-actions>
            <v-btn @click="dialog = false" color="secondary">取消</v-btn>
            <v-btn @click="addObject" color="primary">添加对象</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-card>
  </v-container>
</template>

<script>
import api from "@/api/zone.js";
import { alert } from "@/store/alert.ts";

export default {
  data() {
    return {
      formData: new FormData(),
      valid: false, // 表单验证状态
      coverImage: null, // 封面图片
      zoneTitle: "", // 评分主题
      zoneIntroduction: "", // 评分简介
      objects: [], // 存储评分对象
      dialog: false, // 控制对话框显示
      newObject: { // 新评分对象
        name: "",
        cover: null,
        description: "",
      },
    };
  },
  methods: {
    // 打开评分对象对话框
    openObjectDialog() {
      this.dialog = true;
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      this.formData.append("graphic", file);
    },
    // 添加评分对象到列表
    addObject() {
      if (!(this.newObject.name && this.newObject.cover && this.newObject.description)) {
        alert("请补全对象信息", "error");
        return;
      }
      for (let object of this.objects) {
        if (object.name == this.newObject.name) {
          alert("对象重名", "error");
          return;
        }
      }
      alert("对象添加成功", "success");
      this.objects.push({ ...this.newObject });
      this.resetObjectForm();
      this.dialog = false;
    },
    getImageUrl(cover) {
      return URL.createObjectURL(cover);
    },
    // 重置评分对象表单
    resetObjectForm() {
      this.newObject = { name: "", cover: null, description: "" };
    },
    // 提交表单
    submitForm() {
      if (this.formData.get("graphic") == null || !this.zoneTitle || !this.zoneIntroduction) {
        alert("请补全专区信息", "error");
        return;
      }
      if (this.objects.length < 3) {
        alert("评分对象不得少于 3 个", "error");
        return;
      }
      // 提交逻辑
      this.formData.append("titie", this.zoneTitle);
      this.formData.append("introduction", this.zoneIntroduction);

      const objects = [];
      this.objects.forEach((object) => {
        objects.push({ name: object.name, description: object.description });
        this.formData.append(`files[${object.name}]`, object.cover);
      });
      this.formData.append("objects", JSON.stringify(objects));

      api.createZoneApi(this.formData).then((res) => {
        if (res.code === 200) {
          alert("专区创建成功", "success");
          this.$router.push("/zones"); // 跳转到博客列表页
        } else {
          alert(res.message, "error");
        }
      });
    },
    // 删除评分对象
    removeObject(index) {
      this.objects.splice(index, 1);
      alert("删除对象成功", "success");
    },
    // 返回上一页
    goBack() {
      this.$router.go(-1);
    },
  },
};
</script>

<style scoped>
.v-btn {
  margin-top: 20px;
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

.delete-icon {
  cursor: pointer;
}
</style>
