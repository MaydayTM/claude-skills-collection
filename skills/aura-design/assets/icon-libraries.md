# 📦 Icon Libraries Reference

Quick reference for installing and using icon libraries in Aura Design projects.

---

## Primary: Solar Icons

**7,479 icons • 6 styles • 100% corner smoothing**

### Installation

```bash
# React / Next.js
npm install @solar-icons/react

# CDN (HTML)
<script src="https://code.iconify.design/3/3.1.0/iconify.min.js"></script>
```

### Usage

```jsx
// React
import { CalendarBoldDuotone } from '@solar-icons/react';
<CalendarBoldDuotone size={20} />

// HTML with Iconify
<span class="iconify" data-icon="solar:calendar-bold-duotone"></span>
```

### Style Guide
- **Bold Duotone** - Primary style (used in all brand profiles)
- **Linear** - Secondary, subtle icons
- **Broken** - Decorative, playful contexts

### Browse Icons
https://www.svgrepo.com/collection/solar-bold-duotone-icons/

---

## Secondary: Lucide

**Clean, consistent line icons**

```bash
npm install lucide-react
```

```jsx
import { ArrowRight, Check, X } from 'lucide-react';
<ArrowRight className="w-4 h-4" />
```

https://lucide.dev/icons/

---

## Brand Logos: Simple Icons

**SVG icons for popular brands**

```bash
npm install simple-icons
```

```jsx
import { siSlack, siStripe, siGithub } from 'simple-icons';
```

https://simpleicons.org/

---

## Other Recommended

| Library | Use Case | Link |
|---------|----------|------|
| MingCute | Alternative to Solar | https://www.mingcute.com/ |
| Heroicons | Tailwind ecosystem | https://heroicons.com/ |
| Phosphor | Flexible weights | https://phosphoricons.com/ |

---

## Iconify CDN (Universal)

Use any icon library via CDN:

```html
<script src="https://code.iconify.design/3/3.1.0/iconify.min.js"></script>

<!-- Solar -->
<span class="iconify" data-icon="solar:home-bold-duotone"></span>

<!-- Lucide -->
<span class="iconify" data-icon="lucide:arrow-right"></span>

<!-- Simple Icons -->
<span class="iconify" data-icon="simple-icons:github"></span>
```
