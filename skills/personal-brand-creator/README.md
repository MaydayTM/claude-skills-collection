# Personal Brand Creator

Een diepgaande Claude skill voor het bouwen van authentieke personal brands, gebaseerd op de methodologie van Chris Do (The Futur).

## Wat Deze Skill Doet

Deze skill begeleidt gebruikers door een **transformatief proces** van zelfontdekking naar een volledig uitgewerkte merkidentiteit en contentstrategie. Het is deels therapie, deels strategie.

### De 7-Fasen Journey

1. **SVA** - Smallest Viable Audience definiëren
2. **Positioning** - Love + Good at + Pays well triad
3. **Story** - Origin, Inciting Incident, Mentors, Enemies
4. **Values + Two-Word Brand** - Shadow + Transformer formule
5. **Gift** - Service Promise definiëren
6. **Brand Identity** - Naam, Tagline, ToV, Kleuren, Visueel
7. **Content Machine** - 911 regel + Platform strategie

## Installatie

```bash
# Kopieer naar je project
cp -r personal-brand-creator/ .agent/workflows/
```

Of gebruik direct vanuit de skills collection.

## Gebruik

### Volledige Journey
```
/personal-brand-creator
```
Start bij fase 1 en werk door alle fasen.

### Specifieke Oefening
```
/personal-brand sva          # Doelgroep definiëren
/personal-brand positioning  # Positionering bepalen
/personal-brand story        # Verhaal ontdekken
/personal-brand two-word     # Two-Word Brand maken
/personal-brand content      # Content plan maken
/personal-brand identity     # Visuele identiteit
```

## Mappenstructuur

```
personal-brand-creator/
├── personal-brand-creator.md      # Main entry point
├── README.md                      # Deze file
│
├── claude-context-pack/           # Methodologie + Oefeningen
│   ├── methodologie/
│   │   ├── methodology_01_workflow.md
│   │   ├── methodology_02_doorvragen.md
│   │   └── methodology_03_sales.md
│   ├── oefeningen/
│   │   ├── 01_sva.md
│   │   ├── 02_positioning_triad.md
│   │   ├── 03_story_discovery.md
│   │   ├── 04_values_two_word.md
│   │   ├── 05_gift_promise.md
│   │   ├── 06_empathy_map.md
│   │   ├── 07_content_911.md
│   │   └── 08_sales_prequal.md
│   └── templates/
│       └── templates.md
│
├── brand-identity/                # Visuele & Verbale Identiteit
│   ├── brand-name.md
│   ├── tagline.md
│   ├── tone-of-voice.md
│   ├── color-palette.md
│   └── visual-style.md
│
├── generators/                    # Brainstorm Tools
│   └── two-word-brand-generator.md
│
├── content-strategy/              # Platform Strategie
│   └── platform-strategy.md
│
└── examples/                      # Voorbeelden
    ├── casestudies.md
    └── two-word-brands.md
```

## Kernconcepten

### De 911 Waarderegel
- **9x Waarde** - Educatie, tips, inzichten
- **1x Persoonlijk** - Verhaal, kwetsbaarheid
- **1x Ask** - CTA, aanbod

### Two-Word Brand Formule
```
(Shadow Word) + (Transformer Word) = Two-Word Brand
```

**Voorbeeld:** "Loud Introvert" (Chris Do)

### De 3 Trust Engines
1. **Authenticiteit** - Ben je wie je zegt dat je bent?
2. **Empathie** - Geef je oprecht om anderen?
3. **Logica** - Is je aanpak zinvol?

## Coaching Stijl

Deze skill coacht Socratisch:
- Stelt vragen i.p.v. antwoorden geven
- Accepteert geen oppervlakkige antwoorden
- Pushed door naar diepte
- Valideert met strenge output checks

## Bronnen

Gebaseerd op publiek beschikbare content van:
- [The Futur](https://thefutur.com)
- [Chris Do op LinkedIn](https://linkedin.com/in/thechrisdo)
- [The Futur YouTube](https://youtube.com/@thefutur)

## Licentie

Voor persoonlijk en commercieel gebruik. Methodologie eigendom van Chris Do / The Futur.
