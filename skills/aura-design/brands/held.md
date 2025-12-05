# 🟢 HELD Brand Profile

**Type:** Tech / Health / SaaS Platform  
**Theme:** Dark with Emerald Accents

---

## Color Palette

| Role | Tailwind | Hex |
|------|----------|-----|
| Primary | `emerald-400` | `#34D399` |
| Primary Dark | `emerald-500` | `#10B981` |
| Secondary | `sky-400` | `#38BDF8` |
| Background | `neutral-950` | `#0A0A0A` |
| Surface | `neutral-900` | `#171717` |
| Border | `neutral-800` | `#262626` |
| Text Primary | `slate-50` | `#F8FAFC` |
| Text Secondary | `slate-300` | `#CBD5E1` |

---

## Typography

```css
/* Primary Font */
font-family: 'Inter', sans-serif;

/* Alt Font (logos, headings) */
font-family: 'Bricolage Grotesque', sans-serif;

/* Headings */
.heading { 
  font-size: 40px - 64px;
  font-weight: 600;
  letter-spacing: -0.025em;
}

/* Labels */
.label {
  font-size: 11-12px;
  text-transform: uppercase;
  letter-spacing: 0.16em;
}
```

**Google Fonts:**
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Bricolage+Grotesque:wght@400;500;600;700&display=swap" rel="stylesheet">
```

---

## Design Patterns

### Glassmorphism Card
```html
<div class="bg-neutral-900/80 backdrop-blur-xl rounded-3xl p-6 border border-white/10 shadow-2xl">
```

### Emerald Glow CTA
```html
<button class="bg-emerald-500 text-neutral-900 px-6 py-3 rounded-full font-semibold shadow-[0_14px_35px_rgba(16,185,129,0.55)] hover:bg-emerald-400">
```

### Gradient Border Button
```html
<button class="relative inline-flex items-center gap-3 rounded-full bg-gradient-to-r from-emerald-400 via-emerald-500 to-sky-400 p-[1px]">
  <span class="inline-flex items-center gap-3 bg-neutral-50 rounded-full px-7 py-3 text-neutral-900">
    Button Text
  </span>
</button>
```

### Pulsing Status Dot
```html
<span class="relative flex h-2 w-2">
  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
  <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
</span>
```

### Particle Button (CSS)
```css
.btn-particles:hover .particle {
  animation: particle-float 1.1s ease-out infinite;
}
@keyframes particle-float {
  0% { transform: translate(0, 6px) scale(0.7); opacity: 0; }
  20% { opacity: 1; }
  100% { transform: translate(-4px, -26px) scale(0.2); opacity: 0; }
}
```

---

## Background Animations

**Landing Page:** `EET25BiXxR2StNXZvAzF`
```html
<div data-us-project="EET25BiXxR2StNXZvAzF" class="absolute w-full h-full"></div>
```

**Login/Auth:** `bmaMERjX2VZDtPrh4Zwx`
```html
<div class="saturate-0 brightness-50" data-us-project="bmaMERjX2VZDtPrh4Zwx"></div>
```

---

## Icon Libraries

**Primary:** Solar Icons - Bold Duotone
```bash
npm install @solar-icons/react
```

**Secondary:** Lucide
```bash
npm install lucide-react
```

---

## Example Use Cases

- Health tech dashboards
- AI assistants
- SaaS platforms
- Medical data browsers
- Login/auth screens
