<script setup>
import { computed } from 'vue'

const props = defineProps({
  challenge: { type: Object, required: true }
})

defineEmits(['open'])

const marqueeText = computed(() => (props.challenge.title + ' — ').repeat(6))

const difficultyColor = computed(() => {
  switch (props.challenge.difficulty.toLowerCase()) {
    case 'facile': return 'text-success border-success'
    case 'moyen': return 'text-warning border-warning'
    case 'difficile': return 'text-error border-error'
    case 'insane': return 'text-purple-500 border-purple-500'
    default: return 'text-info border-info'
  }
})
</script>

<template>
  <a href="#" class="card" @click.prevent="$emit('open', challenge.id)">
    <div class="card-container border border-base-300" :class="{ 'border-success shadow-[0_0_15px_rgba(0,255,0,0.2)]': challenge.solved }">
      
      <div class="absolute top-3 left-3 z-10">
        <span class="px-2 py-0.5 text-[10px] font-mono border rounded uppercase bg-base-100/50 backdrop-blur-sm" :class="difficultyColor">
          {{ challenge.difficulty }}
        </span>
      </div>

      <div class="absolute top-3 right-3 z-10 font-mono font-bold text-sm">
        <span v-if="challenge.solved" class="text-success text-xl">✔</span>
        <span v-else class="text-primary">{{ challenge.points }} pts</span>
      </div>

      <div class="card-icon font-cyber text-5xl opacity-10">
        {{ challenge.points }}
      </div>

      <div class="preview-text font-cyber font-bold text-lg flex items-center gap-2">
        {{ challenge.title }}
      </div>

      <div class="card-circle bg-primary"></div>
      <div class="text-wrapper text-base-100">{{ marqueeText }}</div>
      
    </div>
  </a>
</template>

<style scoped>
.card { text-decoration: none; display: block; width: 100%; }

.card-container {
  position: relative;
  background: var(--fallback-b2, oklch(var(--b2)));
  color: var(--fallback-bc, oklch(var(--bc)));
  width: 100%;
  height: 150px; /* Nouvelle hauteur fixe */
  transition: all 0.3s ease-out;
  overflow: hidden;
  border-radius: 10px;
}

.card-icon {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  transition: 0.3s;
}

.preview-text {
  position: absolute;
  bottom: 0; left: 0;
  padding: 15px; /* Réduit pour la petite hauteur */
  z-index: 10;
  transition: color 0.3s;
}

.card-circle {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%) scale(0);
  width: 250px; height: 250px;
  border-radius: 100%;
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1;
}

.card-container:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
}
.card-container:hover .card-circle { transform: translate(-50%, -50%) scale(2.5); }
.card-container:hover .card-icon { opacity: 0; }
.card-container:hover .preview-text { color: var(--fallback-b1, oklch(var(--b1))); }

.text-wrapper {
  position: absolute; top: 50%; left: -20%;
  transform: translate(0, -50%);
  font-family: 'Courier New', monospace;
  font-size: 35px; /* Plus petit */
  font-weight: 900;
  text-transform: uppercase;
  white-space: nowrap;
  transition: 0.2s ease-out;
  animation: float-left 15s linear infinite;
  z-index: 2; opacity: 0; pointer-events: none;
}
@keyframes float-left {
  0% { transform: translate(0, -50%); }
  100% { transform: translate(-50%, -50%); }
}
.card-container:hover .text-wrapper { opacity: 0.3; }
</style>