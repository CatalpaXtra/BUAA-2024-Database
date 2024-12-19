<template>
  <v-container>
    <v-card class="pa-6"
      title="创建帖子"
    >
      <v-row>
        <v-col cols="12">
          <v-file-input
            label="点击添加封面（可选）"
            prepend-icon="mdi-camera"
            type="file"
            ref="fileInput"
            accept="image/*"
            @change="handleFileUpload"
          ></v-file-input>
        </v-col>
      </v-row>

      <v-text-field
        v-model="title"
        label="标题"
        outlined
        dense
        placeholder="请输入文章标题"
      />
      
      

      <v-select
        v-model="selectedCategories"
        :item-props="itemProps"
        :items="categories"
        label="分类"
        multiple
      >
        <!-- 前置插槽：全选选项 -->
        <template v-slot:prepend-item>
          <v-list-item
            title="全选"
            @click="toggleAllCategories"
          >
            <template v-slot:prepend>
              <v-checkbox-btn
                :color="someSelected ? 'primary' : undefined"
                :indeterminate="someSelected && !allSelected"
                :model-value="allSelected"
              ></v-checkbox-btn>
            </template>
          </v-list-item>

          <v-divider class="mt-2"></v-divider>
        </template>

        <!-- 后置插槽：显示附加信息 -->
        <template v-slot:append-item>
          <v-divider class="mb-2"></v-divider>

          <v-list-item
            title="已选分类数量"
            :subtitle="selectedCategories.length"
            disabled
          >
            <template v-slot:prepend>
              <!-- 分类图标 -->
              <v-avatar color="info" icon="mdi-tag"></v-avatar>
            </template>
          </v-list-item>
        </template>
      </v-select>


      <v-md-editor
        v-model="content"
        height="500px"
        :editor-options="editorOptions"
      />

      <v-divider class="mb-4"></v-divider>

      <v-row>
        <v-col cols="12" md="6">
          <v-btn color="error" @click="goBack" block>
            取消发布
          </v-btn>
        </v-col>
        <v-col cols="12" md="6">
          <v-btn color="success" @click="submitBlog" block>
            提交发布
          </v-btn>
        </v-col>
      </v-row>
    </v-card>
  </v-container>
</template>

<script>
import VMdEditor from "@kangc/v-md-editor";
import "@kangc/v-md-editor/lib/style/base-editor.css"; // 基础样式
import vuepressTheme from "@kangc/v-md-editor/lib/theme/vuepress.js"; // 主题样式
import "@kangc/v-md-editor/lib/theme/style/vuepress.css"; // 主题样式的 CSS
import Prism from "prismjs"; // 语法高亮
import api from '@/api/blog.js'
import { ref } from "vue";
import { alert } from "@/store/alert.ts";

// 注册主题
VMdEditor.use(vuepressTheme, { Prism });

export default {
  name: "CreateBlog",
  components: {
    VMdEditor,
  },
  setup() {
    const categories = ref([]);
    api.acquireCtgAllApi().then(data => {
      categories.value = data.categories;
    });

    function itemProps (item) {
      return {
        title: item.name,
      }
    }
    return { categories, itemProps };
  },
  data() {
    return {
      formData: new FormData(),
      title: "",
      content: "",
      selectedCategories: [],
      // 配置自定义图片上传，现在有 bug
      editorOptions: {
        // 使用默认工具栏，但增加图片上传功能
        extendTools: {
          image: {
            className: "custom-image-tool", // 你可以定制图片工具按钮的样式
            execute: this.handleImageUpload,
          },
        },
      },
    };
  },
  computed: {
    // 是否全选
    allSelected() {
      return this.selectedCategories.length === this.categories.length;
    },
    // 是否部分选中
    someSelected() {
      return (
        this.selectedCategories.length > 0 &&
        this.selectedCategories.length < this.categories.length
      );
    },
  },
  methods: {
    // 切换全选状态
    toggleAllCategories() {
      if (this.allSelected) {
        this.selectedCategories = [];
      } else {
        this.selectedCategories = this.categories.slice();
      }
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      this.formData.append('graphic', file);
    },
    async submitBlog() {
      if (!this.title || !this.content) {
        alert('标题和内容不能为空！', 'error');
        return;
      }

      this.formData.append('title', this.title);
      this.formData.append('content', this.content);
      this.formData.append('categories', JSON.stringify(this.selectedCategories));

      api.pubBlogApi(this.formData).then(res => {
        if (res.code === 200) {
          alert('文章发布成功', 'success');
          this.$router.push("/blogs"); // 跳转到博客列表页
        }
        else {
          alert(res.message, 'error');
        }
      }).catch(error => {
        console.log(error)
      })
    },
    goBack() {
      this.$router.go(-1);
    },
  },
};
</script>

<style scoped>

</style>
