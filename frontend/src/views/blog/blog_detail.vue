<template>
  <v-container class="blog-detail">
    <!-- 在数据加载时显示骨架屏 -->
    <v-skeleton-loader 
      v-if="!blog" 
      :loading="!blog"
      class="blog-card-skeleton"
      :type="['card', 'image', 'text', 'avatar']"
    >
      <template #default>
        <!-- 骨架屏卡片 -->
        <v-card>
          <!-- 分类占位 -->
          <div class="d-flex mb-2">
            <v-skeleton-loader class="chip-placeholder" v-for="n in 3" :key="n" :width="'80px'" :height="'32px'" />
          </div>
          <!-- 标题占位 -->
          <v-skeleton-loader :height="'32px'" :width="'70%'" class="mb-4" />
          <!-- 用户信息占位 -->
          <div class="d-flex align-center mb-4">
            <v-skeleton-loader :type="'avatar'" :width="'40px'" :height="'40px'" class="mr-2" />
            <v-skeleton-loader :height="'20px'" :width="'120px'" />
          </div>
          <!-- 内容占位 -->
          <v-skeleton-loader :height="'16px'" :width="'90%'" class="mb-2" />
          <v-skeleton-loader :height="'16px'" :width="'85%'" class="mb-2" />
          <v-skeleton-loader :height="'16px'" :width="'80%'" />
          <!-- 图片占位 -->
          <v-skeleton-loader :type="'image'" :height="'200px'" class="mt-4" />
        </v-card>
      </template>
    </v-skeleton-loader>

    <!-- 博客内容 -->
    <v-card v-else elevation="2" class="blog-card mb-6">
    <v-card-title>
      <div>
        <!-- 帖子分类 -->
        <div class="category-list mb-2">
          <v-chip
            v-for="category in blog.categories"
            :key="category.id"
            class="mr-2"
            outlined
            color="primary"
          >
            {{ category.name }}
          </v-chip>
        </div>
        <!-- 帖子标题 -->
        <h1 class="title">{{ blog.title }}</h1>
        <!-- 发布信息 -->
        <v-row>
          <v-col cols="auto">
            <v-avatar size="40">
              <img :src="'http://localhost:9090/upload/'+blog.author.avatar" :alt="blog.author.username" class="avatar-image"/>
            </v-avatar>
          </v-col>
          <v-col>
            <span class="content">
              <strong>{{ blog.author.username }}</strong> 
            </span>
          </v-col>
        </v-row>
      </div>
    </v-card-title>
    <v-divider></v-divider>
    <v-card-text class="pt-4">
      <div class="content mb-4 ml-2">
        <div v-html="markdown"></div>
      </div>
       <v-img 
        :src="'http://localhost:9090/upload/'+blog.graphic"
        aspect-ratio="16/9"
        max-height="400px"
        class="mb-6 small-image"
        v-if="blog.graphic !== 'kobe.png'"
      ></v-img>
      <span class="date">发布于 {{ formatDate(blog.pub_time) }}</span>
    </v-card-text>
    <!-- 赞同和不赞同按钮 -->
    <v-divider></v-divider>
    <v-card-actions>
      <!-- 赞同按钮 -->
      <v-btn
        class="vote-button"
        :color="isLiked ? 'blue' : 'grey'"
        outlined
        :variant="isLiked ? 'tonal' : 'text'"
        @click="handleLike(blog)"
      >
        <v-icon left>mdi-chevron-up</v-icon>
        {{isLiked ? '已赞同' : '赞同'}} {{ blog.likes }}
      </v-btn>

      <!-- 不赞同按钮 -->
      <v-btn
        class="vote-button"
        :color="isDisliked ? 'blue' : 'grey'"
        outlined
        :variant="isDisliked ? 'tonal' : 'text'"
        @click="handleDislike(blog)"
      >
        <v-icon left>mdi-chevron-down</v-icon>
        {{isDisliked ? '已反对' : '反对'}} {{ blog.dislikes }}
      </v-btn>
      
      <!-- 收藏按钮 -->
      <v-btn
        class="vote-button"
        :color="isCollected ? 'orange' : 'grey'"
        outlined
        :variant="isCollected ? 'tonal' : 'text'"
        @click="handleCollect()"
      >
        <v-icon left>mdi-star</v-icon>
        {{isCollected ? '取消收藏' : '收藏'}}  {{ blog.collects }}
      </v-btn>

      <!-- 删除按钮 -->
      <v-btn @click="deleteBlog(blog.id)" v-if="blog.privilege">
        <v-icon >mdi-trash-can</v-icon>
        删除
      </v-btn>

      <!-- 编辑按钮 -->
      <v-btn @click="openBlogDialog" v-if="blog.privilege">
        <v-icon >mdi-pencil</v-icon>
        编辑
      </v-btn>
    </v-card-actions>
  </v-card>

    <!-- 编辑博客对话框 -->
    <v-dialog v-model="showDialog" max-width="600px">
      <v-card>
        <v-card-title>编辑博客</v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid" lazy-validation>
            <v-text-field
              v-model="editedBlog.title"
              label="博客标题"
              required
            ></v-text-field>
            <v-textarea
              v-model="editedBlog.content"
              label="博客内容"
              required
            ></v-textarea>
            <v-file-input
              v-model="editedBlog.graphic"
              label="博客图片"
              accept="image/*"
            ></v-file-input>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="showDialog = false">取消</v-btn>
          <v-btn @click="save" color="primary">保存</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-divider></v-divider>

    <!-- 评论区，实现在 blog_comment.vue -->
    <blog_comments
      :comments="blog?.comments || []" 
      @update-comments="updateComments"
    />
  </v-container>
