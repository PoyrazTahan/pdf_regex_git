#!/usr/bin/env python3
"""
User-friendly PDF data extraction tool for Turkish insurance policies.

This tool provides a simple interface for extracting structured data from
insurance policy PDFs using regex patterns.

Usage:
    python user_tools/extract_policies.py --company ak_E
    python user_tools/extract_policies.py --company allianz_E --output custom_output.json
    python user_tools/extract_policies.py --all-companies
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path
from typing import Optional, List

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

class PolicyExtractor:
    def __init__(self):
        self.project_root = PROJECT_ROOT
        self.data_dir = self.project_root / "data"
        self.config_dir = self.project_root / "config"
        
    def validate_company(self, company: str) -> bool:
        """Check if company has required files and configurations."""
        # Check if PDFs exist
        pdf_dir = self.data_dir / "00_raw_pdfs" / company
        if not pdf_dir.exists():
            print(f"[ERROR] Error: No PDF directory found for {company}")
            print(f"   Expected: {pdf_dir}")
            return False
            
        pdf_files = list(pdf_dir.glob("*.pdf"))
        if not pdf_files:
            print(f"[ERROR] Error: No PDF files found in {pdf_dir}")
            return False
            
        # Check if extraction config exists
        extraction_config = self.config_dir / "extraction_patterns" / f"{company}.json"
        if not extraction_config.exists():
            print(f"[ERROR] Error: No extraction configuration found for {company}")
            print(f"   Expected: {extraction_config}")
            return False
            
        print(f"[SUCCESS] Company {company} validation passed ({len(pdf_files)} PDFs found)")
        return True
        
    def extract_company(self, company: str, output_file: Optional[str] = None) -> bool:
        """Extract data for a single company."""
        print(f"[EXTRACT] Extracting data for {company}...")
        
        if not self.validate_company(company):
            return False
            
        try:
            cmd = [sys.executable, "agent_tools/output_create.py", "--company", company]
            
            if output_file:
                # Create output directory if needed
                output_path = Path(output_file)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                # Note: output_create.py doesn't support custom output files yet
                # For now, we'll run the standard extraction and inform user
                print(f"ℹ️  Note: Output will be saved to standard location")
                print(f"   Custom output path: {output_file}")
                
            result = subprocess.run(cmd, cwd=self.project_root, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"[SUCCESS] Extraction completed successfully for {company}")
                
                # Show where the output was saved
                standard_output = self.data_dir / "02_output" / f"{company}.json"
                print(f"[FILE] Output saved to: {standard_output}")
                
                if output_file and output_file != str(standard_output):
                    # Copy to custom location if specified
                    import shutil
                    shutil.copy2(standard_output, output_file)
                    print(f"[FILE] Also copied to: {output_file}")
                    
                return True
            else:
                print(f"[ERROR] Extraction failed for {company}")
                if result.stderr:
                    print(f"Error details: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Error running extraction: {e}")
            return False
            
    def get_available_companies(self) -> List[str]:
        """Get list of all available companies."""
        pdf_dir = self.data_dir / "00_raw_pdfs"
        if not pdf_dir.exists():
            return []
            
        companies = []
        for item in pdf_dir.iterdir():
            if item.is_dir() and item.name.endswith('_E'):
                companies.append(item.name)
                
        return sorted(companies)
        
    def extract_all_companies(self) -> bool:
        """Extract data for all available companies."""
        companies = self.get_available_companies()
        if not companies:
            print("[ERROR] No companies found in data/00_raw_pdfs/")
            return False
            
        print(f"[PROCESS] Extracting data for {len(companies)} companies...")
        print(f"Companies: {', '.join(companies)}")
        
        success_count = 0
        for i, company in enumerate(companies, 1):
            print(f"\n[REPORT] Progress: {i}/{len(companies)}")
            try:
                if self.extract_company(company):
                    success_count += 1
            except KeyboardInterrupt:
                print("\n[WARN]  Extraction interrupted by user")
                break
                
        print(f"\n[REPORT] Final Results: {success_count}/{len(companies)} companies extracted successfully")
        return success_count == len(companies)

def main():
    parser = argparse.ArgumentParser(
        description="Extract structured data from Turkish insurance policy PDFs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python user_tools/extract_policies.py --company ak_E
  python user_tools/extract_policies.py --company allianz_E --output custom_results.json  
  python user_tools/extract_policies.py --all-companies
        """
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--company', help='Extract data for specific company (e.g., ak_E)')
    group.add_argument('--all-companies', action='store_true', help='Extract data for all companies')
    
    parser.add_argument('--output', help='Custom output file path (for single company only)')
    
    args = parser.parse_args()
    
    if args.output and args.all_companies:
        print("[ERROR] Error: --output can only be used with --company, not --all-companies")
        sys.exit(1)
        
    extractor = PolicyExtractor()
    
    if args.company:
        success = extractor.extract_company(args.company, args.output)
        sys.exit(0 if success else 1)
        
    elif args.all_companies:
        success = extractor.extract_all_companies()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()