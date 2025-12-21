"""HTML template builder with HELD branding CSS"""

def get_css() -> str:
    """Return the complete HELD branded CSS"""
    return """
        /* HELD Brand Colors v3.0 */
        :root {
            --jungle-green: #34B27B;
            --jungle-green-dark: #2d9e6b;
            --american-orange: #FE8900;
            --bunker-dark: #11181C;
            --white: #FFFFFF;
            --black: #000000;
            --gray-border: #E6E6E6;
            --slate-3: #232326;
            --text-high-contrast: #ededef;

            /* Status colors */
            --status-critical: #EF4444;
            --status-warning: #FE8900;
            --status-optimal: #34B27B;
            --status-good: #10B981;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', 'Open Sans', system-ui, -apple-system, sans-serif;
            background: var(--white);
            color: var(--black);
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }

        /* Header */
        .header {
            background: linear-gradient(135deg, var(--jungle-green) 0%, var(--jungle-green-dark) 100%);
            color: white;
            padding: 3rem 2rem;
            border-radius: 24px;
            margin-bottom: 2rem;
            box-shadow: 0 16px 40px -24px rgba(52, 178, 123, 0.35);
        }

        .header-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
        }

        .logo {
            font-size: 2rem;
            font-weight: 700;
            letter-spacing: 2px;
        }

        .tagline {
            font-size: 0.9rem;
            opacity: 0.9;
            font-weight: 500;
        }

        .patient-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
        }

        .info-card {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .info-label {
            font-size: 0.85rem;
            opacity: 0.8;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .info-value {
            font-size: 1.5rem;
            font-weight: 600;
        }

        /* Critical Alerts */
        .alerts-section {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }

        .alert-card {
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }

        .alert-critical {
            background: rgba(239, 68, 68, 0.1);
            border-color: var(--status-critical);
        }

        .alert-warning {
            background: rgba(254, 137, 0, 0.1);
            border-color: var(--status-warning);
        }

        .alert-good {
            background: rgba(52, 178, 123, 0.1);
            border-color: var(--status-optimal);
        }

        .alert-title {
            font-weight: 700;
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .alert-icon {
            font-size: 1.5rem;
        }

        .alert-description {
            font-size: 0.95rem;
            line-height: 1.5;
            opacity: 0.9;
        }

        /* Section Headers */
        .section {
            margin-bottom: 3rem;
        }

        .section-header {
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid var(--jungle-green);
        }

        .section-title {
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--jungle-green);
            margin-bottom: 0.5rem;
        }

        .section-subtitle {
            font-size: 1rem;
            opacity: 0.7;
        }

        /* Biomarker Grid */
        .biomarkers-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1rem;
        }

        .biomarker-card {
            background: white;
            border: 1px solid var(--gray-border);
            border-radius: 12px;
            padding: 1.25rem;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .biomarker-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
        }

        .biomarker-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1rem;
        }

        .biomarker-name {
            font-weight: 600;
            font-size: 1rem;
            color: var(--black);
        }

        .biomarker-status {
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }

        .status-critical {
            background: rgba(239, 68, 68, 0.15);
            color: #DC2626;
            border: 1px solid rgba(239, 68, 68, 0.4);
        }

        .status-warning {
            background: rgba(254, 137, 0, 0.15);
            color: #EA580C;
            border: 1px solid rgba(254, 137, 0, 0.4);
        }

        .status-optimal {
            background: rgba(52, 178, 123, 0.15);
            color: #059669;
            border: 1px solid rgba(52, 178, 123, 0.4);
        }

        .biomarker-values {
            margin-bottom: 1rem;
        }

        .value-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.5rem;
            font-size: 0.9rem;
        }

        .value-label {
            opacity: 0.7;
        }

        .value-number {
            font-weight: 600;
        }

        .biomarker-bar {
            height: 8px;
            background: var(--gray-border);
            border-radius: 9999px;
            overflow: hidden;
            margin-top: 0.75rem;
        }

        .biomarker-fill {
            height: 100%;
            border-radius: 9999px;
            transition: width 0.3s ease;
        }

        /* DNA Variants */
        .dna-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 1.5rem;
        }

        .dna-card {
            background: white;
            border: 2px solid var(--gray-border);
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.2s;
        }

        .dna-card:hover {
            border-color: var(--jungle-green);
            box-shadow: 0 8px 24px rgba(52, 178, 123, 0.15);
        }

        .dna-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--gray-border);
        }

        .gene-name {
            font-weight: 700;
            font-size: 1.2rem;
            color: var(--jungle-green);
        }

        .genotype {
            background: var(--slate-3);
            color: white;
            padding: 0.35rem 0.85rem;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 600;
            font-family: 'Courier New', monospace;
        }

        .variant-impact {
            background: rgba(254, 137, 0, 0.1);
            border-left: 3px solid var(--american-orange);
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }

        .impact-title {
            font-weight: 600;
            color: var(--american-orange);
            margin-bottom: 0.5rem;
            font-size: 0.9rem;
        }

        .impact-text {
            font-size: 0.9rem;
            line-height: 1.6;
        }

        /* Action Plan Timeline */
        .timeline {
            position: relative;
            padding-left: 2rem;
        }

        .timeline:before {
            content: '';
            position: absolute;
            left: 0.5rem;
            top: 0;
            bottom: 0;
            width: 3px;
            background: var(--jungle-green);
        }

        .timeline-item {
            position: relative;
            margin-bottom: 2rem;
            padding-left: 2rem;
        }

        .timeline-dot {
            position: absolute;
            left: -1.15rem;
            top: 0.25rem;
            width: 1rem;
            height: 1rem;
            background: var(--jungle-green);
            border: 3px solid white;
            border-radius: 50%;
            box-shadow: 0 0 0 3px var(--jungle-green);
        }

        .timeline-phase {
            background: white;
            border: 2px solid var(--gray-border);
            border-radius: 12px;
            padding: 1.5rem;
        }

        .phase-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }

        .phase-title {
            font-size: 1.3rem;
            font-weight: 700;
            color: var(--jungle-green);
        }

        .phase-duration {
            background: rgba(52, 178, 123, 0.15);
            padding: 0.5rem 1rem;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--jungle-green);
        }

        .phase-actions {
            display: grid;
            gap: 1rem;
            margin-top: 1rem;
        }

        .action-item {
            display: flex;
            gap: 1rem;
            padding: 1rem;
            background: rgba(0, 0, 0, 0.02);
            border-radius: 8px;
            border-left: 3px solid var(--jungle-green);
        }

        .action-icon {
            font-size: 1.5rem;
            flex-shrink: 0;
        }

        .action-content {
            flex: 1;
        }

        .action-title {
            font-weight: 600;
            margin-bottom: 0.25rem;
        }

        .action-description {
            font-size: 0.9rem;
            opacity: 0.8;
        }

        .phase-warnings {
            margin-top: 1rem;
            padding: 1rem;
            background: rgba(239, 68, 68, 0.1);
            border-radius: 8px;
            border-left: 4px solid var(--status-critical);
        }

        .phase-warnings ul {
            list-style: none;
            padding: 0;
        }

        .phase-warnings li {
            margin-bottom: 0.5rem;
            font-size: 0.9rem;
            font-weight: 600;
            color: #DC2626;
        }

        /* Supplement Protocol */
        .supplement-grid {
            display: grid;
            gap: 1rem;
        }

        .supplement-card {
            background: white;
            border: 2px solid var(--gray-border);
            border-radius: 12px;
            padding: 1.5rem;
            display: grid;
            grid-template-columns: auto 1fr auto;
            gap: 1.5rem;
            align-items: center;
        }

        .supplement-time {
            background: var(--jungle-green);
            color: white;
            padding: 1rem;
            border-radius: 8px;
            text-align: center;
            min-width: 100px;
        }

        .time-label {
            font-size: 0.75rem;
            opacity: 0.9;
            text-transform: uppercase;
            margin-bottom: 0.25rem;
        }

        .time-value {
            font-size: 1.5rem;
            font-weight: 700;
        }

        .supplement-info {
            flex: 1;
        }

        .supplement-name {
            font-weight: 700;
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
            color: var(--black);
        }

        .supplement-dosage {
            font-size: 0.95rem;
            color: var(--jungle-green);
            font-weight: 600;
            margin-bottom: 0.5rem;
        }

        .supplement-reason {
            font-size: 0.9rem;
            opacity: 0.7;
        }

        .supplement-badge {
            background: var(--american-orange);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 600;
            white-space: nowrap;
        }

        .badge-kern {
            background: var(--status-critical);
        }

        .badge-kritiek {
            background: #DC2626;
        }

        .badge-essentieel {
            background: var(--american-orange);
        }

        .badge-support {
            background: var(--jungle-green);
        }

        .badge-fase-2 {
            background: #6366F1;
        }

        /* Footer */
        .footer {
            margin-top: 3rem;
            padding: 2rem;
            text-align: center;
            border-top: 2px solid var(--gray-border);
        }

        .footer-text {
            color: var(--jungle-green);
            font-weight: 600;
            margin-bottom: 0.5rem;
        }

        .footer-note {
            font-size: 0.85rem;
            opacity: 0.6;
        }

        .disclaimer {
            margin-top: 2rem;
            padding: 1.5rem;
            background: rgba(0, 0, 0, 0.02);
            border-radius: 8px;
            font-size: 0.85rem;
            opacity: 0.7;
            line-height: 1.6;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .container {
                padding: 1rem;
            }

            .header {
                padding: 2rem 1.5rem;
            }

            .section-title {
                font-size: 1.5rem;
            }

            .supplement-card {
                grid-template-columns: 1fr;
                text-align: center;
            }

            .supplement-time {
                justify-self: center;
            }
        }

        /* Print Styles for PDF */
        @media print {
            body {
                background: white;
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }

            .container {
                max-width: 100%;
                padding: 0;
            }

            button {
                display: none !important;
            }

            .header,
            .alert-card,
            .biomarker-fill,
            .timeline-dot {
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }

            .section {
                page-break-inside: avoid;
            }

            .dna-card,
            .biomarker-card {
                page-break-inside: avoid;
                margin-bottom: 1rem;
            }
        }
    """
