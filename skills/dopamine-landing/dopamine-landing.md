---
description: Dopamine-driven landing page design using the 5-level psychological framework
---

# Dopamine Landing Page Skill

Build high-converting landing pages using the **Dopamine Ladder** framework - a 5-section psychological structure that maximizes engagement through strategic stimulation, curiosity, anticipation, validation, and trust.

## Core Philosophy

The human brain responds to dopamine triggers in a predictable sequence. This skill structures landing pages to leverage these psychological phases:

1. **Stimulation** → Immediate visual impact (1-2 seconds)
2. **Engagement** → Open a curiosity loop (question without answer)
3. **Anticipation** → Build mystery and delay resolution ("edging")
4. **Validation** → Deliver the surprising answer/solution
5. **Affection** → Build trust and brand association

---

## Section 1: The Visual "Stun Gun" (Level 1: Stimulation)

**Goal:** Stop the scroll. Create immediate dopamine release through color, movement, and brightness.

### Design Elements
- **Movement & Contrast:** Use looping video, cinemagraph, or subtle animation in the hero section
- **High Visual Impact:** Bright colors, high contrast, immediate visual hierarchy
- **Micro-interactions:** Subtle hover effects or animated icons that react to user attention

### Content Rules
- **Word Count:** MINIMAL - only powerful headline + subheadline
- **Headline:** 5-10 words maximum, impactful and bold
- **Subheadline:** One short sentence (10-15 words)
- **Rule:** "The fewer words, the better" - reduce cognitive load

### Technical Implementation
```css
/* Hero section priorities */
- Video/animated background (autoplay, loop, muted)
- Font size: H1 = 48-72px, Subhead = 18-24px
- Animation: Fade-in on load (0.5-1s delay)
- Contrast ratio: minimum 7:1 for text/background
```

---

## Section 2: The Curiosity Loop (Level 2: Engagement)

**Goal:** Activate the brain with an unanswered question or unknown problem.

### Storytelling Technique
- **Open Question:** Pose a question in the reader's mind ("Why do they do it this way?" or "How is this possible?")
- **Contrast:** Compare familiar vs. shocking/unknown situations to raise stakes
- **Problem Amplification:** Make the reader aware of a problem they didn't know they had

### Content Rules
- **Word Count:** Short, punchy sentences
- **Typography:** Large, bold headlines to make the question stand out
- **Format:** Question → Problem statement → Hint of something different

### Example Structure
```
[Large, bold text]
"Why do 90% of landing pages fail in the first 3 seconds?"

[Medium text]
Most designers focus on features. Your visitors' brains 
don't care about features.

[Teaser]
There's a psychological pattern that changes everything...
```

---

## Section 3: Building the Mystery (Level 3: Anticipation)

**Goal:** Delay the answer and build tension ("edging" the story). Let dopamine rise before the reveal.

### Animation Elements
- **Scrollytelling:** Scroll-triggered animations that reveal content progressively
- **Parallax Scrolling:** Background moves slower than foreground for depth and immersion
- **Data Animation:** Single set of elements that regroup into new charts/visualizations as user scrolls
- **Progressive Disclosure:** Reveal information in steps, not all at once

### Content Rules
- **Word Count:** Minimal annotations (like presentation slides)
- **Format:** ~5 key words or very short phrases per visual element
- **Story Arc:** Build complexity step-by-step, withholding the final answer

### Technical Implementation
```javascript
// Scroll-triggered animation framework
- Use IntersectionObserver or scroll position
- Trigger animations at 50-80% viewport visibility
- Animate: opacity (0→1), translateY (50px→0), scale (0.8→1)
- Duration: 400-600ms per element
- Stagger animations: 100-150ms delay between elements
```

