# 📱 Custom Mobile Brand Profile

**Type:** Mobile-First Apps (Social, Courses, Community)  
**Theme:** Dark with Flexible Accent Color

---

## Color Palette (Default - Swappable)

| Role | Tailwind | Hex | Notes |
|------|----------|-----|-------|
| Primary | `emerald-500` | `#10B981` | **Swap this!** |
| Primary Light | `emerald-400` | `#34D399` | |
| Background | `neutral-950` | `#0A0A0A` | |
| Surface | `neutral-900` | `#171717` | |
| Card | `neutral-800` | `#262626` | |
| Text Primary | `neutral-50` | `#FAFAFA` | |
| Text Secondary | `neutral-400` | `#A3A3A3` | |

**To change accent color:** Replace all `emerald` with your preferred color (e.g., `violet`, `rose`, `cyan`)

---

## Typography

```css
/* System Font (best for mobile) */
font-family: system-ui, -apple-system, sans-serif;

/* Labels */
.label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.16em - 0.22em;
}

/* Headings */
.heading {
  letter-spacing: -0.025em;
  font-weight: 500-600;
}
```

---

## Mobile-Specific Patterns

### Phone Frame Container
```html
<section class="max-w-md mx-auto bg-neutral-900 rounded-[2.2rem] border border-neutral-800 overflow-hidden shadow-2xl">
  <!-- Status bar -->
  <div class="px-5 pt-5 flex items-center justify-between text-[11px] text-neutral-300 border-b border-neutral-800/70 pb-3">
    <span>09:42</span>
    <div class="flex items-center gap-1.5">
      <span class="iconify" data-icon="solar:wifi-bold-duotone"></span>
      <span>Strong</span>
    </div>
  </div>
  <!-- Content -->
</section>
```

### Back Button
```html
<button class="inline-flex items-center gap-2 text-sm text-neutral-400 hover:text-neutral-100 rounded-full px-3 py-1 hover:bg-neutral-800/60 border border-transparent hover:border-neutral-700">
  <svg><!-- arrow-left icon --></svg>
  <span>Back</span>
</button>
```

### Avatar Stack
```html
<div class="flex items-center gap-4">
  <div class="flex -space-x-2">
    <img class="h-9 w-9 rounded-full border border-neutral-900 object-cover" src="..." alt="">
    <img class="h-9 w-9 rounded-full border border-neutral-900 object-cover" src="..." alt="">
    <img class="h-9 w-9 rounded-full border border-neutral-900 object-cover" src="..." alt="">
  </div>
  <!-- Add user button -->
  <button class="flex-none bg-emerald-500 text-neutral-900 w-9 h-9 rounded-full items-center justify-center">
    <svg><!-- user-plus icon --></svg>
  </button>
</div>
```

### Action Circle Buttons
```html
<!-- Primary -->
<button class="h-11 w-11 rounded-full bg-emerald-500 text-neutral-900 flex items-center justify-center shadow-lg">
  <svg><!-- play icon --></svg>
</button>

<!-- Secondary -->
<button class="h-10 w-10 rounded-full bg-neutral-800 text-neutral-300 flex items-center justify-center hover:bg-neutral-700">
  <svg><!-- icon --></svg>
</button>
```

### Course Schedule List
```html
<div class="space-y-2 text-sm">
  <div class="flex items-center justify-between gap-3 pb-2 border-b border-neutral-800/70">
    <div>
      <p class="text-[11px] text-neutral-500 uppercase tracking-[0.2em]">Lesson 01</p>
      <p class="text-neutral-50 font-medium tracking-tight">Lesson Title</p>
    </div>
    <p class="text-xs text-neutral-400">Feb 22 · 19:30</p>
  </div>
</div>
```

### Floating Overlay Card
```html
<div class="absolute bottom-0 translate-y-[60%] right-0">
  <div class="bg-neutral-900/95 backdrop-blur rounded-2xl border border-neutral-800 p-4 shadow-xl">
    <!-- Content -->
  </div>
</div>
```

### Meta Grid (3-column)
```html
<div class="grid grid-cols-3 gap-4 text-[11px] text-neutral-400 border-t border-neutral-800/70 pt-4">
  <div>
    <p class="uppercase tracking-[0.22em] font-medium">Label</p>
    <p class="mt-1 text-neutral-50 font-medium">Value</p>
  </div>
  <!-- ... -->
</div>
```

### Upload Action Strip
```html
<div class="rounded-2xl border border-dashed border-emerald-500/30 bg-gradient-to-r from-emerald-500/10 to-emerald-500/5 p-4 flex items-center justify-between gap-4">
  <div class="space-y-1">
    <p class="text-sm font-medium text-neutral-50">Upload your file</p>
    <p class="text-xs text-neutral-400">Description text</p>
  </div>
  <button class="px-4 py-2 rounded-full bg-emerald-500 text-neutral-900 text-sm font-medium">
    Upload
  </button>
</div>
```

---

## Background Animation

**Unicorn Studio ID:** `ZHhDKfVqqu8PKOSMwfuA`

```html
<div class="aura-background-component fixed top-0 w-full h-screen -z-10 saturate-200 blur-sm">
  <div data-us-project="ZHhDKfVqqu8PKOSMwfuA" class="absolute w-full h-full"></div>
</div>
```

---

## Icon Library

**Primary:** Solar Icons - Bold Duotone (via Iconify CDN for mobile web)
```html
<script src="https://code.iconify.design/3/3.1.0/iconify.min.js"></script>
<span class="iconify" data-icon="solar:play-bold-duotone"></span>
```

---

## Example Use Cases

- Course/learning apps
- Social media apps
- Community platforms
- Event apps
- Fitness trackers
- Chat/messaging
