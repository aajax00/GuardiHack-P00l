<p align="center">
  <img src="https://img.shields.io/badge/Version-1.0.0-primary?style=for-the-badge&logo=github" alt="Version">
  <img src="https://img.shields.io/badge/Vue.js-3.x-4fc08d?style=for-the-badge&logo=vuedotjs" alt="VueJS">
  <img src="https://img.shields.io/badge/Tailwind-CSS-38bdf8?style=for-the-badge&logo=tailwindcss" alt="Tailwind">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
</p>

<p align="center">
<pre align="center">
   ______                     ___ __  __           __      ____  ____  ____  __
  / ____/_  ______ __________/ (_) / / /___ ______/ /__   / __ \/ __ \/ __ \/ /
 / / __/ / / / __ `/ ___/ __  / / /_/ / __ `/ ___/ //_/  / /_/ / / / / / / / / 
/ /_/ / /_/ / /_/ / /  / /_/ / / __  / /_/ / /__/ ,<    / ____/ /_/ / /_/ / /  
\____/\__,_/\__,_/_/   \__,_/_/_/ /_/\__,_/\___/_/|_|  /_/    \____/\____/_/   
                                                                             
        [ CTF PLATFORM v1.0 ]
</pre>
</p>

<p align="center">
  <b>Une plateforme de CTF moderne, immersive et haute performance.</b><br>
  Inspirée par l'esthétique et l'efficacité de CTFd.
</p>

---

## 🚩 À propos du projet

**GuardiHack P00l** est une plateforme de compétition de cybersécurité (Capture The Flag) conçue pour offrir une expérience utilisateur fluide et engageante. Que ce soit pour des challenges Web, PWN, ou Reverse, l'interface est optimisée pour la clarté et l'immersion.

### 🚀 Fonctionnalités Clés
- 📊 **Scoreboard Dynamique** : Graphiques en temps réel avec ECharts (lignes temporelles en escalier).
- 🏆 **Podium Neumorphique** : Visualisation des Top 3 avec avatars et médailles.
- 📂 **Gestion des Challenges** : Catégories rétractables avec persistance locale.
- 🩸 **First Blood** : Système de récompense visuelle pour le premier ayant résolu un défi.
- 📱 **Full Responsive** : Optimisé pour tous les écrans, du mobile au 4K.

---

## 🛠 Stack Technique

| Technologie | Usage |
| :--- | :--- |
| **Vue.js 3** | Framework Frontend (Composition API) |
| **Vite** | Build tool ultra-rapide |
| **Tailwind CSS** | Design atomique et responsive |
| **DaisyUI** | Composants UI Cyberpunk |
| **Apache ECharts** | Visualisation des données du Scoreboard |
| **Lucide Icons** | Set d'icônes minimalistes |

---

## 📂 Structure du Projet

```text
src/
├── assets/          # Images, logos et fonts (Press Start 2P, Roboto Mono)
├── components/      # Composants réutilisables (ChallengeCard, Navbar...)
├── views/           # Pages principales (Challenges, Scoreboard, Users...)
├── router/          # Configuration de Vue Router
└── main.js          # Point d'entrée et config Tailwind/Fonts
```

## ⚙️ Installation et Lancement
Suivez ces étapes pour cloner et lancer le projet sur votre machine locale :

### 1. Cloner le dépôt
```Bash
git clone [https://github.com/votre-username/guardihack-p00l.git](https://github.com/votre-username/guardihack-p00l.git)
cd guardihack-p00l
```
### 2. Installer les dépendances
```Bash
npm install
```
### 3. Lancer en mode développement
```Bash
npm run dev
Le projet sera accessible sur http://localhost:5173
```
### 4. Build pour la production
```Bash
npm run build
```
---

## 🎨 Design System
**Titres** : `'Press Start 2P', cursive (Style Retro-Gaming).`

**Code/Data** : `'Roboto Mono', monospace (Haute lisibilité).`

**Couleurs** :

`Primary : #00FF9F (Vert Néon)`

`Secondary : #FF0055 (Rose Cyber)`

`Background : #0F172A (Deep Slate)`


<p align="center">
Développé avec ❤️ par l'équipe <strong>GuardiHack</strong>
</p>
