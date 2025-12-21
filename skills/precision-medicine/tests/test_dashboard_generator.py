"""Tests for HELD Dashboard Generator"""
import pytest
from held_dashboard_generator import HELDDashboardGenerator
import json
from pathlib import Path


def test_generator_initialization():
    """Test generator initializes with config"""
    generator = HELDDashboardGenerator()

    assert generator.config is not None
    assert generator.config['brand_name'] == 'HELD'


def test_load_config():
    """Test config loading"""
    generator = HELDDashboardGenerator()

    assert 'colors' in generator.config
    assert 'primary' in generator.config['colors']
    assert generator.config['colors']['primary'] == '#34B27B'


def test_identify_critical_alerts_homocysteine():
    """Test identification of critical homocysteine alert"""
    generator = HELDDashboardGenerator()

    biomarkers = [
        {
            'name': 'HomocysteÏne',
            'value': 18.0,
            'unit': 'µmol/L',
            'optimal_range': '<8.0',
            'status': 'critical',
            'flag': '+'
        }
    ]

    alerts = generator.identify_critical_alerts(biomarkers)

    assert len(alerts) >= 1
    assert alerts[0]['marker'].startswith('HomocysteÏne')
    assert '18.0' in alerts[0]['marker']


def test_identify_critical_alerts_top_3_only():
    """Test only top 3 alerts are returned"""
    generator = HELDDashboardGenerator()

    biomarkers = [
        {'name': f'Marker{i}', 'value': 100.0, 'unit': 'x',
         'optimal_range': '<50', 'status': 'critical', 'flag': '+'}
        for i in range(10)
    ]

    alerts = generator.identify_critical_alerts(biomarkers)

    assert len(alerts) <= 3


def test_generate_dashboard_basic():
    """Test basic dashboard generation"""
    generator = HELDDashboardGenerator()

    # Load test data
    test_data_path = Path(__file__).parent / 'fixtures' / 'test_data.json'
    with open(test_data_path) as f:
        test_data = json.load(f)

    html = generator.generate_dashboard(
        patient_name=test_data['patient_name'],
        consult_date=test_data['consult_date'],
        consult_notes='Test consultation notes',
        blood_data=test_data['blood_sample'],
        dna_data=test_data['dna_sample']
    )

    assert isinstance(html, str)
    assert len(html) > 1000  # Should be substantial HTML
    assert 'HELD' in html
    assert test_data['patient_name'] in html


def test_generate_supplement_protocol_pemt_tt():
    """Test supplement protocol includes choline for PEMT TT"""
    generator = HELDDashboardGenerator()

    dna_variants = [
        {
            'gene': 'PEMT',
            'rs_number': 'rs7946',
            'genotype': 'TT',
            'variant_name': '',
            'impact': 'Potential for reduced choline synthesis',
            'severity': 'warning'
        }
    ]
    biomarkers = []

    protocol = generator.generate_supplement_protocol(dna_variants, biomarkers)

    # Should include choline
    choline = next((s for s in protocol if 'choline' in s['name'].lower()), None)
    assert choline is not None
    assert choline['badge'] == 'KERN'
    assert '07:30' in choline['time']


def test_generate_supplement_protocol_cbs_upregulation():
    """Test CBS upregulation gets FASE 2 badge for B-complex"""
    generator = HELDDashboardGenerator()

    dna_variants = [
        {
            'gene': 'CBS',
            'rs_number': 'rs234706',
            'genotype': 'AA',
            'variant_name': '',
            'impact': 'Up to 10x CBS activity',
            'severity': 'critical'
        },
        {
            'gene': 'MTHFR',
            'rs_number': 'rs1801133',
            'genotype': 'AG',
            'variant_name': 'C677T',
            'impact': '40% reduction',
            'severity': 'warning'
        }
    ]
    biomarkers = []

    protocol = generator.generate_supplement_protocol(dna_variants, biomarkers)

    # B-complex should be FASE 2 (not KERN) due to CBS upregulation
    b_complex = next((s for s in protocol if 'B-Complex' in s['name']), None)
    assert b_complex is not None
    assert b_complex['badge'] == 'FASE 2'


def test_generate_supplement_protocol_timing_order():
    """Test supplements are returned in chronological order"""
    generator = HELDDashboardGenerator()

    dna_variants = [
        {'gene': 'PEMT', 'genotype': 'TT', 'severity': 'warning', 'rs_number': 'rs7946'},
        {'gene': 'MTHFR', 'genotype': 'AG', 'severity': 'warning', 'rs_number': 'rs1801133'},
    ]
    biomarkers = [
        {'name': 'Vitamine D', 'value': 35.0, 'status': 'warning'}
    ]

    protocol = generator.generate_supplement_protocol(dna_variants, biomarkers)

    # Verify chronological order
    times = [s['time'] for s in protocol]
    assert times == sorted(times)


def test_generate_3month_plan_phases():
    """Test 3-month plan generates 3 phases"""
    generator = HELDDashboardGenerator()

    dna_variants = []
    biomarkers = []

    plan = generator.generate_3month_plan(dna_variants, biomarkers)

    assert len(plan) == 3
    assert 'Fase 1' in plan[0]['phase']
    assert 'Fase 2' in plan[1]['phase']
    assert 'Fase 3' in plan[2]['phase']


def test_generate_3month_plan_cbs_warning():
    """Test CBS upregulation adds warning to Phase 1"""
    generator = HELDDashboardGenerator()

    dna_variants = [
        {
            'gene': 'CBS',
            'rs_number': 'rs234706',
            'genotype': 'AA',
            'severity': 'critical'
        }
    ]
    biomarkers = []

    plan = generator.generate_3month_plan(dna_variants, biomarkers)

    # Phase 1 should have CBS warning
    phase1 = plan[0]
    assert len(phase1['warnings']) > 0
    assert any('B-complex' in w for w in phase1['warnings'])


def test_generate_3month_plan_high_homocysteine():
    """Test high homocysteine adds choline action to Phase 1"""
    generator = HELDDashboardGenerator()

    dna_variants = []
    biomarkers = [
        {
            'name': 'HomocysteÏne',
            'value': 18.0,
            'status': 'critical'
        }
    ]

    plan = generator.generate_3month_plan(dna_variants, biomarkers)

    # Phase 1 should mention choline
    phase1 = plan[0]
    assert any('choline' in a['description'].lower() for a in phase1['actions'])
