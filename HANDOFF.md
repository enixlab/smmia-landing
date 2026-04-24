# 🚀 SMMIA Landing — Handoff Document

> **Dernière mise à jour :** 2026-04-24
> **Destinataire :** Repreneur du projet
> **Projet :** Bannière Hero SMMIA + Landing page complète

---

## 🌐 Production

- **URL live :** https://smmia-landing.vercel.app
- **Vercel project :** `enix-lab/smmia-landing`
- **Compte Vercel :** enix.lab.ai@gmail.com (enix-lab)

⚠️ **Webhook GitHub → Vercel cassé** — les push sur `main` ne déclenchent pas de rebuild automatique. **Deploy manuel obligatoire** (voir section Commandes).

---

## 📦 Repos GitHub

Deux remotes pointent sur le même code :

| Remote | URL | Usage |
|---|---|---|
| `enixlab` | https://github.com/enixlab/smmia-landing | **Principal** (code source de prod) |
| `origin` | https://github.com/val-ecom/smmia-landing | Miroir (val-ecom) |

- **Branche active :** `main`
- **Historique complet :** préservé dans les 2 remotes

---

## 🛠️ Stack technique

- **Framework :** Astro 6.1.5 (SSG)
- **CSS :** Tailwind 4 + CSS custom inline
- **Animations :** GSAP 3.15
- **Vidéo :** HLS.js
- **3D :** Spline Viewer (web component)
- **Runtime :** Node ≥22.12.0
- **Deploy :** Vercel

---

## 📂 Structure critique

```
smmia-landing/
├── src/
│   ├── layouts/
│   │   └── Layout.astro       # Layout global, theme toggle, Spline loader
│   ├── components/
│   │   ├── Hero.astro         # ⭐ Bannière Hero (port Claude Design V4 Light)
│   │   ├── Navbar.astro
│   │   └── ... (autres sections de la landing)
│   └── styles/
│       └── global.css
├── public/
│   ├── hero-icons/            # Icônes des coins du Hero
│   │   ├── claude.png         # Sunburst orange
│   │   ├── gemini.png         # Diamant bleu/violet
│   │   ├── n8n.png
│   │   └── shopify.png        # Sac vert
│   ├── spline/
│   │   └── earth.splinecode   # Backup Spline local (pas utilisé actuellement)
│   └── images/
│       └── logos/             # Logo SMMIA, favicons
├── astro.config.mjs
├── package.json
└── HANDOFF.md                 # ← Ce fichier
```

---

## ⚡ Commandes

```bash
# 1. Clone
git clone https://github.com/enixlab/smmia-landing.git
cd smmia-landing
npm install

# 2. Dev local
npm run dev
# → http://localhost:4321

# 3. Build
npm run build
# → génère ./dist/

# 4. Preview build local
npm run preview

# 5. Deploy prod (MANUEL — webhook cassé)
export VERCEL_TOKEN="vcp_XXXXXXXXXXXXX"   # À régénérer (ancien token a pu être rotaté)
npx vercel deploy --prod --yes --token="$VERCEL_TOKEN"
```

---

## 🎨 Bannière Hero — État actuel

### Source de design

