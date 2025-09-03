#!/usr/bin/env python3
"""
Field Development Tool
Streamlined tool for field discovery, context analysis, and pattern testing
"""
import argparse
import re
from pathlib import Path
from typing import List, Dict, Tuple
import sys
import os
# Add the agent_tools directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from enhanced_extractor import EnhancedPdfExtractor


class FieldDeveloper:
    """Tool for developing field extraction patterns"""
    
    def __init__(self, company: str):
        self.company = company
        self.pdf_dir = Path(f"data/00_raw_pdfs/{company}")
        self.extractor = EnhancedPdfExtractor(company)
        
        if not self.pdf_dir.exists():
            raise FileNotFoundError(f"PDF directory not found: {self.pdf_dir}")
        
        self.pdf_files = sorted(list(self.pdf_dir.glob("*.pdf")))
        if not self.pdf_files:
            raise FileNotFoundError(f"No PDF files found in {self.pdf_dir}")
    
    def search_field(self, field_name: str, max_files: int = 5) -> None:
        """Search for field across company PDFs"""
        print(f"[SEARCH] SEARCHING FOR FIELD: {field_name}")
        print(f"[COMPANY] Company: {self.company}")
        print(f"[PDF] Scanning {min(len(self.pdf_files), max_files)} PDFs")
        print("=" * 60)
        
        found_count = 0
        files_to_check = self.pdf_files[:max_files]
        
        for pdf_file in files_to_check:
            text = self.extractor.get_pdf_text(str(pdf_file))
            
            # Search for field name (case insensitive)
            matches = re.finditer(re.escape(field_name), text, re.IGNORECASE)
            file_matches = list(matches)
            
            if file_matches:
                found_count += 1
                print(f"\n[FOUND] {pdf_file.name}")
                
                for i, match in enumerate(file_matches[:3]):  # Show max 3 matches per file
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    context = text[start:end].replace('\n', ' ')
                    
                    # Highlight the match
                    highlighted = context.replace(match.group(), f"**{match.group()}**")
                    print(f"   Match {i+1}: ...{highlighted}...")
                
                if len(file_matches) > 3:
                    print(f"   ... and {len(file_matches) - 3} more matches")
        
        print(f"\n[SUMMARY] SUMMARY:")
        print(f"Found in {found_count}/{len(files_to_check)} files")
        
        if found_count == 0:
            print(f"\n[TIP] TRY VARIATIONS:")
            print(f"   - Partial matches: '{field_name[:10]}'")
            print(f"   - Case variations: '{field_name.upper()}', '{field_name.lower()}'")
            print(f"   - Space variations: '{field_name.replace('_', ' ')}'")
    
    def analyze_context(self, field_name: str, lines_before: int = 3, lines_after: int = 3, max_files: int = 3) -> None:
        """Analyze field context with line-based analysis"""
        print(f"[CONTEXT] CONTEXT ANALYSIS: {field_name}")
        print(f"[COMPANY] Company: {self.company}")
        print(f"[LINES] Lines context: {lines_before} before, {lines_after} after")
        print("=" * 60)
        
        found_count = 0
        files_to_check = self.pdf_files[:max_files]
        
        for pdf_file in files_to_check:
            text = self.extractor.get_pdf_text(str(pdf_file))
            lines = text.split('\n')
            
            matches_found = False
            for line_num, line in enumerate(lines):
                if re.search(re.escape(field_name), line, re.IGNORECASE):
                    if not matches_found:
                        found_count += 1
                        print(f"\n[FILE] {pdf_file.name}")
                        matches_found = True
                    
                    print(f"\n--- Match at line {line_num + 1} ---")
                    
                    # Show lines before
                    if lines_before > 0:
                        print("[BEFORE] LINES BEFORE:")
                        start_line = max(0, line_num - lines_before)
                        for i in range(start_line, line_num):
                            print(f"   {i + 1:3}: '{lines[i]}'")
                    
                    # Show matched line
                    print("[MATCH] MATCHED LINE:")
                    print(f"   {line_num + 1:3}: '{line}'")
                    
                    # Show lines after
                    if lines_after > 0:
                        print("[AFTER] LINES AFTER:")
                        end_line = min(len(lines), line_num + lines_after + 1)
                        for i in range(line_num + 1, end_line):
                            print(f"   {i + 1:3}: '{lines[i]}'")
                    
                    # Generate pattern suggestions
                    self._suggest_patterns(lines, line_num, field_name)
                    break  # Only show first match per file
        
        print(f"\n[SUMMARY] SUMMARY:")
        print(f"Found in {found_count}/{len(files_to_check)} files")
    
    def _suggest_patterns(self, lines: List[str], line_num: int, field_name: str) -> None:
        """Generate pattern suggestions based on context"""
        print("\n[SUGGEST] PATTERN SUGGESTIONS:")
        
        current_line = lines[line_num]
        
        # Basic field extraction patterns
        if ':' in current_line:
            print(f"1. After colon: {field_name}\\s*:\\s*([^\\n]+)")
        
        if line_num + 1 < len(lines):
            next_line = lines[line_num + 1]
            print(f"2. Next line: {field_name}\\s*\\n([^\\n]+)")
            print(f"   Would extract: '{next_line}'")
        
        if line_num + 2 < len(lines):
            line_after_next = lines[line_num + 2]
            print(f"3. Line +2: {field_name}[\\s\\S]*?\\n[^\\n]*\\n([^\\n]+)")
            print(f"   Would extract: '{line_after_next}'")
    
    def test_pattern(self, pattern: str, group: int = 1, max_files: int = 5) -> None:
        """Test a regex pattern across PDFs"""
        print(f"[TEST] TESTING PATTERN: {pattern}")
        print(f"[COMPANY] Company: {self.company}")
        print(f"[GROUP] Group: {group}")
        print("=" * 60)
        
        total_matches = 0
        files_with_matches = 0
        files_to_check = self.pdf_files[:max_files]
        
        for pdf_file in files_to_check:
            matches = self.extractor.test_pattern_on_pdf(str(pdf_file), pattern, group)
            
            if matches:
                files_with_matches += 1
                total_matches += len(matches)
                
                print(f"\n[SUCCESS] {pdf_file.name}")
                print(f"   Matches: {len(matches)}")
                
                for i, match in enumerate(matches[:3]):  # Show max 3 matches per file
                    print(f"   {i+1}: '{match}'")
                
                if len(matches) > 3:
                    print(f"   ... and {len(matches) - 3} more")
            else:
                print(f"\n[FAIL] {pdf_file.name}: No matches")
        
        print(f"\n[SUMMARY] PATTERN TEST SUMMARY:")
        print(f"Files with matches: {files_with_matches}/{len(files_to_check)}")
        print(f"Total matches: {total_matches}")
        
        if files_with_matches > 0:
            success_rate = (files_with_matches / len(files_to_check)) * 100
            print(f"Success rate: {success_rate:.1f}%")
            
            if success_rate >= 80:
                print("[OK] Pattern looks good!")
            elif success_rate >= 60:
                print("[WARN] Pattern works but could be improved")
            else:
                print("[FAIL] Pattern needs work")
        else:
            print("[FAIL] Pattern failed - no matches found")


