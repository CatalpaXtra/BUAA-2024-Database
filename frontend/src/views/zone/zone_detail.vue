<template>
  <v-container class="zone-detail">
    <v-skeleton-loader 
      v-if="!zone" 
      :loading="!zone"
      class="zone-card-skeleton"
      :height="'300px'"
    >
      <template #default>
        <v-card>
          <v-card-title>
            <v-skeleton-loader class="d-flex" :height="'50px'" />
          </v-card-title>
          <v-card-subtitle>
            <v-skeleton-loader :height="'30px'" />
          </v-card-subtitle>
          <v-card-text>
            <v-skeleton-loader :height="'20px'" />
            <v-skeleton-loader :height="'20px'" />
            <v-skeleton-loader :height="'20px'" />
          </v-card-text>
        </v-card>
      </template>
    </v-skeleton-loader>

    <v-container v-else>
      <!-- 区域详情 -->
      <v-card elevation="2" class="zone-card">
        <v-row>
          <v-col cols="12" md="4">
            <v-img :src="'http://localhost:9090/upload/' + zone.graphic" alt="zone image" aspect-ratio="1" />
          </v-col>

          <v-col cols="12" md="8">
            <v-card-title>
              <h1>{{ zone.name }}</h1>
            </v-card-title>
            <v-card-subtitle>{{ zone.introduction }}</v-card-subtitle>
            <v-divider></v-divider>
            <v-card-text>
              <div class="d-flex align-center">
                <v-icon>mdi-calendar</v-icon>
                <span class="ml-2">创建于 {{ formatDate(zone.created_at) }}</span>
              </div>
              <div class="d-flex align-center mt-3">
                <v-icon>mdi-eye</v-icon>
                <span class="ml-2">{{ zone.view_num }} 次浏览</span>
              </div>
              <div class="d-flex align-center mt-3">
                <v-icon>mdi-label</v-icon>
                <span class="ml-2">{{ zone.follows }} 人关注</span>
              </div>
              <v-card-actions>
                <!-- 收藏按钮 -->
                <v-btn
                  :color="isFollowed ? 'blue' : 'text'"
                  :variant="isFollowed ? 'tonal' : 'text'"
                  @click="handleFollow(zone.id)"
                >
                  <v-icon left>{{ isFollowed ? 'mdi-label' : 'mdi-label-outline' }}</v-icon>
                  {{isFollowed ? '取消关注' : '关注'}} 
                </v-btn>
                <!--TODO:v-if条件 -->
                <v-btn @click="deleteZone()" v-if="zone.privilege">
                  <v-icon >mdi-trash-can</v-icon>
                  删除
                </v-btn>
                <v-btn @click="reviseZone()" v-if="zone.privilege">
                  <v-icon >mdi-pencil</v-icon>
                  编辑
                </v-btn>
              </v-card-actions>
            </v-card-text>
          </v-col>
        </v-row>
      </v-card>

      <!--修改专区信息-->
      <v-dialog v-model="dialog" max-width="600px">
        <v-card>
          <v-card-title>
            <span class="headline">修改专区信息</span>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                <v-col cols="12">
                  <v-fileInput
                    v-model="editedZone.graphic"
                    label="专区图片"
                    accept="image/*"
                    prepend-icon="mdi-camera"
                    placeholder="选择图片文件"
                    outlined
                    clearable
                  ></v-fileInput>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    v-model="editedZone.name"
                    label="专区主题"
                    required
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12">
                  <v-textarea
                    v-model="editedZone.introduction"
                    label="专区介绍"
                    required
                  ></v-textarea>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="dialog = false">取消</v-btn>
            <v-btn color="blue darken-1" text @click="updateZone">保存</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <div class="d-flex align-center comments-header mb-5">
        <h2 class="mb-0 d-flex align-center comments-title">
          全部评分
          <span class="comment-count">({{ filteredObjects.length }})</span>
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
          <span class="divider">|</span>
          <v-btn
            text
            class="filter-btn no-border no-shadow"
            :class="{ active: filterOption === 'high_rating' }"
            @click="setFilter('high_rating')"
          >
            高分
          </v-btn>
          <span class="divider">|</span>
          <v-btn
            text
            class="filter-btn no-border no-shadow"
            :class="{ active: filterOption === 'low_rating' }"
            @click="setFilter('low_rating')"
          >
            低分
          </v-btn>
        </div>
      </div>

      <!-- 展示对象列表 -->
      <v-row>
        <v-col
          v-for="object in filteredObjects"
          :key="object.id"
          cols="12"
        >
          <v-card @click="goToObjectDetail(object.id)" class="object-card">
            <v-row>
              <v-col cols="2">
                <v-img :src="'http://localhost:9090/upload/' + object.graphic" alt="object image" aspect-ratio="1" class="mb-4" />
              </v-col>
              <v-col cols="6">
                <v-card-title>{{ object.name }}</v-card-title>
              </v-col>
              <v-col cols="4" class="d-flex flex-column align-end">
                <v-rating v-if="object.star_ave !== -1" v-model="object.star_ave" color="blue" size="30" readonly class="mb-5" half-increments/>
                <v-card-title v-else class="mb-5">暂无评分</v-card-title>
                <v-card-subtitle class="mb-5">{{ object.star_count }} JRs评分</v-card-subtitle>
                <v-btn text color="primary" @click.stop="deleteObject(object.id)" v-if="zone.privilege">
                  <v-icon >mdi-trash-can</v-icon>
                  删除
                </v-btn>
              </v-col>
            </v-row>
            <v-divider></v-divider>
            <v-card-text>
                <v-card-subtitle>“{{ object.hot_comment }}”</v-card-subtitle>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- 分页控制 -->
      <v-row justify="center" class="mt-4">
        <v-pagination
          v-model="currentPage"
          :length="totalPages"
          :total-visible="5"
          @input="changePage"
        ></v-pagination>
      </v-row>
    </v-container>

    <!-- 右下角浮动按钮组 -->
    <div class="floating-buttons">
      <v-btn fab @click="createObject">
        <v-icon>mdi-plus</v-icon>
        <v-tooltip activator="parent" location="start">创建对象</v-tooltip>
      </v-btn>

      <v-btn fab @click="viewFavorites">
        <v-icon>mdi-heart</v-icon>
        <v-tooltip activator="parent" location="start">我的收藏</v-tooltip>
      </v-btn>
    </div>
  </v-container>
