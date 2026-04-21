import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import UsersView from '../views/UsersView.vue'
import ScoreboardView from '../views/ScoreboardView.vue'
import ChallengesView from '../views/ChallengesView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView},
    { path: '/users', name: 'users', component: UsersView},
    { path: '/scoreboard', name: 'scoreboard', component: ScoreboardView},
    { path: '/challenges', name: 'challenges', component: ChallengesView},
    { path: '/challenges/:id', name: 'challenge-detail', component: () => import('../views/ChallengeDetailView.vue') },
  ]
})
export default router