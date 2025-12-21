# HELD Precision Health Dashboard Generator

**Skill voor het genereren van gepersonaliseerde health dashboards op basis van DNA methylatie analyse (32 genen), bloedwaarden en consult notities.**

## 🎯 Overzicht

Deze skill automatiseert het creëren van professionele, interactieve HTML health dashboards voor HELD klinieken. Het combineert genetische data, biomarker analyse en expert consultaties in één comprehensive rapport met actionable 3-maanden plannen.

## 📋 Wat Deze Skill Doet

1. **Data Verzameling**: Haalt consult notities uit Notion via MCP + accepteert handmatige input voor bloedwaarden en DNA data
2. **Intelligent Parsing**: Extraheert biomarkers met optimale ranges en DNA varianten met impact
3. **Prioriteits Analyse**: Identificeert kritieke afwijkingen en genetische red flags
4. **Dashboard Generatie**: Creëert branded HTML dashboard met HELD huisstijl
5. **Actionable Plan**: Genereert gepersonaliseerd 3-maanden supplementen- en lifestyle protocol
6. **Legal Compliance**: Include uitgebreide juridische disclaimer (Belgisch/EU recht)
7. **PDF Export**: Print-ready output voor patiënt gebruik

## 🏗️ Skill Structuur

```
/mnt/skills/user/held-precision-health/
├── SKILL.md                          # Deze documentatie
├── held_dashboard_generator.py       # Main Python script
├── templates/
│   └── dashboard_template.html       # HTML template met HELD branding
├── parsers/
│   ├── blood_parser.py              # Bloedwaarden parsing
│   └── dna_parser.py                # DNA methylatie parsing
├── config/
│   ├── brand_config.json            # HELD brand colors & styling
│   └── gene_database.json           # DNA variant interpretaties
└── examples/
    └── mario_example.html           # Volledig voorbeeld dashboard
```

## 🎨 HELD Brand Identity (v3.0)

### Kleuren
```json
{
  "primary": "#34B27B",           // Jungle Green (hoofdkleur)
  "primary_dark": "#2d9e6b",      // Jungle Green Dark
  "secondary": "#FE8900",         // American Orange (waarschuwingen)
  "background": "#FFFFFF",        // Pure White
  "text": "#000000",              // Pure Black
  "border": "#E6E6E6",           // 90% Grey
  "dark_bg": "#11181C",          // Bunker (dark mode)
  "status_critical": "#EF4444",  // Red
  "status_warning": "#FE8900",   // Orange
  "status_optimal": "#34B27B",   // Green
  "status_good": "#10B981"       // Light Green
}
```

### Typography
- **Font**: Inter, Open Sans, system-ui fallback
- **Weights**: 400 (regular), 600 (semibold), 700 (bold)
- **Anti-aliasing**: Enabled voor scherpte

### Design Tokens
- **Border Radius**: 12px (inputs/cards), 24px (large cards), 9999px (buttons - pill shape)
- **Shadows**: Soft, low opacity voor depth
- **Touch Targets**: 44px minimum (mobile-first)
- **Button Style**: Pill-shaped, groene glow, active scale 0.95

## 📊 Input Data Formats

### 1. Notion Data (via MCP)

**Velden om op te halen:**
- `Naam en voornaam` (string)
- `Consult datum` (date)
- `Consult inhoud` (long text - gestructureerde notities)
- `AI notities` (long text - samenvatting)
- `Status` (select)

**Voorbeeld MCP call:**
```python
from mcp import notion_search, notion_fetch

# Zoek patiënt
results = notion_search(query="Mario", query_type="internal")

# Haal data op
patient_data = notion_fetch(id=results[0]['id'])
```

### 2. Bloedwaarden (Handmatige Input)

**Format:**
```
Naam Resultaat Vorig_resultaat Referentiewaarden Eenheid

Voorbeelden:
Hemoglobine 17.2 13.5 - 17.5 g/dL
Ferritine + 307 50-120:opt. 22-322:VN µg/L
HomocysteÏne + 18.0 Opt:<8.0 V.N 3.7-13.9 µmol/L
Vitamine D - 39.7 45-60:opt. 30-100:VN ng/ml
```

