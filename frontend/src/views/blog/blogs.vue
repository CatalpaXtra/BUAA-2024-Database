<template>
  <v-container color="grey lighten-4" >
    <!-- 搜索框 -->
    <v-row justify="center" class="mb-4">
      <v-text-field
        v-model="searchQuery"
        placeholder="搜索帖子标题和内容"
        outlined
        clearable
        @input="filterBlogs"
        class="flex-grow-1"
      >
        <template v-slot:prepend>
          <v-icon>
            mdi-magnify
          </v-icon>
        </template>
      </v-text-field>
    </v-row>

    <!-- 分类选择按钮 -->
    <v-row justify="center" class="mb-4">
      <!-- 添加“全部分类”按钮 -->
      <v-btn
        @click="selectCategory(null)"
        class="category-btn"
        :class="{
          'v-btn--active': selectedCategory === null,
          'all-category-btn': selectedCategory === null
        }"
        style="margin: 0 8px;"
      >
        <v-icon left>mdi-format-list-bulleted</v-icon> 全部
      </v-btn>

      <!-- 循环显示分类按钮 -->
      <v-btn
        v-for="category in categories"
        :key="category.id"
        @click="selectCategory(category)"
        class="category-btn"
        :class="{
          'v-btn--active': selectedCategory === category,
          'category-btn-active': selectedCategory === category
        }"
        style="margin: 0 8px;"
      >
        <v-icon left>mdi-tag</v-icon> {{ category.name }}
      </v-btn>
    </v-row>

    <v-row>
      <v-col
        v-for="blog in filteredBlogs"
        :key="blog.id"
        cols="12"
      >
        <v-card
          class="mb-4 mx-auto"
          outlined
        >
          <!-- 上方头像和作者信息 -->
          <v-card-title class="d-flex align-items-center">
            <v-row>
              <v-col cols="auto">
                <v-avatar size="50">
                  <img :src="'http://localhost:9090/upload/'+blog.avatar" alt="avatar" class="avatar-image"/>
                </v-avatar>
              </v-col>
              <v-col cols="1">
                <div>
                  <div class="text-subtitle-1 font-weight-medium">{{ blog.author }}</div>
                  <div class="text-caption grey--text">{{ blog.categories.map(c => c.name).join(', ') }}</div>
                </div>
              </v-col>
            </v-row>
          </v-card-title>

          <v-row>
            <!-- 只在 blog.graphic 有值时显示图片栏 -->
            <v-col v-if="blog.graphic !== 'kobe.png'" cols="12" md="4">
              <v-img
                :src="'http://localhost:9090/upload/' + blog.graphic"
                max-height="200"
                cover
                @click="viewBlog(blog.id)"
                class="image"
              ></v-img>
            </v-col>
            <v-col cols="12" md="8">
              <!-- 标题 -->
              <v-card-title class="title" @click="viewBlog(blog.id)">
                {{ blog.title }}
              </v-card-title>
              <!-- 正文内容 -->
              <v-card-text @click="viewBlog(blog.id)">
                <div v-if="blog.isExpanded">
                  <div v-html="markDownToHtml(blog.content)"></div>
                </div>
                <div v-else>
                  <div v-html="markDownToHtml(blog.content.length > 100 ? blog.content.slice(0, 100) + '...' : blog.content)"></div>
                  <span
                    v-if="blog.content.length > 100"
                    class="read-more text-primary"
                    @click.stop="blog.isExpanded = true"
                  >
                    阅读全文
                    <v-icon small class="ms-1 text-primary">mdi-chevron-down</v-icon>
                  </span>
                </div>
              </v-card-text>

            </v-col>
          </v-row>

          <!-- 底部点赞、评论和收起 -->
          <v-card-actions class="d-flex align-items-center">
            <!-- 赞同按钮 -->
            <v-btn
              class="vote-button"
              :color="blog.liked ? 'primary' : 'grey'"
              outlined
              :variant="blog.liked ? 'tonal' : 'text'"
              @click="handleLike(blog)"
            >
              <v-icon left>mdi-chevron-up</v-icon>
              {{blog.liked ? '已赞同' : '赞同'}} {{ blog.likes }}
            </v-btn>

            <!-- 不赞同按钮 -->
            <v-btn
              class="vote-button"
              :color="blog.disliked ? 'primary' : 'grey'"
              outlined
              :variant="blog.disliked ? 'tonal' : 'text'"
              @click="handleDislike(blog)"
            >
              <v-icon left>mdi-chevron-down</v-icon>
              {{blog.disliked ? '已反对' : '反对'}} {{ blog.dislikes }}
            </v-btn>

            <!-- 收藏按钮 -->
            <v-btn
              class="vote-button"
              :color="blog.collected ? 'orange' : 'grey'"
              outlined
              :variant="blog.collected ? 'tonal' : 'text'"
              @click="handleCollect(blog)"
            >
              <v-icon left>mdi-star</v-icon>
              {{blog.collected ? '取消收藏' : '收藏'}}  {{ blog.collects }}
            </v-btn>

            <!-- 删除按钮 -->
            <v-btn @click="deleteBlog(blog.id)" v-if="blog.privilege">
              <v-icon >mdi-trash-can</v-icon>
              删除
            </v-btn>
            <span
              v-if="blog.isExpanded"
              class="read-more text-primary ms-auto"
              @click.stop="blog.isExpanded = false"
            >
              收起
              <v-icon small class="ms-1 text-primary">mdi-chevron-up</v-icon>
            </span>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- 分页控制 -->
    <v-row justify="center" class="mt-4">
      <v-pagination
        v-model="pagination.page"
        :length="pagination.totalPages"
        total-visible="5"
        @click="filterBlogs"
      ></v-pagination>
    </v-row>

    <!-- 右下角浮动按钮组 -->
    <div class="floating-buttons">
      <v-btn fab @click="createBlog">
        <v-icon>mdi-plus</v-icon>
        <v-tooltip
          activator="parent"
          location="start"
        >创建帖子</v-tooltip>
      </v-btn>

      <v-btn fab @click="viewFavorites">
        <v-icon>mdi-heart</v-icon>
        <v-tooltip
          activator="parent"
          location="start"
        >我的收藏</v-tooltip>
      </v-btn>

      <!-- <v-btn fab  @click="goBack">
        <v-icon>mdi-arrow-up</v-icon>
        <v-tooltip
          activator="parent"
          location="start"
        >回到顶部</v-tooltip>
      </v-btn> -->
    </div>
  </v-container>
