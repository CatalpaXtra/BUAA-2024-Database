<template>
  <v-container fluid>
    <v-tabs
      v-model="tab"
      align-tabs="center"
      color="deep-purple-accent-4"
    >
      <v-tab :value="1">藏帖锦集</v-tab>
      <v-tab :value="2">焦点专区</v-tab>
      <v-tab :value="3">星级衡鉴</v-tab>
    </v-tabs>

    <v-tabs-window v-model="tab">
      <v-tabs-window-item :value="1">
        <v-container class="my-10">
          <v-row>
            <v-col cols="12" md="4" v-for="blog in filteredBlogs" :key="index">
              <v-card height="400px">
                <v-img :src="'http://localhost:9090/upload/' + blog.graphic" height="200px" v-if="blog.graphic !== 'kobe.png'"/>
                <v-img :src="'http://localhost:9090/upload/default.png'" height="200px" v-else />
                <v-card-title>{{ blog.title }}</v-card-title>
                <v-card-subtitle>{{ blog.author }}</v-card-subtitle>
                <div style="height: 80px">
                  <v-card-text >
                    <div v-html="markDownToHtml(blog.content.length > 50 ? blog.content.slice(0, 50) + '...' : blog.content)"></div>
                  </v-card-text>
                </div>
                <v-card-actions>
                  <v-btn text color="primary" @click="viewBlog(blog.id)">查看详情</v-btn>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>

          <!-- Pagination Controls -->
          <v-row justify="center" class="mt-4">
            <v-pagination
              v-model="pagination.page"
              :length="pagination.totalPages"
              total-visible="5"
              @click="filterBlogs"
            ></v-pagination>
          </v-row>
        </v-container>
      </v-tabs-window-item>
      <v-tabs-window-item :value="2">
        <v-container class="my-10">
          <v-row>
            <v-col cols="12" md="4" v-for="zone in filteredZones" :key="zone.id">
              <v-card>
                <v-img :src="'http://localhost:9090/upload/'+zone.graphic" height="200px" />
                <v-card-title>{{ zone.name }}</v-card-title>
                <v-card-subtitle>{{ zone.view_num }} JRs看过</v-card-subtitle>
                <v-card-actions>
                  <v-btn text color="primary" @click="goToZoneDetail(zone.id)">查看详情</v-btn>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>
          <v-row justify="center" class="mt-4">
            <v-pagination
              v-model="pagination.page1"
              :length="pagination.totalPages1"
              total-visible="6"
              @click="filterZones"
            ></v-pagination>
          </v-row>
        </v-container>
      </v-tabs-window-item>
      <v-tabs-window-item :value="3">
        <v-container class="my-10">
          <v-row>
            <v-col cols="12" md="3" v-for="object in filteredObjects" :key="object.id">
              <v-card>
                <v-img :src="'http://localhost:9090/upload/'+object.graphic" height="150px" />
                <v-card-title>{{ object.name }}</v-card-title>
                <v-card-subtitle>{{ object.star_ave === -1 ? '暂无评分' : object.star_ave }} / 5</v-card-subtitle>
                <v-card-actions>
                  <div>
                    <v-rating v-if="object.star_ave !== -1"
                      v-model="object.star_ave"
                      readonly
                      color="blue"
                      half-increments
                      size="20"
                    />
                    <div v-else>暂未评分</div>

                  </div>
                  <div>
                    <v-btn text color="primary" @click="goToObjectDetail(object.id)" >查看详情</v-btn>
                  </div>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>
          <v-row justify="center" class="mt-4">
            <v-pagination
              v-model="pagination.page2"
              :length="pagination.totalPages2"
              total-visible="8"
              @click="filterObjects"
            ></v-pagination>
          </v-row>
        </v-container>
      </v-tabs-window-item>
    </v-tabs-window>
  </v-container>
</template>

<script>
import api from "@/api/home.js";
import { filterFields } from "element-plus/es/components/form/src/utils";
import {marked} from "marked";

