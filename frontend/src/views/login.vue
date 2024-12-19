<template>
  <!-- 最外层的大盒子 -->
  <div class="bigBox">
    <div class="box" ref="box">
      <!-- 滑动盒子 -->
      <div class="pre-box">
        <h1>WELCOME</h1>
        <p>JOIN US!</p>
        <div class="img-box">
          <img :src="require('@/assets/img/06.gif')" alt="avatar" id="avatar" />
        </div>
      </div>
      <div class="left-block">
        <div class="register-form" v-if="mode === 'register'">
          <!-- 标题盒子 -->
          <div class="title-box">
            <h1>注册</h1>
          </div>
          <!-- 输入框盒子 -->
          <div class="input-box1">
            <input type="text" placeholder="用户名" v-model="registerForm.username"/>
            <input type="email" placeholder="邮箱" v-model="registerForm.email"/>
            <div class="code-input-btn-box">
              <input type="text" placeholder="验证码" v-model="registerForm.captcha"/>
              <div class="code-btn-box">
                  <button @click="sendVerificationCode" :disabled="isSending">{{ sendBtnText }}</button>
              </div>
            </div>
            <input type="password" placeholder="密码" v-model="registerForm.password"/>
            <input type="password" placeholder="确认密码" v-model="registerForm.confirmPassword"/>

          </div>
          <!-- 按钮盒子 -->
          <div class="btn-box">
            <button @click="register">注册</button>
            <p @click="mySwitch">已有账号?去登录</p>
          </div>
        </div>
        <div class="register-form" v-if="mode === 'recoverPassword'">
          <!-- 标题盒子 -->
          <div class="title-box">
            <h1>密码找回</h1>
          </div>
          <!-- 输入框盒子 -->
          <div class="input-box1">
            <input type="email" placeholder="注册邮箱" v-model="recoverPasswordForm.email"/>
            <div class="code-input-btn-box">
              <input type="text" placeholder="验证码" v-model="recoverPasswordForm.captcha"/>
              <div class="code-btn-box1">
                  <button @click="sendVerificationCode1" :disabled="isSending1">{{ sendBtnText1 }}</button>
              </div>
            </div>
            <input type="password" placeholder="重置密码" v-model="recoverPasswordForm.password"/>
            <input type="password" placeholder="确认密码" v-model="recoverPasswordForm.confirmPassword"/>

          </div>
          <!-- 按钮盒子 -->
          <div class="btn-box">
            <button @click="recoverPassword">重置密码</button>
            <p @click="switchMode">去登录</p>
          </div>
        </div>

      </div>
      <!-- 注册盒子 -->

      <!-- 登录盒子 -->
      <div class="login-form">
        <!-- 标题盒子 -->
        <div class="title-box">
          <h1>登录</h1>
        </div>
        <!-- 输入框盒子 -->
        <div class="input-box2">
          <input type="text" placeholder="邮箱" v-model="loginForm.email"/>
          <input type="password" placeholder="密码" v-model="loginForm.password"/>
        </div>
        <div class="btn-box1">
          <button @click="login">登录</button>
          <p style="padding-right: 10px;" @click="mySwitch">没有账号?去注册</p>
          <p style="border-left : 2px solid white;padding-left: 10px;" @click="switchMode">忘记密码?</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import api from '@/api/user.js'
import { useRouter } from 'vue-router'
import { alert } from '@/store/alert.ts';

const loginForm = reactive({
  email: '',
  password: ''
})
const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  captcha: ''
})
const recoverPasswordForm = reactive({
  email: '',
  password: '',
  confirmPassword: '',
  captcha: ''
})

let mode = ref('register')
const router = useRouter()

const login = () => {
  api.loginApi(loginForm).then(res => {
    if (res.code === 200) {
      localStorage.setItem('jwt_token', res.token);
      localStorage.setItem('avatar', res.avatar);
      localStorage.setItem('username', res.username);
      router.push('/home')
    }
    else {
      alert(res.message, 'error');
    }
  }).catch(error => {
    console.log(error)
  })
}

