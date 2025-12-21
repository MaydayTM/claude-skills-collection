# Precision Medicine Skill

Claude Code skill for HELD precision medicine workflows - generates personalized health dashboards from DNA methylation, blood biomarkers, and consultation notes.

## Features

- 🧬 **DNA Methylation Analysis**: Parse and interpret 32-gene methylation panel
- 🩸 **Blood Biomarker Parsing**: Focus on optimal (functional) ranges, not just normal ranges
- ⚕️ **Medical-Grade Accuracy**: Critical safety checks (CBS upregulation, PEMT TT, MTHFR variants)
- 💊 **Personalized Protocols**: Time-based supplement schedules with dosage and rationale
- 📅 **3-Month Action Plans**: Phased approach (Foundation → Optimization → Fine-tuning)
- 🎨 **HELD Branding**: Professional HTML dashboards with Jungle Green (#34B27B) theme
- 📄 **PDF Export**: Print-ready styling for patient distribution
- ⚖️ **Legal Compliance**: Belgian/EU compliant medical disclaimers

## Quick Start

```bash
# Install (no dependencies - Python 3.8+ stdlib only)
git clone https://github.com/MaydayTM/precision-medicine-skill.git
cd precision-medicine-skill

# Generate dashboard
python3 held_dashboard_generator.py
```

Follow prompts to enter patient data.

## Usage

### Interactive CLI

```bash
python3 held_dashboard_generator.py
```

### Programmatic

```python
from held_dashboard_generator import HELDDashboardGenerator

generator = HELDDashboardGenerator()
html = generator.generate_dashboard(
    patient_name="John Doe",
    consult_date="2025-11-05",
    consult_notes="...",
    blood_data="...",  # Paste blood test results
    dna_data="...",    # Paste DNA methylation results
    welldium_link="https://welldium.com/r/xxxxx"
)

filepath = generator.save_dashboard(html, "John Doe")
```

## Input Formats

### Blood Tests
```
HomocysteÏne + 18.0 Opt:<8.0 V.N 3.7-13.9 µmol/L
Ferritine + 307 50-120:opt. 22-322:VN µg/L
```

### DNA Methylation
```
MTHFR rs1801133 AG [C677T] Up to 40% reduction in gene function
CBS rs234706 AA Increased CBS activity (up to 10x)
```

## Critical Safety Features

### CBS Upregulation Detection

The skill automatically detects CBS rs234706 AA variants and:
- Flags B-complex as "FASE 2" (after 6 weeks)
- Prioritizes choline supplementation first
- Adds explicit warnings to action plan

### PEMT TT Variant

Automatically recommends:
- Fosfatidylcholine 600-800mg daily
- Marked as "KERN" (core) supplement
- Dietary choline sources (eggs, meat)

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test suite
pytest tests/test_blood_parser.py -v
pytest tests/test_dna_parser.py -v
pytest tests/test_integration.py -v

# Test with example data
python3 held_dashboard_generator.py
# Use data from: tests/fixtures/test_data.json
```

## Project Structure

```
precision-medicine-skill/
├── held_dashboard_generator.py    # Main script
├── parsers/
│   ├── blood_parser.py            # Blood test parsing
│   └── dna_parser.py              # DNA methylation parsing
├── templates/
│   └── dashboard_template.html    # HTML template
├── config/
│   └── brand_config.json          # HELD branding
├── examples/
│   └── mario_example_for_skill.html  # Example dashboard
├── tests/
│   ├── test_blood_parser.py
│   ├── test_dna_parser.py
│   ├── test_dashboard_generator.py
│   ├── test_integration.py
│   └── fixtures/test_data.json
├── outputs/                       # Generated dashboards
├── SKILL.md                      # Claude Code skill documentation
└── README.md
```

## Dependencies

**None!** Uses only Python 3.8+ standard library:
- `re` - Regular expressions for parsing
- `json` - Config and data handling
- `datetime` - Timestamps
- `pathlib` - File operations
- `typing` - Type hints

## Documentation

- **[SKILL.md](SKILL.md)**: Complete skill documentation for Claude Code
- **[Examples](examples/)**: Sample dashboards (Mario example)
- **[Tests](tests/)**: Test suite with fixtures

## Development

```bash
# Run tests with coverage
pytest tests/ -v --cov=. --cov-report=html

# Lint
pylint held_dashboard_generator.py parsers/

# Format
black held_dashboard_generator.py parsers/ tests/
```

## License

Proprietary - HELD Preventieve Gezondheid & Biohacking
© 2025 HELD. All rights reserved.

## Support

For issues or questions:
1. Check `SKILL.md` documentation
2. Review example dashboard: `examples/mario_example_for_skill.html`
3. Test with fixtures: `tests/fixtures/test_data.json`
4. Open GitHub issue

---

**Version:** 1.0.0
**Last Updated:** November 5, 2025
