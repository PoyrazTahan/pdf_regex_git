#!/usr/bin/env python3
"""
Data loading module for dashboard generation.
Handles loading and processing of extraction and mapping data.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass


@dataclass
class DashboardData:
    """Container for dashboard data."""
    primary_data: Dict[str, Any]
    secondary_data: Dict[str, Any] 
    companies: List[str]
    fields: List[str]
    mode: str
    stats: Dict[str, Any]


class DataLoader:
    """Handles loading data for different dashboard modes."""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.companies = [
            'ak_E', 'allianz_E', 'anadolu_E', 'ankara_E', 'axa_E', 'doga_E',
            'gulf_E', 'hdi_E', 'mapfre_E', 'mg_E', 'neova_E', 'orient_E',
            'quick_E', 'ray_E', 'sompo_E', 'turkiye_E', 'turkiyekatilim_E',
            'turknippon_E', 'unico_E', 'zurich_E'
        ]
    
    def load_data(self, mode: str) -> DashboardData:
        """Load data based on mode (regex or mapped)."""
        if mode == "regex":
            return self._load_regex_data()
        elif mode == "mapped":
            return self._load_mapped_data()
        else:
            raise ValueError(f"Unknown mode: {mode}")
    
    def _load_regex_data(self) -> DashboardData:
        """Load data for regex pattern analysis."""
        output_dir = self.base_dir / "data" / "02_output"
        config_dir = self.base_dir / "config" / "extraction_patterns"
        
        output_data = {}
        config_data = {}
        all_fields = set()
        
        print("Loading regex data from 02_output/...")
        
        for company in self.companies:
            # Load output data
            output_file = output_dir / f"{company}.json"
            if output_file.exists():
                try:
                    with open(output_file, 'r', encoding='utf-8') as f:
                        output_data[company] = json.load(f)
                        all_fields.update(output_data[company].keys())
                        print(f"[SUCCESS] Loaded output data for {company}")
                except Exception as e:
                    print(f"[ERROR] Error loading output for {company}: {e}")
            else:
                print(f"[WARN]  Output file not found for {company}")
            
            # Load config data
            config_file = config_dir / f"{company}.json"
            if config_file.exists():
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        config_data[company] = json.load(f)
                        all_fields.update(config_data[company].keys())
                        print(f"[SUCCESS] Loaded config data for {company}")
                except Exception as e:
                    print(f"[ERROR] Error loading config for {company}: {e}")
            else:
                print(f"[WARN]  Config file not found for {company}")
        
        valid_companies = [c for c in self.companies if c in output_data]
        all_fields = sorted(list(all_fields))
        
        stats = {
            'companies_total': len(self.companies),
            'companies_with_data': len(valid_companies),
            'fields_total': len(all_fields)
        }
        
        print(f"\n[REPORT] Regex Data Summary:")
        print(f"   Companies: {len(valid_companies)}")
        print(f"   Fields: {len(all_fields)}")
        
        return DashboardData(
            primary_data=output_data,
            secondary_data=config_data,
            companies=valid_companies,
            fields=all_fields,
            mode="regex",
            stats=stats
        )
    
    def _load_mapped_data(self) -> DashboardData:
        """Load data for mapped data analysis."""
        mapped_dir = self.base_dir / "data" / "03_mapped"
        mapping_dir = self.base_dir / "config" / "mapping_rules"
        
        mapped_data = {}
        mapping_config_data = {}
        all_fields = set()
        
        print("Loading mapped data from 03_mapped/...")
        
        for company in self.companies:
            # Load mapped data
            mapped_file = mapped_dir / f"{company}.json"
            if mapped_file.exists():
                try:
                    with open(mapped_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Remove metadata from field analysis
                        if '_mapping_metadata' in data:
                            del data['_mapping_metadata']
                        mapped_data[company] = data
                        all_fields.update(data.keys())
                        print(f"[SUCCESS] Loaded mapped data for {company}")
                except Exception as e:
                    print(f"[ERROR] Error loading mapped data for {company}: {e}")
            else:
                print(f"[WARN]  Mapped file not found for {company}")
            
            # Load mapping configuration
            mapping_file = mapping_dir / f"{company}_map.json"
            if mapping_file.exists():
                try:
                    with open(mapping_file, 'r', encoding='utf-8') as f:
                        mapping_config_data[company] = json.load(f)
                        if 'field_mappings' in mapping_config_data[company]:
                            all_fields.update(mapping_config_data[company]['field_mappings'].keys())
                        print(f"[SUCCESS] Loaded mapping config for {company}")
                except Exception as e:
                    print(f"[ERROR] Error loading mapping config for {company}: {e}")
            else:
                print(f"[INFO]  No mapping config found for {company}")
        
        valid_companies = [c for c in self.companies if c in mapped_data]
        all_fields = sorted(list(all_fields))
        
        stats = {
            'companies_total': len(self.companies),
            'companies_with_data': len(valid_companies),
            'companies_with_mapping': len(mapping_config_data),
            'fields_total': len(all_fields)
        }
        
        print(f"\n[REPORT] Mapped Data Summary:")
        print(f"   Companies: {len(valid_companies)}")
        print(f"   Fields: {len(all_fields)}")
        print(f"   Companies with mapping configs: {len(mapping_config_data)}")
        
        return DashboardData(
            primary_data=mapped_data,
            secondary_data=mapping_config_data,
            companies=valid_companies,
            fields=all_fields,
            mode="mapped",
            stats=stats
        )


if __name__ == "__main__":
    # Test data loading
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python dashboard_data.py [regex|mapped]")
        sys.exit(1)
    
    loader = DataLoader()
    data = loader.load_data(sys.argv[1])
    
    print(f"\n[TEST] Loaded {data.mode} data:")
    print(f"  Companies: {len(data.companies)}")
    print(f"  Fields: {len(data.fields)}")
    print(f"  Stats: {data.stats}")