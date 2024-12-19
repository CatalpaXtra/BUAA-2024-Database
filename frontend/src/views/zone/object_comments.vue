<template>
  <div class="comments-section">
    <div class="d-flex align-center comments-header mb-5">
      <h2 class="mb-0 d-flex align-center comments-title">
        评论
        <span class="comment-count">({{ filteredComments.length }})</span>
      </h2>

      <div class="filter-options d-flex align-center">
        <v-btn
          text
          class="filter-btn no-border no-shadow"
          :class="{ active: filterOption === 'popular' }"
          @click="setFilter('popular')"
        >
          最热
        </v-btn>
        <span class="divider">|</span>
        <v-btn
          text
          class="filter-btn no-border no-shadow"
          :class="{ active: filterOption === 'latest' }"
          @click="setFilter('latest')"
        >
          最新
        </v-btn>
      </div>
    </div>

    <!-- 评论输入框 -->
    <div class="comment-input d-flex align-start">
      <!-- 左侧用户头像 -->
      <v-avatar size="48" class="me-3">
        <img :src="'http://localhost:9090/upload/'+currentUser.avatar" alt="User Avatar" class="avatar-image"/>
      </v-avatar>

      <!-- 输入框和功能区 -->
      <div class="flex-grow-1">
        <v-textarea
          v-model="comment"
          placeholder="I mean, man, what can U say"
          outlined
          rows="1"
          auto-grow
          class="mb-3"
          @focus="showOptions = true"
          @blur="hideOptionsWithDelay"
        ></v-textarea>

        <!-- 功能按钮区域 -->
        <div v-if="showOptions" class="action-buttons d-flex align-center" style="margin-bottom: 30px;">
          
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="submitComment">
            <span>发布</span>
          </v-btn>
        </div>
      </div>
    </div>


    <!-- 评论列表 -->
    <v-card
      v-if="filteredComments.length === 0"
      class="py-4"
      color="grey lighten-3"
      elevation="0"
    >
      <v-card-text>你知道的，评论是一件很有意思的事</v-card-text>
    </v-card>

    <Comment
      v-for="comment in filteredComments"
      :key="comment.id"
      :comment="comment"
    />
  </div>
</template>

<script>
import Comment from "@/components/ObjComment.vue";
import api from '@/api/zone.js'
import router from "@/router";

export default {
  name: "object_comments",
  components: { 
    Comment, 
  },
  props: {
    comments: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      filterOption: "latest",
      defaultAvatar: "kobe.png",
      comment: "", // 评论内容
      showOptions: false, // 是否显示功能按钮
      currentUser: {
        avatar: "kobe.png", // 用户头像
      },
    };
  },
  created() {
    const token = localStorage.getItem('jwt_token');
    if (token) {
      this.currentUser.avatar = localStorage.getItem('avatar')
      this.currentUser.username = localStorage.getItem('username')
    }
  },
  computed: {
    filteredComments() {
      // 检查 `comments` 数据
      if (this.filterOption === "popular") {
        return [...this.comments].sort((a, b) => b.likes - a.likes);
      }
      return [...this.comments].sort((a, b) => new Date(b.pub_time) - new Date(a.pub_time));
    },
  },
  methods: {
    setFilter(option) {
      this.filterOption = option;
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString(undefined, {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    },
    insertImage() {
      // 插入图片逻辑
      console.log("Inserting image...");
    },
    mentionUser() {
      // @提及用户逻辑
      console.log("Mentioning user...");
    },
    submitComment() {
      // 提交评论逻辑
      const objectId = this.$route.query.object_id;
      const data = {
        "object_id": objectId,
        "content": this.comment,
      }
      api.pubCmtApi(data).then(res => {
        if (res.code === 200) {
          router.go(0)
        }
      }).catch(error => {
        console.log(error)
      })
      this.comment = ""; // 清空输入框
      this.showOptions = false; // 隐藏功能按钮
    },
    hideOptionsWithDelay() {
      // 延迟隐藏功能按钮，避免失去焦点后立刻隐藏
      setTimeout(() => {
        if (!this.comment) this.showOptions = false;
      }, 50);
    },
  },
};
</script>

<style scoped>
.comments-title {
  max-width: 600px;
  margin-right: 40px;
}

.comment-count {
  font-size: 1rem; /* 可以根据需求调整字体大小 */
  margin-left: 5px; /* 给评论数和标题增加适当的间距 */
  vertical-align: baseline; /* 与标题底部对齐 */
  color: #757575;
}

.filter-options {
  align-items: center;
}

:root {
  --default-color-light: #333; /* 浅色模式下默认颜色（黑色） */
  --default-color-dark: #fff; /* 深夜模式下默认颜色（白色） */
  --hover-color: #1976d2; /* 鼠标悬停时的颜色 */
}

.filter-btn {
  font-size: 1rem; /* 按钮字体大小 */
  text-transform: none;
  padding: 0;
  transition: color 0.3s ease;
  color: #757575;
  border: none !important; /* 强制移除边框 */
  box-shadow: none !important; /* 强制移除阴影 */
  background-color: transparent !important; /* 强制移除背景色，好像没用 */
}

.filter-btn:hover {
  color: #1976d2; /* 鼠标悬停时改变颜色 */
  background-color: transparent !important; /* 强制移除背景色，好像没用 */

}

.filter-btn.active:hover {
  color: #1976d2; /* 鼠标悬停时的颜色优先 */
}

.filter-btn.active {
  font-weight: bold; /* 激活时加粗文本 */
  color: var(--default-color-dark); /* 激活时使用相反的默认颜色 */
}

.divider {
  font-size: 1rem;
  margin: 0 5px;
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 保持比例并裁剪多余部分 */
  border-radius: 50%; /* 确保是圆形 */
}
</style>