export default {
  data() {
    return {
      tab: null,
      blogs: [],
      filteredBlogs: [],
      zones: [],
      filteredZones:[],
      objects: [],
      filteredObjects:[],
      pagination: {
        page: 1, // 当前页码
        totalPages: 1, // 总页数
        page1: 1, // 当前页码
        totalPages1: 1, // 总页数
        page2: 1, // 当前页码
        totalPages2: 1, // 总页数
      },
    };
  },
  created() {
    const savedPage = localStorage.getItem("currentPage"); // 使用 sessionStorage 也可以
    if (savedPage) {
      this.pagination.page = parseInt(savedPage, 10); // 恢复页码
    }
    const tabIndexParam = this.$route.params.tabIndex;
    if (tabIndexParam!== undefined) {
      const parsedIndex = parseInt(tabIndexParam);

      if (!isNaN(parsedIndex) && parsedIndex >= 1 && parsedIndex <= 3) {
        this.tab = parsedIndex;
      }
    }
    api.acquireCollectedBlogsApi().then(data => {
      this.blogs = data.blogs
      this.filterBlogs();
    });
    api.acquireFollowedZonesApi().then(data => {
      this.zones = data.zones
      this.filterZones();
    });
    api.acquireStaredObjectsApi().then(data => {
      this.objects = data.objects
      this.filterObjects();
    });
    
  },
  computed: {
    // Calculate the total number of pages
    pageCount() {
      return Math.ceil(this.recentUpdates.length / this.itemsPerPage);
    },
    // Get the updates for the current page
    paginatedUpdates() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.recentUpdates.slice(start, end);
    },
  },

  watch: {
    'pagination.page'(newPage) {
      localStorage.setItem("currentPage", newPage); // 保存当前页码
    },
     '$route.params.tabIndex': {
       immediate: true, // 组件创建时立即执行一次
       handler() {
         this.changed();
       }
     }
  },
  methods: {
    filterBlogs() {
      const pageSize = 6; // 每页显示博客数量
      this.pagination.totalPages = Math.ceil(this.blogs.length / pageSize); // 更新总页数
      if (this.pagination.page > this.pagination.totalPages) {
        this.pagination.page = 1; // 如果当前页码大于总页数，重置为第一页
      }
      // 分页处理
      const start = (this.pagination.page - 1) * pageSize;
      const end = start + pageSize;

      this.filteredBlogs = this.blogs.slice(start, end); // 当前页显示的数据
    },
    filterZones() {
      const pageSize1 = 6; // 每页显示博客数量
      this.pagination.totalPages1 = Math.ceil(this.zones.length / pageSize1); // 更新总页数
      if (this.pagination.page1 > this.pagination.totalPages1) {
        this.pagination.page1 = 1; // 如果当前页码大于总页数，重置为第一页
      }
      // 分页处理
      const start1 = (this.pagination.page1 - 1) * pageSize1;
      const end1 = start1 + pageSize1;

      this.filteredZones = this.zones.slice(start1, end1); // 当前页显示的数据
    },
    filterObjects() {
      const pageSize2 = 8; // 每页显示博客数量
      this.pagination.totalPages2 = Math.ceil(this.objects.length / pageSize2); // 更新总页数
      if (this.pagination.page2 > this.pagination.totalPages2) {
        this.pagination.page2 = 1; // 如果当前页码大于总页数，重置为第一页
      }
      // 分页处理
      const start2 = (this.pagination.page2 - 1) * pageSize2;
      const end2 = start2 + pageSize2;

      this.filteredObjects = this.objects.slice(start2, end2); // 当前页显示的数据
    },
    changed() {
       const tabIndexParam = this.$route.params.tabIndex;
        if (tabIndexParam!== undefined) {
          const parsedIndex = parseInt(tabIndexParam);

          if (!isNaN(parsedIndex) && parsedIndex >= 1 && parsedIndex <= 3) {
            this.tab = parsedIndex;
          }
        }
     },
    goToZoneDetail(zoneId) {
      this.$router.push({ path: `/zones/zone_detail`, query: { zone_id: zoneId } });
    },
    goToObjectDetail(objectId) {
      this.$router.push({ path: `/zones/object_detail`, query: { object_id: objectId } });
    },
    viewBlog(blogId) {
      this.$router.push({
        path: '/blogs/blog_detail',
        query: { blog_id: blogId }
      });
    },
    markDownToHtml(content) {
      return marked(content);
    },
  }
};
</script>

<style scoped>
.v-footer {
  background-color: #f5f5f5;
  color: #777;
  font-size: 0.9rem;
}

.inactive-color{
    color: #8e9194;
}

.btn-more {
  font-size: 14px; /* 字体大小 */
  color: #7a7a7a; /* 灰色字体，避免过于显眼 */
}

.v-btn {
  background-color: transparent; /* 使背景透明，避免过于突出 */
}
</style>
