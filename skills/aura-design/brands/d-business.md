# 🔶 D-Business Brand Profile

**Type:** AI Automation / n8n Courses / Tech Tools  
**Theme:** Dark with Orange Accents

---

## Color Palette

| Role | Tailwind/Custom | Hex |
|------|-----------------|-----|
| Primary | `orange-500` | `#F97316` |
| Primary Light | `orange-400` | `#FB923C` |
| Primary Dark | `orange-600` | `#EA580C` |
| Background | custom | `#0A0A0A` |
| Card Base | custom | `#151515` |
| Card Elevated | custom | `#1E1E1E` |
| Success | `green-500` | `#22C55E` |
| Accent | `blue-500` | `#3B82F6` |
| Text Primary | `gray-100` | `#F3F4F6` |
| Text Muted | `gray-500` | `#6B7280` |

---

## Typography

```css
/* Primary Font */
font-family: 'Geist', sans-serif;

/* Fallback */
font-family: 'Inter', sans-serif;

/* Headings */
.heading { 
  font-size: 40px - 80px;
  font-weight: 600;
  letter-spacing: -0.05em; /* tracking-tighter */
}

/* Card Numbers */
.card-number {
  font-family: monospace;
  letter-spacing: 0.1em;
  color: rgba(255,255,255,0.1);
}

/* Labels */
.label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: 700;
}
```

**Google Fonts:**
```html
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

---

## Design Patterns

### Spotlight Card (Mouse-following glow)
```css
.spotlight-card {
  --mouse-x: 0px;
  --mouse-y: 0px;
  position: relative;
  background: rgba(255, 255, 255, 0.02);
}
.spotlight-card::before {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: radial-gradient(800px circle at var(--mouse-x) var(--mouse-y), rgba(255,255,255,0.4), transparent 40%);
  opacity: 0;
  transition: opacity 0.5s;
}
.spotlight-card:hover::before { opacity: 1; }
```

### Animated Beam Border
```css
@keyframes beam-spin { to { transform: rotate(360deg); } }

.beam-button {
  position: relative;
}
.beam-button::before {
  content: "";
  position: absolute;
  inset: -100%;
  background: conic-gradient(from 0deg, transparent 0 300deg, #ea580c 360deg);
  animation: beam-spin 3s linear infinite;
}
```

### Glass Navigation
```css
.glass-nav {
  background: rgba(20, 20, 20, 0.6);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.05);
}
```

### Vertical Dashed Lines Background
```html
<div class="fixed inset-0 flex justify-center max-w-7xl mx-auto">
  <div class="w-full h-full border-x border-dashed border-white/5 flex justify-center">
    <div class="h-full w-px bg-white/5"></div>
  </div>
</div>
```

### JSON Code Preview
```html
<div class="bg-[#111] rounded-lg p-3 font-mono text-[10px] border border-white/5">
  <p><span class="text-purple-400">"key"</span>: <span class="text-green-400">"value"</span>,</p>
</div>
```

---

## Background Animation

**Unicorn Studio ID:** `iBWBCzr77BGdZpQZVZNN`

```html
<div class="aura-background-component fixed top-0 w-full h-screen -z-10">
  <div data-us-project="iBWBCzr77BGdZpQZVZNN" class="absolute w-full h-full"></div>
</div>
```

---

## Icon Libraries

**Primary:** Solar Icons - Bold Duotone
```bash
npm install @solar-icons/react
```

**Brands:** Simple Icons
```bash
npm install simple-icons
```

---

## Example Use Cases

- n8n automation courses
- AI tool landing pages
- Developer education
- Workflow builders
- SaaS pricing pages
