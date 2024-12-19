<template>
  <div class="main-layout" :class="{ 'hide-sidebar': isLoginPage }">
    <Navigator v-show="!isLoginPage" />
    <GlobalAlert />
    <div class="content-area">
      <router-view />
    </div>
  </div>
</template>

<script>
import GlobalAlert from "./GlobalAlert.vue";
import Navigator from "./Navigator.vue";

export default {
  name: "Layout",
  components: {
    Navigator,
    GlobalAlert
  },
  computed: {
    isLoginPage() {
      return this.$route.path === "/login";
    },
  },
};
</script>

<style scoped>
.main-layout {
  display: flex;
  height: 100vh;
}

/* Hide the sidebar if the login page is active */
.hide-sidebar Navigator {
  display: none;
}

.content-area {
  flex: 1;
  overflow: auto;
}
</style>
