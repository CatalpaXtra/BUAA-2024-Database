<template>
  <v-card class="comment-card mb-4" elevation="1">
    <!-- 一级评论 -->
    <v-container>
      <v-row align="start">
        <!-- 头像列 -->
        <v-col cols="auto">
          <v-avatar size="40" @click="goToCenter(comment.author.id)">
            <img :src="'http://localhost:9090/upload/' + comment.author.avatar" alt="avatar" class="avatar-image"/>
          </v-avatar>
        </v-col>

        <!-- 内容列 -->
        <v-col>
          <div class="mb-2">
            <span class="font-weight-bold me-2">{{ comment.author.username }}</span>
          </div>
          <!-- 评分 -->
          <div>
            <v-rating
              v-if="comment.star !== undefined"
              v-model="comment.star"
              color="blue"
              size="20"
            ></v-rating>
          </div>
          <!-- 评论内容 -->
          <div>{{ comment.content }}</div>
          <!-- 操作图标（如点赞、回复） -->
          <div>
            <span class="text-caption grey--text" style="color: #757575;">{{ formattedDate(comment.pub_time) }}</span>
            <!-- 点赞按钮 -->
            <v-btn icon text small @click="toggleLike(comment)">
              <v-icon 
                :color="comment.liked ? '#1976d2' : ''"
                :class="{'hover-color': !comment.liked}"
                style="font-size: 18px;"
              >
                {{ comment.liked ? 'mdi-thumb-up' : 'mdi-thumb-up-outline' }}
              </v-icon>
            </v-btn>
            <span v-if="comment.likes > 0" style="color: #757575;">{{ comment.likes }}</span>
            <!-- 点踩按钮 -->
            <v-btn icon text small @click="toggleDislike(comment)">
              <v-icon 
                :color="comment.disliked ? '#1976d2' : ''"
                :class="{'hover-color': !comment.disliked}"
                style="font-size: 18px;"
              >
                {{ comment.disliked ? 'mdi-thumb-down' : 'mdi-thumb-down-outline' }}
              </v-icon>
            </v-btn>
            <span v-if="comment.dislikes > 0" style="color: #757575;">{{ comment.dislikes }}</span>
            <!-- 删除按钮 -->
            <v-btn @click="deleteCmt(comment.id)" v-if="comment.privilege">
              <v-icon >mdi-trash-can</v-icon>
              删除
            </v-btn>
            <!-- 回复按钮 -->
            <v-btn text small @click="toggleReplyBox(comment, null)">
              <span>回复</span>
            </v-btn>
          </div>
        </v-col>
      </v-row>
    </v-container>

    <!-- 二级评论 -->
    <v-card
      v-if="comment.cmtcomments && comment.cmtcomments.length > 0"
      class="nested-comments"
      v-for="reply in comment.cmtcomments"
      :key="reply.id"
    >
      <v-container>
        <v-row align="start">
          <!-- 头像列 -->
          <v-col cols="auto">
            <v-avatar size="40" @click="goToCenter(reply.author.id)">
              <img :src="'http://localhost:9090/upload/' + reply.author.avatar" alt="avatar" class="avatar-image"/>
            </v-avatar>
          </v-col>

          <!-- 内容列 -->
          <v-col>
            <div>
              <span class="font-weight-bold me-2">{{ reply.author.username }}  回复  @ {{ reply.reply_to.username}}:</span>
              <span>{{ reply.content }}</span>
            </div>
            <!-- 评论内容 -->
            <!-- <div>{{ reply.content }}</div> -->
            <!-- 操作图标（如点赞、回复） -->
            <div>
              <span class="text-caption grey--text" style="color: #757575;">{{ formattedDate(reply.pub_time) }}</span>
              <!-- 点赞按钮 -->
              <v-btn icon text small @click="toggleLike(reply)">
                <v-icon 
                  :color="reply.liked ? '#1976d2' : ''"
                  :class="{'hover-color': !reply.liked}"
                  style="font-size: 18px;"
                >
                  {{ reply.liked ? 'mdi-thumb-up' : 'mdi-thumb-up-outline' }}
                </v-icon>
              </v-btn>
              <span v-if="reply.likes > 0" style="color: #757575;">{{ reply.likes }}</span>
              <!-- 点踩按钮 -->
              <v-btn icon text small @click="toggleDislike(reply)">
                <v-icon 
                  :color="reply.disliked ? '#1976d2' : ''"
                  :class="{'hover-color': !reply.disliked}"
                  style="font-size: 18px;"
                >
                  {{ reply.disliked ? 'mdi-thumb-down' : 'mdi-thumb-down-outline' }}
                </v-icon>
              </v-btn>
              <!-- 删除按钮 -->
              <v-btn @click="deleteCmtCmt(reply.id)" v-if="reply.privilege">
                <v-icon >mdi-trash-can</v-icon>
                删除
              </v-btn>
              <span v-if="reply.dislikes > 0" style="color: #757575;">{{ reply.dislikes }}</span>
              <!-- 回复按钮 -->
              <!-- <v-btn text small @click="toggleReplyBox(comment, reply)">
                <span>回复</span>
              </v-btn> -->
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-card>

    <!-- 回复输入框 -->
    <div v-if="showReplyBox" class="comment-input d-flex align-start">
      <!-- <v-avatar size="48" class="me-3">
        <img :src="'http://localhost:9090/upload/'+currentUser.avatar" alt="User Avatar" />
      </v-avatar> -->
      <div class="flex-grow-1">
        <v-textarea
          v-model="replyContent"
          :placeholder="`回复：@ ${placeholderName}`"
          outlined
          rows="1"
          auto-grow
          class="mb-3"
        ></v-textarea>
        <div class="reply-actions d-flex align-center">
          <div class="icons d-flex align-center">
            <!-- <v-btn icon text small class="mr-4" @click="mentionUser">
              <v-icon>mdi-at</v-icon>
            </v-btn>
            <v-btn icon text small @click="insertImage">
              <v-icon>mdi-image-outline</v-icon>
            </v-btn> -->
          </div>
          <v-btn color="primary" @click="submitReply">
            <span>发布</span>
          </v-btn>
        </div>
      </div>
    </div>
  </v-card>
