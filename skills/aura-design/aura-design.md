---
description: Create stunning dark-mode web designs with aura.builder-inspired aesthetics. Supports 4 brand profiles with pre-configured colors, typography, and patterns.
---

# 🎨 Aura Design Skill

Build modern, dark-themed web interfaces with glassmorphism, icon libraries, and animated backgrounds.

## Step 1: Select Brand Profile

**Ask the user which brand this project is for:**

| Brand | Command | Primary Color | Use Case |
|-------|---------|---------------|----------|
| 🥋 Reconnect Academy | `reconnect` | Amber/Gold | MMA, Gym CRM |
| 🟢 HELD | `held` | Emerald | Tech, Health, SaaS |
| 🔶 D-Business | `d-business` | Orange | AI, Automation |
| 📱 Custom/Mobile | `custom` | Flexible | Mobile Apps |

**Load the brand profile from:** `.agent/workflows/brands/[brand-name].md`

---

## Step 2: Install Icon Libraries

**Prompt the user to install icon libraries:**

```bash
# Primary - Solar Icons (7,479 icons, 6 styles)
npm install @solar-icons/react

# Secondary - Lucide (clean, consistent)
npm install lucide-react

# Optional - Brand logos
npm install simple-icons
```

**For HTML/CDN projects:**
```html
<script src="https://code.iconify.design/3/3.1.0/iconify.min.js"></script>
```

---

## Step 3: Apply Design System

**Based on the selected brand, apply:**

1. **Color palette** - Use exact Tailwind classes from brand profile
2. **Typography** - Load Google Fonts specified in brand
3. **Design patterns** - Reference component patterns in brand file
4. **Animations** - Use Unicorn Studio background ID from brand

---

## Step 4: Background Animation Setup

**For animated backgrounds, add this to the HTML:**

```html
<div class="aura-background-component fixed top-0 w-full h-screen -z-10">
  <div data-us-project="[UNICORN_STUDIO_ID]" class="absolute w-full h-full"></div>
  <script type="text/javascript">
    !function(){if(!window.UnicornStudio){window.UnicornStudio={isInitialized:!1};
    var i=document.createElement("script");
    i.src="https://cdn.jsdelivr.net/gh/hiunicornstudio/unicornstudio.js@v1.4.29/dist/unicornStudio.umd.js";
    i.onload=function(){window.UnicornStudio.isInitialized||(UnicornStudio.init(),window.UnicornStudio.isInitialized=!0)};
    (document.head || document.body).appendChild(i)}}();
  </script>
</div>
```

**Replace `[UNICORN_STUDIO_ID]` with the ID from the brand profile.**

---

## Step 5: Component Patterns

**Use these shared patterns across all brands:**

### Glassmorphism Card
```html
<div class="bg-gradient-to-br from-white/10 to-white/0 rounded-3xl p-6 backdrop-blur-xl"
     style="position: relative; --border-gradient: linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0)); --border-radius-before: 24px">
  <!-- Content -->
</div>
```

### Glow Button (Primary)
```html
<button class="inline-flex items-center rounded-full bg-[PRIMARY_COLOR] text-neutral-950 px-6 py-3 font-medium shadow-[0_16px_40px_rgba(PRIMARY_RGB,0.55)] hover:brightness-110 transition">
  Button Text
</button>
```

### Status Dot
```html
<span class="h-2 w-2 rounded-full bg-emerald-400 shadow-[0_0_12px_rgba(52,211,153,0.65)]"></span>
```

---

## Quick Reference

| Resource | Link |
|----------|------|
| Solar Icons | https://www.svgrepo.com/collection/solar-bold-duotone-icons/ |
| Lucide Icons | https://lucide.dev/icons/ |
| Google Fonts | https://fonts.google.com/ |
| Tailwind CSS | https://tailwindcss.com/docs |
| Unicorn Studio | https://unicorn.studio/ |
