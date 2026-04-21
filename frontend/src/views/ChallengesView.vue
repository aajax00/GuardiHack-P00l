<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ChallengeCard from '../components/ChallengeCard.vue'

const router = useRouter()

// --- PERSISTANCE DE L'ÉTAT ---
// On définit les données à l'extérieur ou on utilise un state persistant
// Ici, on initialise depuis le localStorage pour que ça survive même au rafraîchissement F5
const STORAGE_KEY = 'guardiahack_categories_state'

const categories = ref([
  {
    name: 'WEB', isCollapsed: false,
    challenges: [
      { id: 1, title: 'SQLi Bypasser', difficulty: 'Facile', points: 100, solved: true },
      { id: 2, title: 'XSS to Admin', difficulty: 'Moyen', points: 300, solved: false },
      { id: 3, title: 'SSTI Nightmare', difficulty: 'Difficile', points: 500, solved: false },
      { id: 9, title: 'CSRF Token', difficulty: 'Facile', points: 150, solved: false },
      { id: 10, title: 'GraphQL Leak', difficulty: 'Moyen', points: 400, solved: false },
    ]
  },
  {
    name: 'PWN', isCollapsed: false,
    challenges: [
      { id: 4, title: 'Buffer Overflow 101', difficulty: 'Facile', points: 100, solved: true },
      { id: 5, title: 'ROP Chain', difficulty: 'Moyen', points: 300, solved: true },
      { id: 6, title: 'Heap Exploitation', difficulty: 'Insane', points: 1000, solved: false },
    ]
  }
])

// Charger l'état au montage
onMounted(() => {
  const savedState = localStorage.getItem(STORAGE_KEY)
  if (savedState) {
    const parsed = JSON.parse(savedState)
    categories.value.forEach(cat => {
      if (parsed[cat.name] !== undefined) {
        cat.isCollapsed = parsed[cat.name]
      }
    })
  }
})

// Sauvegarder l'état quand on clique
const toggleCategory = (cat) => {
  cat.isCollapsed = !cat.isCollapsed
  const stateToSave = {}
  categories.value.forEach(c => stateToSave[c.name] = c.isCollapsed)
  localStorage.setItem(STORAGE_KEY, JSON.stringify(stateToSave))
}

const getProgress = (challenges) => {
  if (!challenges.length) return 0
  return Math.round((challenges.filter(c => c.solved).length / challenges.length) * 100)
}

const goToChallenge = (id) => {
  router.push(`/challenges/${id}`)
}
</script>

<template>
  <div class="max-w-[1320px] mx-auto w-full animate-fade-in pb-20 px-4">
    
    <div class="mb-10">
      <h1 class="block w-full text-center text-3xl font-cyber font-bold bg-primary text-base-100 py-3 uppercase tracking-widest shadow-sm">
        Challenges
      </h1>
    </div>

    <div class="space-y-10">
      <div v-for="cat in categories" :key="cat.name" class="w-full">
        
        <div class="flex flex-col sm:flex-row justify-between items-center py-4 border-b border-primary/40 gap-4 cursor-pointer hover:bg-primary/5 transition-all px-4 rounded-t-lg"
             @click="toggleCategory(cat)">
          
          <h2 class="text-2xl font-cyber text-primary tracking-widest">{{ cat.name }}</h2>
          
          <div class="flex items-center gap-6">
            <div class="flex items-center gap-3">
              <progress class="progress progress-primary w-32 md:w-48 bg-base-300" :value="getProgress(cat.challenges)" max="100"></progress>
              <span class="font-mono text-sm opacity-80 w-10 text-right">{{ getProgress(cat.challenges) }}%</span>
            </div>
            <button class="btn btn-sm btn-ghost btn-circle transition-transform duration-300" :class="{ 'rotate-180': cat.isCollapsed }">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" /></svg>
            </button>
          </div>
        </div>

        <transition name="expand">
          <div v-show="!cat.isCollapsed" class="overflow-hidden">
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-5 py-8">
              <ChallengeCard 
                v-for="chal in cat.challenges" 
                :key="chal.id" 
                :challenge="chal" 
                @open="goToChallenge"
              />
            </div>
          </div>
        </transition>

      </div>
    </div>
  </div>
</template>

<style scoped>
.animate-fade-in { animation: fadeIn 0.4s ease-out forwards; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

/* ANIMATION DE DÉFILEMENT (Expand/Collapse) */
.expand-enter-active, .expand-leave-active {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  max-height: 1000px; /* Une valeur assez haute pour contenir la grille */
}

.expand-enter-from, .expand-leave-to {
  max-height: 0;
  opacity: 0;
  transform: translateY(-20px);
}
</style>