<template>
  <v-container class="page-container" color="grey lighten-4">
    <v-card class="modify-password-container" title="修改密码" outlined>
      <v-container fluid>
        <!-- 密码修改表单 -->
        <v-form ref="passwordForm" v-model="isFormValid">
          <v-row>
            <!-- 旧密码 -->
            <v-col cols="12">
              <v-text-field
                v-model="passwords.oldPassword"
                :type="showPassword.old ? 'text' : 'password'"
                label="旧密码"
                outlined
                :append-icon="showPassword.old ? 'mdi-eye-off' : 'mdi-eye'"
                @click:append="togglePasswordVisibility('old')"
                :rules="[v => !!v || '旧密码不能为空']"
              ></v-text-field>
            </v-col>

            <!-- 新密码 -->
            <v-col cols="12">
              <v-text-field
                v-model="passwords.newPassword"
                :type="showPassword.new ? 'text' : 'password'"
                label="新密码"
                outlined
                :append-icon="showPassword.new ? 'mdi-eye-off' : 'mdi-eye'"
                @click:append="togglePasswordVisibility('new')"
                :rules="[v => !!v || '新密码不能为空']"
              ></v-text-field>
            </v-col>

            <!-- 确认新密码 -->
            <v-col cols="12">
              <v-text-field
                ref="confirmPasswordField"
                v-model="passwords.confirmPassword"
                :type="showPassword.confirm ? 'text' : 'password'"
                label="确认新密码"
                outlined
                :append-icon="showPassword.confirm ? 'mdi-eye-off' : 'mdi-eye'"
                @click:append="togglePasswordVisibility('confirm')"
                :rules="[v => !v || v === passwords.newPassword || '两次密码输入不一致']"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-form>

        <!-- 按钮操作 -->
        <v-row>
          <!-- 保存密码 -->
          <v-col cols="12" md="6">
            <v-btn
              class="save-btn"
              color="primary"
              block
              :disabled="!isFormValid"
              @click="savePassword"
            >
              保存新密码
            </v-btn>
          </v-col>
          <!-- 返回按钮 -->
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
import { reactive, ref, watch } from "vue";
import { alert } from '@/store/alert.ts'

let user_id = -1;

export default {
  setup() {
    const passwords = reactive({
      oldPassword: "", // 旧密码
      newPassword: "", // 新密码
      confirmPassword: "" // 确认新密码
    });

    const confirmPasswordField = ref(null);

    // 监听新密码的变化
    watch(() => passwords.newPassword, () => {
      // 手动触发确认密码字段的验证
      if (confirmPasswordField.value) {
        confirmPasswordField.value.validate();
      }
    });

    return {
      passwords,
      confirmPasswordField
    };
  },
  data() {
    return {
      // passwords: {
      //   oldPassword: "", // 旧密码
      //   newPassword: "", // 新密码
      //   confirmPassword: "", // 确认新密码
      // },
      showPassword: {
        old: false, // 是否显示旧密码
        new: false, // 是否显示新密码
        confirm: false, // 是否显示确认新密码
      },
      isFormValid: false, // 表单验证状态
      snackbar: {
        visible: false, // 控制 Snackbar 的显示与隐藏
        message: "", // 提示消息内容
      },
    };
  },
  created() {
    api.fetchUserData().then(user => {
      user_id = user.id
    });
  },
  methods: {
    // 切换密码显示状态
    togglePasswordVisibility(field) {
      this.showPassword[field] = !this.showPassword[field];
    },
    // 保存新密码
    savePassword() {
      if (this.isFormValid) {
        const data = {
          ...this.passwords,
          'user_id': user_id,
        }
        api.modifyPaswApi(data).then(res => {
          if (res.code === 200) {
            console.log("新密码已保存:", data);
            alert('新密码已保存', 'success');
            // this.$router.push("/account");
          }
          else {
            alert(res.message, 'error');
            console.log(res.message)
          }
        }).catch(error => {
          console.log(error)
        })
      } else {
        // this.snackbar = {
        //   visible: true,
        //   message: "请检查表单是否填写正确",
        // };
      }
    },
    // 返回个人中心
    returnToAccount() {
      this.$router.push("/account");
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
.modify-password-container {
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
</style>
