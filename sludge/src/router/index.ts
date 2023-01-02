import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/employees',
      name: 'employees',
      component: () => import('../views/EmployeesView.vue')
    },
    {
      path: '/employees/:id',
      name: 'employee',
      component: () => import('../views/EmployeeEditView.vue')
    },
    {
      path: '/roles',
      name: 'roles',
      component: () => import('../views/RolesView.vue')
    },
    {
      path: '/groups',
      name: 'groups',
      component: () => import('../views/GroupsView.vue')
    },
    {
      path: '/resources',
      name: 'resources',
      component: () => import('../views/ResourcesView.vue')
    },
    {
      path: '/structure',
      name: 'structure',
      component: () => import('../views/StructureView.vue')
    },
    {
      path: '/transfers',
      name: 'transfers',
      component: () => import('../views/TransfersView.vue')
    },

  ]
})

export default router
