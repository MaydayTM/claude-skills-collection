# Master Prompt: Marketing Studio Platform

## Project Visie

Bouw een **AI-native Marketing Studio** - een web platform dat meerdere Claude-powered skills combineert tot een complete marketing workflow. Dit platform gaat verder dan tools zoals Jasper AI door een geïntegreerde flow te bieden van brand creatie tot content productie.

---

## De User Journey

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        MARKETING STUDIO FLOW                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. BRAND FOUNDATION          2. DESIGN SYSTEM         3. WEBSITE          │
│  ┌─────────────────┐         ┌─────────────────┐      ┌─────────────────┐  │
│  │ Personal Brand  │────────▶│   Aura Design   │─────▶│Dopamine Landing │  │
│  │    Creator      │         │     System      │      │     Pages       │  │
│  └─────────────────┘         └─────────────────┘      └─────────────────┘  │
│         │                           │                        │             │
│         ▼                           ▼                        ▼             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        SUPABASE (Brand Vault)                       │   │
│  │  • Brand profiles    • Design tokens    • Generated assets         │   │
│  │  • Iterations        • Templates        • Content history          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│         │                                                                   │
│         ▼                                                                   │
│  4. CONTENT ENGINE (Future)                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Social Media Planner  │  Content Generator  │  Multi-platform     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

```yaml
Frontend:
  framework: Next.js 14+ (App Router)
  styling: Tailwind CSS + shadcn/ui
  state: Zustand of React Context
  forms: React Hook Form + Zod validation

Backend:
  api: Next.js API Routes
  ai: Claude API via Vercel AI SDK (@ai-sdk/anthropic)
  database: Supabase (PostgreSQL)
  auth: Supabase Auth
  storage: Supabase Storage (voor gegenereerde assets)

Deployment:
  hosting: Vercel
  domain: Custom domain naar keuze

Monorepo (optioneel):
  tool: Turborepo
  packages:
    - apps/web (hoofdapplicatie)
    - packages/skill-prompts (alle skill prompts)
    - packages/ui (gedeelde componenten)
    - packages/db (Supabase types & queries)
```

---

## Database Schema (Supabase)

```sql
-- Users (via Supabase Auth)

-- Brand Profiles (kern van alles)
CREATE TABLE brands (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  name TEXT NOT NULL,

  -- Brand Identity (output van Personal Brand Creator)
  mission TEXT,
  vision TEXT,
  values JSONB,
  voice_tone JSONB,
  target_audience JSONB,
  unique_value_proposition TEXT,
  brand_story TEXT,
  keywords TEXT[],

  -- Design Tokens (output van Aura Design)
  colors JSONB,          -- {primary, secondary, accent, neutrals}
  typography JSONB,      -- {headings, body, fonts}
  design_style TEXT,     -- 'glassmorphism', 'minimal', etc.

  -- Metadata
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  version INTEGER DEFAULT 1
);

-- Brand Iterations (voor versioning)
CREATE TABLE brand_iterations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  brand_id UUID REFERENCES brands(id),
  changes JSONB,
  feedback TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Generated Assets
CREATE TABLE generated_assets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  brand_id UUID REFERENCES brands(id),
  type TEXT NOT NULL,    -- 'landing_page', 'social_post', 'email', etc.
  skill_used TEXT,       -- 'dopamine-landing', 'aura-design', etc.
  content JSONB,         -- De gegenereerde content
  html TEXT,             -- Indien van toepassing
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Content Calendar (future)
CREATE TABLE content_calendar (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  brand_id UUID REFERENCES brands(id),
  platform TEXT,         -- 'linkedin', 'twitter', 'instagram', etc.
  scheduled_date DATE,
  content TEXT,
  status TEXT DEFAULT 'draft',
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## App Structuur

```
marketing-studio/
├── app/
│   ├── page.tsx                      # Landing page
│   ├── layout.tsx                    # Root layout met auth
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   ├── dashboard/
│   │   ├── page.tsx                  # Overview van brands
│   │   └── layout.tsx
│   ├── brand/
│   │   ├── new/page.tsx              # Brand Creator Wizard
│   │   └── [id]/
│   │       ├── page.tsx              # Brand detail/edit
│   │       ├── design/page.tsx       # Aura Design toepassen
│   │       ├── website/page.tsx      # Dopamine Landing builder
│   │       └── content/page.tsx      # (Future) Content planner
│   └── api/
│       ├── brand/
│       │   ├── create/route.ts       # Personal Brand Creator API
│       │   └── iterate/route.ts      # Brand refinement
│       ├── design/
│       │   └── generate/route.ts     # Aura Design API
│       ├── landing/
│       │   └── generate/route.ts     # Dopamine Landing API
│       └── content/
│           └── generate/route.ts     # (Future) Content API
├── components/
│   ├── brand/
│   │   ├── BrandWizard.tsx           # Multi-step brand creator
│   │   ├── BrandCard.tsx             # Brand preview card
│   │   └── BrandEditor.tsx           # Edit existing brand
│   ├── design/
│   │   ├── ColorPalette.tsx
│   │   ├── TypographyPreview.tsx
│   │   └── DesignPreview.tsx
│   ├── landing/
│   │   ├── SectionBuilder.tsx
│   │   ├── LivePreview.tsx
│   │   └── ExportOptions.tsx
│   └── shared/
│       ├── AIStreamingResponse.tsx   # Voor real-time AI output
│       ├── StepIndicator.tsx
│       └── LoadingStates.tsx
├── lib/
│   ├── supabase/
│   │   ├── client.ts
│   │   ├── server.ts
│   │   └── types.ts                  # Generated types
│   ├── prompts/
│   │   ├── personal-brand.ts         # Skill prompt
│   │   ├── aura-design.ts            # Skill prompt
│   │   ├── dopamine-landing.ts       # Skill prompt
│   │   └── index.ts                  # Prompt orchestration
│   └── utils/
│       └── brand-context.ts          # Inject brand in prompts
├── supabase/
│   └── migrations/                   # Database migrations
└── public/
    └── ...