let isSending = ref(false);
let isSending1 = ref(false);
let sendBtnText = ref('发送验证码');
let sendBtnText1 = ref('发送验证码');
let countdownTimer = ref(null);
let countdownTimer1 = ref(null);

// 注册发送验证码
const sendVerificationCode = () => {
  if (!registerForm.email) {
    alert('请输入邮箱', 'error');
    return
  }
  
  api.captchaApi(registerForm).then(res => {
    if (res.code === 200) {
      isSending.value = true;
      document.querySelector('.code-btn-box button').disabled = true;
      sendBtnText.value = '60s后可重发';

      let count = 60;
      countdownTimer.value = setInterval(() => {
          count--;
          sendBtnText.value = `${count}s后可重发`;
          if (count === 0) {
              clearInterval(countdownTimer.value);
              isSending.value = false;
              // document.querySelector('.code-btn-box button').disabled = false;
              sendBtnText.value = '发送验证码';
          }
      }, 1000);
      alert(res.message, 'success');
    } else {
      alert(res.message, 'error');
    }
  }).catch(error => {
    console.log(error)
  })

};

// 忘记密码发送验证码
const sendVerificationCode1 = () => {
  if (!recoverPasswordForm.email) {
    alert('请输入邮箱', 'error');
    return
  }

  api.recoverCaptchaApi(recoverPasswordForm).then(res => {
    if (res.code === 200) {
      isSending1.value = true;
      document.querySelector('.code-btn-box1 button').disabled = true;
      sendBtnText1.value = '60s后可重发';

      let count1 = 60;
      countdownTimer1.value = setInterval(() => {
          count1--;
          sendBtnText1.value = `${count1}s后可重发`;
          if (count1 === 0) {
              clearInterval(countdownTimer1.value);
              isSending1.value = false;
              // document.querySelector('.code-btn-box1 button').disabled = false;
              sendBtnText1.value = '发送验证码';
          }
      }, 1000);
      alert(res.message, 'success');
    } else {
      alert(res.message, 'error');
    }
  }).catch(error => {
    console.log(error)
  })
};

const register = () => {
  const hasEmptyField = Object.values(registerForm).some(value =>!value);
  if (hasEmptyField) {
    alert('请将信息填写完整', 'error');
    return;
  }
  if (registerForm.password !== registerForm.confirmPassword) {
    alert('密码不一致', 'error');
    return
  }

  api.registerApi(registerForm).then(res => {
    if (res.code === 200) {
      alert('注册成功', 'success');
      mySwitch()
    } else {
      alert(res.message, 'error');
    }
  }).catch(error => {
    console.log(error)
  })
}

const recoverPassword = () => {
  const hasEmptyField = Object.values(recoverPasswordForm).some(value =>!value);
  if (hasEmptyField) {
    alert('请将信息填写完整', 'error');
    return;
  }
  if (recoverPasswordForm.password !== recoverPasswordForm.confirmPassword) {
    alert('密码不一致', 'error');
    return
  }

  api.recoverPasswordApi(recoverPasswordForm).then(res => {
    if (res.code === 200) {
      alert('密码重置成功', 'success');
      switchMode()
    } else {
      alert(res.message, 'error');
    }
  }).catch(error => {
    console.log(error)
  })
}

let flag = ref(true)
const mySwitch = () => {
  const pre_box = document.querySelector('.pre-box')
  const img = document.querySelector("#avatar")
  if (flag.value) {
    pre_box.style.transform = "translateX(100%)"
    pre_box.style.backgroundColor = "#c9e0ed"
    img.src = require("@/assets/img/09.gif")
  } else {
    pre_box.style.transform = "translateX(0%)"
    pre_box.style.backgroundColor = "#edd4dc"
    img.src = require("@/assets/img/06.gif")
  }
  flag.value = !flag.value
}

