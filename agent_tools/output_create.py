#!/usr/bin/env python3
"""
Output Create Tool  
Creates extraction results for all fields in a company
"""
import argparse
import json
from pathlib import Path
from typing import Dict, Any
from collections import defaultdict
import sys
import os
# Add the agent_tools directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from enhanced_extractor import EnhancedPdfExtractor


class OutputCreator:
    """Tool for generating extraction results"""
    
    def __init__(self, company: str, output_dir: str = "data/02_output"):
        self.company = company
        self.pdf_dir = Path(f"data/00_raw_pdfs/{company}")
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.extractor = EnhancedPdfExtractor(company)
        
        if not self.pdf_dir.exists():
            raise FileNotFoundError(f"PDF directory not found: {self.pdf_dir}")
        
        self.pdf_files = sorted(list(self.pdf_dir.glob("*.pdf")))
        if not self.pdf_files:
            raise FileNotFoundError(f"No PDF files found in {self.pdf_dir}")
    
    def generate_all_fields(self) -> Dict[str, Any]:
        """Generate output for all fields"""
        print(f"[COMPANY] GENERATING ALL FIELDS: {self.company}")
        print(f"[PDF] Processing {len(self.pdf_files)} PDFs")
        print("=" * 60)
        
        # Structure: {field_name: {doc_id: value}}
        all_results = defaultdict(dict)
        field_stats = {}
        
        field_names = self.extractor.get_field_names()
        print(f"[FIELDS] Fields to process: {len(field_names)}")
        
        for pdf_file in self.pdf_files:
            doc_id = pdf_file.stem
            print(f"[PDF] Processing: {doc_id}")
            
            field_results = self.extractor.extract_all_fields(str(pdf_file))
            
            for field_name, value in field_results.items():
                all_results[field_name][doc_id] = value
        
        # Calculate field statistics
        total_docs = len(self.pdf_files)
        for field_name, field_data in all_results.items():
            successful = sum(1 for v in field_data.values() if v is not None)
            success_rate = (successful / total_docs) * 100 if total_docs > 0 else 0
            
            field_stats[field_name] = {
                'successful': successful,
                'total': total_docs,
                'success_rate': success_rate
            }
        
        # Save results to file
        output_file = self.output_dir / f"{self.company}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dict(all_results), f, ensure_ascii=False, indent=2)
        
        print(f"\n[SUCCESS] Results saved to: {output_file}")
        
        # Show summary statistics
        self._show_field_summary(field_stats)
        
        return dict(all_results)
    
    def _show_field_summary(self, field_stats: Dict[str, Dict]) -> None:
        """Show field extraction summary"""
        print(f"\n[SUMMARY] EXTRACTION SUMMARY")
        print("=" * 60)
        
        # Sort fields by success rate
        sorted_fields = sorted(field_stats.items(), key=lambda x: x[1]['success_rate'], reverse=True)
        
        successful_fields = 0
        total_fields = len(sorted_fields)
        
        for field_name, stats in sorted_fields:
            success_rate = stats['success_rate']
            successful = stats['successful']
            total = stats['total']
            
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
        print(f"\n[OVERALL] COMPLETION:")
        print(f"Fields working well (>=80%): {successful_fields}/{total_fields} ({completion_rate:.1f}%)")


def main():
    """CLI interface for output creation"""
    parser = argparse.ArgumentParser(description='Output Create Tool - Generate extraction results for all fields')
    parser.add_argument('--company', required=True, help='Company name (e.g., allianz_E)')
    parser.add_argument('--output-dir', default='data/02_output', help='Output directory')
    
    args = parser.parse_args()
    
    try:
        creator = OutputCreator(args.company, args.output_dir)
        creator.generate_all_fields()
    
    except Exception as e:
        print(f"[ERROR] Error: {e}")


if __name__ == "__main__":
    main()