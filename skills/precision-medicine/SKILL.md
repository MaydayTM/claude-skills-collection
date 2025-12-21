---
name: held-precision-health
description: Generate personalized precision health dashboards from DNA methylation, blood biomarkers, and consultation notes with HELD branding
author: HELD Development Team
version: 1.0.0
---

# HELD Precision Health Dashboard Generator

## Overview

This skill generates professional, branded HTML health dashboards for HELD precision health consultations. It combines:
- DNA methylation analysis (32-gene panel)
- Blood biomarker results (focusing on optimal ranges)
- Consultation notes
- Personalized supplement protocols
- 3-month phased action plans

## When to Use This Skill

Use this skill when a user asks to:
- "Generate a HELD health dashboard"
- "Create a precision health report"
- "Make a dashboard from blood tests and DNA results"
- "Generate patient health summary for [name]"

## Usage

### Interactive Mode

```bash
python3 held_dashboard_generator.py
```

Follow the prompts to enter:
1. Patient name (required)
2. Consultation date (YYYY-MM-DD format, defaults to today)
3. Consultation notes (optional)
4. Blood test results (paste full text, press Enter twice to finish)
5. DNA methylation results (paste full text, press Enter twice to finish)
6. Optional Welldium supplement link

### Programmatic Mode

```python
from held_dashboard_generator import HELDDashboardGenerator

generator = HELDDashboardGenerator()

html = generator.generate_dashboard(
    patient_name="John Doe",
    consult_date="2025-11-05",
    consult_notes="Consultation notes here...",
    blood_data=blood_test_text,
    dna_data=dna_methylation_text,
    welldium_link="https://welldium.com/r/xxxxx"
)

filepath = generator.save_dashboard(html, "John Doe")
print(f"Dashboard saved: {filepath}")
```

## Input Format Requirements

### Blood Test Data

Format: `Name [+/-] Value Opt:range V.N:range unit`

Example:
```
HomocysteÏne + 18.0 Opt:<8.0 V.N 3.7-13.9 µmol/L
Ferritine + 307 50-120:opt. 22-322:VN µg/L
Vitamine D - 39.7 45-60:opt. 30-100:VN ng/ml
```

**Key Points:**
- Name can include special characters (Ï, è, etc.)
- Flag (+/-) indicates above/below normal (optional)
- `Opt:` or `:opt.` indicates optimal (functional) range
- `V.N` or `:VN` indicates normal (reference) range
- Unit appears at end of line

### DNA Methylation Data

Format: `GENE rs##### GENOTYPE [VARIANT] Impact description`

Example:
```
MTHFR rs1801133 AG [C677T] Up to 40% reduction in gene function
CBS rs234706 AA Thought to be the strongest indicator of increased (up to 10x) CBS activity
PEMT rs7946 TT Potential for reduced choline synthesis
```

**Key Points:**
- Gene name in UPPERCASE
- RS number format: rs followed by digits
- Genotype: 2-letter combination (AA, AG, GG, TT, TC, CC, etc.)
- Variant name in brackets (optional, e.g., [C677T])
- Impact description follows

## Critical Medical Logic

### CBS Upregulation (rs234706 AA)

**CRITICAL**: This variant requires special handling!

- Indicates up to 10x increased CBS enzyme activity
- **DANGER**: B-vitamins before choline supplementation can cause ammonia buildup
- **PROTOCOL**: Choline FIRST (6 weeks), then B-complex
- Dashboard automatically flags B-complex as "FASE 2" badge
- Adds warning to Phase 1 of action plan

**Implementation:**
```python
has_cbs_upregulation = any(
    v['gene'] == 'CBS' and 'AA' in v['genotype'] and 'rs234706' in v['rs_number']
    for v in dna_variants
)

if has_cbs_upregulation:
    # B-complex gets "FASE 2" badge instead of "KERN"
    # Phase 1 warning: "Nog GEEN methylated B-complex starten!"
```

### PEMT TT Variant

- No endogenous choline production
- Requires dietary/supplemental choline (600-800mg daily)
- Marked as "KERN" (core) supplement
- Priority supplement at 07:30 (morning, fasting)