</template>

<script>
import { ref } from 'vue';
import api from '@/api/blog.js'
import router from "@/router";
import { alert } from "@/store/alert.ts";

export default {
  setup() {
    const placeholderName = ref(''); // 回复框中展示的名字
    const showReplyBox = ref(false); // 是否显示回复框
    const activeComment = ref(null); // 当前活跃的一级评论 ID
    const activeReply = ref(null); // 当前活跃的二级评论 ID
    const activeReplyId = ref(null); // 区分是否是二级评论
    return { placeholderName, showReplyBox, activeComment, activeReply, activeReplyId };
  },
  name: "Comment",
  data() {
    return {
      replyContent: "", // 回复内容
      currentUser: {
        avatar: "kobe.png", // 用户头像
      },
    };
  },
  props: {
    comment: {
      type: Object,
      required: true,
    },
  },
  // created() {
  //   api_user.fetchUserData().then(user => {
  //     this.currentUser = user
  //   });
  // },
  methods: {
    deleteCmt(cmtId) {
      api.deleteCmtApi(cmtId).then(data => {
        // 刷新视图
        location.reload();
      });
    },
    deleteCmtCmt(cmtId) {
      api.deleteCmtCmtApi(cmtId).then(data => {
        // 刷新视图
        location.reload();
      });
    },
    goToCenter(user_id) {
        this.$router.push({ path: '/center', query: { user_id: user_id } });
    },
    // 格式化评论时间
    formattedDate(pub_time) {
      const now = Date.now();
      const pubTime = new Date(pub_time).getTime();
      const timeDiff = Math.floor((now - pubTime) / 1000); // 时间差（秒）

      if (timeDiff < 60) {
        return `${timeDiff}秒前`; // 小于 60 秒
      } else if (timeDiff < 3600) {
        const minutes = Math.floor(timeDiff / 60);
        return `${minutes}分钟前`; // 小于 60 分钟
      } else if (timeDiff < 86400) {
        const hours = Math.floor(timeDiff / 3600);
        return `${hours}小时前`; // 小于 24 小时
      } 
      if (timeDiff < 3600) {
        const hours = Math.floor(timeDiff / 3600);
        return `${hours}小时前;`;
      }
      return new Date(this.comment.pub_time).toLocaleDateString(undefined, {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    },
    // 点赞/取消点赞
    toggleLike(comment) {
      if ('cmtcomments' in comment) {
        // 此时点赞的是一级评论
        api.likeCmtApi(comment.id).then(res => {
          comment.liked = res.created
          if (res.created) {
            comment.likes += 1
          } else {
            comment.likes -= 1
          }
        }).catch(error => {
          console.log(error)
        })
      } else {
        // 此时点赞的是二级评论
        api.likeCmtCmtApi(comment.id).then(res => {
          comment.liked = res.created
          if (res.created) {
            comment.likes += 1
          } else {
            comment.likes -= 1
          }
        }).catch(error => {
          console.log(error)
        })
      }
    //   this.postReaction(comment.id, "like");
    },
    // 点踩/取消点踩
    toggleDislike(comment) {
      if ('cmtcomments' in comment) {
        // 此时点踩的是一级评论
        api.dislikeCmtApi(comment.id).then(res => {
          comment.disliked = res.created
          if (res.created) {
            comment.dislikes += 1
          } else {
            comment.dislikes -= 1
          }
        }).catch(error => {
          console.log(error)
        })
      } else {
        // 此时点踩的是二级评论
        api.dislikeCmtCmtApi(comment.id).then(res => {
          comment.disliked = res.created
          if (res.created) {
            comment.dislikes += 1
          } else {
            comment.dislikes -= 1
          }
        }).catch(error => {
          console.log(error)
        })
      }
    //   this.postReaction(comment.id, "dislike");
    },
    toggleReplyBox(comment, reply) {
      if (this.activeComment === comment.id && this.activeReplyId === (reply?.id || null)) {
        // 点击相同的评论，收起回复框
        this.showReplyBox = !this.showReplyBox;
      } else {
        // 点击其他评论，切换回复框
        this.replyContent = "";
        this.showReplyBox = true;
        this.activeComment = comment.id;
        this.activeReplyId = reply?.id || null;
        this.placeholderName = reply ? reply.author.username : comment.author.username;
      }
    },
    submitReply() {
      if (this.replyContent.trim()) {
        // 提交评论逻辑
        const data = {
          "cmt_id": this.activeComment,
          "cmtcontent": this.replyContent,
        }
        api.pubCmtCmtApi(data).then(res => {
          if (res.code === 200) {
            alert(res.message, "success")
            // 延迟刷新页面，确保提示框有时间显示
            setTimeout(() => {
              router.go(0);
            }, 200); // 1.5 秒后刷新页面
          }
          else {
            alert(res.message, "success")
          }
        }).catch(error => {
          console.log(error)
        })
        // 清空回复框
        this.replyContent = "";
        this.showReplyBox = false;
      }
    },
    mentionUser() {
      this.replyContent += "@";
    },
    insertImage() {
      console.log("插入图片功能");
    },
  },
};
</script>

<style scoped>
.nested-comments {
  margin-left: 48px;
  box-shadow: none !important;
  border: none !important;
  overflow-x: hidden; /* 水平超出隐藏 */
  overflow-y: hidden; /* 垂直超出隐藏 */
  white-space: nowrap; /* 禁止换行 */
  text-overflow: ellipsis; /* 文本超出显示省略号 */
}

.comment-input {
  margin-top: 4px;
  margin-left: 60px;  
}

.comment-text {
  font-size: 1rem;
}

.v-btn {
  box-shadow: none !important;
  border: none !important;
  color: #757575;
}

.v-btn:hover {
  color: #1976d2;
  background-color: transparent !important;
}

.icon-button v-icon {
  transition: color 0.3s ease, font-size 0.3s ease; /* 动画过渡效果 */
}

.icon-button v-icon.hover-color:hover {
  color: #1976d2; /* 鼠标悬停时变色 */
}

.reply-actions {
  display: flex;            /* 启用 Flexbox */
  align-items: center;      /* 垂直居中 */
  justify-content: space-between; /* 两端对齐 */
  gap: 10px;                /* 设置间距 */
}

.icons v-btn {
  margin-right: 8px;        /* 按钮之间的间距 */
}

.icons {
  display: flex;
  align-items: center;      /* 图标垂直居中 */
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 保持比例并裁剪多余部分 */
  border-radius: 50%; /* 确保是圆形 */
  cursor: pointer;
}
</style>