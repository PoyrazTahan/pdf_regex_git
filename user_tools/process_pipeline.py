#!/usr/bin/env python3
"""
Complete end-to-end processing pipeline for Turkish insurance policy PDFs.

This user-friendly tool orchestrates the complete data extraction and normalization
pipeline from raw PDFs to standardized business data.

Usage:
    python user_tools/process_pipeline.py                           # Process all companies
    python user_tools/process_pipeline.py --company ak_E            # Process specific company
    python user_tools/process_pipeline.py --field Police_No         # Process specific field across all companies
    python user_tools/process_pipeline.py --visualize               # Generate both dashboards after processing
    python user_tools/process_pipeline.py --all-companies --visualize --skip-extraction
"""

import sys
import os
import argparse
import json
import subprocess
from pathlib import Path
from typing import Optional, List

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

class ProcessingPipeline:
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
            
        # Check if extraction config exists
        extraction_config = self.config_dir / "extraction_patterns" / f"{company}.json"
        if not extraction_config.exists():
            print(f"[ERROR] Error: No extraction configuration found for {company}")
            print(f"   Expected: {extraction_config}")
            return False
            
        print(f"[SUCCESS] Company {company} validation passed")
        return True
        
    def run_extraction(self, company: str) -> bool:
        """Run PDF data extraction for the specified company."""
        print(f"[EXTRACT] Running extraction for {company}...")
        
        try:
            # Use the agent tools output_create.py
            result = subprocess.run([
                sys.executable, "agent_tools/output_create.py", "--company", company
            ], cwd=self.project_root, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"[SUCCESS] Extraction completed successfully for {company}")
                return True
            else:
                print(f"[ERROR] Extraction failed for {company}")
                print(f"Error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Error running extraction: {e}")
            return False
            
    def run_normalization(self, company: str) -> bool:
        """Run data normalization for the specified company."""
        # Check if mapping config exists
        mapping_config = self.config_dir / "mapping_rules" / f"{company}_map.json"
        if not mapping_config.exists():
            print(f"[WARN]  No mapping configuration found for {company}")
            print(f"   Expected: {mapping_config}")
            print(f"   Skipping normalization step")
            return True  # Not an error, just skip normalization
            
        print(f"[MAP]  Running normalization for {company}...")
        
        try:
            input_file = self.data_dir / "02_output" / f"{company}.json"
            output_file = self.data_dir / "03_mapped" / f"{company}.json"
            
            # Ensure output directory exists
            output_file.parent.mkdir(exist_ok=True)
            
            # Run mapping engine
            result = subprocess.run([
                sys.executable, "mapping/mapping_engine.py",
                "--input", str(input_file),
                "--output", str(output_file), 
                "--config", str(mapping_config)
            ], cwd=self.project_root, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"[SUCCESS] Normalization completed successfully for {company}")
                return True
            else:
                print(f"[ERROR] Normalization failed for {company}")
                print(f"Error: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Error running normalization: {e}")
            return False
            
    def generate_report(self, company: str, field: Optional[str] = None):
        """Generate processing quality report."""
        if field:
            print(f"[REPORT] Generating field report for {field} in {company}...")
            cmd = [sys.executable, "agent_tools/output_check.py", "--company", company, "--field", field]
        else:
            print(f"[REPORT] Generating report for {company}...")
            cmd = [sys.executable, "agent_tools/output_check.py", "--company", company]
        
        try:
            result = subprocess.run(cmd, cwd=self.project_root, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(result.stdout)
            else:
                print(f"[WARN]  Report generation had issues: {result.stderr}")
                
        except Exception as e:
            print(f"[WARN]  Error generating report: {e}")
            
    def run_field_extraction(self, companies: List[str], field: str) -> bool:
        """Run extraction for a specific field across multiple companies."""
        print(f"[EXTRACT] Processing field '{field}' across {len(companies)} companies...")
        
        success_count = 0
        for company in companies:
            print(f"\n[REPORT] Processing {company} for field: {field}")
            
            if not self.validate_company(company):
                continue
                
            try:
                # Use agent tools field_dev.py to test the field pattern
                result = subprocess.run([
                    sys.executable, "agent_tools/field_dev.py", "--company", company, "--field", field
                ], cwd=self.project_root, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"[SUCCESS] Field '{field}' processed successfully for {company}")
                    success_count += 1
                else:
                    print(f"[WARN]  Field '{field}' processing had issues for {company}")
                    
            except Exception as e:
                print(f"[ERROR] Error processing field '{field}' for {company}: {e}")
                
        print(f"\n[REPORT] Field '{field}' Results: {success_count}/{len(companies)} companies processed successfully")
        return success_count > 0
        
    def generate_dashboard(self):
        """Generate both regex and mapped visualization dashboards."""
        print(f"[VIZ] Generating visualization dashboards...")
        
        try:
            # Use the new clean dashboard architecture to generate both dashboards
            result = subprocess.run([
                sys.executable, "viz/dashboard.py", "both"
            ], cwd=self.project_root, capture_output=True, text=True)
            
            if result.returncode == 0:
                regex_path = self.project_root / "data" / "static_dashboard.html"
                mapped_path = self.project_root / "data" / "static_map_dashboard.html"
                
                print(f"[SUCCESS] Both dashboards generated successfully!")
                print(f"[REGEX] Pattern Analysis: {regex_path}")
                print(f"[MAPPED] Business Intelligence: {mapped_path}")
                print(f"[BROWSER] Open regex dashboard: file://{regex_path.absolute()}")
                print(f"[BROWSER] Open mapped dashboard: file://{mapped_path.absolute()}")
                return True
            else:
                print(f"[ERROR] Dashboard generation failed")
                if result.stderr:
                    print(f"Error details: {result.stderr}")
                if result.stdout:
                    print(f"Output: {result.stdout}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Error generating dashboards: {e}")
            return False
            
    def process_company(self, company: str, skip_extraction: bool = False) -> bool:
        """Process a single company through the complete pipeline."""
        print(f"\n[PROCESS] Processing {company}")
        print("=" * 50)
        
        # Step 1: Validate
        if not self.validate_company(company):
            return False
            
        # Step 2: Extract (unless skipped)
        if not skip_extraction:
            if not self.run_extraction(company):
                return False
        else:
            print(f"⏭️  Skipping extraction for {company}")
            
        # Step 3: Normalize
        if not self.run_normalization(company):
            return False
            
        # Step 4: Report
        self.generate_report(company)
        
        print(f"[SUCCESS] Complete pipeline finished for {company}")
        return True
        
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
        
def main():
    parser = argparse.ArgumentParser(
        description="Complete processing pipeline for Turkish insurance policy PDFs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python user_tools/process_pipeline.py                           # Process all companies
  python user_tools/process_pipeline.py --company ak_E            # Process specific company  
  python user_tools/process_pipeline.py --field Police_No         # Process specific field across all companies
  python user_tools/process_pipeline.py --visualize               # Process all and generate both dashboards
  python user_tools/process_pipeline.py --company ak_E --visualize --skip-extraction
        """
    )
    
    # Main processing options (mutually exclusive)
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--company', help='Process specific company (e.g., ak_E)')
    group.add_argument('--field', help='Process specific field across all companies (e.g., Police_No)')
    group.add_argument('--all-companies', action='store_true', help='Process all available companies (default if no options)')
    
    # Processing modifiers
    parser.add_argument('--skip-extraction', action='store_true', 
                       help='Skip extraction step (use existing data)')
    parser.add_argument('--visualize', action='store_true',
                       help='Generate both regex and mapped dashboards after processing')
    
    args = parser.parse_args()
    
    pipeline = ProcessingPipeline()
    
    # Default to all companies if no specific option is given
    if not args.company and not args.field and not args.all_companies:
        args.all_companies = True
    
    success = False
    
    if args.company:
        # Process single company
        success = pipeline.process_company(args.company, args.skip_extraction)
        
    elif args.field:
        # Process specific field across all companies
        companies = pipeline.get_available_companies()
        if not companies:
            print("[ERROR] No companies found in data/00_raw_pdfs/")
            sys.exit(1)
            
        success = pipeline.run_field_extraction(companies, args.field)
        
    elif args.all_companies:
        # Process all companies
        companies = pipeline.get_available_companies()
        if not companies:
            print("[ERROR] No companies found in data/00_raw_pdfs/")
            sys.exit(1)
            
        print(f"[PROCESS] Processing {len(companies)} companies...")
        print(f"Companies: {', '.join(companies)}")
        
        success_count = 0
        for company in companies:
            try:
                if pipeline.process_company(company, args.skip_extraction):
                    success_count += 1
            except KeyboardInterrupt:
                print("\n[WARN]  Processing interrupted by user")
                break
                
        success = success_count == len(companies)
        print(f"\n[REPORT] Final Results: {success_count}/{len(companies)} companies processed successfully")
    
    # Generate dashboards if requested
    if args.visualize:
        print(f"\n[VIZ] Generating visualization dashboards...")
        dashboard_success = pipeline.generate_dashboard()
        success = success and dashboard_success
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()