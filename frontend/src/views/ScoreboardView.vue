<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'

// --- ÉTAT ---
const viewMode = ref('global') // 'global' ou 'categories'
const chartRef = ref(null)
let chartInstance = null

// --- DONNÉES SIMULÉES (J'ai ajouté des avatars) ---
const top10Users = ref([
  { id: 1, username: 'Vex_Root', score: 2500, lvl: 42, color: '#ffd700', avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=Vex_Root' },
  { id: 2, username: '0xGhost', score: 2100, lvl: 38, color: '#c0c0c0', avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=0xGhost' },
  { id: 3, username: 'CyberSlayer', score: 1850, lvl: 35, color: '#cd7f32', avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=CyberSlayer' },
  { id: 4, username: 'Alice_In_Pwn', score: 1600, lvl: 30, color: '#ff3366' },
  { id: 5, username: 'Bob_The_Hacker', score: 1400, lvl: 28, color: '#33cc33' },
  { id: 6, username: 'NullPointer', score: 1250, lvl: 25, color: '#cccc00' },
  { id: 7, username: 'Root_Me', score: 1100, lvl: 22, color: '#ff9900' },
  { id: 8, username: 'ScriptKiddie', score: 950, lvl: 18, color: '#9933ff' },
  { id: 9, username: 'Flag_Hunter', score: 800, lvl: 15, color: '#3399ff' },
  { id: 10, username: 'BufferOver', score: 750, lvl: 14, color: '#cc3300' },
])

const categoryScores = ref([
  { name: 'WEB', top: top10Users.value.slice(0, 5) },
  { name: 'PWN', top: top10Users.value.slice(2, 7) },
  { name: 'REVERSE', top: top10Users.value.slice(1, 6) },
  { name: 'CRYPTO', top: top10Users.value.slice(3, 8) },
])

// --- CONFIGURATION ECHARTS (Basée sur le vrai TEMPS / Submissions) ---
const chartOptions = computed(() => {
  
  // Simulation d'une heure de début de CTF
  const startTime = new Date('2026-04-21T09:00:00').getTime()

  return {
    title: {
      text: 'TOP 10',
      left: 'center',
      top: 10,
      textStyle: { color: '#a6adbb', fontSize: 18, fontFamily: 'sans-serif', fontWeight: 'bold' }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' },
      // Formate la date dans le petit tooltip quand on survole
      formatter: function (params) {
        if (!params.length) return '';
        let date = new Date(params[0].value[0]).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
        let tooltipStr = `<div style="font-weight:bold;margin-bottom:5px;">${date}</div>`;
        params.forEach(p => {
          tooltipStr += `<div style="display:flex;justify-content:space-between;gap:15px;">
            <span><span style="display:inline-block;width:10px;height:10px;background-color:${p.color};border-radius:50%;margin-right:5px;"></span>${p.seriesName}</span>
            <span style="font-weight:bold;">${p.value[1]}</span>
          </div>`;
        });
        return tooltipStr;
      }
    },
    legend: {
      type: 'scroll',
      bottom: 0,
      textStyle: { color: '#888' },
      data: top10Users.value.map(u => u.username)
    },
    grid: {
      left: '2%', right: '3%', bottom: '12%', top: '15%', containLabel: true
    },
    xAxis: {
      type: 'time', // <-- C'EST ICI LA MAGIE : L'axe devient temporel !
      axisLabel: { 
        color: '#888',
        formatter: '{HH}:{mm}' // Affichage Heure:Minute sur l'axe
      },
      splitLine: { show: false }
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: '#888' },
      splitLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.05)' } }
    },
    series: top10Users.value.map(user => {
      // Pour l'exemple, on simule des heures de validation aléatoires pour chaque joueur
      const submission1 = startTime + Math.random() * 3600000;       // ~1h après
      const submission2 = submission1 + Math.random() * 7200000;     // ~2h après
      const submission3 = submission2 + Math.random() * 7200000;     // ~2h après
      const submission4 = new Date().getTime();                      // Heure actuelle

      return {
        name: user.username,
        type: 'line',
        step: 'end', // Conserve l'effet "Escalier"
        // Le format attendu : [Timestamp, Score Cumulé à ce moment-là]
        data: [
          [startTime, 0], 
          [submission1, Math.floor(user.score * 0.2)], 
          [submission2, Math.floor(user.score * 0.5)], 
          [submission3, Math.floor(user.score * 0.8)], 
          [submission4, user.score]
        ],
        itemStyle: { color: user.color || '#4b5563' },
        lineStyle: { width: 2 },
        symbolSize: 6
      }
    })
  }
})


// --- INITIALISATION DU GRAPHIQUE ---
const initChart = () => {
  if (chartRef.value) {
    if (!chartInstance) chartInstance = echarts.init(chartRef.value)
    chartInstance.setOption(chartOptions.value)
  }
}

const resizeChart = () => { if (chartInstance) chartInstance.resize() }

onMounted(() => {
  initChart()
  window.addEventListener('resize', resizeChart)
})

onUnmounted(() => {
  window.removeEventListener('resize', resizeChart)
  if (chartInstance) chartInstance.dispose()
})

watch(viewMode, async (newVal) => {
  if (newVal === 'global') {
    await nextTick()
    initChart()
  }
})
</script>

<template>
  <div class="w-full animate-fade-in pb-20">
    
    <div class="mb-6">
      <h1 class="block w-full text-center text-3xl font-cyber font-bold bg-primary text-base-100 py-3 uppercase tracking-widest shadow-sm">
        Scoreboard
      </h1>
    </div>

    <div class="flex justify-center mb-10 w-full">
      <div class="tabs tabs-boxed bg-base-300 p-1">
        <button @click="viewMode = 'global'" :class="['tab tab-lg px-8 font-cyber transition-all', viewMode === 'global' ? 'tab-active bg-primary text-base-100' : '']">
          Global
        </button>
        <button @click="viewMode = 'categories'" :class="['tab tab-lg px-8 font-cyber transition-all', viewMode === 'categories' ? 'tab-active bg-primary text-base-100' : '']">
          Catégories
        </button>
      </div>
    </div>

    <div v-if="viewMode === 'global'" class="w-full animate-fade-in flex flex-col items-center">
      
      <div class="w-full bg-base-200/50 pt-4 pb-2 px-2 rounded-xl border border-base-300 mb-10 shadow-lg">
        <div ref="chartRef" class="w-full h-[500px]"></div>
      </div>

      <div class="flex justify-center items-end gap-6 w-full mb-16 pt-4">
        
        <div class="flex flex-col items-center gap-2">
          <div class="card-neumorph second flex flex-col items-center justify-center p-4 text-center relative overflow-hidden"
               :style="{ backgroundImage: `linear-gradient(rgba(30,30,30,0.8), rgba(30,30,30,0.9)), url(${top10Users[1].avatar})`, backgroundSize: 'cover', backgroundPosition: 'center' }">
            <div class="text-3xl mb-1">🥈</div>
            <div class="font-bold text-sm truncate w-full px-1 text-white">{{ top10Users[1].username }}</div>
            <div class="text-gray-300 font-mono text-xs">{{ top10Users[1].score }} pts</div>
          </div>
          <div class="text-xs font-cyber opacity-60">#2</div>
        </div>

        <div class="flex flex-col items-center gap-2 z-10">
          <div class="card-neumorph first flex flex-col items-center justify-center p-4 text-center relative overflow-hidden"
               :style="{ backgroundImage: `linear-gradient(rgba(20,20,20,0.75), rgba(20,20,20,0.85)), url(${top10Users[0].avatar})`, backgroundSize: 'cover', backgroundPosition: 'center' }">
            <div class="text-6xl mb-2 animate-bounce drop-shadow-md">👑</div>
            <div class="font-black text-lg truncate w-full px-1 text-white drop-shadow-lg">{{ top10Users[0].username }}</div>
            <div class="text-yellow-400 font-mono text-base font-bold drop-shadow-lg">{{ top10Users[0].score }} pts</div>
          </div>
          <div class="text-sm font-cyber text-yellow-400 font-bold">#1</div>
        </div>

        <div class="flex flex-col items-center gap-2">
          <div class="card-neumorph third flex flex-col items-center justify-center p-4 text-center relative overflow-hidden"
               :style="{ backgroundImage: `linear-gradient(rgba(30,30,30,0.8), rgba(30,30,30,0.9)), url(${top10Users[2].avatar})`, backgroundSize: 'cover', backgroundPosition: 'center' }">
            <div class="text-3xl mb-1">🥉</div>
            <div class="font-bold text-sm truncate w-full px-1 text-white">{{ top10Users[2].username }}</div>
            <div class="text-orange-300 font-mono text-xs">{{ top10Users[2].score }} pts</div>
          </div>
          <div class="text-xs font-cyber opacity-60">#3</div>
        </div>

      </div>

      <div class="overflow-x-auto w-full">
        <table class="table table-zebra w-full">
          <thead>
            <tr class="text-base-content/70 text-sm border-b border-base-content/20">
              <th class="w-20 font-normal pb-4">Rank</th>
              <th class="font-normal pb-4">Utilisateur</th>
              <th class="font-normal pb-4">Score</th>
              <th class="font-normal pb-4">Level</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, index) in top10Users.slice(3)" :key="user.id" class="border-none">
              <td class="font-mono font-bold opacity-60 text-lg py-4">#{{ index + 4 }}</td>
              <td class="py-4">
                <router-link :to="`/users/${user.id}`" class="hover:text-primary font-bold text-base transition-colors flex items-center gap-3">
                  <img v-if="user.avatar" :src="user.avatar" class="w-6 h-6 rounded-full bg-base-300" />
                  {{ user.username }}
                </router-link>
              </td>
              <td class="font-mono py-4">{{ user.score }} pts</td>
              <td class="py-4">
                <div class="badge badge-outline border-base-content/20 text-xs py-2">{{ user.lvl }}</div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-8 w-full animate-fade-in">
      <div v-for="cat in categoryScores" :key="cat.name" class="bg-base-200/30 rounded-lg p-6 border border-base-300">
        <h3 class="font-cyber text-primary mb-4 border-b border-primary/20 pb-2 uppercase tracking-widest">{{ cat.name }}</h3>
        <table class="table table-sm w-full">
          <tbody>
            <tr v-for="(u, idx) in cat.top" :key="u.id" class="border-none hover:bg-base-300/50 transition-colors">
              <td class="w-10 opacity-50 font-mono py-3">#{{ idx + 1 }}</td>
              <td class="font-bold py-3 flex items-center gap-2">
                <img v-if="u.avatar" :src="u.avatar" class="w-5 h-5 rounded-full bg-base-300" />
                {{ u.username }}
              </td>
              <td class="text-right font-mono text-primary py-3">{{ Math.floor(u.score / 4) }} pts</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>

