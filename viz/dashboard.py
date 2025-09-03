#!/usr/bin/env python3
"""
Single entry point for dashboard generation.
Supports different modes with clean separation of data loading and HTML generation.
"""

import argparse
import sys
from pathlib import Path
from dashboard_data import DataLoader
from dashboard_html import HTMLGenerator


def generate_dashboard(mode: str, output_file: str = None) -> str:
    """Generate dashboard based on mode."""
    
    # Validate mode
    valid_modes = ['regex', 'mapped']
    if mode not in valid_modes:
        raise ValueError(f"Invalid mode '{mode}'. Valid modes: {', '.join(valid_modes)}")
    
    # Set default output file if not provided
    if not output_file:
        if mode == "regex":
            output_file = "static_dashboard.html"
        else:
            output_file = "static_map_dashboard.html"
    
    # Get full output path
    base_dir = Path(__file__).parent.parent
    output_path = base_dir / "data" / output_file
    
    print(f"[{mode.upper()}] Generating dashboard...")
    
    try:
        # Load data
        loader = DataLoader()
        data = loader.load_data(mode)
        
        # Generate HTML
        generator = HTMLGenerator()
        html_content = generator.generate_dashboard(data, output_path)
        
        # Print summary
        print(f"\n[INFO] {mode.title()} Dashboard contains:")
        print(f"   • {len(data.companies)} companies with data")
        print(f"   • {len(data.fields)} fields")
        if 'companies_with_mapping' in data.stats:
            print(f"   • {data.stats['companies_with_mapping']} companies with mapping configurations")
        print(f"   • Interactive matrix view with success percentages")
        print(f"   • {'Business logic mapping rules' if mode == 'mapped' else 'Regex patterns'} and values")
        print(f"   • No external dependencies - fully self-contained")
        
        return str(output_path)
        
    except Exception as e:
        print(f"[ERROR] Failed to generate {mode} dashboard: {e}")
        sys.exit(1)


def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description='Generate PDF analysis dashboards',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python dashboard.py regex                    # Generate regex pattern dashboard
  python dashboard.py mapped                   # Generate mapped data dashboard  
  python dashboard.py regex -o my_regex.html   # Custom output filename
  python dashboard.py both                     # Generate both dashboards

Available modes:
  regex    - Regex pattern analysis (02_output + extraction_patterns)
  mapped   - Mapped data analysis (03_mapped + mapping_rules)
  both     - Generate both dashboards
        """
    )
    
    parser.add_argument(
        'mode', 
        choices=['regex', 'mapped', 'both'],
        help='Dashboard mode to generate'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output filename (optional, defaults based on mode)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Set verbosity (could be used to control print statements)
    if args.verbose:
        print(f"[VERBOSE] Mode: {args.mode}")
        if args.output:
            print(f"[VERBOSE] Custom output: {args.output}")
    
    try:
        if args.mode == 'both':
            # Generate both dashboards
            print("[BOTH] Generating both regex and mapped dashboards...\n")
            
            regex_path = generate_dashboard('regex')
            print()  # Separator
            mapped_path = generate_dashboard('mapped')
            
            print(f"\n[SUCCESS] Both dashboards generated!")
            print(f"[REGEX] {regex_path}")
            print(f"[MAPPED] {mapped_path}")
            
        else:
            # Generate single dashboard
            output_path = generate_dashboard(args.mode, args.output)
            print(f"\n[SUCCESS] {args.mode.title()} dashboard generated: {output_path}")
    
    except KeyboardInterrupt:
        print("\n[CANCELLED] Dashboard generation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()