def main():
    """CLI interface for field development"""
    parser = argparse.ArgumentParser(description='Field Development Tool')
    parser.add_argument('--company', required=True, help='Company name (e.g., allianz_E)')
    parser.add_argument('--field', help='Field name to search for')
    parser.add_argument('--context', action='store_true', help='Show detailed context analysis')
    parser.add_argument('--pattern', help='Test a regex pattern')
    parser.add_argument('--group', type=int, default=1, help='Regex group to extract (default: 1)')
    parser.add_argument('--max-files', type=int, default=5, help='Maximum files to process (default: 5)')
    parser.add_argument('--lines-before', type=int, default=3, help='Lines to show before match (default: 3)')
    parser.add_argument('--lines-after', type=int, default=3, help='Lines to show after match (default: 3)')
    
    args = parser.parse_args()
    
    try:
        developer = FieldDeveloper(args.company)
        
        if args.pattern:
            # Test pattern mode
            developer.test_pattern(args.pattern, args.group, args.max_files)
        
        elif args.field:
            if args.context:
                # Context analysis mode
                developer.analyze_context(args.field, args.lines_before, args.lines_after, args.max_files)
            else:
                # Field search mode
                developer.search_field(args.field, args.max_files)
        
        else:
            print("[ERROR] Please specify either --field or --pattern")
            print("Examples:")
            print("  python field_dev.py --company allianz_E --field 'Police_No'")
            print("  python field_dev.py --company allianz_E --field 'Police_No' --context")
            print("  python field_dev.py --company allianz_E --pattern 'Policy.*?([0-9-]+)'")
    
    except Exception as e:
        print(f"[ERROR] Error: {e}")


if __name__ == "__main__":
    main()