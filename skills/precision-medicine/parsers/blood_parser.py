"""Blood test data parser with focus on optimal ranges"""
import re
from typing import Dict, List, Optional


class BloodParser:
    """Parser for blood test results focusing on optimal (functional) ranges"""

    def parse(self, text: str) -> List[Dict]:
        """
        Parse blood test results text into structured biomarker data

        Args:
            text: Raw blood test results (one biomarker per line)

        Returns:
            List of biomarker dictionaries with structure:
            {
                'name': str,
                'value': float,
                'unit': str,
                'optimal_range': str,
                'normal_range': str,
                'status': str ('critical'|'warning'|'optimal'),
                'flag': str ('+'|'-'|'')
            }
        """
        if not text or not text.strip():
            return []

        biomarkers = []
        lines = text.strip().split('\n')

        for line in lines:
            if not line.strip() or line.startswith('Naam'):
                continue

            biomarker = self._parse_line(line)
            if biomarker:
                biomarkers.append(biomarker)

        return biomarkers

    def _parse_line(self, line: str) -> Optional[Dict]:
        """Parse a single biomarker line"""
        # Pattern: Name [+/-] Value Opt:range V.N:range unit
        # Example: HomocysteÏne + 18.0 Opt:<8.0 V.N 3.7-13.9 µmol/L

        # Extract components
        parts = line.split()
        if len(parts) < 3:
            return None

        try:
            # Find the flag (+/-)
            flag = ''
            flag_idx = -1
            for i, part in enumerate(parts):
                if part in ['+', '-']:
                    flag = part
                    flag_idx = i
                    break

            # Name is everything before flag (or before first number if no flag)
            if flag_idx > 0:
                name = ' '.join(parts[:flag_idx])
                value_idx = flag_idx + 1
            else:
                # No flag, find first number
                name_parts = []
                value_idx = 0
                for i, part in enumerate(parts):
                    try:
                        float(part)
                        value_idx = i
                        break
                    except ValueError:
                        name_parts.append(part)
                name = ' '.join(name_parts)

            # Value
            value = float(parts[value_idx])

            # Extract optimal range (priority)
            optimal_range = ''
            normal_range = ''
            opt_match = re.search(r'Opt:([<>]?[\d\.\-]+)', line)
            if opt_match:
                optimal_range = opt_match.group(1)
            else:
                # Try alternative format: "45-60:opt."
                alt_match = re.search(r'([\d\.\-]+):opt\.?', line)
                if alt_match:
                    optimal_range = alt_match.group(1)

            # Extract normal range
            vn_match = re.search(r'V\.?N\.?\s+([\d\.\-]+)', line)
            if vn_match:
                normal_range = vn_match.group(1)
            else:
                # Try alternative: "22-322:VN"
                alt_match = re.search(r'([\d\.\-]+):VN', line)
                if alt_match:
                    normal_range = alt_match.group(1)

            # Extract unit (last token, typically contains letters or special chars)
            unit = ''
            unit_match = re.search(r'([µmg/dLIUngpmol%]+)$', line)
            if unit_match:
                unit = unit_match.group(1)

            # Determine status
            status = self.determine_status(value, optimal_range, flag)

            return {
                'name': name.strip(),
                'value': value,
                'unit': unit,
                'optimal_range': optimal_range,
                'normal_range': normal_range,
                'status': status,
                'flag': flag
            }

        except (ValueError, IndexError) as e:
            # Malformed line, skip it
            return None

    def determine_status(self, value: float, optimal_range: str, flag: str) -> str:
        """
        Determine biomarker status based on optimal range

        Returns: 'critical' | 'warning' | 'optimal'
        """
        if not optimal_range:
            # No optimal range, use flag
            if flag == '+':
                return 'warning'
            elif flag == '-':
                return 'warning'
            return 'optimal'

        # Parse optimal range
        if '<' in optimal_range:
            # Upper limit (e.g., "<8.0")
            max_val = float(optimal_range.replace('<', ''))
            if value > max_val * 1.5:  # 50% over = critical
                return 'critical'
            elif value > max_val:
                return 'warning'
            else:
                return 'optimal'

        elif '>' in optimal_range:
            # Lower limit (e.g., ">30")
            min_val = float(optimal_range.replace('>', ''))
            if value < min_val * 0.7:  # 30% under = critical
                return 'critical'
            elif value < min_val:
                return 'warning'
            else:
                return 'optimal'

        elif '-' in optimal_range:
            # Range (e.g., "45-60")
            parts = optimal_range.split('-')
            min_val = float(parts[0])
            max_val = float(parts[1])

            if value < min_val:
                # Below range
                if value < min_val * 0.8:  # 20% below = critical
                    return 'critical'
                else:
                    return 'warning'
            elif value > max_val:
                # Above range
                if value > max_val * 1.2:  # 20% above = critical
                    return 'critical'
                else:
                    return 'warning'
            else:
                # Within range
                return 'optimal'

        # Default: use flag
        if flag == '+':
            return 'warning'
        elif flag == '-':
            return 'warning'

        return 'optimal'
