#!/usr/bin/env python3
"""
Enhanced PDF Extractor
Supports single patterns, multiple patterns, and list collection modes
"""
import fitz  # PyMuPDF
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Union, Any


class EnhancedPdfExtractor:
    """Enhanced PDF extractor supporting flexible pattern configurations"""
    
    def __init__(self, company: str):
        self.company = company
        self.config_dir = Path("config/extraction_patterns")
        self.config = self._load_config()
        self._pdf_cache = {}
    
    def _load_config(self) -> Dict:
        """Load company configuration"""
        config_path = self.config_dir / f"{self.company.lower()}.json"
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_pdf_text(self, pdf_path: str) -> str:
        """Extract and cache text from PDF"""
        if pdf_path not in self._pdf_cache:
            try:
                doc = fitz.open(pdf_path)
                text = ""
                for page in doc:
                    text += page.get_text()
                doc.close()
                self._pdf_cache[pdf_path] = text
            except Exception as e:
                raise RuntimeError(f"Failed to extract text from {pdf_path}: {e}")
        
        return self._pdf_cache[pdf_path]
    
    def extract_single_pattern(self, text: str, pattern: str, group: int = 1) -> Optional[str]:
        """Extract using single pattern"""
        try:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                if group == 0:
                    return match.group(0).strip()
                elif isinstance(group, int) and group <= len(match.groups()):
                    value = match.group(group)
                    return value.strip() if value else None
            return None
        except re.error:
            return None
    
    def extract_all_matches(self, text: str, pattern: str, group: int = 1) -> List[str]:
        """Extract all matches for a pattern"""
        try:
            matches = re.finditer(pattern, text, re.DOTALL | re.IGNORECASE)
            results = []
            for match in matches:
                if group == 0:
                    value = match.group(0).strip()
                elif isinstance(group, int) and group <= len(match.groups()):
                    value = match.group(group)
                    value = value.strip() if value else None
                else:
                    continue
                
                if value:
                    results.append(value)
            return results
        except re.error:
            return []
    
    def extract_field(self, pdf_path: str, field_name: str) -> Union[str, List[str], None]:
        """Extract field using flexible configuration"""
        if field_name not in self.config:
            return None
        
        field_config = self.config[field_name]
        if not field_config:
            return None
        
        text = self.get_pdf_text(pdf_path)
        
        # Legacy single pattern mode
        if 'pattern' in field_config:
            pattern = field_config['pattern']
            group = field_config.get('group', 1)
            # Handle special 'all' group parameter
            if group == 'all':
                return self.extract_all_matches(text, pattern, 0)
            return self.extract_single_pattern(text, pattern, group)
        
        # New multiple patterns mode
        elif 'patterns' in field_config:
            all_results = []
            
            for pattern_config in field_config['patterns']:
                if isinstance(pattern_config, str):
                    # Simple string pattern
                    pattern = pattern_config
                    group = 1
                else:
                    # Pattern object with group info
                    pattern = pattern_config.get('pattern', '')
                    group = pattern_config.get('group', 1)
                
                if not pattern:
                    continue
                
                # Collect matches based on mode
                mode = field_config.get('mode', 'first')
                if mode == 'all':
                    matches = self.extract_all_matches(text, pattern, group)
                    all_results.extend(matches)
                else:
                    match = self.extract_single_pattern(text, pattern, group)
                    if match:
                        all_results.append(match)
                        if mode == 'first':
                            break  # Stop after first successful pattern
            
            # Return results based on mode
            mode = field_config.get('mode', 'first')
            if mode == 'all':
                return all_results if all_results else None
            else:
                return all_results[0] if all_results else None
        
        return None
    
    def extract_all_fields(self, pdf_path: str) -> Dict[str, Union[str, List[str], None]]:
        """Extract all fields from a PDF"""
        results = {}
        for field_name in self.config.keys():
            results[field_name] = self.extract_field(pdf_path, field_name)
        return results
    
    def get_field_names(self) -> List[str]:
        """Get list of all field names in configuration"""
        return list(self.config.keys())
    
    def test_pattern_on_pdf(self, pdf_path: str, pattern: str, group: int = 1) -> List[str]:
        """Test a pattern on a specific PDF and return all matches"""
        text = self.get_pdf_text(pdf_path)
        return self.extract_all_matches(text, pattern, group)