**Parsing Regels:**
- `+` of `-` symbool = afwijking flag
- `Opt:` = optimale/functionele range (PRIORITEIT)
- `V.N` of `VN:` = normale medische range (secundair)
- Focus altijd op optimale range voor statusbepaling

**Kritieke Biomarkers (altijd includen):**
- HomocysteÏne, Ferritine, Vitamine D, Triglyceriden
- HbA1c, Glucose, Insuline
- CRP (inflammatie marker)
- Active B12, Foliumzuur, Magnesium RBC
- Cholesterol panel (Total, LDL, HDL)

### 3. DNA Methylatie Data (Handmatige Input)

**Format:**
```
Gen rs-nummer Genotype Impact_beschrijving

Voorbeeld:
MTHFR rs1801133 AG [C677T] Up to 40% reduction in gene function which may impact supply of methyl-folate (5-MTHF) needed for THF and homocysteine regeneration...
```

**Kritieke Genen (32-panel):**

**Folate Cycle:**
- DHFR, FOLH1, MTHFD1, MTHFR (C677T & A1298C), MTR, RFC1, SHMT1, TYMS

**Methionine Cycle:**
- AHCY, BHMT (3 variants), CHDH, FUT2, MAT1A, MTRR, MTR, PEMT, TCN2

**Transsulphuration:**
- CBS (rs234706 - kritiek voor upregulatie), CTH, GSS, MUT, SUOX

**BH4/Neurotransmitter Cycle:**
- COMT (rs4633 & rs4680), MAOA, MAOB, MTHFR A1298C, PNMT, QDPR, VDR (2 variants)

**Urea Cycle:**
- BDKRB2, NOS3 (2 variants), SOD2 (2 variants)

**Parsing Logic:**
```python
# Identificeer genotype
genotypes = ["AA", "AG", "GG", "TT", "TC", "CC", "GA", "CT", "CA"]

# Extract impact
if "reduction" in impact.lower() or "decreased" in impact.lower():
    severity = "warning"
elif "increased" in impact.lower() or "up to" in impact.lower():
    severity = "critical" if "10x" in impact else "warning"
else:
    severity = "info"
```

## 🔧 Implementation Details

### Python Script Structure

