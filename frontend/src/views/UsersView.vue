<script setup>
import { ref, computed, watch } from 'vue'

const searchQuery = ref('')
const selectedPromo = ref('')
const currentPage = ref(1)
const itemsPerPage = 50

// --- SIMULATION DE DONNÉES ---
const generateUsers = () => {
  const users = []
  for (let i = 1; i <= 120; i++) {
    users.push({
      id: i,
      username: `Hacker_0x${i.toString(16).padStart(2, '0')}`,
      website: i % 3 === 0 ? `https://hacker${i}.net` : null,
      promo: i % 2 === 0 ? 'M1 Sécurité' : 'M2 Sécurité',
      avatarUrl: null // Pas d'avatar par défaut
    })
  }
  return users
}
const users = ref(generateUsers())

const filteredUsers = computed(() => {
  return users.value.filter(user => {
    const matchName = user.username.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchPromo = selectedPromo.value === '' || user.promo === selectedPromo.value
    return matchName && matchPromo
  })
})

const totalPages = computed(() => Math.ceil(filteredUsers.value.length / itemsPerPage))
const paginatedUsers = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredUsers.value.slice(start, end)
})

watch([searchQuery, selectedPromo], () => {
  currentPage.value = 1
})

// Remonter en haut quand on change de page
watch(currentPage, () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth' // Pour un effet de défilement fluide "Cyber"
  })
})
</script>

<template>
  <div class="w-full animate-fade-in">
    
    <div class="mb-10">
      <h1 class="block w-full text-center text-2xl font-cyber font-bold bg-primary text-base-100 py-2 uppercase tracking-widest shadow-sm">
        Utilisateurs
      </h1>
    </div>

    <div class="flex flex-col sm:flex-row gap-4 mb-6 w-full">
      <div class="form-control w-full sm:w-64 flex-shrink-0">
        <select v-model="selectedPromo" class="select select-bordered w-full bg-base-200 focus:border-primary transition-colors">
          <option value="">Toutes les promos</option>
          <option value="M1 Sécurité">M1 Sécurité</option>
          <option value="M2 Sécurité">M2 Sécurité</option>
        </select>
      </div>
      <div class="form-control w-full flex-grow">
        <input v-model="searchQuery" type="text" placeholder="Rechercher par nom..." class="input input-bordered w-full bg-base-200 focus:border-primary transition-colors" />
      </div>
    </div>

    <div class="overflow-x-auto w-full">
      <table class="table table-zebra w-full">
        <thead>
          <tr class="bg-transparent text-base-content/70 text-sm border-b border-base-content/20">
            <th class="w-1/2 font-normal pb-4">Utilisateur</th>
            <th class="font-normal pb-4">Site Web</th>
            <th class="font-normal pb-4">Promo</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in paginatedUsers" :key="user.id" class="border-none">
            <td class="py-4">
              <div class="flex items-center gap-4">
                <div class="avatar">
                  <div class="w-8 h-8 rounded bg-transparent">
                    <img v-if="user.avatarUrl" :src="user.avatarUrl" alt="avatar" />
                  </div>
                </div>
                <router-link :to="`/users/${user.id}`" class="font-bold text-base hover:text-primary transition-colors duration-200">
                  {{ user.username }}
                </router-link>
              </div>
            </td>
            <td class="py-4 text-base-content/80">
              <a v-if="user.website" :href="user.website" target="_blank" class="link link-hover hover:text-primary transition-colors flex items-center gap-2">
                {{ user.website }}
              </a>
            </td>
            <td class="py-4">
              <span class="text-sm opacity-80">{{ user.promo }}</span>
            </td>
          </tr>
          
          <tr v-if="paginatedUsers.length === 0">
            <td colspan="3" class="text-center py-8 text-base-content/50 font-medium">
              Aucun hacker trouvé.
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="flex justify-center mt-8" v-if="totalPages > 1">
      <div class="join shadow-sm">
        <button class="join-item btn btn-sm bg-base-200 hover:bg-primary hover:text-base-100 border-base-300" :disabled="currentPage === 1" @click="currentPage--">«</button>
        <button 
          v-for="page in totalPages" 
          :key="page" 
          class="join-item btn btn-sm border-base-300"
          :class="{ 'bg-primary text-base-100 pointer-events-none': currentPage === page, 'bg-base-200 hover:bg-base-300': currentPage !== page }" 
          @click="currentPage = page"
        >
          {{ page }}
        </button>
        <button class="join-item btn btn-sm bg-base-200 hover:bg-primary hover:text-base-100 border-base-300" :disabled="currentPage === totalPages" @click="currentPage++">»</button>
      </div>
    </div>
    
  </div>
</template>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.4s ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>