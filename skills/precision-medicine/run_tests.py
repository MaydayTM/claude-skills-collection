#!/usr/bin/env python3
"""Simple test runner for dashboard generator tests"""

import sys
import json
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from held_dashboard_generator import HELDDashboardGenerator


def test_generator_initialization():
    """Test generator initializes with config"""
    print("TEST: test_generator_initialization...", end=" ")
    try:
        generator = HELDDashboardGenerator()
        assert generator.config is not None
        assert generator.config['brand_name'] == 'HELD'
        print("✓ PASS")
        return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False


def test_load_config():
    """Test config loading"""
    print("TEST: test_load_config...", end=" ")
    try:
        generator = HELDDashboardGenerator()
        assert 'colors' in generator.config
        assert 'primary' in generator.config['colors']
        assert generator.config['colors']['primary'] == '#34B27B'
        print("✓ PASS")
        return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False


def test_identify_critical_alerts_homocysteine():
    """Test identification of critical homocysteine alert"""
    print("TEST: test_identify_critical_alerts_homocysteine...", end=" ")
    try:
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
        print("✓ PASS")
        return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False


def test_identify_critical_alerts_top_3_only():
    """Test only top 3 alerts are returned"""
    print("TEST: test_identify_critical_alerts_top_3_only...", end=" ")
    try:
        generator = HELDDashboardGenerator()
        biomarkers = [
            {'name': f'Marker{i}', 'value': 100.0, 'unit': 'x',
             'optimal_range': '<50', 'status': 'critical', 'flag': '+'}
            for i in range(10)
        ]
        alerts = generator.identify_critical_alerts(biomarkers)
        assert len(alerts) <= 3
        print("✓ PASS")
        return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False


def test_generate_dashboard_basic():
    """Test basic dashboard generation"""
    print("TEST: test_generate_dashboard_basic...", end=" ")
    try:
        generator = HELDDashboardGenerator()

        # Load test data
        test_data_path = Path(__file__).parent / 'tests' / 'fixtures' / 'test_data.json'
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
        assert len(html) > 1000, f"HTML too short: {len(html)} chars"
        assert 'HELD' in html
        assert test_data['patient_name'] in html
        print("✓ PASS")
        return True
    except Exception as e:
        print(f"✗ FAIL: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 70)
    print("Running Dashboard Generator Tests")
    print("=" * 70)

    tests = [
        test_generator_initialization,
        test_load_config,
        test_identify_critical_alerts_homocysteine,
        test_identify_critical_alerts_top_3_only,
        test_generate_dashboard_basic
    ]

    results = [test() for test in tests]

    print("=" * 70)
    print(f"Results: {sum(results)}/{len(results)} tests passed")

    if all(results):
        print("✓ All tests PASSED!")
        sys.exit(0)
    else:
        print("✗ Some tests FAILED")
        sys.exit(1)