</template>

<script>
import api from '@/api/blog.js'
import { marked } from 'marked'

export default {
  props: {
    // blog: {
    //   type: Object,
    //   required: true,
    // },
  },
  data() {
    return {
      userid: 4, // 当前用户 ID
      isAdmin: false, // 是否是管理员
      isCategoryMode: false, // 是否处于分类选择模式
      searchQuery: "", // 搜索关键字
      selectedCategory: null, // 选中的分类
      blogs: [], // 博客数据
      categories: [], // 分类数据
      filteredBlogs: [], // 筛选后的博客数据
      pagination: {
        page: 1, // 当前页码
        totalPages: 1, // 总页数
      },
      scrollTop: 0, //默认距离顶部的距离
      isShow: false, //控制返回顶部按钮的显隐
      scrollTrigger: false, //默认初始值
    };
  },
  created() {
    // 从 localStorage 或 sessionStorage 获取保存的页码
    const savedPage = localStorage.getItem("currentPage"); // 使用 sessionStorage 也可以
    if (savedPage) {
      this.pagination.page = parseInt(savedPage, 10); // 恢复页码
    }
    // 获取博客和分类数据
    api.acquireBlogsApi().then(data => {
      this.blogs = data.blogs
      this.filterBlogs(); // 过滤博客数据，更新视图
    });
    api.acquireCtgAllApi().then(data => {
      this.categories = data.categories
    });
  },
  watch: {
    // 监听页码变化并保存到 localStorage
    'pagination.page'(newPage) {
      localStorage.setItem("currentPage", newPage); // 保存当前页码
    },
  },
  methods: {
    // 将 markdown 转换为 HTML
    markDownToHtml(content) {
      return marked(content);
    },
    // 创建帖子
    createBlog() {
      this.$router.push('/blogs/create_blog');
    },
    // 查看收藏夹，这个先等调整讨论区卡片再改
    viewFavorites() {
      this.$router.push('/account/folder/1')
    },
    // 返回顶部
    goBack() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    // 初始化筛选博客数据
    filterBlogs() {
      const query = this.searchQuery.toLowerCase();
      const category = this.selectedCategory;

      // 基于搜索和分类筛选博客
      const filtered = this.blogs.filter((blog) => {
        const matchesTitle = blog.title.toLowerCase().includes(query) || blog.content.toLowerCase().includes(query);
        const matchesCategory = category ? blog.categories.some(c => c.id === category.id) : true;
        return matchesTitle && matchesCategory;
      });

      const pageSize = 6; // 每页显示博客数量
      this.pagination.totalPages = Math.ceil(filtered.length / pageSize); // 更新总页数
      if (this.pagination.page > this.pagination.totalPages) {
        this.pagination.page = 1; // 如果当前页码大于总页数，重置为第一页
      }
      
      // 分页处理
      const start = (this.pagination.page - 1) * pageSize;
      const end = start + pageSize;

      this.filteredBlogs = filtered.slice(start, end); // 当前页显示的数据
    },
    // 选择分类
    selectCategory(category) {
      // 如果选择了“全部”，清除选中的分类
      if (category === null) {
        this.selectedCategory = null;
      } else {
        this.selectedCategory = category;
      }

      // 调用 API 搜索分类
      if (this.selectedCategory) {
        // 根据选中的分类获取相关的博客数据
        api.searchByCategoryApi(this.selectedCategory.id).then(data => {
          this.blogs = data.blogs; // 更新博客数据
          this.filterBlogs(); // 过滤博客数据，更新视图
        });
      } else {
        // 如果没有选择分类，展示所有博客
        api.acquireBlogsApi().then(data => {
          this.blogs = data.blogs; // 更新博客数据
          this.filterBlogs(); // 过滤博客数据，更新视图
        });
      }
    },
    // 查看帖子详情，在新窗口打开
    viewBlog(blogId) {
      this.$router.push({ path: `/blogs/blog_detail`, query: { blog_id: blogId } });
      //  window.open(`/blogs/blog_detail?blog_id=${blogId}`, '_blank');
    },
    deleteBlog(blogId) {
      api.deleteBlogApi(blogId).then(data => {
        // 刷新视图
        location.reload();
        // this.filterBlogs();
      });
    },
    handleLike(blog) {
      api.likeBlogApi(blog.id).then(res => {
        blog.liked = res.created
        if (res.created) {
          blog.likes += 1
        } else {
          blog.likes -= 1
        }
      }).catch(error => {
        console.log(error)
      })
    },
    handleDislike(blog) {
      api.dislikeBlogApi(blog.id).then(res => {
        blog.disliked = res.created
        if (res.created) {
          blog.dislikes += 1
        } else {
          blog.dislikes -= 1
        }
      }).catch(error => {
        console.log(error)
      })
    },
    handleCollect(blog) {
      api.collectBlogApi(blog.id).then(res => {
        blog.collected = res.created
        if (res.created) {
          blog.collects += 1
        } else {
          blog.collects -= 1
        }
      }).catch(error => {
        console.log(error)
      })
    },
  },
};
</script>

