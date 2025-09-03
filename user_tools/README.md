# User Tools - Simple Policy Processing

This directory contains user-friendly tools for processing Turkish insurance policy PDFs. These tools provide a simple interface for the complete data extraction and normalization pipeline.

## 🚀 Quick Start

### Process Everything (Recommended)
```bash
# Complete pipeline: PDFs → Extracted data → Normalized data
python user_tools/process_pipeline.py --company ak_E
```

### Step-by-Step Processing
```bash
# Step 1: Extract data from PDFs
python user_tools/extract_policies.py --company ak_E

# Step 2: Normalize extracted data  
python user_tools/normalize_data.py --company ak_E
```

## 📋 Available Tools

### 1. **process_pipeline.py** - Complete Pipeline
The main tool that orchestrates the entire processing workflow.

**Basic Usage:**
```bash
# Process all companies (DEFAULT - no arguments needed!)
python user_tools/process_pipeline.py

# Process single company
python user_tools/process_pipeline.py --company ak_E

# Process specific field across all companies
python user_tools/process_pipeline.py --field Police_No

# Generate dashboard after processing
python user_tools/process_pipeline.py --visualize

# Skip extraction step (use existing data)
python user_tools/process_pipeline.py --skip-extraction

# Combine options
python user_tools/process_pipeline.py --company ak_E --visualize --skip-extraction
```

**What it does:**
1. ✅ Validates company files and configurations
2. 🔍 Extracts structured data from PDFs (if not skipped)
3. 🗺️ Normalizes data using mapping rules (if config exists)
4. 📊 Generates quality report
5. 📊 Creates visualization dashboard (if --visualize flag used)

**NEW FEATURES:**
- **Default behavior**: Runs on all companies when no arguments provided
- **Field analysis**: `--field FieldName` processes specific field across all companies
- **Dashboard generation**: `--visualize` creates interactive HTML dashboard at `data/static_dashboard.html` with all data embedded

### 2. **extract_policies.py** - PDF Data Extraction
Extracts structured data from insurance policy PDFs using regex patterns.

**Usage:**
```bash
# Extract single company
python user_tools/extract_policies.py --company ak_E

# Extract with custom output location
python user_tools/extract_policies.py --company allianz_E --output custom_results.json

# Extract all companies
python user_tools/extract_policies.py --all-companies
```

**Requirements:**
- PDF files in `data/00_raw_pdfs/company_E/`
- Extraction config in `config/extraction_patterns/company_E.json`

**Output:** JSON file in `data/02_output/company_E.json`

### 3. **normalize_data.py** - Data Normalization
Transforms extracted data into standardized business formats.

**Usage:**
```bash
# Normalize single company
python user_tools/normalize_data.py --company ak_E

# Custom input/output files
python user_tools/normalize_data.py --input custom_data.json --config custom_map.json

# Normalize all companies with mapping configs
python user_tools/normalize_data.py --all-companies
```

**Requirements:**
- Extracted data in `data/02_output/company_E.json`
- Mapping config in `config/mapping_rules/company_E_map.json`

**Output:** Normalized JSON file in `data/03_mapped/company_E.json`

## 📊 Company Status

### ✅ Fully Supported (Extraction + Normalization)
- **ak_E** - AK Sigorta (complete mapping rules)
- **allianz_E** - Allianz (complete mapping rules)  
- **anadolu_E** - Anadolu (complete mapping rules)
- **ankara_E** - Ankara (complete mapping rules)
- **axa_E** - AXA (complete mapping rules)

### 🔍 Extraction Only (Normalization Pending)
- doga_E, gulf_E, hdi_E, mapfre_E, mg_E, neova_E, orient_E
- quick_E, ray_E, sompo_E, turkiye_E, turkiyekatilim_E, turknippon_E
- unico_E, zurich_E

## 💡 Common Usage Patterns

### New User - Quick Start
```bash
# Process everything with dashboard (RECOMMENDED)
python user_tools/process_pipeline.py --visualize

# Process single company (works with ak_E, allianz_E, anadolu_E, ankara_E, axa_E)
python user_tools/process_pipeline.py --company ak_E
```

### Batch Processing All Companies
```bash
# Extract data for all companies
python user_tools/extract_policies.py --all-companies

# Normalize only companies with mapping rules
python user_tools/normalize_data.py --all-companies
```

### Development/Testing Workflow
```bash
# Re-run only normalization after config changes
python user_tools/process_pipeline.py --company ak_E --skip-extraction

# Test specific field across all companies
python user_tools/process_pipeline.py --field "Police_No"

# Extract only (for testing new patterns)
python user_tools/extract_policies.py --company test_company_E
```

### Dashboard and Visualization
```bash
# Generate dashboard for all processed data
python user_tools/process_pipeline.py --visualize --skip-extraction

# Process and visualize single company
python user_tools/process_pipeline.py --company ak_E --visualize

# View dashboard: Open data/static_dashboard.html in browser
# Dashboard contains all data embedded - no external dependencies!
```

### Custom Data Processing
```bash
# Use your own files
python user_tools/normalize_data.py --input my_data.json --config my_rules.json --output my_output.json
```

## 🎯 Expected Output Structure

### Extraction Output (`data/02_output/company_E.json`)
```json
{
  "document1.pdf": {
    "Police_No": "12345-67890",
    "Baslangic_Tarihi": "01/01/2024",
    "Arac_Plaka": "34 ABC 123"
  },
  "document2.pdf": {
    "Police_No": "67890-12345", 
    "Baslangic_Tarihi": "15/02/2024",
    "Arac_Plaka": "06 XYZ 789"
  }
}
```

### Normalized Output (`data/03_mapped/company_E.json`)
```json
{
  "document1.pdf": {
    "policy_number": "12345-67890",
    "start_date": "2024-01-01",
    "license_plate": "34ABC123",
    "coverage_glass": "Available"
  },
  "document2.pdf": {
    "policy_number": "67890-12345",
    "start_date": "2024-02-15", 
    "license_plate": "06XYZ789",
    "coverage_glass": "Not Available"
  }
}
```

## ❌ Common Errors and Solutions

### "No PDF directory found"
**Problem:** Company doesn't exist or wrong name
**Solution:** 
```bash
# Check available companies
ls data/00_raw_pdfs/
# Use exact directory name (usually ends with _E)
```

### "No extraction configuration found"
**Problem:** Company doesn't have regex patterns configured
**Solution:** Contact development team to create extraction patterns

### "No mapping configuration found"  
**Problem:** Company doesn't have normalization rules yet
**Solution:** This is normal - most companies only have extraction so far

### "No extraction results found"
**Problem:** Need to run extraction before normalization
**Solution:**
```bash
# Run extraction first
python user_tools/extract_policies.py --company company_E
```

## 📚 Need More Control?

If you need advanced features or debugging capabilities, see the agent development tools:
- **[Agent Tools Directory](../agent_tools/README.md)** - Development tool reference
- **[Agent Tools Guide](../docs/AGENT_TOOLS.md)** - Advanced development workflow
- **[Field Patterns Guide](../docs/FIELD_PATTERNS_GUIDE.md)** - Pattern development reference
- **[Configuration Guide](../config/README.md)** - Config file management

## 🆘 Getting Help

1. **Check tool help:** Add `--help` to any command
2. **Validate setup:** Ensure PDF files and configs exist in expected locations  
3. **Check logs:** Tools show detailed error messages and suggestions
4. **Contact support:** For new company setup or advanced configuration needs