<template>
  <v-container class="page-container" color="grey lighten-4">
    <v-card class="modify-profile-container" title="修改资料" outlined>
      <v-container fluid>
        <!-- 用户信息编辑表单 -->
        <v-form ref="profileForm" v-model="isFormValid">
          <v-row>
            <!-- 可编辑信息字段 -->
            <v-col cols="12" md="6" v-for="(value, key) in userInfoEditable" :key="key">
              
              <!-- 邮箱设置为不可编辑 -->
              <v-text-field
                v-if="key === '邮箱'"
                v-model="userEditable[key]"
                :label="key"
                outlined
                disabled
              ></v-text-field>
              <!-- 性别选择下拉框 -->
              <v-select
                v-else-if="key === '性别'"
                v-model="userEditable[key]"
                :items="['男', '女', '保密']"
                :label="key"
                outlined
              ></v-select>
              <!-- 年龄选择，带步进按钮 -->
              <v-text-field
                v-else-if="key === '年龄'"
                v-model="userEditable[key]"
                :label="key"
                outlined
                :rules="[v => /^\d+$/.test(v) || '请输入有效数字']"
                type="number"
              >
              </v-text-field>
              <v-text-field
                v-if="key !== '性别' && key !== '年龄' && key !== '邮箱'"
                v-model="userEditable[key]"
                :label="key"
                outlined
                :rules="[v => !!v || '此字段不能为空']"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-form>

        <!-- 按钮操作 -->
        <v-row>
          <v-col cols="12" md="6">
            <v-btn
              class="save-btn"
              color="primary"
              block
              :disabled="!isFormValid"
              @click="saveProfile"
            >
              保存修改
            </v-btn>
          </v-col>
          <v-col cols="12" md="6">
            <v-btn
              class="return-btn"
              color="secondary"
              block
              @click="returnToAccount"
            >
              返回个人中心
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-card>
  </v-container>
</template>

<script>
import api from '@/api/user.js'
import { alert } from '@/store/alert.ts'
import ChildComponent from '@/components/Navigator.vue';

let user_id = -1;

export default {
  data() {
    return {
      // 可编辑的用户信息
      userEditable: {
        昵称: "",
        邮箱: "",
        年龄: "",
        性别: "",
        专业: "",
        年级: "",
      },
      isFormValid: true,
    };
  },
  computed: {
    // 定义可编辑信息的键值对
    userInfoEditable() {
      return {
        昵称: "请输入昵称",
        邮箱: "请输入邮箱",
        年龄: "请输入年龄",
        性别: "请选择性别",
        专业: "请输入专业",
        年级: "请输入年级",
      };
    },
  },
  created() {
    api.fetchUserData().then(user => {
      user_id = user.id
      this.userEditable.昵称 = user.name
      this.userEditable.邮箱 = user.mail
      this.userEditable.年龄 = user.age
      this.userEditable.性别 = user.gender
      this.userEditable.专业 = user.major
      this.userEditable.年级 = user.grade
    });
  },
  methods: {
    // 保存用户资料
    saveProfile() {
      if (this.isFormValid) {
        const data = {
          ...this.userEditable,
          'user_id': user_id,
        }
        api.modifyInfoApi(data).then(res => {
          if (res.code === 200) {
            alert('用户资料已保存', 'success');
            localStorage.setItem('username', res.username);
          }
          else {
            alert(res.message, 'error');
          }
        }).catch(error => {
          console.log(error)
        })
        // this.$router.push("/account");
      }
    },
    // 返回到个人中心
    returnToAccount() {
      this.$router.push("/account");
    },
    // 步进调整年龄
    stepAge(step) {
      const currentAge = parseInt(this.userEditable["年龄"], 10) || 0;
      const newAge = Math.max(0, currentAge + step); // 年龄最小为 0
      this.userEditable["年龄"] = newAge.toString();
    },
  },
};
</script>

<style scoped>
/* 页面容器 */
.page-container {
  position: relative;
  width: 100%;
  height: 100%;
}

/* 调整 v-card 的样式 */
.modify-profile-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 16px;
  width: 80%;
}

/* 按钮样式 */
.save-btn {
  margin-top: 16px;
}

.return-btn {
  margin-top: 16px;
  background-color: #f5f5f5;
  color: black;
}

/* 添加步进按钮样式 */
.with-stepper {
  display: flex;
  align-items: center;
}
</style>
