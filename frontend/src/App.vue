<script setup>
import { ref, watch, onMounted } from 'vue'

// --- 1. GESTION DU THÈME ---
const isDark = ref(true)

const applyTheme = (darkState) => {
  const themeName = darkState ? 'piscine-dark' : 'piscine-light'
  document.documentElement.setAttribute('data-theme', themeName)
  localStorage.setItem('theme', themeName)
}

watch(isDark, (newVal) => {
  applyTheme(newVal)
})

// --- 2. SKELETON LOADING (Correction : l'arrêt du chargement) ---
const isLoading = ref(true)

onMounted(() => {
  // Récupération du thème
  const savedTheme = localStorage.getItem('theme') || 'piscine-dark'
  isDark.value = savedTheme === 'piscine-dark'
  applyTheme(isDark.value)

  // CORRECTION : On arrête le loading après 1.5s
  setTimeout(() => {
    isLoading.value = false
  }, 1500)
})
</script>

<template>
  <div class="flex flex-col min-h-screen bg-base-100 text-base-content font-sans transition-colors duration-300">

    <nav class="sticky top-0 z-50 w-full bg-base-200/90 backdrop-blur border-b border-base-300 shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex-shrink-0 flex items-center gap-2">
            <span class="text-primary text-2xl font-cyber font-bold tracking-wider">GUARDIA<span class="text-base-content">_</span>HACK</span>
          </div>

          <div class="hidden md:block">
            <div class="flex items-baseline space-x-4">
              <a href="#" class="px-3 py-2 rounded-md text-sm font-medium text-primary bg-primary/10">Dashboard</a>
              <a href="#" class="px-3 py-2 rounded-md text-sm font-medium hover:text-primary transition-colors">Challenges</a>
              <a href="#" class="px-3 py-2 rounded-md text-sm font-medium hover:text-primary transition-colors">Scoreboard</a>
            </div>
          </div>

          <div class="flex items-center gap-4">
            <label class="btn btn-ghost btn-circle swap swap-rotate">
              <input type="checkbox" v-model="isDark" />
              <svg class="swap-on fill-current w-6 h-6 text-yellow-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M5.64,17l-.71.71a1,1,0,0,0,0,1.41,1,1,0,0,0,1.41,0l.71-.71A1,1,0,0,0,5.64,17ZM5,12a1,1,0,0,0-1-1H3a1,1,0,0,0,0,2H4A1,1,0,0,0,5,12Zm7-7a1,1,0,0,0,1-1V3a1,1,0,0,0-2,0V4A1,1,0,0,0,12,5ZM5.64,7.05a1,1,0,0,0,.7.29,1,1,0,0,0,.71-.29,1,1,0,0,0,0-1.41l-.71-.71A1,1,0,0,0,4.93,6.34Zm12,.29a1,1,0,0,0,.7-.29l.71-.71a1,1,0,1,0-1.41-1.41L17,5.64a1,1,0,0,0,0,1.41A1,1,0,0,0,17.66,7.34ZM21,11H20a1,1,0,0,0,0,2h1a1,1,0,0,0,0-2Zm-9,8a1,1,0,0,0-1,1v1a1,1,0,0,0,2,0V20A1,1,0,0,0,12,19ZM18.36,17A1,1,0,0,0,17,18.36l.71.71a1,1,0,0,0,1.41,0,1,1,0,0,0,0-1.41ZM12,6.5A5.5,5.5,0,1,0,17.5,12,5.51,5.51,0,0,0,12,6.5Zm0,9A3.5,3.5,0,1,1,15.5,12,3.5,3.5,0,0,1,12,15.5Z" /></svg>
              <svg class="swap-off fill-current w-6 h-6 text-primary" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M21.64,13a1,1,0,0,0-1.05-.14,8.05,8.05,0,0,1-3.37.73A8.15,8.15,0,0,1,9.08,5.49a8.59,8.59,0,0,1,.25-2A1,1,0,0,0,8,2.36,10.14,10.14,0,1,0,22,14.05,1,1,0,0,0,21.64,13Zm-9.5,6.69A8.14,8.14,0,0,1,7.08,5.22v.27A10.15,10.15,0,0,0,17.22,15.63a9.79,9.79,0,0,0,2.1-.22A8.11,8.11,0,0,1,12.14,19.73Z" /></svg>
            </label>

            <div class="flex items-center gap-3 border-l border-base-300 pl-4">
              <div class="text-right hidden sm:block">
                <div class="text-sm font-bold">Vex_Root</div>
                <div class="text-xs text-primary font-mono">LVL 42</div>
              </div>
              <div class="avatar">
                <div class="w-8 h-8 rounded bg-primary text-base-100 flex items-center justify-center font-bold">V</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <main class="flex-grow max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-3xl font-cyber font-bold mb-1">Active Challenges</h1>
          <p class="text-sm opacity-70">Sélectionnez une cible pour commencer l'exploitation.</p>
        </div>
      </div>

      <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="i in 6" :key="i" class="card bg-base-200 shadow-xl border border-base-300 animate-pulse">
          <div class="card-body">
            <div class="h-4 bg-base-300 rounded w-16 mb-4"></div>
            <div class="h-6 bg-base-300 rounded w-3/4 mb-4"></div>
            <div class="h-3 bg-base-300 rounded w-full mb-2"></div>
            <div class="h-3 bg-base-300 rounded w-5/6"></div>
          </div>
        </div>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div class="card bg-base-200 shadow-xl border border-base-300 hover:border-primary hover:-translate-y-1 transition-all duration-300 group">
          <div class="card-body">
            <div class="flex justify-between items-start">
              <div class="badge badge-outline border-green-500 text-green-500 font-mono text-xs">WEB</div>
              <div class="text-primary font-mono font-bold text-sm">300 pts</div>
            </div>
            <h2 class="card-title font-cyber mt-2 group-hover:text-primary transition-colors">SQLi Bypasser</h2>
            <p class="text-sm opacity-70">La base de données semble vulnérable. Trouvez le flag.</p>
            <div class="card-actions justify-between items-center mt-4">
               <div class="text-xs opacity-50 flex items-center gap-1">
                <span class="w-2 h-2 rounded-full bg-success"></span> 42 solves
              </div>
              <button class="btn btn-primary btn-sm rounded-md font-bold">Lancer</button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <footer class="flex flex-col md:flex-row gap-4 items-center justify-around w-full py-6 text-sm bg-base-300 text-base-content/70 border-t border-base-100">
      <p class="font-medium">Copyright © 2026 <span class="text-primary font-cyber">GuardiHack</span>. All rights reserved.</p>
      <div class="flex items-center gap-6">
        <a href="#" class="hover:text-primary transition-all">Contact Us</a>
        <div class="h-6 w-px bg-base-content/20"></div>
        <a href="#" class="hover:text-primary transition-all">Privacy Policy</a>
        <div class="h-6 w-px bg-base-content/20"></div>
        <a href="#" class="hover:text-primary transition-all">Trademark Policy</a>
      </div>
    </footer>

  </div>
</template>