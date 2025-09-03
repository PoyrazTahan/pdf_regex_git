#!/usr/bin/env python3
"""
Output Check Tool  
Reads and analyzes existing extraction results
"""
import argparse
import json
from pathlib import Path
from typing import Dict, List, Union, Any


class OutputChecker:
    """Tool for checking existing extraction results"""
    
    def __init__(self, output_dir: str = "data/02_output"):
        self.output_dir = Path(output_dir)
        if not self.output_dir.exists():
            raise FileNotFoundError(f"Output directory not found: {self.output_dir}")
    
    def load_company_data(self, company: str) -> Dict[str, Any]:
        """Load existing company data"""
        output_file = self.output_dir / f"{company}.json"
        if not output_file.exists():
            raise FileNotFoundError(f"No data found for {company}. Run: python output_create.py --company {company}")
        
        with open(output_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def check_fields(self, company: str, field_names: Union[str, List[str]] = None) -> None:
        """Check specific fields or all fields from existing data"""
        data = self.load_company_data(company)
        
        if isinstance(field_names, str):
            field_names = [field_names]
        
        # If no fields specified, show all
        if not field_names:
            field_names = list(data.keys())
        
        print(f"[CHECK] CHECKING FIELD{'S' if len(field_names) > 1 else ''}: {', '.join(field_names)}")
        print(f"[COMPANY] Company: {company}")
        print("=" * 60)
        
        for field_name in field_names:
            if field_name not in data:
                print(f"\n[ERROR] Field '{field_name}' not found in {company} data")
                continue
                
            field_data = data[field_name]
            
            # Calculate statistics
            total_docs = len(field_data)
            successful = sum(1 for v in field_data.values() if v is not None)
            success_rate = (successful / total_docs) * 100 if total_docs > 0 else 0
            
            # Show results summary
            print(f"\n[RESULTS] FIELD RESULTS: {field_name}")
            print(f"Success Rate: {success_rate:.1f}% ({successful}/{total_docs})")
            
            # Show sample successful values
            successful_samples = [(doc_id, value) for doc_id, value in field_data.items() if value is not None]
            if successful_samples:
                print(f"\n[SUCCESS] Sample successful extractions:")
                for doc_id, value in successful_samples[:5]:
                    if isinstance(value, list):
                        display_value = f"{value[:3]}..." if len(value) > 3 else str(value)
                    else:
                        display_value = f"'{value}'"
                    print(f"   {doc_id}: {display_value}")
            
            # Show failed cases
            failed_docs = [doc_id for doc_id, value in field_data.items() if value is None]
            if failed_docs:
                print(f"\n[FAIL] Failed extractions ({len(failed_docs)} docs):")
                for doc_id in failed_docs[:5]:
                    print(f"   {doc_id}")
                if len(failed_docs) > 5:
                    print(f"   ... and {len(failed_docs) - 5} more")
            
            if len(field_names) > 1:
                print("-" * 40)  # Separator between fields
    
    def show_summary(self, company: str) -> None:
        """Show overall field summary for a company"""
        data = self.load_company_data(company)
        
        print(f"[SUMMARY] EXTRACTION SUMMARY: {company}")
        print("=" * 60)
        
        field_stats = []
        for field_name, field_data in data.items():
            total_docs = len(field_data)
            successful = sum(1 for v in field_data.values() if v is not None)
            success_rate = (successful / total_docs) * 100 if total_docs > 0 else 0
            field_stats.append((field_name, success_rate, successful, total_docs))
        
        # Sort by success rate
        field_stats.sort(key=lambda x: x[1], reverse=True)
        
        successful_fields = 0
        total_fields = len(field_stats)
        
        for field_name, success_rate, successful, total in field_stats:
            if success_rate >= 80:
                status = "[OK]"
                successful_fields += 1
            elif success_rate > 0:
                status = "[WARN]"
            else:
                status = "[FAIL]"
            
            print(f"{status} {field_name}: {success_rate:.1f}% ({successful}/{total})")
        
        # Overall statistics
        completion_rate = (successful_fields / total_fields) * 100 if total_fields > 0 else 0
        print(f"\n[OVERALL] OVERALL COMPLETION:")
        print(f"Fields working well (>=80%): {successful_fields}/{total_fields} ({completion_rate:.1f}%)")
    
    def compare_field_across_companies(self, field_name: str, companies: List[str]) -> None:
        """Compare a field across multiple companies"""
        print(f"[COMPARE] CROSS-COMPANY COMPARISON: {field_name}")
        print(f"[COMPANIES] Companies: {', '.join(companies)}")
        print("=" * 60)
        
        for company in companies:
            try:
                data = self.load_company_data(company)
                
                if field_name in data:
                    field_data = data[field_name]
                    total = len(field_data)
                    successful = sum(1 for v in field_data.values() if v is not None)
                    success_rate = (successful / total) * 100 if total > 0 else 0
                    
                    # Get sample values
                    sample_values = [v for v in field_data.values() if v is not None][:3]
                    
                    status = "[OK]" if success_rate >= 80 else "[WARN]" if success_rate > 0 else "[FAIL]"
                    print(f"\n{status} {company}: {success_rate:.1f}% ({successful}/{total})")
                    
                    if sample_values:
                        sample_str = ', '.join([f"'{s}'" if isinstance(s, str) else str(s) for s in sample_values])
                        print(f"   Samples: {sample_str}")
                else:
                    print(f"\n[FAIL] {company}: Field '{field_name}' not found")
                    
            except FileNotFoundError:
                print(f"\n[FAIL] {company}: No data file found")
    
    def check_multiple_companies_fields(self, companies: List[str], field_names: List[str]) -> None:
        """Check multiple fields across multiple companies"""
        print(f"[CHECK] CHECKING FIELDS: {', '.join(field_names)}")
        print(f"[COMPANIES] Companies: {', '.join(companies)}")
        print("=" * 60)
        
        for field_name in field_names:
            print(f"\n[FIELD] FIELD: {field_name}")
            print("-" * 40)
            
            for company in companies:
                try:
                    data = self.load_company_data(company)
                    
                    if field_name in data:
                        field_data = data[field_name]
                        total = len(field_data)
                        successful = sum(1 for v in field_data.values() if v is not None)
                        success_rate = (successful / total) * 100 if total > 0 else 0
                        
                        # Get sample values
                        sample_values = [v for v in field_data.values() if v is not None][:2]
                        
                        status = "[OK]" if success_rate >= 80 else "[WARN]" if success_rate > 0 else "[FAIL]"
                        print(f"{status} {company}: {success_rate:.1f}% ({successful}/{total})")
                        
                        if sample_values:
                            sample_str = ', '.join([f"'{s}'" if isinstance(s, str) else str(s) for s in sample_values])
                            print(f"   Samples: {sample_str}")
                    else:
                        print(f"[FAIL] {company}: Field not found")
                        
                except FileNotFoundError:
                    print(f"[FAIL] {company}: No data file found")
            
            if field_name != field_names[-1]:  # Not the last field
                print()
    
    def show_multiple_company_summary(self, companies: List[str]) -> None:
        """Show summary for multiple companies"""
        print(f"[MULTI] COMPANY SUMMARIES: {', '.join(companies)}")
        print("=" * 60)
        
        for company in companies:
            try:
                print(f"\n[COMPANY] {company.upper()}")
                print("-" * 30)
                
                data = self.load_company_data(company)
                
                field_stats = []
                for field_name, field_data in data.items():
                    total_docs = len(field_data)
                    successful = sum(1 for v in field_data.values() if v is not None)
                    success_rate = (successful / total_docs) * 100 if total_docs > 0 else 0
                    field_stats.append((success_rate, successful, total_docs))
                
                # Calculate overall stats
                successful_fields = sum(1 for rate, _, _ in field_stats if rate >= 80)
                total_fields = len(field_stats)
                avg_success_rate = sum(rate for rate, _, _ in field_stats) / total_fields if total_fields > 0 else 0
                
                print(f"Fields working well (>=80%): {successful_fields}/{total_fields}")
                print(f"Average success rate: {avg_success_rate:.1f}%")
                
            except FileNotFoundError:
                print(f"\n[FAIL] {company}: No data file found")


def main():
    """CLI interface for output checking"""
    parser = argparse.ArgumentParser(description='Output Check Tool - Analyze existing extraction results')
    parser.add_argument('--company', nargs='+', required=True, help='Company name(s) (e.g., allianz_E ak_E turkiye_E)')
    parser.add_argument('--field', nargs='*', help='Specific field(s) to check (if not specified, shows summary)')
    parser.add_argument('--output-dir', default='data/02_output', help='Output directory')
    
    args = parser.parse_args()
    
    try:
        checker = OutputChecker(args.output_dir)
        
        if len(args.company) == 1:
            # Single company
            if args.field:
                checker.check_fields(args.company[0], args.field)
            else:
                checker.show_summary(args.company[0])
        else:
            # Multiple companies
            if args.field:
                if len(args.field) == 1:
                    # Single field across multiple companies
                    checker.compare_field_across_companies(args.field[0], args.company)
                else:
                    # Multiple fields across multiple companies
                    checker.check_multiple_companies_fields(args.company, args.field)
            else:
                # Summary for multiple companies
                checker.show_multiple_company_summary(args.company)
    
    except Exception as e:
        print(f"[ERROR] Error: {e}")


if __name__ == "__main__":
    main()