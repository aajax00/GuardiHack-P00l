<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// --- ÉTAT DES ONGLETS ---
const activeTab = ref('challenge') // 'challenge' ou 'solves'

// --- SIMULATION DU CHALLENGE FETCHÉ ---
const challenge = ref({
  id: route.params.id,
  title: 'XSS to Admin',
  category: 'WEB',
  points: 300,
  difficulty: 'Moyen',
  solves: 5,
  hasInstance: true,
  description: `
    <p>Nous avons intercepté un portail d'administration d'une ancienne faction cybernétique. Votre objectif est de pénétrer les défenses et de récupérer le cookie de l'administrateur système.</p>
    <br>
    <p><strong>Règles d'engagement :</strong> Ne lancez pas de scanners automatisés (dirb, nikto, etc) sous peine de bannissement.</p>
    <p>Format du flag : <code class="bg-base-300 text-primary px-2 py-1 rounded font-mono">GH{...}</code></p>
  `,
  // Classé du plus ancien (First Blood) au plus récent
  solvers: [
    { username: 'CyberSlayer', date: '21 Avril 2026, 10:15' }, // <-- FIRST BLOOD
    { username: '0xGhost', date: '21 Avril 2026, 11:42' },
    { username: 'Vex_Root', date: '21 Avril 2026, 14:05' },
    { username: 'Alice_In_Pwn', date: '21 Avril 2026, 16:30' },
    { username: 'Bob_The_Hacker', date: '21 Avril 2026, 18:00' }
  ]
})

// --- GESTION DU FLAG ---
const flag = ref('')
const submissionStatus = ref(null)
const submissionMessage = ref('')

const submitFlag = () => {
  if (flag.value === 'GH{test}') {
    submissionStatus.value = 'success'
    submissionMessage.value = 'Correct ! Vous avez validé ce challenge.'
  } else {
    submissionStatus.value = 'error'
    submissionMessage.value = 'Flag incorrect. Essayez encore !'
    setTimeout(() => { submissionStatus.value = null }, 4000)
  }
}
</script>

<template>
  <div class="max-w-[1320px] mx-auto w-full animate-fade-in pb-20 pt-6 px-4">
    
    <button @click="router.push('/challenges')" class="btn btn-sm btn-ghost mb-8 font-mono text-base-content/60 hover:text-primary gap-2">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" /></svg>
      Retour aux challenges
    </button>

    <div class="flex border-b border-base-300 mb-8 w-full">
      <button 
        @click="activeTab = 'challenge'" 
        class="flex-1 py-3 text-center font-cyber tracking-widest transition-colors duration-200 text-lg"
        :class="activeTab === 'challenge' ? 'text-primary border-b-2 border-primary' : 'hover:bg-base-200/50 text-base-content/60'"
      >
        CHALLENGE
      </button>
      <button 
        @click="activeTab = 'solves'" 
        class="flex-1 py-3 text-center font-cyber tracking-widest transition-colors duration-200 text-lg"
        :class="activeTab === 'solves' ? 'text-primary border-b-2 border-primary' : 'hover:bg-base-200/50 text-base-content/60'"
      >
        {{ challenge.solves }} RÉSOLUTIONS
      </button>
    </div>

    <div class="min-h-[400px] w-full">

      <div v-show="activeTab === 'challenge'" class="animate-fade-in w-full">
        
        <div class="text-center mb-10">
          <h1 class="text-4xl md:text-5xl font-cyber text-primary mb-5">{{ challenge.title }}</h1>
          <div class="flex justify-center items-center gap-4 font-mono text-sm">
            <span class="text-base-content/70 font-bold uppercase">{{ challenge.category }}</span>
            <span class="opacity-30">|</span>
            <span class="text-primary font-bold text-lg">{{ challenge.points }} pts</span>
            <span class="opacity-30">|</span>
            <span class="text-base-content/70">{{ challenge.difficulty }}</span>
          </div>
        </div>

        <div class="prose prose-invert max-w-none text-base-content/80 leading-relaxed font-sans mb-12" v-html="challenge.description"></div>

        <div class="max-w-2xl mx-auto flex flex-col gap-6 mt-12">
          
          <div v-if="challenge.hasInstance" class="bg-base-200/50 p-3 rounded-lg flex items-center justify-between border border-base-300">
            <div class="flex items-center gap-2 font-mono text-sm text-secondary">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" /></svg>
              <span class="opacity-70">Environnement inactif</span>
            </div>
            <button class="btn btn-secondary btn-sm font-cyber tracking-wide px-6">
              DÉMARRER
            </button>
          </div>

          <form @submit.prevent="submitFlag" class="w-full">
            <div class="flex w-full gap-2">
              <input 
                v-model="flag" 
                type="text" 
                placeholder="GH{flag_ici}" 
                class="input input-sm input-bordered w-full bg-base-100 focus:border-primary font-mono text-center" 
                required 
                :disabled="submissionStatus === 'success'"
              />
              <button 
                type="submit" 
                class="btn btn-primary btn-sm px-8 font-bold font-cyber tracking-widest"
                :disabled="submissionStatus === 'success' || flag.length === 0"
              >
                SOUMETTRE
              </button>
            </div>
          </form>

          <transition name="fade">
            <div v-if="submissionStatus">
              <div v-if="submissionStatus === 'success'" class="alert alert-success bg-success/10 border border-success/30 text-success-content flex items-center justify-center gap-3 py-2 rounded-md">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 shrink-0 stroke-current text-success" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span class="font-bold text-sm">{{ submissionMessage }}</span>
              </div>
              <div v-if="submissionStatus === 'error'" class="alert alert-error bg-error/10 border border-error/30 text-error-content flex items-center justify-center gap-3 py-2 rounded-md">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 shrink-0 stroke-current text-error" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span class="font-bold text-sm">{{ submissionMessage }}</span>
              </div>
            </div>
          </transition>

        </div>

      </div>

      <div v-show="activeTab === 'solves'" class="animate-fade-in w-full">
        
        <div class="max-w-4xl mx-auto">
          <table class="table table-zebra w-full">
            <thead>
              <tr class="text-base-content/70 border-b border-base-300">
                <th class="font-normal text-sm pb-3">Utilisateur</th>
                <th class="font-normal text-sm pb-3 text-right">Date de validation</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(solver, index) in challenge.solvers" :key="index" class="border-none hover:bg-base-300/30 transition-colors">
                <td class="py-4">
                  <div class="flex items-center gap-3">
                    <router-link :to="`/users/`" class="font-bold font-mono text-primary hover:underline text-lg">
                      {{ solver.username }}
                    </router-link>
                    <span v-if="index === 0" class="text-xl" title="First Blood">🩸</span>
                  </div>
                </td>
                <td class="py-4 text-right text-base-content/60 font-mono text-sm">
                  {{ solver.date }}
                </td>
              </tr>
              <tr v-if="challenge.solvers.length === 0">
                <td colspan="2" class="text-center py-8 opacity-50 font-mono">
                  Aucune résolution pour le moment. Soyez le premier !
                </td>
              </tr>
            </tbody>
          </table>
        </div>

      </div>

    </div>
  </div>
</template>

<style scoped>
.animate-fade-in { animation: fadeIn 0.3s ease-out forwards; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

.fade-enter-active, .fade-leave-active { transition: all 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translateY(-5px); }
</style>