```python
#!/usr/bin/env python3
"""
HELD Precision Health Dashboard Generator
Generates personalized health dashboards from DNA and biomarker data
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from pathlib import Path

class HELDDashboardGenerator:
    """Main class for generating HELD precision health dashboards"""
    
    def __init__(self, config_path: str = "config/brand_config.json"):
        """Initialize with HELD branding configuration"""
        self.load_config(config_path)
        self.template = self.load_template()
        
    def generate_dashboard(
        self,
        patient_name: str,
        consult_date: str,
        consult_notes: str,
        blood_data: str,
        dna_data: str,
        welldium_link: str = ""
    ) -> str:
        """
        Generate complete HTML dashboard
        
        Args:
            patient_name: Patient's name
            consult_date: Date of consultation
            consult_notes: Structured consultation notes from Notion
            blood_data: Raw blood test results text
            dna_data: Raw DNA methylation results text
            welldium_link: Optional Welldium supplement order link
            
        Returns:
            Complete HTML dashboard as string
        """
        # Parse data
        biomarkers = self.parse_blood_data(blood_data)
        dna_variants = self.parse_dna_data(dna_data)
        
        # Analyze priorities
        critical_alerts = self.identify_critical_alerts(biomarkers)
        priorities = self.generate_priorities(biomarkers, dna_variants)
        
        # Generate protocol
        supplement_protocol = self.generate_supplement_protocol(dna_variants, biomarkers)
        action_plan = self.generate_3month_plan(dna_variants, biomarkers, consult_notes)
        
        # Build HTML
        html = self.build_html(
            patient_name=patient_name,
            consult_date=consult_date,
            biomarkers=biomarkers,
            dna_variants=dna_variants,
            critical_alerts=critical_alerts,
            priorities=priorities,
            supplement_protocol=supplement_protocol,
            action_plan=action_plan,
            welldium_link=welldium_link
        )
        
        return html
        
    def parse_blood_data(self, blood_text: str) -> List[Dict]:
        """
        Parse blood test results with focus on optimal ranges
        
        Returns list of biomarkers with structure:
        {
            "name": "HomocysteÏne",
            "value": 18.0,
            "unit": "µmol/L",
            "optimal_range": "<8.0",
            "normal_range": "3.7-13.9",
            "status": "critical",  # critical/warning/optimal
            "flag": "+"  # +/- from lab
        }
        """
        biomarkers = []
        
        lines = blood_text.strip().split('\n')
        for line in lines:
            if not line.strip() or line.startswith('Naam'):
                continue
                
            # Parse line
            parts = line.split()
            if len(parts) < 3:
                continue
                
            marker = self.extract_biomarker(parts)
            if marker:
                biomarkers.append(marker)
                
        return biomarkers
        
    def parse_dna_data(self, dna_text: str) -> List[Dict]:
        """
        Parse DNA methylation results
        
        Returns list of variants with structure:
        {
            "gene": "MTHFR",
            "rs_number": "rs1801133",
            "genotype": "AG",
            "variant_name": "C677T",
            "impact": "Up to 40% reduction...",
            "severity": "warning",
            "recommendations": ["5-MTHF 400mcg", "Avoid folic acid", ...]
        }
        """
        variants = []
        
        # Split by gene sections
        gene_sections = self.split_by_genes(dna_text)
        
        for section in gene_sections:
            variant = self.extract_variant(section)
            if variant:
                # Enrich with recommendations from gene database
                variant = self.enrich_variant(variant)
                variants.append(variant)
                
        return variants
        
    def identify_critical_alerts(self, biomarkers: List[Dict]) -> List[Dict]:
        """Identify top 3 critical alerts for immediate attention"""
        critical = []
        
        # Priority 1: Homocysteine
        hcy = next((b for b in biomarkers if "homocyst" in b['name'].lower()), None)
        if hcy and hcy['status'] == 'critical':
            critical.append({
                "title": "Kritieke Afwijking",
                "icon": "🔴",
                "marker": f"{hcy['name']}: {hcy['value']} {hcy['unit']}",
                "optimal": f"Optimaal: {hcy['optimal_range']}",
                "description": "Verhoogd risico op cardiovasculaire problematiek door methylatie-stoornis"
            })
            
        # Priority 2: Inflammation (Ferritin)
        ferr = next((b for b in biomarkers if "ferritin" in b['name'].lower()), None)
        if ferr and ferr['status'] in ['critical', 'warning']:
            critical.append({
                "title": "Verhoogd Inflammatieprofiel",
                "icon": "🔴" if ferr['status'] == 'critical' else "🟡",
                "marker": f"{ferr['name']}: {ferr['value']} {ferr['unit']}",
                "optimal": f"Optimaal: {ferr['optimal_range']}",
                "description": "Wijst op actief ontstekingsproces - oorzaak identificeren"
            })
            
        # Priority 3: Vitamin D
        vitd = next((b for b in biomarkers if "vitamine d" in b['name'].lower() or "vitamin d" in b['name'].lower()), None)
        if vitd and vitd['status'] == 'warning':
            critical.append({
                "title": "Vitamine D Deficiëntie",
                "icon": "🟡",
                "marker": f"{vitd['name']}: {vitd['value']} {vitd['unit']}",
                "optimal": f"Optimaal: {vitd['optimal_range']}",
                "description": "Immuunfunctie suboptimaal, receptor mogelijk downgereguleerd"
            })
            
        return critical[:3]  # Top 3 alleen
        
    def generate_supplement_protocol(self, dna_variants: List[Dict], biomarkers: List[Dict]) -> List[Dict]:
        """
        Generate personalized supplement protocol with timing
        
        Returns schedule with structure:
        {
            "time": "07:30",
            "time_label": "Ochtend (nuchter)",
            "name": "Fosfatidylcholine",
            "dosage": "600-800 mg",
            "reason": "PEMT TT variant & BHMT downregulatie...",
            "badge": "KERN"  # KERN/KRITIEK/ESSENTIEEL/SUPPORT/FASE 2
        }
        """
        protocol = []
        
        # Check for critical variants
        has_pemt_tt = any(v['gene'] == 'PEMT' and v['genotype'] == 'TT' for v in dna_variants)
        has_bhmt_issues = any(v['gene'] == 'BHMT' and v['severity'] == 'warning' for v in dna_variants)
        has_mthfr = any(v['gene'] == 'MTHFR' for v in dna_variants)
        has_cbs_upregulation = any(v['gene'] == 'CBS' and 'AA' in v['genotype'] and 'rs234706' in v['rs_number'] for v in dna_variants)
        has_comt_slow = any(v['gene'] == 'COMT' and v['severity'] in ['warning', 'info'] for v in dna_variants)
        has_vdr_variants = any(v['gene'] == 'VDR' for v in dna_variants)
        
        # Check biomarkers
        low_vitd = any(b['name'].lower().startswith('vitamine d') and b['status'] in ['warning', 'critical'] for b in biomarkers)
        high_homocysteine = any('homocyst' in b['name'].lower() and b['status'] == 'critical' for b in biomarkers)
        
        # 1. Choline (if PEMT TT or BHMT issues)
        if has_pemt_tt or has_bhmt_issues:
            protocol.append({
                "time": "07:30",
                "time_label": "Ochtend (nuchter)",
                "name": "Fosfatidylcholine",
                "dosage": "600-800 mg (Sunflower Lecithin vorm)",
                "reason": f"PRIORITEIT: {'PEMT TT variant - geen endogene choline productie. ' if has_pemt_tt else ''}{'BHMT downregulatie - shortcut pathway ondersteuning. ' if has_bhmt_issues else ''}Essentieel voor homocysteïne conversie.",
                "badge": "KERN"
            })
            
        # 2. Vitamin D (if low or VDR variants)
        if low_vitd or has_vdr_variants:
            vitd_marker = next((b for b in biomarkers if 'vitamine d' in b['name'].lower() or 'vitamin d' in b['name'].lower()), None)
            current = f"Huidige waarde {vitd_marker['value']} {vitd_marker['unit']} → " if vitd_marker else ""
            protocol.append({
                "time": "08:00",
                "time_label": "Bij Ontbijt",
                "name": "Vitamine D3 + K2 (vloeibaar)",
                "dosage": "4000-5000 IU D3 + 100 mcg K2-MK7",
                "reason": f"{current}doel 50-60 ng/ml. Vloeibare vorm voor betere absorptie. K2 voor calcium metabolisme. {'VDR variants vereisen hogere dosis.' if has_vdr_variants else ''}",
                "badge": "KRITIEK" if low_vitd else "ESSENTIEEL"
            })
            
        # 3. Zinc (always if BHMT or methylation issues)
        if has_bhmt_issues or has_mthfr or high_homocysteine:
            protocol.append({
                "time": "12:30",
                "time_label": "Lunch",
                "name": "Zink Bisglycinaat",
                "dosage": "25-30 mg elementair zink",
                "reason": "Cruciaal voor: BHMT cofactor, SAMe conversie, methylatie support. Bisglycinaat vorm voor optimale absorptie.",
                "badge": "ESSENTIEEL"
            })
            
        # 4. Magnesium (if COMT slow)
        if has_comt_slow or has_mthfr:
            protocol.append({
                "time": "15:00",
                "time_label": "Middag",
                "name": "Magnesium Glycinaat",
                "dosage": "400 mg elementair magnesium",
                "reason": f"{'COMT ondersteuning voor neurotransmitter afbraak. ' if has_comt_slow else ''}SAMe conversie cofactor. Glycinaat vorm voor maximale absorptie en geen laxerend effect.",
                "badge": "SUPPORT"
            })
            
        # 5. Methylated B-Complex (ONLY after 6 weeks if CBS upregulation)
        if has_mthfr:
            warning = "⚠️ START PAS NA 6 WEKEN als choline pathway geoptimaliseerd is. " if has_cbs_upregulation else ""
            protocol.append({
                "time": "20:00",
                "time_label": "Avond",
                "name": "Methylated B-Complex",
                "dosage": "5-MTHF 400mcg, Methylcobalamin 500mcg, P5P 25mg, R5P 25mg",
                "reason": f"{warning}MTHFR varianten ondersteuning. Actieve vormen vereist voor optimale methylatie. {'P5P voor CBS upregulatie.' if has_cbs_upregulation else ''}",
                "badge": "FASE 2" if has_cbs_upregulation else "KERN"
            })
            
        # 6. TMG/Betaine (if BHMT issues)
        if has_bhmt_issues or has_cbs_upregulation:
            protocol.append({
                "time": "22:00",
                "time_label": "Voor Bed",
                "name": "Trimethylglycine (TMG/Betaine)",
                "dosage": "500-1000 mg",
                "reason": "Direct cofactor voor BHMT 'shortcut' pathway. Ondersteunt methylatie zonder CBS upregulatie. Synergistisch met choline.",
                "badge": "KERN"
            })
            
        return sorted(protocol, key=lambda x: x['time'])
        
    def generate_3month_plan(self, dna_variants: List[Dict], biomarkers: List[Dict], consult_notes: str) -> List[Dict]:
        """
        Generate phased 3-month action plan
        
        Returns phases with structure:
        {
            "phase": "Fase 1: Fundament Leggen",
            "duration": "Week 1-6",
            "actions": [
                {
                    "icon": "🥚",
                    "title": "Choline Pathway Herstellen",
                    "description": "Start fosfatidylcholine..."
                }
            ],
            "warnings": ["⚠️ Nog GEEN methylated B-complex..."]
        }
        """
        phases = []
        
        # Detect key issues
        has_high_homocysteine = any('homocyst' in b['name'].lower() and b['status'] == 'critical' for b in biomarkers)
        has_inflammation = any(('ferritin' in b['name'].lower() or 'crp' in b['name'].lower()) and b['status'] in ['critical', 'warning'] for b in biomarkers)
        has_cbs_upregulation = any(v['gene'] == 'CBS' and 'AA' in v['genotype'] for v in dna_variants)
        has_comt_variants = any(v['gene'] == 'COMT' for v in dna_variants)
        
        # Phase 1: Foundation (Week 1-6)
        phase1_actions = []
        
        if has_high_homocysteine:
            phase1_actions.append({
                "icon": "🥚",
                "title": "Choline Pathway Herstellen (PRIORITEIT)",
                "description": "Start fosfatidylcholine 600-800mg + TMG 500mg + zink 25mg. Dit is het fundament - BHMT shortcut moet werken voordat we methylatie verder pushen. Eet dagelijks 2-3 eieren + rund/kip/vis voor extra choline."
            })
            
        phase1_actions.append({
            "icon": "☀️",
            "title": "Vitamine D Normaliseren",
            "description": "Vloeibare D3 4000-5000 IU + K2 100mcg dagelijks. Doel: 50-60 ng/ml binnen 6-8 weken. Meet opnieuw bij hertest."
        })
        
        if has_inflammation:
            phase1_actions.append({
                "icon": "🧘",
                "title": "Inflammatie Onderzoek",
                "description": "Ferritine te hoog wijst op onderliggende oorzaak. Zoek: infectie? Chronische inflammatie? Auto-immuun? Werk samen met arts voor verder onderzoek."
            })
            
        if has_comt_variants:
            phase1_actions.append({
                "icon": "🧠",
                "title": "COMT Support Starten",
                "description": "Magnesium glycinaat 400mg vanaf week 1. COMT slow variants + lage SAMe = nog tragere catecholamine afbraak. Magnesium helpt COMT enzym werken."
            })
            
        phase1_warnings = []
        if has_cbs_upregulation:
            phase1_warnings.append("⚠️ LET OP Week 1-6: Nog GEEN methylated B-complex starten! CBS upregulatie + onvoldoende choline = ammonia buildup risico. Wacht tot week 6 voor veilige implementatie.")
            
        phases.append({
            "phase": "Fase 1: Fundament Leggen",
            "duration": "Week 1-6",
            "actions": phase1_actions,
            "warnings": phase1_warnings
        })
        
        # Phase 2: Optimization (Week 6-8)
        phase2_actions = [
            {
                "icon": "📊",
                "title": "Hertest & Evaluatie (Week 6)",
                "description": "Meet opnieuw: HomocysteÏne (doel: <10), Ferritine (doel: <200), Vitamine D (doel: 50+), Triglyceriden, Zink (nu toevoegen aan panel), Magnesium RBC. Evalueer of choline pathway werkt voordat je verder gaat."
            },
            {
                "icon": "💊",
                "title": "B-Complex Toevoegen (NA Week 6)",
                "description": "ALS homocysteïne gedaald: Start methylated B-complex (5-MTHF 400mcg, methylcobalamin 500mcg, P5P 25mg, R5P 25mg). Start laag en bouw op. Monitor op overstimulatie (COMT slow!). ALS homocysteïne niet gedaald: verhoog eerst choline/betaine dosis."
            },
            {
                "icon": "🥬",
                "title": "Voeding Optimaliseren",
                "description": "Verhoog: Groene bladgroenten (folaat), citrus (vitamine C), bonen, quinoa/spinazie/biet (betaine), eieren (choline), vette vis (omega-3). Modereer: Rood vlees (ammonia), alcohol (MAOA remming)."
            },
            {
                "icon": "🔬",
                "title": "Antioxidant Support",
                "description": "NAC 600mg 2x/dag voor glutathione. Vitamine C 1000mg. NOS3 variants verhogen vrije radicalen - antioxidanten zijn essentieel."
            }
        ]
        
        phases.append({
            "phase": "Fase 2: Methylatie Optimaliseren",
            "duration": "Week 6-8",
            "actions": phase2_actions,
            "warnings": []
        })
        
        # Phase 3: Fine-tuning (Week 8-12)
        phase3_actions = [
            {
                "icon": "🎯",
                "title": "Symptoom Tracking",
                "description": "Monitor: energie levels, slaapkwaliteit, mentale helderheid, mood stabiliteit, stress tolerantie. COMT/MAOA/VDR variants beïnvloeden neurotransmitters - let op veranderingen. Te veel methylatie = overstimulatie. Te weinig = vermoeidheid."
            },
            {
                "icon": "⚖️",
                "title": "Dosering Aanpassen",
                "description": "Op basis van lab resultaten en symptomen: fine-tune B-complex dosis, overweeg SAMe (100-200mg) als homocysteïne laag genoeg, adjust choline indien nodig. Personalisatie is key - geen 'one size fits all'."
            },
            {
                "icon": "🔄",
                "title": "Lifestyle Optimalisatie",
                "description": "Slaap: 7-8u consistent. Stress: Meditatie/ademwerk (MAOA warrior gene). Beweging: Mix cardio/kracht, niet overtrainen. Hydratatie: 2-3L water."
            },
            {
                "icon": "📋",
                "title": "Week 12: Complete Hertest",
                "description": "Full panel: Homocysteïne (doel: <8), Ferritine (doel: 70-90), Vitamine D (doel: 50-60), Triglyceriden, Cholesterol panel, HbA1c, CRP, Complete bloedbeeld, Zink, Magnesium RBC, B12 actief. Evaluatie: Progress review + plan voor maanden 4-6 indien nodig."
            }
        ]
        
        phases.append({
            "phase": "Fase 3: Fine-tuning & Monitoring",
            "duration": "Week 8-12",
            "actions": phase3_actions,
            "warnings": []
        })
        
        return phases
        
    def build_html(self, **kwargs) -> str:
        """Build final HTML from template and data"""
        # Load template
        template = self.template
        
        # Replace placeholders
        html = template.replace("{{PATIENT_NAME}}", kwargs['patient_name'])
        html = html.replace("{{CONSULT_DATE}}", kwargs['consult_date'])
        
        # Insert sections
        html = self.insert_alerts(html, kwargs['critical_alerts'])
        html = self.insert_priorities(html, kwargs['priorities'])
        html = self.insert_biomarkers(html, kwargs['biomarkers'])
        html = self.insert_dna_variants(html, kwargs['dna_variants'])
        html = self.insert_supplement_protocol(html, kwargs['supplement_protocol'])
        html = self.insert_action_plan(html, kwargs['action_plan'])
        html = self.insert_welldium_link(html, kwargs.get('welldium_link', ''))
        
        return html
        
    def save_dashboard(self, html: str, patient_name: str) -> str:
        """Save HTML to file and return path"""
        timestamp = datetime.now().strftime("%Y%m%d")
        filename = f"{patient_name.replace(' ', '_')}_HELD_Dashboard_{timestamp}.html"
        filepath = Path(f"/mnt/user-data/outputs/{filename}")
        
        filepath.write_text(html, encoding='utf-8')
        
        return str(filepath)


def main():
    """Main execution flow"""
    print("🏥 HELD Precision Health Dashboard Generator")
    print("=" * 60)
    
    # Initialize generator
    generator = HELDDashboardGenerator()
    
    # Step 1: Get patient name
    patient_name = input("\n📝 Patiënt naam: ").strip()
    
    # Step 2: Try to fetch from Notion
    print(f"\n🔍 Zoeken naar '{patient_name}' in Notion...")
    try:
        from mcp import notion_search, notion_fetch
        
        results = notion_search(query=patient_name, query_type="internal")
        if results:
            print(f"✓ Gevonden in Notion")
            patient_data = notion_fetch(id=results[0]['id'])
            
            consult_date = patient_data.get('Consult datum', datetime.now().strftime("%Y-%m-%d"))
            consult_notes = patient_data.get('Consult inhoud', '')
            ai_notes = patient_data.get('AI notities', '')
        else:
            print("⚠️  Niet gevonden in Notion - gebruik handmatige input")
            consult_date = input("Consult datum (YYYY-MM-DD): ").strip()
            consult_notes = ""
            ai_notes = ""
    except:
        print("⚠️  Notion MCP niet beschikbaar - gebruik handmatige input")
        consult_date = input("Consult datum (YYYY-MM-DD): ").strip()
        consult_notes = ""
        ai_notes = ""
    
    # Step 3: Get blood data
    print("\n🩸 BLOEDWAARDEN")
    print("Plak de volledige bloedwaarden tekst (druk Enter 2x om te stoppen):")
    print("-" * 60)
    blood_lines = []
    while True:
        line = input()
        if not line:
            break
        blood_lines.append(line)
    blood_data = '\n'.join(blood_lines)
    
    # Step 4: Get DNA data
    print("\n🧬 DNA METHYLATIE DATA")
    print("Plak de DNA methylatie resultaten (druk Enter 2x om te stoppen):")
    print("-" * 60)
    dna_lines = []
    while True:
        line = input()
        if not line:
            break
        dna_lines.append(line)
    dna_data = '\n'.join(dna_lines)
    
    # Step 5: Get Welldium link
    welldium_link = input("\n💊 Welldium bestel link (optioneel): ").strip()
    
    # Step 6: Generate dashboard
    print("\n⚙️  Genereren van dashboard...")
    html = generator.generate_dashboard(
        patient_name=patient_name,
        consult_date=consult_date,
        consult_notes=consult_notes or ai_notes,
        blood_data=blood_data,
        dna_data=dna_data,
        welldium_link=welldium_link
    )
    
    # Step 7: Save dashboard
    filepath = generator.save_dashboard(html, patient_name)
    
    print("\n✅ Dashboard succesvol gegenereerd!")
    print(f"📄 Bestand: {filepath}")
    print(f"\n🔗 Open in browser:")
    print(f"   file://{filepath}")
    print(f"\n📥 Voor PDF export:")
    print(f"   1. Open het bestand in een browser")
    print(f"   2. Klik op 'Download als PDF' knop")
    print(f"   3. Of gebruik Print → Save as PDF")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
```