const switchMode = () => {
  const pre_box = document.querySelector('.pre-box')
  const img = document.querySelector("#avatar")
  if (flag.value) {
    pre_box.style.transform = "translateX(100%)"
    pre_box.style.backgroundColor = "#c9e0ed"
    img.src = require("@/assets/img/09.gif")
  } else {
    pre_box.style.transform = "translateX(0%)"
    pre_box.style.backgroundColor = "#edd4dc"
    img.src = require("@/assets/img/06.gif")
  }
  if (mode.value === 'register') {

    mode.value = 'recoverPassword'
  }
  else {
    setTimeout(() => {
    mode.value ='register';
  }, 500);

  }
  flag.value = !flag.value
}
</script>

<style scoped>

.code-input-btn-box {
    width: 80%;
    height: 40px;
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
}

/* 验证码输入框样式 */
.input-box1 input[type="text"][placeholder="验证码"] {
    align-items: flex-start;
    padding: 10px;
    height: 40px;
    margin-bottom: 8px;
    padding: 12px;
    border: 1px solid #bbb;
    border-radius: 8px;
}


/* 发送验证码按钮盒子样式 */
.code-btn-box {
    width: 150px;
    height: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.code-btn-box1 {
    width: 150px;
    height: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
}

/* 发送验证码按钮样式 */
.code-btn-box button {
    width: 120px;
    height: 40px;
    line-height: 40px;
    border: none;
    border-radius: 4px;
    background-color: #69b3f0;
    color: white;

    &:disabled {
        background-color: #ccc; /* 灰色背景 */
        cursor: default; /* 鼠标指针变为默认样式 */
        opacity: 0.6; /* 可根据需要调整透明度，让其看起来更有禁用的效果 */
    }
}

.code-btn-box button:hover {
    cursor: pointer;
    opacity: 0.8;
}

.code-btn-box1 button {
    width: 120px;
    height: 40px;
    line-height: 40px;
    border: none;
    border-radius: 4px;
    background-color: #69b3f0;
    color: white;

    &:disabled {
        background-color: #ccc; /* 灰色背景 */
        cursor: default; /* 鼠标指针变为默认样式 */
        opacity: 0.6; /* 可根据需要调整透明度，让其看起来更有禁用的效果 */
    }
}

.code-btn-box1 button:hover {
    cursor: pointer;
    opacity: 0.8;
}

/* 去除input的轮廓 */
input {
  outline: none;
  padding: 12px 20px;
  margin: 8px 0;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.input-box1,.input-box2  {
  display: flex;
  flex-direction: column;
  gap: 10px; /* 设置输入框之间的间距 */
  align-items: center; /* 水平居中对齐 */
}

.input-box1 input {
  width: 80%; /* 设置输入框宽度 */
  height: 40px;
  margin-bottom: 8px;
  padding: 12px;
  border: 1px solid #bbb;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.input-box2 input {
  width: 80%; /* 设置输入框宽度 */
  padding: 12px;
  border: 1px solid #bbb;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.input-box1 input:focus,.input-box2 input:focus {
  border-color: #66afe9;
  box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075), 0 0 8px rgba(102, 175, 233, 0.6);
  color: gray;
}


.bigBox {
  /* 溢出隐藏 */
  height: 100vh;
  overflow-x: hidden;
  display: flex;
  /* 渐变方向从左到右 */
  background: linear-gradient(to right, rgb(247, 209, 215), rgb(191, 227, 241));
}

/* 最外层的大盒子 */
.box {
  width: 1050px;
  height: 600px;
  display: flex;
  /* 相对定位 */
  position: relative;
  z-index: 2;
  margin: auto;
  /* 设置圆角 */
  border-radius: 8px;
  /* 设置边框 */
  border: 1px solid rgba(255, 255, 255, 0.6);
  /* 设置盒子阴影 */
  box-shadow: 2px 1px 19px rgba(0, 0, 0, 0.1);
}

/* 滑动的盒子 */
.pre-box {
  /* 宽度为大盒子的一半 */
  width: 50%;
  height: 100%;
  /* 绝对定位 */
  position: absolute;
  /* 距离大盒子左侧为0 */
  left: 0;
  /* 距离大盒子顶部为0 */
  top: 0;
  z-index: 99;
  border-radius: 4px;
  background-color: #edd4dc;
  box-shadow: 2px 1px 19px rgba(0, 0, 0, 0.1);
  /* 动画过渡，先加速再减速 */
  transition: 0.5s ease-in-out;
}

/* 滑动盒子的标题 */
.pre-box h1 {
  margin-top: 150px;
  text-align: center;
  /* 文字间距 */
  letter-spacing: 5px;
  color: white;
  /* 禁止选中 */
  user-select: none;
  /* 文字阴影 */
  text-shadow: 4px 4px 3px rgba(0, 0, 0, 0.1);
}

/* 滑动盒子的文字 */
.pre-box p {
  height: 30px;
  line-height: 30px;
  text-align: center;
  margin: 20px 0;
  /* 禁止选中 */
  user-select: none;
  font-weight: bold;
  color: white;
  text-shadow: 4px 4px 3px rgba(0, 0, 0, 0.1);
}

/* 图片盒子 */
.img-box {
  width: 200px;
  height: 200px;
  margin: 20px auto;
  /* 设置为圆形 */
  border-radius: 50%;
  /* 设置用户禁止选中 */
  user-select: none;
  overflow: hidden;
  box-shadow: 4px 4px 3px rgba(0, 0, 0, 0.1);
}

/* 图片 */
.img-box img {
  width: 100%;
  transition: 0.5s;
}

/* 登录和注册盒子 */
.login-form,
.register-form,
.left-block{
  flex: 1;
  height: 100%;
}

/* 标题盒子 */
.title-box {
  height: 220px;
  line-height: 340px;
}

/* 标题 */
.title-box h1 {
  text-align: center;
  color: white;
  /* 禁止选中 */
  user-select: none;
  letter-spacing: 5px;
  text-shadow: 4px 4px 3px rgba(0, 0, 0, 0.1);
}

/* 输入框盒子 */
.el-form {
  display: flex;
  /* 纵向布局 */
  flex-direction: column;
  /* 水平居中 */
  align-items: center;
}
.el-form-item {
  width: 65%;
}
/* 输入框 */
input {
  /* width: 60%; */
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 40px;
  margin-bottom: 20px;
  text-indent: 10px;
  border: 1px solid #fff;
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 120px;
  /* 增加磨砂质感 */
  backdrop-filter: blur(10px);
}


input:focus {
  /* 光标颜色 */
  color: #b0cfe9;
}

/* 聚焦时隐藏文字 */
input:focus::placeholder {
  opacity: 0;
}

/* 按钮盒子 */
.btn-box {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.btn-box1 {
  display: flex;
  justify-content: right;
  padding-right: 60px;
  margin-top: 20px;
}

/* 按钮 */
button {
  width: 100px;
  height: 30px;
  margin: 0 7px;
  line-height: 30px;
  border: none;
  border-radius: 4px;
  background-color: #69b3f0;
  color: white;
}

/* 按钮悬停时 */
button:hover {
  /* 鼠标小手 */
  cursor: pointer;
  /* 透明度 */
  opacity: 0.8;
}

/* 按钮文字 */
.btn-box,.btn-box1 p {
  height: 30px;
  line-height: 30px;
  /* 禁止选中 */
  user-select: none;
  font-size: 14px;
  color: white;
}

.btn-box p:hover {
  cursor: pointer;
  border-bottom: 1px solid white;
}
.btn-box1 p:hover {
  cursor: pointer;
  border-bottom: 1px solid white;
}
</style>