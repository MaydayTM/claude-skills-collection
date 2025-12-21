# 🚀 HELD SKILL - SNELLE SETUP VOOR CLAUDE CODE

## STAP 1: Open Claude Code
```bash
claude-code
```

## STAP 2: Plak deze EXACTE instructie

```
Ik wil een skill maken voor HELD precision health dashboards.

TAAK: Maak de skill in /mnt/skills/user/held-precision-health/

Ik heb 3 bestanden voor je die je EXACT moet gebruiken:

1. HELD_SKILL_COMPLETE.md - Dit is de complete documentatie
2. mario_example_for_skill.html - Dit is het voorbeeld dashboard (gebruik als template)
3. brand_config.json - HELD brand configuratie

BELANGRIJKE INSTRUCTIES:

1. Lees EERST de volledige SKILL.md documentatie
2. Gebruik mario_example_for_skill.html als basis template
3. Implementeer EXACT de parsing logica zoals beschreven in SKILL.md
4. Focus op:
   - Bloedwaarden parsing met "Opt:" range prioriteit
   - DNA methylatie parsing met genotype extractie
   - Supplement protocol generatie op basis van varianten
   - 3-maanden gefaseerd plan
   - Juridische disclaimer (VERPLICHT)

5. Maak deze bestanden:
   /mnt/skills/user/held-precision-health/
   ├── SKILL.md (copy from HELD_SKILL_COMPLETE.md)
   ├── held_dashboard_generator.py (implementeer de HELDDashboardGenerator class)
   ├── config/
   │   └── brand_config.json (copy from brand_config.json)
   └── examples/
       └── mario_example.html (copy from mario_example_for_skill.html)

6. TEST de skill met Mario's data:
   - Patient: Mario
   - Consult datum: 2025-11-05
   - Gebruik de blood/DNA data uit het voorbeeld

KRITIEKE REGELS:
- NOOIT medische waarden raden
- ALTIJD "Opt:" ranges gebruiken voor status bepaling
- CBS upregulatie (rs234706 AA) = KRITIEK - choline VOOR B-vitamines
- Juridische disclaimer is VERPLICHT
- PDF export functionaliteit includen

Start nu met het maken van de skill!
```

## STAP 3: Geef Claude Code de bestanden

Wanneer Claude Code vraagt om de bestanden, geef:

1. **HELD_SKILL_COMPLETE.md** - complete documentatie
2. **mario_example_for_skill.html** - HTML template voorbeeld
3. **brand_config.json** - HELD branding config

## STAP 4: Laat Claude Code de skill bouwen

Claude Code zal:
✅ Skill directory aanmaken
✅ Python generator implementeren
✅ Template systeem opzetten
✅ Parsing logica bouwen
✅ Test met Mario's data

## STAP 5: Test de skill

```bash
cd /mnt/skills/user/held-precision-health
python held_dashboard_generator.py
```

Voer in:
- Patient naam: Mario
- Plak bloedwaarden
- Plak DNA data
- Welldium link: https://welldium.com/r/q89756e

## ✅ Success Criteria

De skill werkt als:
- [ ] Dashboard genereert zonder errors
- [ ] Biomarkers correct geparsed (met Opt ranges)
- [ ] DNA varianten correct geïnterpreteerd
- [ ] Supplement protocol is gepersonaliseerd
- [ ] 3-maanden plan is gefaseerd
- [ ] Juridische disclaimer is volledig
- [ ] PDF export knop werkt
- [ ] HELD branding is correct

## 🆘 Als iets niet werkt

1. Check of alle bestanden in `/mnt/skills/user/held-precision-health/` staan
2. Valideer input data formatting
3. Test met Mario's voorbeeld data eerst
4. Check console voor errors

---

**Pro tip:** Bewaar Mario's data (blood + DNA tekst) in een apart bestand om snel te kunnen testen!
