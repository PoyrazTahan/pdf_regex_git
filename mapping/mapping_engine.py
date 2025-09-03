#!/usr/bin/env python3
"""
Insurance Data Mapping Engine

Transforms raw extracted policy data into normalized, standardized formats
using configurable mapping rules for cross-company consistency.
"""

import json
import re
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional, Union


class MappingEngine:
    def __init__(self, config_path: str):
        """Initialize mapping engine with configuration."""
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.company = self.config.get('company', 'unknown')
        
    def _load_config(self) -> Dict:
        """Load mapping configuration from JSON file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Failed to load mapping config: {e}")
    
    def _format_turkish_amount(self, value: str) -> str:
        """Transform Turkish number format to normalized format."""
        if not value:
            return ""
            
        # Remove trailing decimals (,00)
        value = re.sub(r',00$', '', value)
        
        # Replace dots with commas for thousands separator
        value = value.replace('.', ',')
        
        # Add surrounding spaces
        return f" {value} "
    
    def _format_simple_amount(self, value: str) -> str:
        """Format simple amount with spaces and proper comma format."""
        if not value:
            return ""
        
        # Replace dots with commas for thousands separator
        value = value.replace('.', ',')
        
        # Add surrounding spaces
        return f" {value} "
    
    def _extract_from_array(self, data: List[str], patterns: List[Dict]) -> Optional[str]:
        """Extract values from array data using multiple patterns."""
        extracted_values = []
        
        for item in data:
            for pattern_config in patterns:
                pattern = pattern_config['pattern']
                group = pattern_config.get('group', 0)
                
                match = re.search(pattern, item, re.IGNORECASE)
                if match:
                    if group > 0:
                        extracted_values.append(match.group(group))
                    else:
                        extracted_values.append(match.group(0))
        
        # Return highest numeric value if multiple found (for duration fields)
        if extracted_values:
            try:
                numeric_values = [int(v) for v in extracted_values if v.isdigit()]
                if numeric_values:
                    return str(max(numeric_values))
            except:
                pass
            return extracted_values[0]
        
        return None
    
    def _apply_pattern_mapping(self, value: Any, field_config: Dict) -> Any:
        """Apply pattern-based mapping to field value."""
        # Handle explicit null mapping
        if value is None:
            mappings = field_config.get('mappings', [])
            for mapping in mappings:
                if mapping.get('input_pattern') is None or mapping.get('input_pattern') == 'null':
                    return mapping['output']
            return field_config.get('default', None)  # Keep null as null if no explicit mapping
        
        if not value:
            return field_config.get('default', value)  # Preserve empty strings
        
        # Handle array values
        if isinstance(value, list):
            # Check all items in array for patterns
            for item in value:
                result = self._apply_pattern_mapping(item, field_config)
                if result != field_config.get('default', value):
                    return result
            return field_config.get('default', value)
        
        # Convert to string for pattern matching
        value_str = str(value)
        
        mappings = field_config.get('mappings', [])
        for mapping in mappings:
            pattern = mapping['input_pattern']
            # Normalize whitespace and handle compressed patterns from CSV
            if pattern:
                # First try exact normalized match
                normalized_pattern = re.sub(r'\s+', ' ', pattern.strip())
                normalized_value = re.sub(r'\s+', ' ', value_str.strip())
                
                if re.search(re.escape(normalized_pattern), normalized_value, re.IGNORECASE):
                    return mapping['output']
                
                # If no match, try fuzzy match by removing all spaces (for CSV compressed patterns)
                compressed_pattern = re.sub(r'\s+', '', pattern.strip())
                compressed_value = re.sub(r'\s+', '', value_str.strip())
                
                if re.search(re.escape(compressed_pattern), compressed_value, re.IGNORECASE):
                    return mapping['output']
        
        return field_config.get('default', value)
    
    def _apply_extract_normalize(self, value: Any, field_config: Dict) -> str:
        """Extract specific values and normalize them."""
        if not value:
            return field_config.get('default', '')
        
        # Handle array values  
        if isinstance(value, list):
            extract_patterns = field_config.get('extract_patterns', [])
            extracted = self._extract_from_array(value, extract_patterns)
            if not extracted:
                return field_config.get('default', '')
            value = extracted
        
        # Apply mappings
        mappings = field_config.get('mappings', [])
        for mapping in mappings:
            if str(value) == mapping['input']:
                return mapping['output']
        
        return field_config.get('default', str(value))
    
    def _apply_amount_normalization(self, value: Any, field_config: Dict) -> str:
        """Normalize monetary amounts."""
        if not value:
            return field_config.get('default', '')
        
        value_str = str(value)
        
        mappings = field_config.get('mappings', [])
        for mapping in mappings:
            pattern = mapping['pattern']
            match = re.search(pattern, value_str)
            if match:
                if 'output' in mapping:
                    return mapping['output']
                elif mapping.get('transform') == 'format_turkish_amount':
                    return self._format_turkish_amount(match.group(1))
                elif mapping.get('transform') == 'format_simple_amount':
                    return self._format_simple_amount(match.group(1))
        
        return field_config.get('default', value_str)
    
    def _parse_turkish_number(self, value_str: str, output_type: str = "integer", turkish_format: bool = None) -> Optional[Union[int, float]]:
        """Parse Turkish/English number format to integer or float."""
        if not value_str or value_str.lower() in ['none', 'nan', 'null']:
            return None
        
        # Handle various formats: "2.500.000,75", "1.000.-TL", "500,000.00 TL"
        cleaned = value_str.strip()
        
        # Remove common currency suffixes
        suffixes = [' TL', '.-TL', '-TL', 'TL', '.-', '-']
        for suffix in suffixes:
            if cleaned.endswith(suffix):
                cleaned = cleaned[:-len(suffix)].strip()
                break
        
        # If format is explicitly specified, use it
        if turkish_format is True:
            # Turkish format: "2.500.000,00" or "500.000,00"
            if ',' in cleaned:
                # With decimals: "2.500.000,00"
                parts = cleaned.split(',')
                if len(parts) == 2:
                    integer_part = parts[0].replace('.', '')  # Remove thousands separators
                    decimal_part = parts[1]
                    
                    if integer_part.isdigit() and decimal_part.isdigit():
                        if output_type == "float":
                            return float(f"{integer_part}.{decimal_part}")
                        else:  # integer - truncate decimals
                            return int(integer_part)
            else:
                # No decimals: "2.500.000"
                integer_only = cleaned.replace('.', '')
                if integer_only.isdigit():
                    number = int(integer_only)
                    return float(number) if output_type == "float" else number
                    
        elif turkish_format is False:
            # English format: "2,500,000.00" or "750,000.00"
            if '.' in cleaned:
                # With decimals: "2,500,000.00"
                parts = cleaned.split('.')
                if len(parts) == 2:
                    integer_part = parts[0].replace(',', '')  # Remove thousands separators
                    decimal_part = parts[1]
                    
                    if integer_part.isdigit() and decimal_part.isdigit():
                        if output_type == "float":
                            return float(f"{integer_part}.{decimal_part}")
                        else:  # integer - truncate decimals
                            return int(integer_part)
            else:
                # No decimals: "2,500,000"
                integer_only = cleaned.replace(',', '')
                if integer_only.isdigit():
                    number = int(integer_only)
                    return float(number) if output_type == "float" else number
        
        else:
            # Auto-detect format (fallback for backwards compatibility)
            # Turkish format: ends with comma (for decimals)
            if ',' in cleaned and cleaned.rindex(',') > cleaned.rfind('.'):
                return self._parse_turkish_number(value_str, output_type, turkish_format=True)
            # English format: ends with dot (for decimals) 
            elif '.' in cleaned and cleaned.rindex('.') > cleaned.rfind(','):
                return self._parse_turkish_number(value_str, output_type, turkish_format=False)
            # No clear indicators, try simple parsing
            elif cleaned.replace('.', '').replace(',', '').isdigit():
                # Prefer Turkish if has dots, English if has commas
                if '.' in cleaned and ',' not in cleaned:
                    return self._parse_turkish_number(value_str, output_type, turkish_format=True)
                elif ',' in cleaned and '.' not in cleaned:
                    return self._parse_turkish_number(value_str, output_type, turkish_format=False)
        
        return None
    
    def _apply_numeric_conversion(self, value: Any, field_config: Dict) -> Optional[Union[int, float]]:
        """Convert string values to clean integers or floats."""
        if not value:
            return field_config.get('default', None)
        
        value_str = str(value)
        output_type = field_config.get('output_type', 'integer')
        
        # Handle array values - take first valid number
        if isinstance(value, list):
            for item in value:
                result = self._apply_numeric_conversion(item, field_config)
                if result is not None:
                    return result
            return field_config.get('default', None)
        
        # Check explicit mappings first (for special cases like "SINIRSIZ")
        mappings = field_config.get('mappings', [])
        for mapping in mappings:
            input_pattern = mapping.get('input_pattern', '')
            
            # Check if input matches
            if str(value_str).strip() == str(input_pattern).strip():
                output = mapping.get('output')
                if isinstance(output, (int, float)):
                    return output  # Return as configured (int or float)
                
                # Apply multiplier if configured
                multiplier = mapping.get('multiplier', 1)
                if field_config.get('turkish_format', False):
                    parsed = self._parse_turkish_number(input_pattern, output_type)
                    if parsed is not None:
                        result = parsed * multiplier
                        return int(result) if output_type == 'integer' else float(result)
                
                # Try to convert output to requested type
                try:
                    return int(output) if output_type == 'integer' else float(output)
                except (ValueError, TypeError):
                    return output
        
        # Try to parse as number (handles both Turkish and English formats)
        turkish_format = field_config.get('turkish_format')
        parsed = self._parse_turkish_number(value_str, output_type, turkish_format)
        if parsed is not None:
            return parsed
        
        # Fallback: try to convert directly
        try:
            number = float(value_str)
            return int(number) if output_type == 'integer' else number
        except (ValueError, TypeError):
            return field_config.get('default', None)
    
    def _map_field(self, field_name: str, value: Any) -> Any:
        """Map a single field value using the configured mapping."""
        field_config = self.config['field_mappings'].get(field_name)
        if not field_config:
            return value  # Return original value (including None) if no mapping config
        
        mapping_type = field_config['type']
        
        if mapping_type == 'fixed_value':
            return field_config['output']
        elif mapping_type == 'pattern_to_value':
            return self._apply_pattern_mapping(value, field_config)
        elif mapping_type == 'extract_normalize':
            return self._apply_extract_normalize(value, field_config)
        elif mapping_type == 'amount_normalization':
            return self._apply_amount_normalization(value, field_config)
        elif mapping_type == 'numeric_conversion':
            return self._apply_numeric_conversion(value, field_config)
        else:
            print(f"Warning: Unknown mapping type '{mapping_type}' for field '{field_name}'")
            return value
    
    def process_file(self, input_path: str, output_path: str):
        """Process entire JSON file and generate mapped output."""
        input_file = Path(input_path)
        output_file = Path(output_path)
        
        # Load input data
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
        except Exception as e:
            raise Exception(f"Failed to load input file: {e}")
        
        # Process each field
        mapped_data = {}
        stats = {'total_fields': 0, 'mapped_fields': 0, 'errors': []}
        
        for field_name, field_data in raw_data.items():
            stats['total_fields'] += 1
            
            try:
                # Create mapped field structure
                mapped_field = {}
                
                for document_id, document_value in field_data.items():
                    mapped_value = self._map_field(field_name, document_value)
                    mapped_field[document_id] = mapped_value
                
                mapped_data[field_name] = mapped_field
                stats['mapped_fields'] += 1
                
            except Exception as e:
                error_msg = f"Error mapping field '{field_name}': {e}"
                stats['errors'].append(error_msg)
                print(f"WARNING: {error_msg}")
                # Keep original data on error
                mapped_data[field_name] = field_data
        
        # Add metadata
        mapped_data['_mapping_metadata'] = {
            'company': self.company,
            'config_version': self.config.get('version', '1.0'),
            'processing_stats': stats,
            'timestamp': __import__('datetime').datetime.now().isoformat()
        }
        
        # Write output
        output_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(mapped_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise Exception(f"Failed to write output file: {e}")
        
        # Print summary
        print(f"[SUCCESS] Mapping completed for {self.company}")
        print(f"[REPORT] Processed {stats['mapped_fields']}/{stats['total_fields']} fields successfully")
        if stats['errors']:
            print(f"[WARN]  {len(stats['errors'])} errors encountered")
        print(f"[SAVE] Output saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Insurance Data Mapping Engine')
    parser.add_argument('--input', required=True, help='Input JSON file path')
    parser.add_argument('--output', required=True, help='Output JSON file path')
    parser.add_argument('--config', required=True, help='Mapping configuration file path')
    
    args = parser.parse_args()
    
    try:
        engine = MappingEngine(args.config)
        engine.process_file(args.input, args.output)
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())