**Rationale:**
- Choline pathway must work before methylation pathway
- Essential for homocysteine conversion via BHMT "shortcut"
- Synergistic with TMG/betaine

### MTHFR Variants

- C677T (rs1801133) and A1298C (rs1801131)
- Heterozygous (AG, CT, GT) = WARNING
- Homozygous (AA, TT, CC) = CRITICAL
- Requires methylated B-vitamins (5-MTHF, methylcobalamin, P5P, R5P)
- NOT regular folic acid (cannot convert properly)

**Key Supplement:**
- Methylated B-Complex: 5-MTHF 400mcg, Methylcobalamin 500mcg, P5P 25mg, R5P 25mg
- Timing: 20:00 (evening)
- If CBS upregulation: FASE 2 (after 6 weeks)
- Otherwise: KERN (core protocol)

## Output

Dashboard includes:

1. **Patient Header**
   - Name, consultation date
   - HELD branding (Jungle Green gradient)
   - PDF export button

2. **Critical Alerts**
   - Top 3 priority issues
   - Homocysteine (cardiovascular risk)
   - Ferritin (inflammation marker)
   - Vitamin D (immune function)
   - Color-coded: Red (critical), Orange (warning), Green (optimal)

3. **Biomarkers Grid**
   - All blood tests with status badges
   - Current value vs optimal range
   - Status: critical / warning / optimal

4. **DNA Variants**
   - All genetic variants with severity
   - Gene, RS number, genotype
   - Variant name (if applicable)
   - Impact description
   - Severity: critical / warning / info

5. **Supplement Protocol**
   - Time-based daily schedule
   - 07:30 to 22:00 timing
   - Each supplement includes:
     - Specific dosage and form
     - Medical rationale
     - Badge: KERN / KRITIEK / ESSENTIEEL / SUPPORT / FASE 2

6. **3-Month Action Plan**
   - Phased timeline approach
   - **Fase 1 (Week 1-6):** Foundation - choline pathway, vitamin D, inflammation
   - **Fase 2 (Week 6-8):** Optimization - retest, add B-complex, diet, antioxidants
   - **Fase 3 (Week 8-12):** Fine-tuning - symptom tracking, dosing adjustments, final retest
   - Includes warnings for CBS upregulation

7. **Legal Disclaimer**
   - Belgian/EU compliant medical disclaimer
   - Clarifies informational purpose only
   - Advises consulting healthcare professionals

8. **PDF Export**
   - Print-ready styling with `@media print` rules
   - Color preservation (`print-color-adjust: exact`)
   - Page break optimization
   - No interactive elements in print

## HELD Branding