## 🚀 Gebruik

### Quick Start

```bash
# In Claude Code
python held_dashboard_generator.py
```

Volg de prompts:
1. Voer patiënt naam in (wordt gezocht in Notion)
2. Plak bloedwaarden tekst
3. Plak DNA methylatie tekst
4. Voer optioneel Welldium link in
5. Dashboard wordt gegenereerd!

### Programmatisch Gebruik

```python
from held_dashboard_generator import HELDDashboardGenerator

generator = HELDDashboardGenerator()

html = generator.generate_dashboard(
    patient_name="Mario",
    consult_date="2025-11-05",
    consult_notes=notion_consult_data,
    blood_data=blood_text,
    dna_data=dna_text,
    welldium_link="https://welldium.com/r/q89756e"
)

filepath = generator.save_dashboard(html, "Mario")
print(f"Dashboard saved: {filepath}")
```

## ⚠️ Belangrijke Opmerkingen

### Medische Precisie
- **NOOIT** waarden raden of interpoleren
- **ALTIJD** originele biomarker waarden behouden
- Bij twijfel: vraag user om verificatie
- Fouten in medische data zijn ONACCEPTABEL

### Genetische Interpretatie
- Gebruik gene_database.json voor accurate interpretaties
- Combineer nooit interpretaties van verschillende varianten
- CBS upregulatie (AA genotype rs234706) is KRITIEK - speciale aandacht
- MTHFR dubbel variant (C677T + A1298C) vereist beide analyses

