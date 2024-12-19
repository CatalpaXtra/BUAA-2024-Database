<template>
  <v-container>
    <v-row>
      <!-- 搜索框 -->
      <v-text-field
        v-model="searchQuery"
        placeholder="搜索专区标题"
        outlined
        clearable
        @input="filterZones"
        class="flex-grow-1"
      >
        <template v-slot:prepend>
          <v-icon>
            mdi-magnify
          </v-icon>
        </template>
      </v-text-field>
    </v-row>

    <v-skeleton-loader
      v-if="!zones"
      :loading="!zones"
      :rows="9"
      :height="300"
    >
      <template v-slot:default>
        <v-row>
          <v-col
            v-for="index in 9"
            :key="index"
            cols="4"
          >
            <v-card variant="tonal" style="zone-card">
              <v-card-title class="zone-title card-skeleton"></v-card-title>
              <v-card-subtitle class="card-skeleton"></v-card-subtitle>
              <v-row>
                <v-col
                  v-for="index in 3"
                  :key="index"
                  cols="12"
                >
                  <v-card style="object-card">
                    <v-row>
                      <v-col cols="2">
                        <v-img aspect-ratio="1" style="width: 80px" />
                      </v-col>
                      <v-col cols="6">
                        <v-card-title class="card-skeleton"></v-card-title>
                        <v-card-subtitle class="card-skeleton"></v-card-subtitle>
                      </v-col>
                      <v-col cols="4" class="d-flex flex-column align-end">
                        <v-card-title class="card-skeleton"></v-card-title>
                        <v-card-subtitle class="card-skeleton"></v-card-subtitle>
                        <v-card-subtitle class="card-skeleton"></v-card-subtitle>
                      </v-col>
                    </v-row>
                  </v-card>
                </v-col>
              </v-row>
            </v-card>
          </v-col>
        </v-row>
      </template>
    </v-skeleton-loader>

    <v-container v-else>

    <v-row>
      <v-col
        v-for="zone in filteredZones"
        :key="zone.id"
        cols="6"
      >
        <!-- Zone Card -->
        <v-card variant="tonal" style="zone-card">
          <v-card-title @click="goToZoneDetail(zone.id)" class="zone-title-card">
            <span class="zone-title">{{ zone.name }}</span>
            <v-icon>mdi-arrow-right</v-icon>
          </v-card-title>
          <v-row>
            <v-col cols="12">
              <v-card-subtitle>{{ zone.view_num }} JRs看过</v-card-subtitle>
            </v-col>
          </v-row>

          <!-- Show the top 3 objects in this zone -->
          <v-row>
            <v-col
              v-for="object in zone.objects.slice(0, 3)"
              :key="object.id"
              cols="12"
            >
              <!-- Object Card -->
              <v-card @click="goToObjectDetail(object.id)" 
                :style="{ 
                  cursor: 'pointer',
                  boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
                  borderRadius: '8px',
                  marginLeft: '10px',
                  marginRight: '10px',
                }"
              >
                <v-row>
                  <!-- Object Image -->
                  <v-col cols="2" class="d-flex justify-center">
                    <v-img 
                      :src="'http://localhost:9090/upload/'+object.graphic" 
                      height="50"
                      width="60"
                      cover
                      class="ml-2 mt-2"
                      borderRadius="10px"
                    />
                  </v-col>
                  <!-- Object Content -->
                  <v-col cols="6">
                    <v-card-title :style="{ fontSize: '16px' }">{{ object.name }}</v-card-title>
                    <v-card-subtitle :style="{ fontSize: '12px' }">“{{ object.hot_comment }}”</v-card-subtitle>
                  </v-col>
                  <!-- Object Rating -->
                  <v-col cols="4" class="d-flex flex-column align-end">
                    <v-card-title :style="{ color: '#2196F3' }">
                      {{ object.star_ave === -1 ? '暂无评分' : object.star_ave + ' 分' }}
                    </v-card-title>
                    <v-card-subtitle :style="{ fontSize: '10px' }">{{ object.star_count }} JRs评分</v-card-subtitle>
                  </v-col>
                  
                </v-row>
              </v-card>
            </v-col>
            <!-- Fill missing card slots with placeholder content -->
            <v-col v-if="zone.objects.length < 3" cols="12" v-for="n in 3 - zone.objects.length" :key="'placeholder-' + n">
              <!-- Placeholder Card -->
              <v-card 
                :style="{ 
                  cursor: 'pointer',
                  boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
                  borderRadius: '8px',
                  marginLeft: '10px',
                  marginRight: '10px',
                }"
              >
                <v-row>
                  <!-- Placeholder Image -->
                  <v-col cols="2" class="d-flex justify-center">
                    <v-img 
                      src="http://localhost:9090/upload/placeholder.jpg" 
                      height="50"
                      width="60"
                      cover
                      class="ml-2 mt-2"
                      borderRadius="10px"
                    />
                  </v-col>
                  <!-- Placeholder Content -->
                  <v-col cols="6">
                    <v-card-title :style="{ fontSize: '16px' }">虚位以待</v-card-title>
                    <v-card-subtitle :style="{ fontSize: '12px' }">（请补充评分对象）</v-card-subtitle>
                  </v-col>
                </v-row>
              </v-card>
            </v-col>
          </v-row>
          <!--占位-->
          <v-card-title>
          </v-card-title>
        </v-card>
      </v-col>
    </v-row>

    <!-- 分页控制 -->
    <v-row justify="center" class="mt-4">
      <v-pagination
        v-model="pagination.page"
        :length="pagination.totalPages"
        :total-visible="5"
        @click="filterZones"
      ></v-pagination>
    </v-row>

    </v-container>

    <!-- 右下角浮动按钮组 -->
    <div class="floating-buttons">
      <v-btn fab @click="createZone">
        <v-icon>mdi-plus</v-icon>
        <v-tooltip
          activator="parent"
          location="start"
        >创建专区</v-tooltip>
      </v-btn>

      <v-btn fab @click="viewFavorites">
        <v-icon>mdi-heart</v-icon>
        <v-tooltip
          activator="parent"
          location="start"
        >我的收藏</v-tooltip>
      </v-btn>
    </div>
  </v-container>