<style scoped>

.category-btn {
  font-size: 16px;
  padding: 8px 16px;
  border-radius: 30px; /* 圆角按钮 */
  transition: background-color 0.3s ease, transform 0.3s ease;
}

/* 默认按钮样式 */
.category-btn {
  font-size: 16px;
  padding: 8px 16px;
  border-radius: 30px;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

/* 鼠标悬停时按钮的阴影效果 */
.v-btn:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transform: scale(1.05);
}

/* “全部分类”按钮样式与其他分类区别 */
.all-category-btn {
  background-color: #ff5722; /* 明亮的颜色 */
  color: white;
}

/* 被选中的分类按钮样式 */
.v-btn--active {
  background-color: #26c6da !important; /* 默认选中颜色 */
  color: white;
}

/* 其他分类按钮被选中的颜色 */
.category-btn-active {
  background-color: #4caf50;
  color: white;
}

/* 分类按钮的过渡效果 */
.category-btn,
.v-btn--active,
.category-btn-active {
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.mx-auto {
  cursor: pointer; /* 添加鼠标手势，提示卡片是可点击的 */
  transition: transform 0.2s ease-in-out;
}
.mx-auto:hover {
  transform: scale(1.02); /* 鼠标悬浮时稍微放大卡片 */
}

.floating-buttons {
  position: fixed;
  bottom: 16px; /* 距离页面底部的距离 */
  right: 16px; /* 距离页面右侧的距离 */
  display: flex;
  flex-direction: column; /* 按列排列 */
  gap: 16px; /* 按钮之间的间距 */
  z-index: 1000; /* 确保按钮始终在最上层 */
}

.read-more {
  color: #1976D2; /* 默认使用 Vuetify primary 颜色 */
  font-weight: 500; /* 半粗体 */
  cursor: pointer; /* 鼠标悬停手型指针 */
  display: inline-flex; /* 图标和文字对齐 */
  align-items: center;
}
.read-more:hover {
  color: var(--v-primary-darken1); /* 悬浮时加深 */
  color: #0056b3; /* 悬停时稍微加深颜色 */
}

.read-more-icon {
  color: #1976D2; /* 图标颜色和文字一致 */
  transition: color 0.2s ease; /* 添加图标过渡效果 */
}
.read-more:hover .read-more-icon {
  color: var(--v-primary-darken1); /* 悬浮时图标颜色同步变化 */
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 保持比例并裁剪多余部分 */
  border-radius: 50%; /* 确保是圆形 */
}

.v-deep(.title) :hover {
  text-decoration: underline;
}

</style>
