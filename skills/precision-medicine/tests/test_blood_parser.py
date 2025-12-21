"""Tests for blood test data parser"""
from parsers.blood_parser import BloodParser


def test_parse_single_biomarker_with_optimal_range():
    """Test parsing a single biomarker with optimal range"""
    parser = BloodParser()
    text = "HomocysteÏne + 18.0 Opt:<8.0 V.N 3.7-13.9 µmol/L"

    result = parser.parse(text)

    assert len(result) == 1
    assert result[0]['name'] == 'HomocysteÏne'
    assert result[0]['value'] == 18.0
    assert result[0]['unit'] == 'µmol/L'
    assert result[0]['optimal_range'] == '<8.0'
    assert result[0]['status'] == 'critical'
    assert result[0]['flag'] == '+'


def test_parse_multiple_biomarkers():
    """Test parsing multiple biomarkers"""
    parser = BloodParser()
    text = """HomocysteÏne + 18.0 Opt:<8.0 V.N 3.7-13.9 µmol/L
Ferritine + 307 50-120:opt. 22-322:VN µg/L
Vitamine D - 39.7 45-60:opt. 30-100:VN ng/ml"""

    result = parser.parse(text)

    assert len(result) == 3
    assert result[0]['name'] == 'HomocysteÏne'
    assert result[1]['name'] == 'Ferritine'
    assert result[2]['name'] == 'Vitamine D'


def test_determine_status_critical_high():
    """Test status determination for critically high values"""
    parser = BloodParser()

    # Homocysteine 18.0 with optimal <8.0 = critical
    status = parser.determine_status(18.0, '<8.0', '+')
    assert status == 'critical'


def test_determine_status_warning_low():
    """Test status determination for warning low values"""
    parser = BloodParser()

    # Vitamin D 39.7 with optimal 45-60 = warning
    status = parser.determine_status(39.7, '45-60', '-')
    assert status == 'warning'


def test_determine_status_optimal():
    """Test status determination for optimal values"""
    parser = BloodParser()

    # Value within optimal range = optimal
    status = parser.determine_status(55.0, '45-60', '')
    assert status == 'optimal'


def test_parse_empty_string():
    """Test parsing empty string returns empty list"""
    parser = BloodParser()
    result = parser.parse('')
    assert result == []


def test_parse_malformed_line():
    """Test parsing malformed line skips it gracefully"""
    parser = BloodParser()
    text = "Invalid line\nHomocysteÏne + 18.0 Opt:<8.0 V.N 3.7-13.9 µmol/L"

    result = parser.parse(text)

    assert len(result) == 1  # Only valid line parsed
    assert result[0]['name'] == 'HomocysteÏne'


def test_parse_with_header_line():
    """Test parsing skips header lines gracefully"""
    parser = BloodParser()
    text = """Naam Waarde Range
HomocysteÏne + 18.0 Opt:<8.0 V.N 3.7-13.9 µmol/L"""

    result = parser.parse(text)

    assert len(result) == 1
    assert result[0]['name'] == 'HomocysteÏne'