<style scoped>
.animate-fade-in { animation: fadeIn 0.3s ease-out forwards; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }

/* PODIUM AGRANDI ET ADAPTÉ POUR L'IMAGE DE FOND */
.card-neumorph {
  width: 160px; /* Plus grand */
  height: 200px;
  border-radius: 20px;
  background-color: var(--fallback-b2,oklch(var(--b2)));
  box-shadow: 10px 10px 20px rgba(0, 0, 0, 0.2),
             -10px -10px 20px rgba(255, 255, 255, 0.05);
  transition: transform 0.3s ease;
  border: 1px solid rgba(255,255,255,0.05);
}

.card-neumorph.first {
  width: 190px; /* Le numéro 1 est encore plus grand */
  height: 250px;
  /* Bordure dorée pour le roi */
  border: 3px solid #ffd700; 
  box-shadow: 0px 0px 30px rgba(255, 215, 0, 0.15);
}

.card-neumorph:hover { transform: translateY(-5px); }

/* Couleurs spécifiques pour le 2 et 3 */
.second { border-bottom: 6px solid #c0c0c0; } /* Argent */
.third { border-bottom: 6px solid #cd7f32; } /* Bronze */

/* Ombres douces pour le mode clair */
[data-theme='piscine-light'] .card-neumorph {
  box-shadow: 10px 10px 20px #c8c8c8, -10px -10px 20px #ffffff;
}
[data-theme='piscine-light'] .card-neumorph.first {
  box-shadow: 0px 0px 20px rgba(255, 215, 0, 0.4);
}
</style>