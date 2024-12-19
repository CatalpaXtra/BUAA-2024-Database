<template>
  <v-container class="object-detail">
    <!-- 在数据加载时显示骨架屏 -->
    <v-skeleton-loader 
      v-if="!object" 
      :loading="!object"
      class="object-card-skeleton"
      :height="'300px'"
    >
      <!-- 骨架屏占位内容 -->
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
      <!-- 对象内容 -->
      <v-card elevation="2" class="object-card mb-6">
        <!-- <v-row class="mb-6"> -->
        <v-row>
          <!-- 图片列 -->
          <v-col cols="4">
            <v-img :src="'http://localhost:9090/upload/'+this.object.graphic" />
          </v-col>

          <!-- 对象名称和介绍列 -->
          <v-col cols="8">
            <v-card-title>
              <h1 class="mb-2">{{ object.name }}</h1>
            </v-card-title>
            <v-divider></v-divider>
            <v-card-subtitle>{{ object.introduction }}</v-card-subtitle>
            <v-divider></v-divider>
            <v-card-text>
              <div class="d-flex align-center">
                <v-icon>mdi-calendar</v-icon>
                <span class="ml-2">发布于 {{ formatDate(object.created_at) }}</span>
              </div>
              <v-btn @click="deleteObj(object.id)" v-if="object.privilege">
                <v-icon >mdi-trash-can</v-icon>
                删除
              </v-btn>
              <v-btn @click="openObjectDialog" v-if="object.privilege_modi">
                <v-icon >mdi-pencil</v-icon>
                编辑
              </v-btn>
            </v-card-text>
          </v-col>
        </v-row>
      </v-card>

      <!-- 修改对象信息 -->
      <v-dialog v-model="showDialog" max-width="600px">
        <v-card>
          <v-card-title>修改对象信息</v-card-title>
          <v-card-text>
            <v-form ref="form" v-model="valid" lazy-validation>
              <v-file-input
                v-model="editedObject.graphic"
                label="对象图片"
                accept="image/*"
              ></v-file-input>
              <v-text-field
                v-model="editedObject.name"
                label="对象名称"
                required
              ></v-text-field>
              <v-textarea
                v-model="editedObject.introduction"
                label="对象介绍"
                required
              ></v-textarea>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn @click="showDialog = false">取消</v-btn>
            <v-btn @click="save" color="primary">保存</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>


      <!-- 评分区 -->
      <v-card class="object-card mb-6">
        <v-card
          color="indigo lighten-5"
          variant="tonal"
          class="d-flex flex-column mx-auto py-8"
          elevation="10"
          
        > 
          <v-row>
            <!-- 左边的空列 -->
            <v-col cols="1"></v-col>

            <!-- 评分和相关信息 -->
            <v-col cols="3">
              <div class="d-flex flex-column mt-auto text-h4">
                <span class="font-weight-bold">航扑评分</span>
              </div>
              
              <div v-if="object.star_ave === -1" class="text-h3 font-weight-bold" style="margin-top: 2rem;">
                暂无评分
              </div>

              <div v-else class="text-h2 font-weight-bold" style="margin-top: 2rem;">
                {{ object.star_ave }}
                <span class="text-h6 ml-n3">/5</span>
              </div>
              
              <div class="text-body-2" style="margin-top: 2rem; color: gray;">
                {{ object.star_count }} JRs评分
              </div>
            </v-col>

            <!-- 评分详情条目 -->
            <v-col cols="8">
              <v-list
                bg-color="transparent"
                class="d-flex flex-column-reverse"
                density="compact"
              >
                <v-list-item v-for="(count, rating) in object.star_num" :key="rating">
                  <v-progress-linear
                    :model-value="(count / totalStars) * 100"
                    class="mx-n5"
                    height="20"
                    rounded
                  ></v-progress-linear>

                  <template v-slot:prepend>
                    <span>{{ rating }}</span>
                    <v-icon class="mx-3" icon="mdi-star"></v-icon>
                  </template>

                  <template v-slot:append>
                    <div class="rating-values">
                      <span class="d-flex justify-end"> 
                        {{ ((count / totalStars) * 100).toFixed(1) }} %
                      </span>
                    </div>
                  </template>
                </v-list-item>
              </v-list>
            </v-col>
          </v-row>

          <v-row>
            <!-- 左边的空列 -->
            <v-col cols="1"></v-col>

            <!-- 立即评分或者已评分文字 -->
            <v-col cols="3">
              <div class="d-flex mt-auto text-h5 font-weight-light" style="color: gray;">
                {{ user_star === -1 ? '立即评分' : '已评分' }}
              </div>
            </v-col>

            <!-- 评分组件 -->
            <v-col cols="7" class="d-flex justify-end">
              <v-rating
                :model-value="user_star === -1 ? 0 : this.user_star"
                hover
                @update:model-value="onRatingUpdate"
                size="x-large"
              ></v-rating>
            </v-col>

            <!-- 右边的空列 -->
            <v-col cols="1"></v-col>
          </v-row>
        </v-card>
      </v-card>

    </v-container>

    <!-- 评论区，实现在 object_comments.vue -->
    <object_comments
      :comments="object?.comments || []" 
      @update-comments="updateComments"
    />
  </v-container>
