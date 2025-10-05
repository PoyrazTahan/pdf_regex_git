# Configuration Directory

## 📁 **Structure**

```
config/
├── extraction_patterns/    # Regex patterns for PDF data extraction
│   ├── ak_E.json           # AK Sigorta extraction rules
│   ├── allianz_E.json      # Allianz extraction rules
│   ├── ...                 # Other company patterns
│   └── universal.json      # Cross-company field definitions
└── mapping_rules/          # Data normalization mappings
    ├── ak_E_map.json       # AK Sigorta normalization rules
    ├── allianz_E_map.json  # Allianz normalization rules
    └── universal_map.json  # Cross-company standards
```

## 🔧 **Extraction Patterns** (`extraction_patterns/`)

**Purpose**: Define regex patterns for extracting structured data from PDF text
**Format**: JSON files with field definitions and regex patterns
**Usage**: Used by `enhanced_extractor.py` and agent tools

**Example Structure**:
```json
{
  "Police_No": {
    "pattern": "Policy\\s*No[:\\s]*([0-9-]+)",
    "group": 1,
    "description": "Policy number extraction"
  },
  "Teminat_Oto_Cam_Klozu": {
    "patterns": [
      "(CAM KIRILMASI TEMİNATI[\\s\\S]*?uygulanmamaktadır\\.)",
      "(CAM KIRILMASI TEMİNATI[\\s\\S]*?uygulanacaktır\\.)"
    ],
    "mode": "first"
  }
}
```

## 🗺️ **Mapping Rules** (`mapping_rules/`)

**Purpose**: Normalize extracted data into standardized formats across companies
**Format**: JSON files with transformation rules and business logic
**Usage**: Used by `mapping_engine.py` and normalization tools

**Example Structure**:
```json
{
  "company": "ak_E",
  "field_mappings": {
    "Teminat_Yedek_Parca": {
      "type": "fixed_value",
      "output": "Var"
    },
    "Teminat_IMM_Bedeni_Maddi_Ayrimsiz_Bedeli": {
      "type": "amount_normalization",
      "mappings": [
        {
          "pattern": "SINIRSIZ İMM",
          "output": " 9,999,999,999 "
        }
      ]
    }
  }
}
```

## 🔄 **Relationship Between Configs**

1. **extraction_patterns** → Extract raw data from PDFs
2. **mapping_rules** → Normalize raw data into standardized format

**Example Flow**:
```
PDF: "Poliçe No: 123456789"
↓ (extraction_patterns/ak_E.json)
Raw: "123456789"
↓ (mapping_rules/ak_E_map.json)  
Normalized: "K-123456789-0-0"
```

## 📝 **Configuration Management**

### **Adding New Company**
1. Create `extraction_patterns/newcompany_E.json`
2. Create `mapping_rules/newcompany_E_map.json`
3. Test extraction and mapping
4. Document any special patterns or business rules

### **Updating Existing Company**
1. Modify appropriate config file
2. Test changes against sample data
3. Update documentation if adding new field types

### **Version Control**
- All config changes should be tracked in git
- Include description of what patterns/mappings were added/changed
- Test thoroughly before committing changes that affect multiple policies