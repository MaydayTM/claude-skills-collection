"""Integration tests for complete dashboard generation"""
import pytest
from pathlib import Path
import json
from held_dashboard_generator import HELDDashboardGenerator


def test_full_dashboard_generation_mario():
    """Test complete dashboard generation with Mario's data"""
    # Load Mario's test data
    test_data_path = Path(__file__).parent / 'fixtures' / 'test_data.json'
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
    assert '<!DOCTYPE html>' in html
    assert 'HELD' in html
    assert mario_data['patient_name'] in html

    # Verify critical content
    assert 'HomocysteÏne' in html  # Blood marker
    assert 'MTHFR' in html  # DNA variant
    assert 'CBS' in html  # Critical CBS variant
    assert 'PEMT' in html  # PEMT TT variant

    # Verify supplement protocol
    assert 'Fosfatidylcholine' in html  # Choline for PEMT
    assert 'FASE 2' in html  # CBS upregulation warning

    # Verify 3-month plan
    assert 'Fase 1' in html
    assert 'Fase 2' in html
    assert 'Fase 3' in html

    # Verify safety warnings
    assert 'B-complex' in html  # CBS warning should mention B-complex

    # Verify legal
    assert 'disclaimer' in html.lower()

    # Verify branding
    assert '#34B27B' in html or 'jungle-green' in html.lower()

    # Save for manual inspection
    output_path = Path('outputs/test_mario_dashboard.html')
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(html, encoding='utf-8')

    print(f"\n✅ Integration test passed!")
    print(f"📄 Dashboard saved to: {output_path}")
    print(f"🔗 Open: file://{output_path.absolute()}")


def test_dashboard_save():
    """Test dashboard save functionality"""
    generator = HELDDashboardGenerator()

    html = "<html><body>Test Dashboard</body></html>"
    filepath = generator.save_dashboard(html, "Test Patient")

    # Verify file exists
    assert Path(filepath).exists()

    # Verify content
    saved_html = Path(filepath).read_text(encoding='utf-8')
    assert saved_html == html

    # Clean up
    Path(filepath).unlink()