</template>

<script>
import object_comments from "@/views/zone/object_comments.vue";
import { alert } from "@/store/alert.ts";
import api from '@/api/zone.js'

export default {
  name: "object_detail",
  components: { object_comments },
  data() {
    return {
      object: null, // 初始值为空，加载数据后赋值
      user_star : null, // 用户评分
      showDialog: false,
      editedObject: {
        graphic: null,
        name: "",
        introduction: "",
      },
    };
  },
  created() {
    const objectId = this.$route.query.object_id;
    if (objectId) {
      api.acquireObjectDetailApi(objectId).then(data => {
        this.object = data.data.object;
        this.user_star = data.data.user_star
      });
    }
  },
  computed: {
    totalStars() {
      // 计算所有评分的总和
      return Object.values(this.object.star_num).reduce((sum, num) => sum + num, 0) === 0 ? 1 : 
       Object.values(this.object.star_num).reduce((sum, num) => sum + num, 0);
    },
  },
  methods: {
    openObjectDialog() {
      this.showDialog = true;
      this.editedObject = { ...this.object };
    },
    save() {
      const formData = new FormData();
      formData.append('graphic', this.editedObject.graphic);
      formData.append('name', this.editedObject.name);
      formData.append('introduction', this.editedObject.introduction);

      // 提交编辑后的数据到后端
      const objectId = this.$route.query.object_id;
      api.updateObjectApi(formData, objectId).then(response => {
          if (response.code === 200) {
            // 更新当前页面对象信息
            this.object = { ...this.object, ...this.editedObject };
            if (response.graphic !== "") {
              this.object.graphic = response.graphic
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
    deleteObj(objId) {
      api.deleteObjApi(objId).then(data => {
        // 刷新视图
        this.$router.push({ path: '/zones/zone_detail', query: { zone_id: this.object.zone_id } });
      });
    },
    onRatingUpdate(value) {
      const objectId = this.$route.query.object_id;
      api.starObjectApi({ "value": value }, objectId).then(data => {
        alert('评分成功', 'success');
        if (this.user_star === -1) {
          this.object.star_count += 1;
        }
        this.user_star = value;
        this.object.star_ave = data.star_ave
        this.object.star_num = data.star_num;
      });
    },
    goBack() {
      this.$router.go(-1);
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
    updateComments(updatedComments) {
      this.object.comments = updatedComments;
    }
  }
};
</script>

<style scoped>
.object-card {
  box-shadow: none !important;
}

.v-chip {
  margin-bottom: 10px;
}

.v-divider {
  margin: 16px 0;
}

.object-detail {
  padding: 16px;
}

.v-btn {
  margin-top: 20px;
  border: none !important; /* 强制移除边框 */
  box-shadow: none !important; /* 强制移除阴影 */
  background-color: transparent !important; /* 强制移除背景色，好像没用 */
}

.object-card-skeleton {
  margin-top: 16px;
}
</style>
