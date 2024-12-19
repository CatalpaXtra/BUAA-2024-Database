import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/navigator',
    name: 'navigator',
    component: () => import('../components/Navigator.vue')
  },
  {
    path: '/comment',
    name: 'comment',
    component: () => import('../components/Comment.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/login.vue')
  },
  {
    path: '/home',
    name: 'home',
    component: () => import('../views/home.vue')
  },
  {
    path: '/blogs',
    name: 'blogs',
    component: () => import('../views/blog/blogs.vue')
  },
  {
    path: '/blogs/blog_detail',
    name: 'blog_detail',
    component: () => import('../views/blog/blog_detail.vue'),
    children: [
      {
        path: '/blog_comments',
        name: 'blog_comments',
        component: () => import('../views/blog/blog_comments.vue')
      },
    ]
  },
  {
    path: '/blogs/create_blog',
    name: 'create_blog',
    component: () => import('../views/blog/create_blog.vue')
  },
  {
    path: '/zones',
    name: 'zones',
    component: () => import('../views/zone/zones.vue')
  },
  {
    path: '/zones/object_detail',
    name: 'object_detail',
    component: () => import('../views/zone/object_detail.vue'),
    children: [
      {
        path: '/object_comments',
        name: 'object_comments',
        component: () => import('../views/zone/object_comments.vue')
      },
    ]
  },
  {
    path: '/zones/zone_detail',
    name: 'zone_detail',
    component: () => import('../views/zone/zone_detail.vue')
  },
  {
    path: '/zones/create_zone',
    name: 'create_zone',
    component: () => import('../views/zone/create_zone.vue')
  },
  {
    path: '/zones/create_object',
    name: 'create_object',
    component: () => import('../views/zone/create_object.vue')
  },
  {
    path: '/account',
    name: 'account',
    component: () => import('../views/user/account.vue'),
  },
  {
    path: '/center',
    name: 'center',
    component: () => import('../views/user/center.vue'),
  },
  {
    path: '/account/modify_profile',
    name: 'modify_profile',
    component: () => import('../views/user/modify_profile.vue')
  },
  {
    path: '/account/modify_password',
    name: 'modify_password',
    component: () => import('../views/user/modify_password.vue')
  },
  {
    path: '/account/folder/:tabIndex',
    name: 'folder',
    component: () => import('../views/user/folder.vue')
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
