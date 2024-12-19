<template>
  <v-container fluid>

    <!-- 骨架屏占位 -->
    <template v-if="!zones || zones.length === 0">
      <v-skeleton-loader type="image" class="mx-auto" style="height: 400px; width: 100%;" />
    </template>
    
    <!-- Recent Hot Posts Carousel -->
    <v-carousel v-else height="400px" 
      cycle 
      hide-delimiters
      progress="primary"
      show-arrows="hover"
    >
      <!-- 加载内容 -->
      <template v-if="zones.length > 0">
        <v-carousel-item 
          v-for="zone in zones.slice(0, 3)" 
          :key="zone.id"
        >
          <v-sheet class="d-flex align-center justify-center" height="100%" @click="goToZoneDetail(zone.id)" >
            <v-img :src="'http://localhost:9090/upload/' + zone.graphic" :alt="zone.name" contain max-height="300"/>
            <v-overlay :value="true" color="rgba(0, 0, 0, 0.6)">
              <div class="text-h4 white--text">{{ zone.name }}</div>
            </v-overlay>
          </v-sheet>
        </v-carousel-item>
      </template>
    </v-carousel>

    <v-container class="my-10">
      <v-row class="align-center">
        <v-col>
          <h4 class="inactive-color">讨论区</h4>
          <h2 class="h3-md">新鲜出炉</h2>
        </v-col>
        <v-col class="text-right">
          <router-link to="/blogs">
            <v-btn text class="inactive-color">
              <span>更多</span>
              <v-icon right>mdi-arrow-right</v-icon>
            </v-btn>
          </router-link>
        </v-col>
      </v-row>
      <v-row>
        <v-chip-group active-class="primary--text" column>
          <v-chip v-for="category in categories" :key="category.id" color="primary" class="white--text mx-2 my-2"
            @click="viewCtg(category.id)">
            {{ category.name }}
          </v-chip>
        </v-chip-group>
      </v-row>
      <v-row>
        <v-col cols="12" md="4" v-for="blog in filteredBlogs" :key="index">
          <v-card height="400px">
            <v-img :src="'http://localhost:9090/upload/' + blog.graphic" height="200px" v-if="blog.graphic !== 'kobe.png'"/>
            <v-img :src="'http://localhost:9090/upload/default.png'" height="200px" v-else />
            <v-card-title>{{ blog.title }}</v-card-title>
            <v-card-subtitle>{{ blog.author }}</v-card-subtitle>
            <div style="height: 90px">
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
      <v-pagination
        v-model="currentPage"
        :length="pageCount"
        class="mt-4"
        color="primary"
        @click="changePage"
      />
    </v-container>

    <v-container class="my-10">
      <v-row class="align-center">
        <v-col>
          <h4 class="inactive-color">本周</h4>
          <h2 class="h3-md">热门评分</h2>
        </v-col>
        <v-col class="text-right">
          <router-link to="/zones">
            <v-btn text class="inactive-color">
              <span>更多</span>
              <v-icon right>mdi-arrow-right</v-icon>
            </v-btn>
          </router-link>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="3" v-for="object in objects" :key="object.id">
          <v-card>
            <v-img :src="'http://localhost:9090/upload/'+object.graphic" height="150px" />
            <v-card-title>{{ object.name }}</v-card-title>
            <v-card-subtitle>{{ object.star_ave === -1 ? '暂无评分' : object.star_ave + " / 5"}} </v-card-subtitle>
            <v-card-actions>
              <div>
                <v-rating v-if="object.star_ave !== -1"
                  v-model="object.star_ave"
                  readonly
                  half-increments
                  color="blue"
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
    </v-container>

    <!-- Currently Trending -->
    <v-container class="my-10">
      <v-row class="align-center">
        <v-col>
          <h4 class="inactive-color">动态</h4>
          <h2 class="h3-md">他们在看</h2>
        </v-col>
        <v-col class="text-right">
          <router-link to="/zones">
            <v-btn text class="inactive-color">
              <span>更多</span>
              <v-icon right>mdi-arrow-right</v-icon>
            </v-btn>
          </router-link>
        </v-col>
      </v-row>
      <v-row>
        <template v-if="!zones">
          <v-skeleton-loader type="image" class="mx-auto" style="height: 400px; width: 100%;" />
        </template>
        <template v-else>
          <v-col cols="12" md="4" v-for="zone in zones.slice(0, 6)" :key="zone.id">
            <v-card>
              <v-img :src="'http://localhost:9090/upload/'+zone.graphic" height="200px" />
              <v-card-title>{{ zone.name }}</v-card-title>
              <v-card-subtitle>{{ zone.view_num }} JRs看过</v-card-subtitle>
              <v-card-actions>
                <v-btn text color="primary" @click="goToZoneDetail(zone.id)">查看详情</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>

        </template>
        
      </v-row>
    </v-container>

    <!-- Footer Watermark -->
    <v-footer class="text-center pa-4 mt-10">
      <span>&copy; 2024 Mamba Forever. No Rights Reserved.</span>
    </v-footer>
  </v-container>
</template>

<script>
import { marked } from 'marked'
import api from "@/api/home.js";

export default {

  data() {
    return {
      blogs: [],
      filteredBlogs: [],
      categories: [],
      zones: [],
      objects: [],
      index: 0,
      currentPage: 1, // Current page for pagination
      itemsPerPage: 3, // Number of items to display per page
      recentUpdates: [
        { title: 'Update 1', subtitle: 'Subtitle 1', description: 'Description for update 1', image: 'path/to/update1.jpg' },
        { title: 'Update 2', subtitle: 'Subtitle 2', description: 'Description for update 2', image: 'path/to/update2.jpg' },
        { title: 'Update 3', subtitle: 'Subtitle 3', description: 'Description for update 3', image: 'path/to/update3.jpg' },
        { title: 'Update 4', subtitle: 'Subtitle 4', description: 'Description for update 4', image: 'path/to/update4.jpg' },
        { title: 'Update 5', subtitle: 'Subtitle 5', description: 'Description for update 5', image: 'path/to/update5.jpg' },
        { title: 'Update 6', subtitle: 'Subtitle 6', description: 'Description for update 6', image: 'path/to/update6.jpg' },
      ],
    };
  },
  created() {
    api.acquireZonesApi().then(data => {
      this.zones = data.zones
    });
    api.acquireBlogsApi().then(data => {
      this.blogs = data.blogs
      this.changePage()
    });
    api.acquireCtgAllApi().then(data => {
      this.categories = data.categories
    });
    api.acquireObjectsApi().then(data => {
      this.objects = data.objects
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
  methods: {
    goToZoneDetail(zoneId) {
      this.$router.push({ path: `/zones/zone_detail`, query: { zone_id: zoneId } });
    },
    goToObjectDetail(objectId) {
      this.$router.push({ path: `/zones/object_detail`, query: { object_id: objectId } });
    },
    changePage() {
      const pageSize = 6; // 每页显示博客数量
      const start = (this.currentPage - 1) * pageSize;
      const end = start + pageSize;
      this.filteredBlogs = this.blogs.slice(start, end);
    },
    viewBlog(blogId) {
      this.$router.push({
        path: '/blogs/blog_detail',
        query: { blog_id: blogId }
      });
    },
    viewCtg(category_id) {
      this.$router.push({
        path: '/blogs',
        query: { category_id: category_id }
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
  border: none !important; /* 强制移除边框 */
  box-shadow: none !important; /* 强制移除阴影 */
  background-color: transparent !important; /* 强制移除背景色，好像没用 */
}

</style>