```

---

## Skill Integration Pattern

Elke skill wordt een API endpoint met streaming:

```typescript
// lib/prompts/personal-brand.ts
export const personalBrandPrompt = (input: BrandInput) => `
Je bent een expert personal brand strateeg...

[VOLLEDIGE SKILL CONTENT UIT skills/personal-brand-creator/]

Input van gebruiker:
- Naam: ${input.name}
- Industrie: ${input.industry}
- Doelgroep: ${input.targetAudience}
- Kernwaarden: ${input.values}
...

Genereer een complete brand identity in JSON formaat:
{
  "mission": "...",
  "vision": "...",
  ...
}
`;

// app/api/brand/create/route.ts
import { streamText } from 'ai';
import { anthropic } from '@ai-sdk/anthropic';
import { personalBrandPrompt } from '@/lib/prompts/personal-brand';

export async function POST(req: Request) {
  const input = await req.json();

  const result = await streamText({
    model: anthropic('claude-sonnet-4-20250514'),
    prompt: personalBrandPrompt(input),
  });

  return result.toDataStreamResponse();
}
```

---

## Brand Context Injection

Wanneer een brand gemaakt is, wordt deze meegestuurd naar alle volgende skills:

```typescript
// lib/utils/brand-context.ts
export function injectBrandContext(brand: Brand, skillPrompt: string) {
  return `
## ACTIEVE BRAND CONTEXT
Alle output moet consistent zijn met deze brand:

**Brand:** ${brand.name}
**Mission:** ${brand.mission}
**Voice & Tone:** ${JSON.stringify(brand.voice_tone)}
**Kleuren:** ${JSON.stringify(brand.colors)}
**Target Audience:** ${JSON.stringify(brand.target_audience)}

---

${skillPrompt}
`;
}
```

---

## UI/UX Principes

1. **Wizard-based flows** - Stap voor stap, niet overweldigend
2. **Real-time streaming** - Zie AI denken en genereren
3. **Preview-first** - Altijd live preview van output
4. **Iteratie-friendly** - Makkelijk feedback geven en verfijnen
5. **Export ready** - Alles exporteerbaar (HTML, JSON, Markdown)
6. **Dark mode** - Gebruik het Aura Design system voor de app zelf

---

## Development Roadmap

### Phase 1: Foundation (MVP)
- [ ] Next.js project setup met Supabase
- [ ] Authentication flow
- [ ] Database schema implementatie
- [ ] Personal Brand Creator wizard
- [ ] Brand opslaan en bekijken

### Phase 2: Design Integration
- [ ] Aura Design skill integratie
- [ ] Design tokens genereren vanuit brand
- [ ] Live preview componenten
- [ ] Design export (Tailwind config, CSS variables)

### Phase 3: Website Builder
- [ ] Dopamine Landing skill integratie
- [ ] Section-based page builder
- [ ] Brand-consistent templates
- [ ] HTML/React export

### Phase 4: Content Engine
- [ ] Social Media Content Planner skill
- [ ] Multi-platform content generatie
- [ ] Content calendar
- [ ] Scheduling integratie

### Phase 5: Polish & Scale
- [ ] Team collaboration
- [ ] Brand guidelines PDF export
- [ ] API access voor externe tools
- [ ] White-label optie

---

## Start Commando

```bash
# In een nieuwe directory
npx create-next-app@latest marketing-studio --typescript --tailwind --eslint --app --src-dir=false

cd marketing-studio

# Installeer dependencies
npm install @supabase/supabase-js @supabase/ssr
npm install ai @ai-sdk/anthropic
npm install zustand
npm install zod react-hook-form @hookform/resolvers
npx shadcn@latest init

# Setup Supabase
npx supabase init
npx supabase start
```

---

## Referenties

- Skills source: `/skills/` directory in claude-skills-collection
- Bestaande brands: `skills/aura-design/brands/`
- Design patterns: `skills/aura-design/aura-design.md`
- Landing structure: `skills/dopamine-landing/`

---

## Succes Criteria

Het platform is succesvol wanneer een gebruiker kan:
1. ✅ In 10 minuten een complete brand identity creëren
2. ✅ Design tokens automatisch laten genereren
3. ✅ Een high-converting landing page bouwen zonder code
4. ✅ Content genereren die consistent is met hun brand
5. ✅ Alles itereren en verbeteren over tijd
