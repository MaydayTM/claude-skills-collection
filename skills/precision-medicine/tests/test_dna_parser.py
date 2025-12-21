"""Tests for DNA methylation data parser"""
import pytest
from parsers.dna_parser import DNAParser


def test_parse_single_variant():
    """Test parsing a single DNA variant"""
    parser = DNAParser()
    text = "MTHFR rs1801133 AG [C677T] Up to 40% reduction in gene function"

    result = parser.parse(text)

    assert len(result) == 1
    assert result[0]['gene'] == 'MTHFR'
    assert result[0]['rs_number'] == 'rs1801133'
    assert result[0]['genotype'] == 'AG'
    assert result[0]['variant_name'] == 'C677T'
    assert 'reduction' in result[0]['impact'].lower()
    assert result[0]['severity'] in ['critical', 'warning', 'info']


def test_parse_multiple_variants():
    """Test parsing multiple DNA variants"""
    parser = DNAParser()
    text = """MTHFR rs1801133 AG [C677T] Up to 40% reduction in gene function
CBS rs234706 AA Thought to be the strongest indicator of increased (up to 10x) CBS activity
PEMT rs7946 TT Potential for reduced choline synthesis"""

    result = parser.parse(text)

    assert len(result) == 3
    assert result[0]['gene'] == 'MTHFR'
    assert result[1]['gene'] == 'CBS'
    assert result[2]['gene'] == 'PEMT'


def test_determine_severity_cbs_upregulation():
    """Test CBS rs234706 AA is flagged as critical"""
    parser = DNAParser()

    severity = parser.determine_severity(
        gene='CBS',
        rs_number='rs234706',
        genotype='AA',
        impact='increased (up to 10x) CBS activity'
    )

    assert severity == 'critical'


def test_determine_severity_pemt_tt():
    """Test PEMT TT is flagged as warning"""
    parser = DNAParser()

    severity = parser.determine_severity(
        gene='PEMT',
        rs_number='rs7946',
        genotype='TT',
        impact='reduced choline synthesis'
    )

    assert severity == 'warning'


def test_determine_severity_mthfr_heterozygous():
    """Test MTHFR heterozygous variants are warning"""
    parser = DNAParser()

    severity = parser.determine_severity(
        gene='MTHFR',
        rs_number='rs1801133',
        genotype='AG',
        impact='40% reduction in gene function'
    )

    assert severity == 'warning'


def test_extract_variant_name():
    """Test variant name extraction from brackets"""
    parser = DNAParser()
    text = "MTHFR rs1801133 AG [C677T] Some impact text"

    result = parser.parse(text)

    assert result[0]['variant_name'] == 'C677T'


def test_parse_empty_string():
    """Test parsing empty string returns empty list"""
    parser = DNAParser()
    result = parser.parse('')
    assert result == []


def test_parse_no_variant_name():
    """Test parsing without variant name still works"""
    parser = DNAParser()
    text = "COMT rs4680 AG Some impact without brackets"

    result = parser.parse(text)

    assert len(result) == 1
    assert result[0]['gene'] == 'COMT'
    assert result[0]['variant_name'] == ''
