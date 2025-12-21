#!/usr/bin/env python3
"""
HELD Precision Health Dashboard Generator
Generates personalized health dashboards from DNA and biomarker data
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from parsers.blood_parser import BloodParser
from parsers.dna_parser import DNAParser


class HELDDashboardGenerator:
    """Main class for generating HELD precision health dashboards"""

    def __init__(self, config_path: str = "config/brand_config.json"):
        """Initialize with HELD branding configuration"""
        self.config = self._load_config(config_path)
        self.blood_parser = BloodParser()
        self.dna_parser = DNAParser()

    def _load_config(self, config_path: str) -> Dict:
        """Load brand configuration"""
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

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
            consult_date: Date of consultation (YYYY-MM-DD)
            consult_notes: Consultation notes from Notion
            blood_data: Raw blood test results text
            dna_data: Raw DNA methylation results text
            welldium_link: Optional Welldium supplement order link

        Returns:
            Complete HTML dashboard as string
        """
        # Parse data
        biomarkers = self.blood_parser.parse(blood_data)
        dna_variants = self.dna_parser.parse(dna_data)

        # Analyze
        critical_alerts = self.identify_critical_alerts(biomarkers)
        priorities = self.generate_priorities(biomarkers, dna_variants)

        # Generate protocols
        supplement_protocol = self.generate_supplement_protocol(dna_variants, biomarkers)
        action_plan = self.generate_3month_plan(dna_variants, biomarkers)

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

    def identify_critical_alerts(self, biomarkers: List[Dict]) -> List[Dict]:
        """
        Identify top 3 critical alerts for immediate attention

        Priority order:
        1. Homocysteine (cardiovascular risk)
        2. Ferritin (inflammation)
        3. Vitamin D (immune function)
        """
        alerts = []

        # Priority 1: Homocysteine
        hcy = next((b for b in biomarkers if 'homocyst' in b['name'].lower()), None)
        if hcy and hcy['status'] in ['critical', 'warning']:
            alerts.append({
                'title': 'Kritieke Afwijking' if hcy['status'] == 'critical' else 'Verhoogd HomocysteÏne',
                'icon': '🔴' if hcy['status'] == 'critical' else '🟡',
                'marker': f"{hcy['name']}: {hcy['value']} {hcy['unit']}",
                'optimal': f"Optimaal: {hcy['optimal_range']} {hcy['unit']}",
                'description': 'Verhoogd risico op cardiovasculaire problematiek door methylatie-stoornis'
            })

        # Priority 2: Ferritin (inflammation marker)
        ferr = next((b for b in biomarkers if 'ferritin' in b['name'].lower()), None)
        if ferr and ferr['status'] in ['critical', 'warning']:
            alerts.append({
                'title': 'Verhoogd Inflammatieprofiel',
                'icon': '🔴' if ferr['status'] == 'critical' else '🟡',
                'marker': f"{ferr['name']}: {ferr['value']} {ferr['unit']}",
                'optimal': f"Optimaal: {ferr['optimal_range']} {ferr['unit']}",
                'description': 'Wijst op actief ontstekingsproces - oorzaak identificeren'
            })

        # Priority 3: Vitamin D
        vitd = next((b for b in biomarkers
                    if 'vitamine d' in b['name'].lower() or 'vitamin d' in b['name'].lower()),
                   None)
        if vitd and vitd['status'] in ['critical', 'warning']:
            alerts.append({
                'title': 'Vitamine D Deficiëntie',
                'icon': '🟡',
                'marker': f"{vitd['name']}: {vitd['value']} {vitd['unit']}",
                'optimal': f"Optimaal: {vitd['optimal_range']} {vitd['unit']}",
                'description': 'Immuunfunctie suboptimaal, receptor mogelijk downgereguleerd'
            })

        return alerts[:3]  # Top 3 only

    def generate_priorities(
        self,
        biomarkers: List[Dict],
        dna_variants: List[Dict]
    ) -> List[Dict]:
        """Generate priority action areas (stub for now)"""
        # TODO: Implement in next task
        return []

    def generate_supplement_protocol(
        self,
        dna_variants: List[Dict],
        biomarkers: List[Dict]
    ) -> List[Dict]:
        """
        Generate personalized supplement protocol with timing

        Returns schedule with structure:
        {
            'time': '07:30',
            'time_label': 'Ochtend (nuchter)',
            'name': 'Fosfatidylcholine',
            'dosage': '600-800 mg',
            'reason': 'PEMT TT variant...',
            'badge': 'KERN' | 'KRITIEK' | 'ESSENTIEEL' | 'SUPPORT' | 'FASE 2'
        }
        """
        protocol = []

        # Detect key variants
        has_pemt_tt = any(
            v['gene'] == 'PEMT' and v['genotype'] == 'TT'
            for v in dna_variants
        )
        has_bhmt_issues = any(
            v['gene'] == 'BHMT' and v['severity'] in ['warning', 'critical']
            for v in dna_variants
        )
        has_mthfr = any(v['gene'] == 'MTHFR' for v in dna_variants)
        has_cbs_upregulation = any(
            v['gene'] == 'CBS' and 'AA' in v['genotype'] and 'rs234706' in v['rs_number']
            for v in dna_variants
        )
        has_comt_slow = any(
            v['gene'] == 'COMT' and v['severity'] in ['warning', 'info']
            for v in dna_variants
        )
        has_vdr_variants = any(v['gene'] == 'VDR' for v in dna_variants)

        # Check biomarkers
        low_vitd = any(
            ('vitamine d' in b['name'].lower() or 'vitamin d' in b['name'].lower())
            and b['status'] in ['warning', 'critical']
            for b in biomarkers
        )
        high_homocysteine = any(
            'homocyst' in b['name'].lower() and b['status'] == 'critical'
            for b in biomarkers
        )

        # 1. CHOLINE (if PEMT TT or BHMT issues) - ALWAYS FIRST
        if has_pemt_tt or has_bhmt_issues:
            reason_parts = []
            if has_pemt_tt:
                reason_parts.append("PEMT TT variant - geen endogene choline productie.")
            if has_bhmt_issues:
                reason_parts.append("BHMT downregulatie - shortcut pathway ondersteuning.")
            reason_parts.append("Essentieel voor homocysteïne conversie.")

            protocol.append({
                'time': '07:30',
                'time_label': 'Ochtend (nuchter)',
                'name': 'Fosfatidylcholine',
                'dosage': '600-800 mg (Sunflower Lecithin vorm)',
                'reason': ' '.join(reason_parts),
                'badge': 'KERN'
            })

        # 2. VITAMIN D (if low or VDR variants)
        if low_vitd or has_vdr_variants:
            vitd_marker = next(
                (b for b in biomarkers
                 if 'vitamine d' in b['name'].lower() or 'vitamin d' in b['name'].lower()),
                None
            )

            reason_parts = []
            if vitd_marker:
                unit = vitd_marker.get('unit', 'ng/ml')
                reason_parts.append(
                    f"Huidige waarde {vitd_marker['value']} {unit} → doel 50-60 ng/ml."
                )
            reason_parts.append("Vloeibare vorm voor betere absorptie. K2 voor calcium metabolisme.")
            if has_vdr_variants:
                reason_parts.append("VDR variants vereisen hogere dosis.")

            protocol.append({
                'time': '08:00',
                'time_label': 'Bij Ontbijt',
                'name': 'Vitamine D3 + K2 (vloeibaar)',
                'dosage': '4000-5000 IU D3 + 100 mcg K2-MK7',
                'reason': ' '.join(reason_parts),
                'badge': 'KRITIEK' if low_vitd else 'ESSENTIEEL'
            })

        # 3. ZINC (if BHMT or methylation issues)
        if has_bhmt_issues or has_mthfr or high_homocysteine:
            protocol.append({
                'time': '12:30',
                'time_label': 'Lunch',
                'name': 'Zink Bisglycinaat',
                'dosage': '25-30 mg elementair zink',
                'reason': 'Cruciaal voor: BHMT cofactor, SAMe conversie, methylatie support. Bisglycinaat vorm voor optimale absorptie.',
                'badge': 'ESSENTIEEL'
            })

        # 4. MAGNESIUM (if COMT slow or MTHFR)
        if has_comt_slow or has_mthfr:
            reason_parts = []
            if has_comt_slow:
                reason_parts.append("COMT ondersteuning voor neurotransmitter afbraak.")
            reason_parts.append("SAMe conversie cofactor. Glycinaat vorm voor maximale absorptie en geen laxerend effect.")

            protocol.append({
                'time': '15:00',
                'time_label': 'Middag',
                'name': 'Magnesium Glycinaat',
                'dosage': '400 mg elementair magnesium',
                'reason': ' '.join(reason_parts),
                'badge': 'SUPPORT'
            })

        # 5. METHYLATED B-COMPLEX (ONLY after 6 weeks if CBS upregulation)
        if has_mthfr:
            reason_parts = []
            if has_cbs_upregulation:
                reason_parts.append(
                    "⚠️ START PAS NA 6 WEKEN als choline pathway geoptimaliseerd is."
                )
            reason_parts.append("MTHFR varianten ondersteuning. Actieve vormen vereist voor optimale methylatie.")
            if has_cbs_upregulation:
                reason_parts.append("P5P voor CBS upregulatie.")

            protocol.append({
                'time': '20:00',
                'time_label': 'Avond',
                'name': 'Methylated B-Complex',
                'dosage': '5-MTHF 400mcg, Methylcobalamin 500mcg, P5P 25mg, R5P 25mg',
                'reason': ' '.join(reason_parts),
                'badge': 'FASE 2' if has_cbs_upregulation else 'KERN'
            })

        # 6. TMG/BETAINE (if BHMT issues or CBS upregulation)
        if has_bhmt_issues or has_cbs_upregulation:
            protocol.append({
                'time': '22:00',
                'time_label': 'Voor Bed',
                'name': 'Trimethylglycine (TMG/Betaine)',
                'dosage': '500-1000 mg',
                'reason': 'Direct cofactor voor BHMT "shortcut" pathway. Ondersteunt methylatie zonder CBS upregulatie. Synergistisch met choline.',
                'badge': 'KERN'
            })

        # Sort by time
        return sorted(protocol, key=lambda x: x['time'])

    def generate_3month_plan(
        self,
        dna_variants: List[Dict],
        biomarkers: List[Dict]
    ) -> List[Dict]:
        """
        Generate phased 3-month action plan

        Returns phases with structure:
        {
            'phase': 'Fase 1: Fundament Leggen',
            'duration': 'Week 1-6',
            'actions': [
                {
                    'icon': '🥚',
                    'title': 'Choline Pathway Herstellen',
                    'description': 'Start fosfatidylcholine...'
                }
            ],
            'warnings': ['⚠️ GEEN B-complex...']
        }
        """
        phases = []

        # Detect key issues
        has_high_homocysteine = any(
            'homocyst' in b['name'].lower() and b['status'] == 'critical'
            for b in biomarkers
        )
        has_inflammation = any(
            ('ferritin' in b['name'].lower() or 'crp' in b['name'].lower())
            and b['status'] in ['critical', 'warning']
            for b in biomarkers
        )
        has_cbs_upregulation = any(
            v['gene'] == 'CBS' and 'AA' in v['genotype']
            for v in dna_variants
        )
        has_comt_variants = any(v['gene'] == 'COMT' for v in dna_variants)

        # PHASE 1: Foundation (Week 1-6)
        phase1_actions = []

        if has_high_homocysteine:
            phase1_actions.append({
                'icon': '🥚',
                'title': 'Choline Pathway Herstellen (PRIORITEIT)',
                'description': 'Start fosfatidylcholine 600-800mg + TMG 500mg + zink 25mg. Dit is het fundament - BHMT shortcut moet werken voordat we methylatie verder pushen. Eet dagelijks 2-3 eieren + rund/kip/vis voor extra choline.'
            })

        phase1_actions.append({
            'icon': '☀️',
            'title': 'Vitamine D Normaliseren',
            'description': 'Vloeibare D3 4000-5000 IU + K2 100mcg dagelijks. Doel: 50-60 ng/ml binnen 6-8 weken. Meet opnieuw bij hertest.'
        })

        if has_inflammation:
            phase1_actions.append({
                'icon': '🧘',
                'title': 'Inflammatie Onderzoek',
                'description': 'Ferritine te hoog wijst op onderliggende oorzaak. Zoek: infectie? Chronische inflammatie? Auto-immuun? Werk samen met arts voor verder onderzoek.'
            })

        if has_comt_variants:
            phase1_actions.append({
                'icon': '🧠',
                'title': 'COMT Support Starten',
                'description': 'Magnesium glycinaat 400mg vanaf week 1. COMT slow variants + lage SAMe = nog tragere catecholamine afbraak. Magnesium helpt COMT enzym werken.'
            })

        phase1_warnings = []
        if has_cbs_upregulation:
            phase1_warnings.append(
                "⚠️ LET OP Week 1-6: Nog GEEN methylated B-complex starten! CBS upregulatie + onvoldoende choline = ammonia buildup risico. Wacht tot week 6 voor veilige implementatie."
            )

        phases.append({
            'phase': 'Fase 1: Fundament Leggen',
            'duration': 'Week 1-6',
            'actions': phase1_actions,
            'warnings': phase1_warnings
        })

        # PHASE 2: Optimization (Week 6-8)
        phase2_actions = [
            {
                'icon': '📊',
                'title': 'Hertest & Evaluatie (Week 6)',
                'description': 'Meet opnieuw: HomocysteÏne (doel: <10), Ferritine (doel: <200), Vitamine D (doel: 50+), Triglyceriden, Zink, Magnesium RBC. Evalueer of choline pathway werkt voordat je verder gaat.'
            },
            {
                'icon': '💊',
                'title': 'B-Complex Toevoegen (NA Week 6)',
                'description': 'ALS homocysteïne gedaald: Start methylated B-complex (5-MTHF 400mcg, methylcobalamin 500mcg, P5P 25mg). Start laag en bouw op. Monitor op overstimulatie. ALS niet gedaald: verhoog eerst choline/betaine dosis.'
            },
            {
                'icon': '🥬',
                'title': 'Voeding Optimaliseren',
                'description': 'Verhoog: Groene bladgroenten (folaat), citrus (vitamine C), bonen, quinoa/spinazie/biet (betaine), eieren (choline), vette vis (omega-3). Modereer: Rood vlees (ammonia), alcohol (MAOA remming).'
            },
            {
                'icon': '🔬',
                'title': 'Antioxidant Support',
                'description': 'NAC 600mg 2x/dag voor glutathione. Vitamine C 1000mg. NOS3 variants verhogen vrije radicalen - antioxidanten zijn essentieel.'
            }
        ]

        phases.append({
            'phase': 'Fase 2: Methylatie Optimaliseren',
            'duration': 'Week 6-8',
            'actions': phase2_actions,
            'warnings': []
        })

        # PHASE 3: Fine-tuning (Week 8-12)
        phase3_actions = [
            {
                'icon': '🎯',
                'title': 'Symptoom Tracking',
                'description': 'Monitor: energie levels, slaapkwaliteit, mentale helderheid, mood stabiliteit, stress tolerantie. COMT/MAOA/VDR variants beïnvloeden neurotransmitters - let op veranderingen.'
            },
            {
                'icon': '⚖️',
                'title': 'Dosering Aanpassen',
                'description': 'Op basis van lab resultaten en symptomen: fine-tune B-complex dosis, overweeg SAMe (100-200mg) als homocysteïne laag genoeg, adjust choline indien nodig.'
            },
            {
                'icon': '🔄',
                'title': 'Lifestyle Optimalisatie',
                'description': 'Slaap: 7-8u consistent. Stress: Meditatie/ademwerk (MAOA warrior gene). Beweging: Mix cardio/kracht, niet overtrainen. Hydratatie: 2-3L water.'
            },
            {
                'icon': '📋',
                'title': 'Week 12: Complete Hertest',
                'description': 'Full panel: Homocysteïne (doel: <8), Ferritine (doel: 70-90), Vitamine D (doel: 50-60), Triglyceriden, Cholesterol, HbA1c, CRP, Complete bloedbeeld, Zink, Magnesium RBC, B12 actief.'
            }
        ]

        phases.append({
            'phase': 'Fase 3: Fine-tuning & Monitoring',
            'duration': 'Week 8-12',
            'actions': phase3_actions,
            'warnings': []
        })

        return phases

    def build_html(self, **kwargs) -> str:
        """Build final HTML from data using HELD branded template"""
        from template_builder import get_css

        patient_name = kwargs['patient_name']
        consult_date = kwargs['consult_date']
        biomarkers = kwargs['biomarkers']
        dna_variants = kwargs['dna_variants']
        critical_alerts = kwargs['critical_alerts']
        supplement_protocol = kwargs['supplement_protocol']
        action_plan = kwargs['action_plan']
        welldium_link = kwargs.get('welldium_link', '')

        # Build HTML sections
        alerts_html = self._build_alerts_html(critical_alerts)
        biomarkers_html = self._build_biomarkers_html(biomarkers)
        dna_html = self._build_dna_html(dna_variants)
        supplements_html = self._build_supplements_html(supplement_protocol)
        plan_html = self._build_plan_html(action_plan)

        # Format date
        from datetime import datetime
        try:
            date_obj = datetime.strptime(consult_date, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%-d %b %Y")
        except:
            formatted_date = consult_date

        return f"""<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{patient_name} - Precision Health Dashboard | HELD</title>
    <style>
        {get_css()}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <div class="header-top">
                <div>
                    <div class="logo">HELD</div>
                    <div class="tagline">Preventieve Gezondheid & Biohacking</div>
                </div>
                <button onclick="window.print()" style="background: white; color: var(--jungle-green); padding: 0.75rem 1.5rem; border-radius: 9999px; border: 2px solid white; font-weight: 700; font-size: 0.95rem; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; gap: 0.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                    <span style="font-size: 1.2rem;">📄</span>
                    Download als PDF
                </button>
            </div>

            <div class="patient-info">
                <div class="info-card">
                    <div class="info-label">Patiënt</div>
                    <div class="info-value">{patient_name}</div>
                </div>
                <div class="info-card">
                    <div class="info-label">Consult Datum</div>
                    <div class="info-value">{formatted_date}</div>
                </div>
            </div>
        </div>

        <!-- Critical Alerts -->
        <div class="alerts-section">
            {alerts_html}
        </div>

        <!-- Blood Biomarkers -->
        <div class="section">
            <div class="section-header">
                <h2 class="section-title">🩸 Bloedwaarden Analyse</h2>
                <p class="section-subtitle">Focus op optimale (functionele) ranges</p>
            </div>
            <div class="biomarkers-grid">
                {biomarkers_html}
            </div>
        </div>

        <!-- DNA Variants -->
        <div class="section">
            <div class="section-header">
                <h2 class="section-title">🧬 DNA Methylatie Analyse</h2>
                <p class="section-subtitle">32-gene panel resultaten met impact assessments</p>
            </div>
            <div class="dna-grid">
                {dna_html}
            </div>
        </div>

        <!-- Supplement Protocol -->
        <div class="section">
            <div class="section-header">
                <h2 class="section-title">💊 Dagelijks Supplementenprotocol</h2>
                <p class="section-subtitle">Gepersonaliseerd op basis van DNA & biomarkers - timing is cruciaal</p>
            </div>
            <div class="supplement-grid">
                {supplements_html}
            </div>
            {f'<a href="{welldium_link}" target="_blank" style="display: inline-block; margin-top: 1rem; padding: 1rem 2rem; background: var(--american-orange); color: white; text-decoration: none; border-radius: 9999px; font-weight: 700;">Bestel via Welldium →</a>' if welldium_link else ''}
        </div>

        <!-- 3-Month Action Plan -->
        <div class="section">
            <div class="section-header">
                <h2 class="section-title">📅 3-Maanden Actieplan</h2>
                <p class="section-subtitle">Gefaseerde aanpak voor optimale resultaten</p>
            </div>
            <div class="timeline">
                {plan_html}
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <div class="footer-text">HELD Preventieve Gezondheid & Biohacking</div>
            <div class="footer-note">&copy; 2025 HELD. Alle rechten voorbehouden.</div>
            <div class="disclaimer">
                <strong>Medische Disclaimer:</strong> Dit rapport is uitsluitend bedoeld voor informatieve doeleinden en vormt geen medisch advies, diagnose of behandeling. Consulteer altijd een bevoegde arts of gezondheidsprofessional voordat u wijzigingen aanbrengt in uw supplementgebruik, medicatie of levensstijl. De informatie in dit rapport is gebaseerd op genetische en biomarker analyses en moet worden geïnterpreteerd in de context van uw individuele gezondheidssituatie. HELD is niet aansprakelijk voor enige gevolgen die voortvloeien uit het gebruik van deze informatie.
            </div>
        </div>
    </div>
</body>
</html>"""

    def _build_alerts_html(self, alerts: List[Dict]) -> str:
        """Build HTML for critical alerts section"""
        if not alerts:
            return '<div class="alert-card alert-good"><div class="alert-title"><span class="alert-icon">✅</span><span>Geen Kritieke Afwijkingen</span></div><div class="alert-description">Alle kritieke markers binnen acceptabele ranges.</div></div>'

        html_parts = []
        for alert in alerts:
            alert_class = 'alert-critical' if alert['icon'] == '🔴' else 'alert-warning'
            html_parts.append(f"""
            <div class="alert-card {alert_class}">
                <div class="alert-title">
                    <span class="alert-icon">{alert['icon']}</span>
                    <span>{alert['title']}</span>
                </div>
                <div class="alert-description">
                    <strong>{alert['marker']}</strong> ({alert['optimal']})<br>
                    {alert['description']}
                </div>
            </div>
            """)

        return '\n'.join(html_parts)

    def _build_biomarkers_html(self, biomarkers: List[Dict]) -> str:
        """Build HTML for biomarkers grid"""
        if not biomarkers:
            return '<p>Geen bloedwaarden beschikbaar.</p>'

        html_parts = []
        for marker in biomarkers:
            status_class = marker['status']

            html_parts.append(f"""
            <div class="biomarker-card">
                <div class="biomarker-header">
                    <div class="biomarker-name">{marker['name']}</div>
                    <div class="biomarker-status status-{status_class}">{status_class.upper()}</div>
                </div>
                <div class="biomarker-values">
                    <div class="value-row">
                        <span class="value-label">Waarde:</span>
                        <span class="value-number">{marker['value']} {marker['unit']}</span>
                    </div>
                    <div class="value-row">
                        <span class="value-label">Optimaal:</span>
                        <span class="value-number">{marker['optimal_range']} {marker['unit']}</span>
                    </div>
                </div>
            </div>
            """)

        return '\n'.join(html_parts)

    def _build_dna_html(self, dna_variants: List[Dict]) -> str:
        """Build HTML for DNA variants section"""
        if not dna_variants:
            return '<p>Geen DNA data beschikbaar.</p>'

        html_parts = []
        for variant in dna_variants:
            severity_class = variant['severity']

            html_parts.append(f"""
            <div class="dna-card">
                <div class="dna-header">
                    <div class="gene-name">{variant['gene']} {variant['rs_number']}</div>
                    <div class="genotype">{variant['genotype']}</div>
                </div>
                {f"<div style='font-size: 0.9rem; color: var(--jungle-green); font-weight: 600; margin-bottom: 0.5rem;'>[{variant['variant_name']}]</div>" if variant['variant_name'] else ''}
                <div class="variant-impact">
                    <div class="impact-title">Impact</div>
                    <div class="impact-text">{variant['impact']}</div>
                </div>
            </div>
            """)

        return '\n'.join(html_parts)

    def _build_supplements_html(self, supplements: List[Dict]) -> str:
        """Build HTML for supplement protocol"""
        if not supplements:
            return '<p>Geen supplementenprotocol gegenereerd.</p>'

        html_parts = []
        for supp in supplements:
            badge_class = supp['badge'].lower().replace(' ', '-')

            html_parts.append(f"""
            <div class="supplement-card">
                <div class="supplement-time">
                    <div class="time-label">{supp['time_label']}</div>
                    <div class="time-value">{supp['time']}</div>
                </div>
                <div class="supplement-info">
                    <div class="supplement-name">{supp['name']}</div>
                    <div class="supplement-dosage">{supp['dosage']}</div>
                    <div class="supplement-reason">{supp['reason']}</div>
                </div>
                <div class="supplement-badge badge-{badge_class}">{supp['badge']}</div>
            </div>
            """)

        return '\n'.join(html_parts)

    def _build_plan_html(self, phases: List[Dict]) -> str:
        """Build HTML for 3-month action plan"""
        if not phases:
            return '<p>Geen actieplan gegenereerd.</p>'

        html_parts = []
        for phase in phases:
            # Build actions HTML
            actions_html = []
            for action in phase['actions']:
                actions_html.append(f"""
                <div class="action-item">
                    <div class="action-icon">{action['icon']}</div>
                    <div class="action-content">
                        <div class="action-title">{action['title']}</div>
                        <div class="action-description">{action['description']}</div>
                    </div>
                </div>
                """)

            # Build warnings HTML
            warnings_html = ''
            if phase.get('warnings'):
                warnings_items = ''.join(f'<li>{w}</li>' for w in phase['warnings'])
                warnings_html = f"""
                <div class="phase-warnings">
                    <ul>{warnings_items}</ul>
                </div>
                """

            html_parts.append(f"""
            <div class="timeline-item">
                <div class="timeline-dot"></div>
                <div class="timeline-phase">
                    <div class="phase-header">
                        <div class="phase-title">{phase['phase']}</div>
                        <div class="phase-duration">{phase['duration']}</div>
                    </div>
                    <div class="phase-actions">
                        {''.join(actions_html)}
                    </div>
                    {warnings_html}
                </div>
            </div>
            """)

        return '\n'.join(html_parts)

    def save_dashboard(self, html: str, patient_name: str) -> str:
        """Save HTML to file and return path"""
        # Create outputs directory
        output_dir = Path('outputs')
        output_dir.mkdir(exist_ok=True)

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d")
        filename = f"{patient_name.replace(' ', '_')}_HELD_Dashboard_{timestamp}.html"
        filepath = output_dir / filename

        # Write file
        filepath.write_text(html, encoding='utf-8')

        return str(filepath)


def main():
    """Interactive CLI for dashboard generation"""
    print("=" * 70)
    print("HELD Precision Health Dashboard Generator")
    print("=" * 70)
    print()

    # Initialize generator
    try:
        generator = HELDDashboardGenerator()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Make sure you're running from the project root directory.")
        return 1

    # Step 1: Get patient name
    patient_name = input("Patient naam: ").strip()
    if not patient_name:
        print("Error: Patient naam is verplicht")
        return 1

    # Step 2: Get consultation date
    consult_date = input("Consult datum (YYYY-MM-DD) [vandaag]: ").strip()
    if not consult_date:
        consult_date = datetime.now().strftime("%Y-%m-%d")

    # Step 3: Get consultation notes (optional)
    print("\nConsult notities (optioneel, Enter om over te slaan):")
    consult_notes = input().strip()

    # Step 4: Get blood data
    print("\nBLOEDWAARDEN")
    print("Plak de bloedwaarden tekst (druk Enter 2x om te stoppen):")
    print("-" * 70)
    blood_lines = []
    empty_count = 0
    while empty_count < 2:
        line = input()
        if not line:
            empty_count += 1
        else:
            empty_count = 0
            blood_lines.append(line)
    blood_data = '\n'.join(blood_lines)

    if not blood_data.strip():
        print("Error: Bloedwaarden zijn verplicht")
        return 1

    # Step 5: Get DNA data
    print("\nDNA METHYLATIE DATA")
    print("Plak de DNA methylatie resultaten (druk Enter 2x om te stoppen):")
    print("-" * 70)
    dna_lines = []
    empty_count = 0
    while empty_count < 2:
        line = input()
        if not line:
            empty_count += 1
        else:
            empty_count = 0
            dna_lines.append(line)
    dna_data = '\n'.join(dna_lines)

    if not dna_data.strip():
        print("Error: DNA data is verplicht")
        return 1

    # Step 6: Get Welldium link (optional)
    welldium_link = input("\nWelldium bestel link (optioneel): ").strip()

    # Step 7: Generate dashboard
    print("\nGenereren van dashboard...")
    try:
        html = generator.generate_dashboard(
            patient_name=patient_name,
            consult_date=consult_date,
            consult_notes=consult_notes,
            blood_data=blood_data,
            dna_data=dna_data,
            welldium_link=welldium_link
        )
    except Exception as e:
        print(f"Fout bij genereren: {e}")
        import traceback
        traceback.print_exc()
        return 1

    # Step 8: Save dashboard
    try:
        filepath = generator.save_dashboard(html, patient_name)
    except Exception as e:
        print(f"Fout bij opslaan: {e}")
        return 1

    # Success!
    print("\n" + "=" * 70)
    print("Dashboard succesvol gegenereerd!")
    print(f"Bestand: {filepath}")
    print(f"\nOpen in browser:")
    print(f"   file://{Path(filepath).absolute()}")
    print(f"\nVoor PDF export:")
    print(f"   1. Open het bestand in een browser")
    print(f"   2. Klik op 'Download als PDF' knop")
    print(f"   3. Of gebruik Print -> Save as PDF")
    print("=" * 70)

    return 0


if __name__ == "__main__":
    exit(main())