### Supplementen Protocol
- **TIMING is cruciaal**: choline voor B-complex bij CBS upregulatie
- Doseringen moeten binnen therapeutische ranges blijven
- Contra-indicaties checken (zwangerschap, medicatie)
- ALTIJD disclaimer includen over arts raadplegen

### Legal Compliance
- Uitgebreide disclaimer is VERPLICHT
- Belgische en EU wetgeving compliance
- Geen medische claims maken
- Privacy (GDPR) waarborgen

## 📝 Output Voorbeeld

Zie `examples/mario_example.html` voor volledig voorbeeld dashboard met:
- ✅ Complete HELD branding
- ✅ Interactieve visualisaties
- ✅ Kritieke alerts sectie
- ✅ 12 DNA varianten met interpretaties
- ✅ Gepersonaliseerd supplementenprotocol met timing
- ✅ 3-maanden gefaseerd actieplan
- ✅ Uitgebreide juridische disclaimer
- ✅ PDF export functionaliteit
- ✅ Welldium bestel integratie

## 🔧 Troubleshooting

### "Notion MCP niet beschikbaar"
→ Check of Notion MCP enabled is in Claude Code settings
→ Fallback: gebruik handmatige input voor alle data

### "Parse error in blood data"
→ Controleer format: "Naam Resultaat Referentie Eenheid"
→ Let op spaties en speciale karakters (±, µ)

### "DNA variant niet herkend"
→ Check gene_database.json voor ondersteunde genen
→ Voeg nieuwe varianten toe aan database

### "HTML niet correct gerenderd"
→ Valideer HTML syntax
→ Check of alle placeholders vervangen zijn
→ Test in verschillende browsers

## 📚 Dependencies

```
python >= 3.8
pathlib (stdlib)
json (stdlib)
re (stdlib)
datetime (stdlib)
typing (stdlib)
```

**Optioneel voor Notion:**
```
mcp (Notion MCP integration)
```

## 🆘 Support

Bij vragen of problemen:
- Check `examples/mario_example.html` voor referentie
- Review gene_database.json voor DNA interpretaties
- Valideer input data formatting
- Test met Mario's example data eerst

## 📄 Licentie

Proprietary - HELD Preventieve Gezondheid & Biohacking
© 2025 HELD. Alle rechten voorbehouden.

---

**Versie:** 1.0.0  
**Laatste update:** 5 november 2025  
**Auteur:** HELD Development Team