</template>

<script>
import api from '@/api/zone.js'

export default {
  data() {
    return {
      searchQuery: '',  // 搜索框内容
      itemsPerPage: 9,  // 每页显示的专区数量
      currentPage: 1,  // 当前页码
      pagination: {
        page: 1, // 当前页码
        totalPages: 1, // 总页数
      },
      zones: null,
      filteredZones: null,
    };
  },
  created() {
    // 从本地存储中获取当前页码
    const savedPage = localStorage.getItem("currentPage"); // 使用 sessionStorage 也可以
    if (savedPage) {
      this.pagination.page = parseInt(savedPage, 10); // 恢复页码
    }

    api.acquireZonesApi().then(data => {
      this.zones = data.zones;
      this.filterZones();
    });
  },
  watch: {
    'pagination.page'(newPage) {
      localStorage.setItem("currentPage", newPage); // 保存当前页码
    },
  },
  methods: {
    // 搜索过滤逻辑
    filterZones() {
      const query = this.searchQuery.toLowerCase();

      const filtered = this.zones.filter(zone => 
        zone.name.toLowerCase().includes(query)
      );

      // 分页逻辑
      const pageSize = 6;
      this.pagination.totalPages = Math.ceil(filtered.length / pageSize);
      
      if (this.pagination.page > this.pagination.totalPages) {
        this.pagination.page = 1;
      }

      const start = (this.pagination.page - 1) * pageSize;
      const end = start + pageSize;

      this.filteredZones = filtered.slice(start, end);
    },
    goToZoneDetail(zoneId) {
      this.$router.push({ path: `/zones/zone_detail`, query: { zone_id: zoneId } });
      // window.open(`/zones/zone_detail?zone_id=${zoneId}`, '_blank');
    },
    goToObjectDetail(objectId) {
      this.$router.push({ path: `/zones/object_detail`, query: { object_id: objectId } });
      // window.open(`/zones/object_detail?object_id=${objectId}`, '_blank');
    },
    changePage(page) {
      this.currentPage = page;
    },
    createZone() {
      this.$router.push('/zones/create_zone');
    },
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    viewFavorites() {
      this.$router.push('/account/folder/2')
    },
  }
};
</script>

<style scoped>

.zone-title-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.zone-title-card:hover {
  cursor: pointer;
  color: #2196F3;
}

.v-btn {
  text-transform: none;
}

.floating-buttons {
  position: fixed;
  bottom: 16px;
  right: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  z-index: 1000;
}
</style>
