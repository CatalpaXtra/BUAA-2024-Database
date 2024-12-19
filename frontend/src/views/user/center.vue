<template>
  <v-container class="page-container"
    color="grey lighten-4"
  >
    <v-skeleton-loader
      v-if="!user"
      :loading="!user"
      class="user-profile-skeleton"
      height="300px"
      type="card"
    >
      <!-- 骨架屏标题部分 -->
      <template #header>
        <v-skeleton-loader
          class="skeleton-header d-flex align-center"
          :height="'40px'"
          :width="'70%'"
        />
      </template>

      <!-- 骨架屏内容部分 -->
      <template #body>
        <v-row>
          <!-- 头像骨架 -->
          <v-col cols="12" md="4" class="d-flex justify-center">
            <v-skeleton-loader
              class="skeleton-avatar"
              type="image"
              :height="'150px'"
              :width="'150px'"
              style="border-radius: 50%"
            />
          </v-col>

          <!-- 信息骨架 -->
          <v-col cols="12" md="8">
            <v-skeleton-loader
              v-for="n in 4"
              :key="n"
              class="skeleton-info"
              :height="'20px'"
              :width="`${70 + Math.random() * 20}%`"
              style="margin-bottom: 16px"
            />
          </v-col>
        </v-row>

        <!-- 按钮骨架 -->
        <v-row>
          <v-col cols="12" md="6">
            <v-skeleton-loader
              class="skeleton-button"
              :height="'40px'"
              :width="'100%'"
              style="border-radius: 4px"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-skeleton-loader
              class="skeleton-button"
              :height="'40px'"
              :width="'100%'"
              style="border-radius: 4px"
            />
          </v-col>
        </v-row>
      </template>
    </v-skeleton-loader>

    <v-card v-else 
      class="user-profile-container"
      outlined
    >
      <v-container fluid>
        <v-row>
          <!-- 用户头像 -->
          <v-col cols="12" md="6" class="avatar-container">
            <v-img
              :src="'http://localhost:9090/upload/'+this.user.avatar"
              class="circle-image"
              width="200"
              height="200"
            >
            </v-img>
          </v-col>

          <!-- 用户信息 -->
          <v-col cols="12" md="6">
            <v-list dense>
              <v-list-item v-for="(value, key) in userInfoDisplay" :key="key">
                <v-list-item-title>
                  <v-icon class="mr-2">{{ getIcon(key) }}</v-icon>
                  {{ key }}:
                </v-list-item-title>
                <v-list-item-subtitle>{{ value }}</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-col>
        </v-row>

        <!-- 底部信息 -->
        <v-footer class="footer-info">
          上次登录时间: {{ formatDate(user.logintime) || '未登录过' }}
        </v-footer>
      </v-container>
    </v-card>
  </v-container>
</template>

<script>
import api from '@/api/user.js'

export default {
  name: "center",
  data() {
    return {
      user: null,
    };
  },
  computed: {
    // 用户信息展示
    userInfoDisplay() {
      return {
        昵称: this.user.name,
        邮箱: this.user.mail || "未设置",
        年龄: this.user.age || "未设置",
        性别: this.user.gender || "未设置",
        专业: this.user.major || "未设置",
        年级: this.user.grade || "未设置",
      };
    },
  },
  created() {
    const userId = this.$route.query.user_id;
    api.fetchUserDataById(userId).then(user => {
      this.user = user
    });
  },
  methods: {
    getIcon(key) {
      const icons = {
        昵称: "mdi-account",
        邮箱: "mdi-email",
        年龄: "mdi-calendar",
        性别: "mdi-gender-male-female",
        专业: "mdi-school",
        年级: "mdi-clipboard-text",
      };
      return icons[key] || "mdi-help-circle";
    },
    formatDate(dateString) {
      if (!dateString) return null;
      const date = new Date(dateString);
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric',
      });
    },
  },
};
</script>

<style scoped>
.avatar-container {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 将头像设为圆形 */
.circle-image {
  border-radius: 50%;
  object-fit: cover;
  overflow: hidden;
}

/* 覆盖文字样式 */
.overlay-text {
  position: absolute;
  bottom: 0; /* 固定到图片的底部 */
  width: 100%; /* 覆盖图片宽度 */
  background-color: rgba(0, 0, 0, 0.5); /* 半透明背景 */
  color: white;
  text-align: center;
  padding: 10px;
  font-size: 16px;
}

/* 隐藏元素 */
.d-none {
  display: none;
}

/* icon 大小 */
.v-icon {
  font-size: 15px; 
  vertical-align: middle;
}

/* 调整 v-card 长宽 */
.page-container {
  position: relative;
  width: 100%;
  height: 100%;
}

/* 用户信息卡片，将 v-card 置于页面中心 */
.user-profile-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 16px;
  width: 80%;
}

.divider {
  margin: 16px 0;
}

.footer-info {
  text-align: center;
  font-size: 0.8rem;
  color: gray;
  margin-top: 16px;
}
</style>