### Visual Strategy
- Use one cohesive visual metaphor that transforms
- Keep context visible (don't jump to disconnected graphics)
- Each scroll reveals one new piece of information
- Maximum 3-4 scroll-triggered sections

---

## Section 4: The Solution (Level 4: Validation)

**Goal:** Close the curiosity loop opened in Section 2. Deliver the dopamine reward.

### Storytelling Technique
- **Resolution:** Provide the answer, tip, or solution
- **Surprise Factor:** The answer must be non-trivial and unexpected
- **Proof:** Support with infographics, data visualization, or case studies

### Animation Elements
- **Interactive Elements:** Tooltips, hover effects on charts for deeper exploration
- **Reveal Animation:** Dramatic entrance for the solution (scale up, fade in)
- **Data Visualization:** Clean, modern charts that prove the point

### Content Rules
- **Word Count:** Still concise, but slightly more detailed
- **Format:** Clear statement of solution + supporting evidence
- **Visual Proof:** Use graphics to show before/after or comparison

### Example Structure
```
[Bold headline]
"The answer: Your brain decides in 0.05 seconds"

[Supporting visual]
[Animated infographic showing brain processing speed]

[Explanation - 2-3 short paragraphs]
Research shows the human brain processes images 60,000x 
faster than text. That's why the first visual frame 
determines everything.

[Data proof]
[Interactive chart showing conversion rates: Visual-first 
pages convert 3.2x better]
```

---

## Section 5: Trust & Value (Level 5-6: Affection & Revelation)

**Goal:** Create a "Pavlovian response" where seeing your brand triggers dopamine through association with value.

### Storytelling Technique
- **Humanity:** Show the people behind the brand/product
- **Attractiveness:** Use professional photos, passion, genuine smiles
- **Consistency:** Prove you're a reliable source of value (testimonials, case studies, track record)
- **Social Proof:** Leverages others' validation to build trust

### Content Rules
- **Word Count:** More generous than previous sections, but still scannable
- **White Space:** Isolate the main CTA and value proposition
- **Testimonials:** 2-3 powerful testimonials with photos
- **CTA:** One clear, prominent call-to-action

### Visual Strategy
- Human faces (team photos, founder story)
- Logos of clients/partners (if applicable)
- Clear, high-contrast CTA button
- Trust badges or certifications

---

## Technical Summary

### Core Rules for Implementation

1. **Visual Hierarchy Over Text**
   - Titles: Large and bold (36-72px)
   - Body text: Small and minimal (14-18px)
   - Maximize visual communication, minimize reading

2. **Word Count Guidelines**
   - Section 1: 15-25 words total
   - Section 2: 30-50 words total
   - Section 3: 5 words per scroll-triggered element
   - Section 4: 75-150 words total
   - Section 5: 150-250 words total

3. **Animation Triggers**
   - **Header (Section 1):** Auto-play on load (movement/video)
   - **Sections 2-4:** Scroll-triggered animations
   - **Section 5:** Hover interactions on CTA/testimonials

4. **Content Loop Structure**
   Every landing page must follow:
   ```
   Surprising Question → Mystery Building → Delayed Answer → Surprising Solution
   ```

5. **Typography Hierarchy**
   ```
   H1: 48-72px, bold, high contrast
   H2: 32-48px, bold
   H3: 24-32px, medium weight
   Body: 16-18px, regular
   Captions: 12-14px, light
   ```

6. **Scroll-triggered Sections**
   - Use smooth scroll behavior
   - Trigger animations at 60-80% viewport visibility
   - Each section should fit roughly in one viewport
   - Maximum 5-7 scroll sections total

---

## Usage Instructions

When creating a landing page with this skill:

1. **Identify the core question/problem** your product solves
2. **Create the curiosity gap** - what's the surprising insight?
3. **Map the story arc:**
   - What visual will stop the scroll?
   - What question opens the loop?
   - What mystery builds anticipation?
   - What's the surprising answer?
   - How do you prove trustworthiness?

4. **Apply the 5-section structure** with strict word limits
5. **Design visuals first, add minimal text** to support them
6. **Implement scroll-triggered animations** for sections 2-4
7. **Test the dopamine loop:** Does each section create the intended psychological response?

---

## Examples of Dopamine Triggers

### Visual Triggers (Section 1)
- Unexpected color combinations
- Movement in periphery
- High-contrast elements
- Faces looking at the viewer
- Bright, saturated colors

### Curiosity Triggers (Section 2)
- "What most people don't know about [topic]..."
- "The hidden reason why [common problem]..."
- "Why [surprising fact] changes everything..."

### Anticipation Triggers (Section 3)
- Progressive data reveals
- Transforming visualizations
- Step-by-step unveiling
- "Wait until you see what happens next..."

### Validation Triggers (Section 4)
- "Here's the truth:"
- Data-backed proof
- Unexpected statistics
- Before/after comparisons

### Trust Triggers (Section 5)
- Real faces with names
- Specific testimonials with details
- Recognized brand logos
- Transparent pricing/process

---

## Anti-Patterns to Avoid

❌ **Don't:** Wall of text in any section  
✅ **Do:** Maximum visual communication with minimal words

❌ **Don't:** Give away the answer in Section 2  
✅ **Do:** Build mystery and delay resolution until Section 4

❌ **Don't:** Use stock photos of random people  
✅ **Do:** Show real team members or authentic user photos

❌ **Don't:** Multiple CTAs competing for attention  
✅ **Do:** One clear, prominent CTA at the end

❌ **Don't:** Static, boring visuals throughout  
✅ **Do:** Movement, animation, and interactivity strategically placed

❌ **Don't:** Explain everything immediately  
✅ **Do:** Create gaps that the brain wants to close

---

## Measuring Success

A well-executed dopamine landing page should show:

- **Bounce rate:** <40% (people stay to see the resolution)
- **Scroll depth:** >70% reach Section 4 (the solution)
- **Time on page:** >60 seconds (engaged with the story)
- **Conversion rate:** 2-5x improvement over traditional pages

Track these metrics and iterate based on where users drop off.

---

## Credits & Research Foundation

This skill is based on research combining:
- Neuroscience of dopamine and reward prediction
- Visual processing and "bottom-up" attention
- Data storytelling and "scrollytelling" best practices
- Landing page optimization and conversion psychology

Use this skill to create landing pages that don't just inform—they captivate, engage, and convert by working *with* human psychology, not against it.