- **Primary Color:** Jungle Green (#34B27B)
- **Secondary Color:** American Orange (#FE8900)
- **Status Colors:**
  - Critical: #EF4444 (red)
  - Warning: #FE8900 (orange)
  - Optimal: #34B27B (green)
- **Typography:** Inter, Open Sans, system-ui
- **Border Radius:** 12px (cards), 24px (large), 9999px (buttons/badges)
- **Shadows:** Subtle depth with green tint
- **Responsive:** Mobile-friendly grid layouts

## Testing

### Run All Tests

```bash
python3 -m pytest tests/ -v
```

### Test Individual Parsers

```bash
python3 -m pytest tests/test_blood_parser.py -v
python3 -m pytest tests/test_dna_parser.py -v
python3 -m pytest tests/test_dashboard_generator.py -v
```

### Test with Example Data

Use the test fixtures:
```bash
cat tests/fixtures/test_data.json
```

### Manual Testing

```python
from held_dashboard_generator import HELDDashboardGenerator

blood_data = """HomocysteÏne + 18.0 Opt:<8.0 V.N 3.7-13.9 µmol/L
Ferritine + 307 50-120:opt. 22-322:VN µg/L
Vitamine D - 39.7 45-60:opt. 30-100:VN ng/ml"""

dna_data = """MTHFR rs1801133 AG [C677T] Up to 40% reduction in gene function
CBS rs234706 AA Thought to be the strongest indicator of increased (up to 10x) CBS activity
PEMT rs7946 TT Potential for reduced choline synthesis"""

gen = HELDDashboardGenerator()
html = gen.generate_dashboard(
    patient_name="Test Patient",
    consult_date="2025-11-05",
    consult_notes="Test consultation",
    blood_data=blood_data,
    dna_data=dna_data
)

filepath = gen.save_dashboard(html, "Test_Patient")
print(f"Dashboard saved: {filepath}")
```

## Important Notes

1. **Medical Accuracy**: Never guess or interpolate values. Use exact data only.
2. **Optimal Ranges**: Prioritize "Opt:" ranges over "V.N" (normal) ranges
3. **CBS Safety**: Always check for CBS upregulation before recommending B-vitamins
4. **Disclaimer Required**: Every dashboard MUST include legal disclaimer
5. **PDF Export**: Ensure print CSS works correctly
6. **No External Dependencies**: Uses Python 3.8+ standard library only

## Files

- `held_dashboard_generator.py`: Main generator script with CLI
- `parsers/blood_parser.py`: Blood test parser with optimal range detection
- `parsers/dna_parser.py`: DNA methylation parser with severity assessment
- `template_builder.py`: HELD branded CSS template
- `config/brand_config.json`: HELD brand configuration
- `examples/mario_example_for_skill.html`: Complete example dashboard
- `tests/`: Test suite with fixtures

## Project Structure

```
precision-medicine-skill/
├── held_dashboard_generator.py    # Main script (executable)
├── template_builder.py             # CSS template
├── parsers/
│   ├── __init__.py
│   ├── blood_parser.py             # Blood test parsing
│   └── dna_parser.py               # DNA methylation parsing
├── templates/
│   └── .gitkeep
├── config/
│   └── brand_config.json           # HELD branding
├── examples/
│   └── mario_example_for_skill.html
├── tests/
│   ├── __init__.py
│   ├── test_blood_parser.py
│   ├── test_dna_parser.py
│   ├── test_dashboard_generator.py
│   └── fixtures/
│       └── test_data.json
├── outputs/                        # Generated dashboards
├── SKILL.md                        # This file
└── README.md
```

## Troubleshooting

### "Config file not found"
- Run from project root directory
- Check that `config/brand_config.json` exists

### "Parse error in blood data"
- Verify format: `Name [+/-] Value Range Unit`
- Check for special characters (µ, Ï, etc.)
- Ensure optimal range uses `Opt:` or `:opt.`

### "Template not found"
- Template is dynamically generated
- Check that `template_builder.py` exists
- Verify running from project root

### "No supplements generated"
- Check DNA data includes PEMT, MTHFR, or other variants
- Verify blood data includes vitamin D or other markers
- Review parser output for errors

### HTML looks wrong
- Check browser console for errors
- Verify CSS is embedded in HTML
- Test in different browsers (Chrome, Firefox, Safari)

### PDF export issues
- Use Chrome for best results
- Click "Download als PDF" button in dashboard
- Or use browser Print → Save as PDF
- Check print preview before saving

## Safety Warnings

### CBS Upregulation
- NEVER recommend B-vitamins in Phase 1 if CBS rs234706 AA detected
- ALWAYS prioritize choline supplementation first
- Wait minimum 6 weeks before introducing B-complex
- Monitor for ammonia buildup symptoms

### Supplement Interactions
- Inform patients to consult prescribing physician before changes
- Check for drug interactions (especially blood thinners with vitamin K2)
- Monitor retest labs at 6 weeks

### Medical Disclaimer
- Dashboard is informational only, not medical advice
- Always recommend consulting qualified healthcare professionals
- Document patient consent for genetic testing

## License

Proprietary - HELD Preventieve Gezondheid & Biohacking
© 2025 HELD. All rights reserved.

## Support

For issues or questions:
1. Check this SKILL.md documentation
2. Review example dashboard: `examples/mario_example_for_skill.html`
3. Test with fixtures: `tests/fixtures/test_data.json`
4. Check existing tests for usage examples
5. Verify running from project root with correct file structure

## Version History

**v1.0.0** (2025-11-05)
- Initial release
- Blood parser with optimal range detection
- DNA parser with severity assessment
- Supplement protocol generator with CBS safety logic
- 3-month phased action plan
- HELD branded HTML template
- Interactive CLI
- Complete test suite
- Documentation and examples
