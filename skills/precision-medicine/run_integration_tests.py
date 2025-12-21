"""Simple integration test runner without pytest"""
import sys
from pathlib import Path
import json
from held_dashboard_generator import HELDDashboardGenerator


def test_full_dashboard_generation_mario():
    """Test complete dashboard generation with Mario's data"""
    print("\n" + "="*70)
    print("TEST: Full Dashboard Generation with Mario's Data")
    print("="*70)

    # Load Mario's test data
    test_data_path = Path('tests/fixtures/test_data.json')
    with open(test_data_path) as f:
        mario_data = json.load(f)

    # Generate dashboard
    generator = HELDDashboardGenerator()
    html = generator.generate_dashboard(
        patient_name=mario_data['patient_name'],
        consult_date=mario_data['consult_date'],
        consult_notes='Test consultation for Mario',
        blood_data=mario_data['blood_sample'],
        dna_data=mario_data['dna_sample'],
        welldium_link='https://welldium.com/r/test123'
    )

    # Verify HTML structure
    assert '<!DOCTYPE html>' in html, "Missing DOCTYPE"
    assert 'HELD' in html, "Missing HELD branding"
    assert mario_data['patient_name'] in html, "Missing patient name"

    # Verify critical content
    assert 'HomocysteÏne' in html, "Missing HomocysteÏne blood marker"
    assert 'MTHFR' in html, "Missing MTHFR DNA variant"
    assert 'CBS' in html, "Missing CBS DNA variant"
    assert 'PEMT' in html, "Missing PEMT DNA variant"

    # Verify supplement protocol
    assert 'Fosfatidylcholine' in html, "Missing Choline supplement"
    assert 'FASE 2' in html, "Missing CBS upregulation warning (FASE 2 badge)"

    # Verify 3-month plan
    assert 'Fase 1' in html, "Missing Fase 1 in action plan"
    assert 'Fase 2' in html, "Missing Fase 2 in action plan"
    assert 'Fase 3' in html, "Missing Fase 3 in action plan"

    # Verify safety warnings
    assert 'B-complex' in html, "Missing B-complex in CBS warning"

    # Verify legal
    assert 'disclaimer' in html.lower(), "Missing disclaimer"

    # Verify branding
    assert '#34B27B' in html or 'jungle-green' in html.lower(), "Missing HELD brand colors"

    # Save for manual inspection
    output_path = Path('outputs/test_mario_dashboard.html')
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(html, encoding='utf-8')

    print(f"✅ All assertions passed!")
    print(f"📄 Dashboard saved to: {output_path}")
    print(f"🔗 Open: file://{output_path.absolute()}")

    return True


def test_dashboard_save():
    """Test dashboard save functionality"""
    print("\n" + "="*70)
    print("TEST: Dashboard Save Functionality")
    print("="*70)

    generator = HELDDashboardGenerator()

    html = "<html><body>Test Dashboard</body></html>"
    filepath = generator.save_dashboard(html, "Test Patient")

    # Verify file exists
    assert Path(filepath).exists(), f"File not created: {filepath}"

    # Verify content
    saved_html = Path(filepath).read_text(encoding='utf-8')
    assert saved_html == html, "Saved content doesn't match"

    print(f"✅ Dashboard saved successfully to: {filepath}")

    # Clean up
    Path(filepath).unlink()
    print(f"✅ Cleanup complete")

    return True


def main():
    """Run all integration tests"""
    print("\n" + "="*70)
    print("INTEGRATION TESTS FOR HELD DASHBOARD GENERATOR")
    print("="*70)

    tests = [
        test_full_dashboard_generation_mario,
        test_dashboard_save
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    print("\n" + "="*70)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*70)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
