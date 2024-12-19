<template>
  <v-card>
    <v-layout>
      <v-navigation-drawer
        v-model="drawer"
        :rail="rail"
        permanent
        @click="rail = false"
      >
        <!-- 用户信息部分 -->
        <v-skeleton-loader
          v-if="!currentUser"
          class="mx-3"
          :loading="!currentUser"
          :height="'50px'"
          :animation="'wave'"
        >
          <v-list-item>
            <v-avatar class="skeleton-avatar"></v-avatar>
            <v-list-item-title class="skeleton-title"></v-list-item-title>
          </v-list-item>
        </v-skeleton-loader>

        <!-- 数据加载后显示用户信息 -->
        <v-list-item v-else
          :prepend-avatar="'http://localhost:9090/upload/'+currentUser.avatar"
          :title= "currentUser.username"
          nav
        >
          <template v-slot:append>
            <v-btn
              icon="mdi-chevron-left"
              variant="text"
              @click.stop="rail = !rail"
            ></v-btn>
          </template>
        </v-list-item>

        <v-divider></v-divider>

        <!-- 导航菜单 -->
        <v-list density="compact" nav>
          <router-link to="/home" custom v-slot="{ navigate, href }">
            <v-list-item prepend-icon="mdi-home-city" title="首页" value="home" :href="href" />
          </router-link>

          <!-- 讨论区菜单 -->
          <v-list-group prepend-icon="mdi-account-group-outline" title="讨论区" value="topics">
            <template v-slot:activator="{ props }">
              <v-list-item v-bind="props" title="讨论区"></v-list-item>
            </template>
            <router-link to="/blogs" custom v-slot="{ navigate, href }">
              <v-list-item title="讨论区首页" :href="href" @click="navigate" />
            </router-link>
            <router-link to="/blogs/create_blog" custom v-slot="{ navigate, href }">
              <v-list-item title="发布帖子" :href="href" @click="navigate" />
            </router-link>
            <router-link to="/account/folder/1" custom v-slot="{ navigate, href }">
              <v-list-item title="藏帖锦集" :href="href" @click="navigate" />
            </router-link>
          </v-list-group>

          <!-- 专区菜单 -->
          <v-list-group prepend-icon="mdi-trophy-outline" title="专区" value="zones">
            <template v-slot:activator="{ props }">
              <v-list-item v-bind="props" title="专区"></v-list-item>
            </template>
            <router-link to="/zones" custom v-slot="{ navigate, href }">
              <v-list-item title="专区首页" :href="href" @click="navigate" />
            </router-link>
            <router-link to="/zones/create_zone" custom v-slot="{ navigate, href }">
              <v-list-item title="创建专区" :href="href" @click="navigate" />
            </router-link>
            <router-link to="/account/folder/2" custom v-slot="{ navigate, href }">
              <v-list-item title="焦点专区" :href="href" @click="navigate" />
            </router-link>
          </v-list-group>

          <!-- 个人账户菜单 -->
          <v-list-group prepend-icon="mdi-account" title="我的" value="account">
            <template v-slot:activator="{ props }">
              <v-list-item v-bind="props" title="我的"></v-list-item>
            </template>
            <router-link to="/account" custom v-slot="{ navigate, href }">
              <v-list-item title="个人中心" :href="href" @click="navigate" />
            </router-link>
            <router-link to="/account/folder/3" custom v-slot="{ navigate, href }">
              <v-list-item title="我的收藏" :href="href" @click="navigate" />
            </router-link>
          </v-list-group>

        </v-list>

        <!-- 底部操作 -->
        <template v-slot:append>
          <!-- 切换主题按钮 -->
          <div class="pa-2">
            <v-btn block @click="toggleTheme">
              <v-icon left>{{ theme === 'light' ? 'mdi-weather-sunny' : 'mdi-weather-night' }}</v-icon>
              <span v-if="!rail">{{ theme === 'light' ? 'Light Mode' : 'Dark Mode' }}</span>
            </v-btn>
          </div>

          <!-- 登出按钮 -->
          <div class="pa-2">
            <v-btn block @click="logout">
              <v-icon left>mdi-logout</v-icon>
              <span v-if="!rail">Logout</span>
            </v-btn>
          </div>
        </template>
      </v-navigation-drawer>

      <!-- 主内容区 -->
      <v-main style="height: 100vh"></v-main>
    </v-layout>
  </v-card>
</template>

<script>
import { theme, toggleTheme } from '@/composables/theme';

export default {
  name: 'Navigator',
  setup() {
    return {
      theme,
      toggleTheme,
      currentUser: {
        avatar: "kobe.png",
        username: "请先登录"
      },
    };
  },
  data() {
    return {
      drawer: true,
      rail: JSON.parse(localStorage.getItem('rail')) ?? true, // 从 localStorage 获取状态
    };
  },
  created() {
    const token = localStorage.getItem('jwt_token');
    if (token) {
      this.currentUser.avatar = localStorage.getItem('avatar')
      this.currentUser.username = localStorage.getItem('username')
    }
  },
  watch: {
    // 监听 rail 的变化，将其保存到 localStorage
    rail(val) {
      localStorage.setItem('rail', JSON.stringify(val));
    },
  },
  methods: {
    // 登出并重定向到登录页
    logout() {
      localStorage.removeItem('jwt_token');
      localStorage.removeItem('avatar');
      localStorage.removeItem('username');
      this.$router.push('/login');
    },
  },
};
</script>

<style scoped>
/* 可在此处添加样式 */
.skeleton-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.skeleton-title {
  width: 120px;
  height: 16px;
  margin-left: 16px;
  background: linear-gradient(90deg, #f0f0f0, #e0e0e0, #f0f0f0);
  border-radius: 4px;
}
</style>
