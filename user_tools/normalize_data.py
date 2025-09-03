#!/usr/bin/env python3
"""
User-friendly data normalization tool for Turkish insurance policy data.

This tool provides a simple interface for normalizing extracted insurance data
into standardized business formats using configurable mapping rules.

Usage:
    python user_tools/normalize_data.py --company ak_E
    python user_tools/normalize_data.py --input custom_data.json --config custom_map.json
    python user_tools/normalize_data.py --all-companies
"""

import sys
import os
import argparse
import json
import subprocess
from pathlib import Path
from typing import Optional, List, Dict

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

class DataNormalizer:
    def __init__(self):
        self.project_root = PROJECT_ROOT
        self.data_dir = self.project_root / "data"
        self.config_dir = self.project_root / "config"
        
    def validate_company_files(self, company: str) -> bool:
        """Check if company has required files for normalization."""
        # Check if extraction results exist
        input_file = self.data_dir / "02_output" / f"{company}.json"
        if not input_file.exists():
            print(f"[ERROR] Error: No extraction results found for {company}")
            print(f"   Expected: {input_file}")
            print(f"   [TIP] Tip: Run extraction first with:")
            print(f"   python user_tools/extract_policies.py --company {company}")
            return False
            
        # Check if mapping config exists
        mapping_config = self.config_dir / "mapping_rules" / f"{company}_map.json"
        if not mapping_config.exists():
            print(f"[WARN]  No mapping configuration found for {company}")
            print(f"   Expected: {mapping_config}")
            print(f"   [TIP] This company doesn't have normalization rules yet")
            return False
            
        print(f"[SUCCESS] Company {company} validation passed")
        return True
        
    def normalize_company(self, company: str) -> bool:
        """Normalize data for a single company."""
        print(f"[MAP]  Normalizing data for {company}...")
        
        if not self.validate_company_files(company):
            return False
            
        try:
            input_file = self.data_dir / "02_output" / f"{company}.json"
            output_file = self.data_dir / "03_mapped" / f"{company}.json"
            mapping_config = self.config_dir / "mapping_rules" / f"{company}_map.json"
            
            # Ensure output directory exists
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Run mapping engine
            result = subprocess.run([
                sys.executable, "mapping/mapping_engine.py",
                "--input", str(input_file),
                "--output", str(output_file), 
                "--config", str(mapping_config)
            ], cwd=self.project_root, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"[SUCCESS] Normalization completed successfully for {company}")
                print(f"[FILE] Output saved to: {output_file}")
                
                # Show some stats if available
                self.show_normalization_stats(output_file)
                return True
            else:
                print(f"[ERROR] Normalization failed for {company}")
                if result.stderr:
                    print(f"Error details: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Error running normalization: {e}")
            return False
            
    def normalize_custom(self, input_file: str, config_file: str, output_file: Optional[str] = None) -> bool:
        """Normalize data using custom input and config files."""
        input_path = Path(input_file)
        config_path = Path(config_file)
        
        if not input_path.exists():
            print(f"[ERROR] Error: Input file not found: {input_file}")
            return False
            
        if not config_path.exists():
            print(f"[ERROR] Error: Config file not found: {config_file}")
            return False
            
        if output_file is None:
            output_file = str(input_path.parent / f"{input_path.stem}_normalized.json")
            
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"[MAP]  Normalizing custom data...")
        print(f"[INPUT] Input: {input_file}")
        print(f"[CONFIG]  Config: {config_file}")
        print(f"[OUTPUT] Output: {output_file}")
        
        try:
            result = subprocess.run([
                sys.executable, "mapping/mapping_engine.py",
                "--input", str(input_path),
                "--output", str(output_path),
                "--config", str(config_path)
            ], cwd=self.project_root, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"[SUCCESS] Custom normalization completed successfully")
                self.show_normalization_stats(output_path)
                return True
            else:
                print(f"[ERROR] Custom normalization failed")
                if result.stderr:
                    print(f"Error details: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Error running custom normalization: {e}")
            return False
            
    def show_normalization_stats(self, output_file: Path):
        """Show brief statistics about the normalization results."""
        try:
            if not output_file.exists():
                return
                
            with open(output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if not isinstance(data, dict):
                return
                
            # Count documents and fields
            doc_count = len(data)
            if doc_count == 0:
                return
                
            # Sample a document to count fields
            sample_doc = next(iter(data.values()))
            if isinstance(sample_doc, dict):
                field_count = len(sample_doc)
                print(f"[REPORT] Results: {doc_count} documents, {field_count} fields per document")
                
        except Exception:
            # Don't fail on stats errors
            pass
            
    def get_companies_with_mapping(self) -> List[str]:
        """Get list of companies that have mapping configurations."""
        mapping_dir = self.config_dir / "mapping_rules"
        if not mapping_dir.exists():
            return []
            
        companies = []
        for mapping_file in mapping_dir.glob("*_map.json"):
            company = mapping_file.stem.replace("_map", "")
            companies.append(company)
            
        return sorted(companies)
        
    def normalize_all_companies(self) -> bool:
        """Normalize data for all companies that have mapping configs."""
        companies = self.get_companies_with_mapping()
        if not companies:
            print("[ERROR] No companies found with mapping configurations")
            print(f"   Expected mapping files in: {self.config_dir / 'mapping_rules'}")
            return False
            
        print(f"[PROCESS] Normalizing data for {len(companies)} companies...")
        print(f"Companies with mapping: {', '.join(companies)}")
        
        success_count = 0
        for i, company in enumerate(companies, 1):
            print(f"\n[REPORT] Progress: {i}/{len(companies)}")
            try:
                if self.normalize_company(company):
                    success_count += 1
                else:
                    print(f"[WARN]  Skipping {company} due to missing prerequisites")
            except KeyboardInterrupt:
                print("\n[WARN]  Normalization interrupted by user")
                break
                
        print(f"\n[REPORT] Final Results: {success_count}/{len(companies)} companies normalized successfully")
        return success_count == len(companies)

def main():
    parser = argparse.ArgumentParser(
        description="Normalize extracted insurance policy data into standardized formats",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python user_tools/normalize_data.py --company ak_E
  python user_tools/normalize_data.py --input custom_data.json --config custom_map.json
  python user_tools/normalize_data.py --input data.json --config map.json --output normalized.json
  python user_tools/normalize_data.py --all-companies
        """
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--company', help='Normalize data for specific company (e.g., ak_E)')
    group.add_argument('--all-companies', action='store_true', 
                      help='Normalize data for all companies with mapping configs')
    group.add_argument('--input', help='Custom input file path (requires --config)')
    
    parser.add_argument('--config', help='Mapping configuration file (required with --input)')
    parser.add_argument('--output', help='Custom output file path (optional with --input)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.input and not args.config:
        print("[ERROR] Error: --config is required when using --input")
        sys.exit(1)
        
    if args.config and not args.input:
        print("[ERROR] Error: --input is required when using --config")
        sys.exit(1)
        
    if args.output and not args.input:
        print("[ERROR] Error: --output can only be used with --input")
        sys.exit(1)
        
    normalizer = DataNormalizer()
    
    if args.company:
        success = normalizer.normalize_company(args.company)
        sys.exit(0 if success else 1)
        
    elif args.all_companies:
        success = normalizer.normalize_all_companies()
        sys.exit(0 if success else 1)
        
    elif args.input:
        success = normalizer.normalize_custom(args.input, args.config, args.output)
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()