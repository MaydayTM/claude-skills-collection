"""DNA methylation data parser"""
import re
from typing import Dict, List, Optional


class DNAParser:
    """Parser for DNA methylation test results (32-gene panel)"""

    def parse(self, text: str) -> List[Dict]:
        """
        Parse DNA methylation results into structured variant data

        Args:
            text: Raw DNA test results (one variant per line)

        Returns:
            List of variant dictionaries with structure:
            {
                'gene': str,
                'rs_number': str,
                'genotype': str (AA, AG, GG, TT, TC, CC, etc.),
                'variant_name': str (C677T, A1298C, etc.),
                'impact': str (description text),
                'severity': str ('critical'|'warning'|'info')
            }
        """
        if not text or not text.strip():
            return []

        variants = []
        lines = text.strip().split('\n')

        for line in lines:
            if not line.strip():
                continue

            variant = self._parse_line(line)
            if variant:
                variants.append(variant)

        return variants

    def _parse_line(self, line: str) -> Optional[Dict]:
        """Parse a single DNA variant line"""
        # Pattern: GENE rs##### GENOTYPE [VARIANT] Impact description
        # Example: MTHFR rs1801133 AG [C677T] Up to 40% reduction...

        try:
            # Extract gene (uppercase letters at start)
            gene_match = re.match(r'^([A-Z]+)', line)
            if not gene_match:
                return None
            gene = gene_match.group(1)

            # Extract rs number
            rs_match = re.search(r'(rs\d+)', line)
            if not rs_match:
                return None
            rs_number = rs_match.group(1)

            # Extract genotype (2-letter combination after rs number)
            genotype_match = re.search(r'rs\d+\s+([AGTC]{2})', line)
            if not genotype_match:
                return None
            genotype = genotype_match.group(1)

            # Extract variant name from brackets (optional)
            variant_name = ''
            variant_match = re.search(r'\[([A-Z]\d+[A-Z])\]', line)
            if variant_match:
                variant_name = variant_match.group(1)

            # Extract impact (everything after genotype/variant)
            if variant_name:
                impact_start = line.find(']') + 1
            else:
                impact_start = line.find(genotype) + len(genotype)
            impact = line[impact_start:].strip()

            # Determine severity
            severity = self.determine_severity(gene, rs_number, genotype, impact)

            return {
                'gene': gene,
                'rs_number': rs_number,
                'genotype': genotype,
                'variant_name': variant_name,
                'impact': impact,
                'severity': severity
            }

        except Exception as e:
            # Malformed line, skip it
            return None

    def determine_severity(
        self,
        gene: str,
        rs_number: str,
        genotype: str,
        impact: str
    ) -> str:
        """
        Determine severity of genetic variant

        Returns: 'critical' | 'warning' | 'info'
        """
        # CRITICAL: CBS upregulation (rs234706 AA)
        if gene == 'CBS' and rs_number == 'rs234706' and genotype == 'AA':
            return 'critical'

        # WARNING: PEMT TT (no endogenous choline production)
        if gene == 'PEMT' and genotype == 'TT':
            return 'warning'

        # WARNING: MTHFR heterozygous variants
        if gene == 'MTHFR' and genotype in ['AG', 'GT', 'CT']:
            return 'warning'

        # WARNING: BHMT downregulation
        if gene == 'BHMT' and genotype in ['TT', 'CC']:
            return 'warning'

        # Severity based on impact text
        impact_lower = impact.lower()

        # CRITICAL indicators
        if '10x' in impact_lower or 'ten times' in impact_lower:
            return 'critical'

        # WARNING indicators
        if any(word in impact_lower for word in [
            'reduction', 'decreased', 'reduced', 'impaired',
            'deficiency', 'impairment', 'compromise'
        ]):
            return 'warning'

        # INFO: mild or unclear impact
        return 'info'