- **Projet Claude Design :** [SMMIA Hero v4 Light.html](https://claude.ai/design/p/6cb92b07-fe86-4062-8949-d8f47fb566dd?file=SMMIA+Hero+v4+Light.html)
- Le Hero.astro est un **port EXACT** de ce design Claude Design (React JSX + Tailwind transpilé en Astro + CSS custom)

### Éléments

- Fond blanc pur + halo violet soft animé
- Grille carrés 60×60 violet très subtil
- Planète 3D Spline (`RhEy0ALrUQlCxkVR`) avec filtres DAY (brightness + saturate)
- Logo **SMM** outline blanc + **IA** néon violet (Barlow Condensed italic 900)
- Tagline bas : TON AGENCE RENTABLE / **BOOSTÉE** (néon violet méga) / PAR L'IA
- 4 icônes PNG flottantes aux coins avec animations float + spin
  - TL : Claude (sunburst orange)
  - TR : Gemini (diamant bleu)
  - BL : N8N
  - BR : Shopify (sac vert)

### Fichier clé

`src/components/Hero.astro` — tout-en-un (HTML + CSS + JS inline)

---

## 🐞 BUGS CONNUS / TODO

### 1. ⚠️ Planète elliptique sur desktop large

**Problème :** Le canvas Spline est rendu en 1440×1080 (aspect 4:3) mais stretch-é dans un container carré → planète ovale sur desktop/tablet.

**Fix tenté (voir WIP en bas de `Hero.astro`) :**
- Re-setting `canvas.style.width/height` + `canvas.width/height` (drawing buffer) pour forcer carré
- Problème : modifier `canvas.width` reset le WebGL context, peut casser Spline
- Infinite loop quand on dispatche `resize` event

**Solution recommandée :**
- Soit utiliser le wrapper officiel Spline pour React/Vue avec resize observer natif
- Soit réduire le `.planet-stage` à une taille qui évite le stretch (ex: fixer à 780px carré)
- Soit utiliser un autre Spline scene avec aspect 1:1 natif

### 2. ⚠️ Section Dashboard pas responsive mobile

**Problème :** Sur mobile (390×844), la section "Dashboard" est **beaucoup trop longue** → l'utilisateur doit scroller énormément.

**Solution :** Réduire les hauteurs, paddings verticaux, tailles de cards dans le composant correspondant (à trouver dans `src/components/` — probablement `CRMSection.astro` ou `Dashboard.astro`).

### 3. ⚠️ Watermark Spline "Built with Spline"

**Statut :** Masqué via injection CSS dans le shadow DOM du `<spline-viewer>` (voir `Hero.astro` fonction `nukeSplineWatermark`).

**Fonctionne :** oui, après 800ms environ.

**À savoir :**
- NE PAS supprimer l'élément `<a id="logo">` du shadow DOM → casse Spline
- NE PAS modifier `canvas.width/height` sans stratégie anti-boucle
- Le seul moyen propre est l'injection d'un `<style>` avec `display: none !important`

### 4. ⚠️ Webhook Vercel inactif

- Les push sur `main` ne déclenchent **pas** de rebuild Vercel
- Reconnecter le webhook GitHub → Vercel dans les settings du projet Vercel
- En attendant : deploy manuel obligatoire

---

## 🎯 Design System SMMIA

### Couleurs

```css
--violet-100: #F3E8FF;
--violet-300: #D8B4FE;
--violet-500: #A855F7;  /* Principal */
--violet-700: #7C3AED;
--violet-900: #4C1D95;
--ink: #1A0933;         /* Texte principal */
```

### Fonts

- **Headlines :** Oswald 900, Archivo Black, Barlow Condensed italic
- **UI :** Inter, IBM Plex Sans
- **Mono :** JetBrains Mono, IBM Plex Mono

### Règles absolues

- **Fond BLANC uniquement** — pas de dark mode agressif
- **Palette violette** — pas d'orange (sauf sunburst Claude logo)
- **3D/Neon** pour les accents SMMIA
- Grille 60×60 pour les fonds subtils

---

## 🔐 Secrets & Tokens

⚠️ **À rotater / régénérer côté nouveau propriétaire :**

1. **Vercel token** (l'ancien a été rotaté/transféré hors du repo)
   - Régénérer sur https://vercel.com/account/tokens
   - Obtenir le token actuel directement auprès du propriétaire original (Enix)
2. **GitHub PAT** embarqué dans `.git/config` (remote URLs)
   - Nettoyer via `git remote set-url enixlab https://github.com/enixlab/smmia-landing.git` (utiliser SSH ou auth GitHub CLI)
3. **Aucun `.env`** n'est committé — tout est inline dans le code

---

## 📝 Historique des 10 derniers commits

```
5146126 fix(hero): kill infinite resize loop + remove double spline-viewer loader
db343dd fix(hero): restore visible Earth — dial back brightness filter
9e0dac3 fix(hero): diminue halo violet (opacity 0.12) + retire encadré blanc du watermark
b797755 feat(hero): update to SMMIA Hero v4 Light LATEST from Claude Design
e3a7eff feat(hero): port EXACT du rendu Claude Design "SMMIA Hero v4 Light"
0ce5857 fix(hero): utilise la VRAIE Terre c1hpRlTUtuLLXEFU (scène Spline du site live)
b247626 feat(hero): port EXACT du rendu Claude Design — SMMIA Hero Banner premium
9909e81 copy(programme): aligne titres/sous-titres cartes piliers
003797a feat(programme): remplace les 5 visuels piliers par nouveaux PNG + cache-bust
a6792ce feat(hero): bannière fond BLANC — brand SMMIA Signal Blue + Prism palette
```

---

## 🤝 Contact

- **Propriétaire original :** Enix Lab (enix.lab.ai@gmail.com)
- **Société :** ENIX LAB SAS

Bon courage pour la suite 🚀