</template>

<script>
import blog_comments from "@/views/blog/blog_comments.vue";
import api from '@/api/blog.js'
import { marked } from 'marked'
import { alert } from '@/store/alert.ts'

export default {
  name: "blog_detail",
  components: { blog_comments },
  data() {
    return {
      userid: 4,
      isAdmin: false,
      markdown: "",
      blog: null,
      currentUser: { id: 4, username: "CurrentUser", avatar: "kobe.png" },
      defaultAvatar: "kobe.png",
      isLiked: false, // 控制赞同按钮的状态
      isDisliked: false, // 控制不赞同按钮的状态
      isCollected: false,
      showDialog: false,
      valid: false,
      editedBlog: {
        title: "",
        content: "",
        graphic: null,
      },
    };
  },
  created() {
    const blogId = this.$route.query.blog_id;
    if (blogId) {
      api.acquireBlogDetailApi(blogId).then(data => {
        this.blog = data.blog
        this.isLiked = data.blog.liked
        this.isDisliked = data.blog.disliked
        this.isCollected = data.blog.collected
      });
    }
  },
  watch: {
    blog(newBlog) {
      if (newBlog) {
        this.markdown = marked(newBlog.content);
      }
    }
  },
  methods: {
    openBlogDialog() {
      this.showDialog = true;
      this.editedBlog = { ...this.blog };
    },
    save() {
      const formData = new FormData();
      formData.append('graphic', this.editedBlog.graphic);
      formData.append('title', this.editedBlog.title);
      formData.append('content', this.editedBlog.content);

      // 提交编辑后的数据到后端
      const blogId = this.$route.query.blog_id;
      api.updateBlogApi(this.editedBlog, blogId).then(response => {
        if (response.code === 200) {
          // 更新当前页面对象信息
          this.blog = { ...this.blog, ...this.editedBlog };
          if (response.graphic !== "") {
            this.blog.graphic = response.graphic
          }

          // 显示成功提示
          alert('修改成功', 'success');
          
          // 关闭对话框
          this.showDialog = false;
        }
        else {
          alert(response.message, 'error');
        }
      })
      .catch(error => {
        alert('修改失败，请重试', 'error');
      });
    },
    deleteBlog(blogId) {
      api.deleteBlogApi(blogId).then(data => {
        // 刷新视图
        this.$router.push('/blogs');
      });
    },
    handleCollect() {
      const blogId = this.$route.query.blog_id;
      api.collectBlogApi(blogId).then(res => {
        this.isCollected = res.created
        if (res.created) {
          this.blog.collects += 1
        } else {
          this.blog.collects -= 1
        }
      }).catch(error => {
        console.log(error)
      })
    },
    handleLike() {
      const blogId = this.$route.query.blog_id;
      api.likeBlogApi(blogId).then(res => {
        this.isLiked = res.created
        if (res.created) {
          this.blog.likes += 1
        } else {
          this.blog.likes -= 1
        }
      }).catch(error => {
        console.log(error)
      })
    },
    handleDislike() {
      const blogId = this.$route.query.blog_id;
      api.dislikeBlogApi(blogId).then(res => {
        this.isDisliked = res.created
        if (res.created) {
          this.blog.dislikes += 1
        } else {
          this.blog.dislikes -= 1
        }
      }).catch(error => {
        console.log(error)
      })
    },
    updateComments(updatedComments) {
      this.blog.comments = updatedComments;
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
  },
};
</script>

<style scoped>
.v-chip {
  margin-bottom: 10px;
}

.category-list {
  display: flex;
  flex-wrap: wrap;
}

.v-card {
  box-shadow: none !important;
}

.v-divider {
  margin: 16px 0;
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 保持比例并裁剪多余部分 */
  border-radius: 50%; /* 确保是圆形 */
}

.vote-button {
  display: inline-flex;
  padding: 8px 16px;
}

.vote-button .v-btn__content {
  display: inline-flex;
}

.vote-button .v-icon {
  font-size: 18px; /* 控制图标大小 */
  margin-right: 8px; /* 图标和文本之间的间隔 */
}

/* 自定义字体大小和样式 */
.title {
  font-size: 32px; /* 调整标题大小 */
  font-weight: bold; /* 标题加粗 */
  margin-bottom: 16px;
}

.content {
  font-size: 18px; /* 正文稍大一点 */
  line-height: 1.6; /* 行高调整 */
}

.date {
  font-size: 14px; /* 发布日期小一些 */
  color: #757575; /* 灰色 */
}

/* 图片样式：控制图片的大小 */
.small-image {
  max-width: 80%; /* 控制图片最大宽度 */
  margin: 0 auto;
  display: block; /* 居中显示 */
}

/* 骨架屏整体样式 */
.blog-card-skeleton {
  padding: 16px;
}

/* 自定义骨架占位元素的样式 */
.chip-placeholder {
  border-radius: 16px;
  margin-right: 8px;
}
</style>
