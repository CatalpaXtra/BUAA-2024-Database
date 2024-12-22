# 航扑
## 项目简介
“航扑”是一个专注于校园领域的综合性评分及交流平台。学生可对北航的各个方面进行评分，包括但不限于课程设计、师资力量、食堂餐饮等。  
“航扑”为学生提供了一个表达对校园生活看法和感受的空间，大家可以分享自己在北航的各种体验，也能从他人的评价中获取对北航的更全面认识。

## 项目架构
Vue + Django + GaussDB

## 环境配置
node + vue安装参考 https://blog.csdn.net/qq_52611686/article/details/142653081  
mysql安装参考 https://blog.csdn.net/weixin_42868605/article/details/119821028  
navicat安装参考 https://www.bilibili.com/read/cv34556397/

## 初始化项目
执行 `python backend/manage.py import_categories backend/static` 以初始化博客标签  
执行 `python backend/manage.py create_superuser` 按要求创建超级管理员

## 运行
执行 `.\run_backend.bat` ，以运行后端  
执行 `.\run_frontend.bat` ，以运行前端  

## 致谢
- 前端开发  
@[JacckMa](https://github.com/JacckMa)   @[stardreaming](https://github.com/stardreaming)
- 后端开发  
@[CatalpaXtra](https://github.com/CatalpaXtra)
