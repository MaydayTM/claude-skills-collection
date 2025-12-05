# 🥋 Reconnect Academy Brand Profile

**Type:** MMA Gym / Vechtsport CRM  
**Theme:** Dark Premium with Amber Accents

---

## Color Palette

| Role | Tailwind | Hex |
|------|----------|-----|
| Primary | `amber-300` | `#FCD34D` |
| Primary Light | `amber-100` | `#FEF3C7` |
| Primary Hover | `amber-200` | `#FDE68A` |
| Background | `neutral-950` | `#0A0A0A` |
| Surface | `neutral-900` | `#171717` |
| Border | `neutral-800` | `#262626` |
| Success | `emerald-400` | `#34D399` |
| Text Primary | `neutral-50` | `#FAFAFA` |
| Text Secondary | `neutral-400` | `#A3A3A3` |

---

## Typography

```css
/* Font */
font-family: 'Inter', sans-serif;

/* Headings */
.heading { 
  font-size: 40px - 80px;
  font-weight: 600;
  letter-spacing: -0.025em; /* tracking-tight */
}

/* Labels */
.label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.22em;
}
```

**Google Fonts:**
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

---

## Design Patterns

### Glassmorphism Card
```html
<div class="bg-gradient-to-br from-white/10 to-white/0 rounded-3xl p-6 backdrop-blur-xl border border-white/10">
```

### Amber Glow CTA
```html
<button class="bg-amber-300 text-neutral-950 px-6 py-3 rounded-full font-medium shadow-[0_16px_40px_rgba(251,191,36,0.55)] hover:bg-amber-200">
```

### Status Indicator
```html
<div class="flex items-center gap-2">
  <span class="h-1.5 w-1.5 rounded-full bg-emerald-400 shadow-[0_0_12px_rgba(52,211,153,0.65)]"></span>
  <span class="text-xs uppercase tracking-[0.22em] text-neutral-400">Live</span>
</div>
```

### KPI Card
```html
<div class="bg-gradient-to-br from-white/10 to-white/0 rounded-2xl p-4" style="--border-gradient: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0));">
  <p class="text-[11px] uppercase tracking-[0.22em] text-neutral-500">Label</p>
  <p class="mt-2 text-[20px] font-medium text-neutral-50">Value</p>
</div>
```

---

## Background Animation

**Unicorn Studio ID:** `HzcaAbRLaALMhHJp8gLY`

```html
<div class="aura-background-component fixed top-0 w-full h-screen -z-10 hue-rotate-90 brightness-150 saturate-0"
     style="mask-image: linear-gradient(to bottom, transparent, black 0%, black 15%, transparent);">
  <div data-us-project="HzcaAbRLaALMhHJp8gLY" class="absolute w-full h-full"></div>
</div>
```

---

## Icon Library

**Primary:** Solar Icons - Bold Duotone
```bash
npm install @solar-icons/react
```

---

## Example Use Cases

- Gym CRM Dashboard
- Member management
- Class scheduling
- Lead pipeline
- Payment tracking