</template>

<script>
import api from '@/api/zone.js'
import { alert } from '@/store/alert.ts'

export default {
  data() {
    return {
      zone: null, // 当前专区的数据
      currentPage: 1, // 当前页码
      itemsPerPage: 9, // 每页展示的对象数
      filterOption: 'popular', // 当前的筛选选项
      isFollowed: false, // 是否已收藏
      dialog: false, // 控制对话框显示
      editedZone: {
        graphic: null,
        name: "",
        introduction: "",
      },
    };
  },
  created() {
    const zoneId = this.$route.query.zone_id;
    if (zoneId) {
      api.acquireZoneDetailApi(zoneId).then(data => {
        this.zone = data.data.zone;
        this.isFollowed = data.data.isFollowed;
      });
    }
  },
  computed: {
    totalPages() {
      return Math.ceil(this.zone.objects.length / this.itemsPerPage);
    },
    filteredObjects() {
      let objects = [...this.zone.objects];

      // 按筛选条件过滤
      if (this.filterOption === 'popular') {
        // objects = objects.sort((a, b) => b.reviews_count - a.reviews_count); // 按评论数降序
        objects = objects; // 按评分人数降序
      } else if (this.filterOption === 'latest') {
        objects = objects.sort((a, b) => new Date(b.created_at) - new Date(a.created_at)); // 按创建时间降序
      } else if (this.filterOption === 'high_rating') {
        objects = objects.sort((a, b) => b.star_ave - a.star_ave); // 按评分高低排序（高到低）
      } else if (this.filterOption === 'low_rating') {
        objects = objects.sort((a, b) => a.star_ave - b.star_ave); // 按评分低到高排序
      }

      // 返回当前页显示的数据
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      return objects.slice(startIndex, startIndex + this.itemsPerPage);
    }
  },
  methods: {
    reviseZone() {
      this.dialog = true;
      this.editedZone = { ...this.zone };
    },
    updateZone() {
      const formData = new FormData();
      formData.append('graphic', this.editedZone.graphic);
      formData.append('name', this.editedZone.name);
      formData.append('introduction', this.editedZone.introduction);

      const zoneId = this.$route.query.zone_id;
      api.updateZoneApi(this.editedZone, zoneId).then(response => {
        if (response.code === 200) {
          // 更新当前页面对象信息
          this.zone = { ...this.zone, ...this.editedZone };
          if (response.graphic !== "") {
            this.zone.graphic = response.graphic
          }

          // 显示成功提示
          alert('修改成功', 'success');
          
          // 关闭对话框
          this.dialog = false;
        }
        else {
          alert(response.message, 'error');
        }
      })
      .catch(error => {
        alert('修改失败，请重试', 'error');
      });
    },
    deleteZone(zoneId) {
      api.deleteZoneApi(zoneId).then(data => {
        // 刷新视图
        this.$router.push('/zones');
      });
    },
    goBack() {
      this.$router.go(-1);
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString(undefined, {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      });
    },
    goToObjectDetail(objectId) {
      this.$router.push({ path: `/zones/object_detail`, query: { object_id: objectId } });
      // window.open(`/zones/object_detail?object_id=${objectId}`, '_blank');
    },
    rateOnObject(objectId) {
      // TODO: 评分逻辑，会报错
      api.starObjectApi({ "value": object.star_ave }, objectId).then(data => {
        alert('评分成功', 'success');
        
      });
    },
    changePage(page) {
      this.currentPage = page;
    },
    setFilter(option) {
      this.filterOption = option;
      this.currentPage = 1; // 重置页码为第一页
    },
    createObject() {
      this.$router.push({ path: '/zones/create_object', query: { zone_id: this.$route.query.zone_id } });
    },
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    viewFavorites() {
      this.$router.push('/account/folder/2')
    },
    handleFollow(zoneId) {
      api.followZoneApi(zoneId).then(res => {
        this.isFollowed = res.created
        if (res.created) {
          this.zone.follows += 1
        } else {
          this.zone.follows -= 1
        }
      }).catch(error => {
        console.log(error)
      })
    },
    deleteZone() {
      api.deleteZoneApi(this.zone.id).then(data => {
        this.$router.push('/zones');
      });
    },
    deleteObject(objectId) {
      api.deleteObjApi(objectId).then(data => {
        this.$router.go(0);
      });
    }

  }
};
</script>

<style scoped>
.zone-detail {
  padding: 16px;
}

.zone-card {
  margin-bottom: 16px;
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

.comment-count {
  font-size: 1rem; /* 可以根据需求调整字体大小 */
  margin-left: 5px; /* 给评论数和标题增加适当的间距 */
  vertical-align: baseline; /* 与标题底部对齐 */
  color: #757575;
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
</style>
