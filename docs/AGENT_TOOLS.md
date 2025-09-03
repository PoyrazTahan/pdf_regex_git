# Agent Development Tools - Insurance PDF Regex Pattern Development

## 🎯 **Project Overview**

Internal development tools for extracting structured data from Turkish insurance policy PDFs across **20 companies** using company-specific regex patterns. Target: ~30 standardized fields per company using agent development tools.

## 🏗️ **Current System Architecture**

```
pdf_regex/
├── agent_tools/              # 🔧 Development & debugging tools ✅
│   ├── field_dev.py          # Pattern discovery, context analysis & testing
│   ├── output_create.py      # Generate extraction results (all fields)
│   ├── output_check.py       # Analyze existing results (read-only)
│   └── enhanced_extractor.py # Multi-pattern extraction engine
├── user_tools/               # 👤 End-user pipeline tools ✅
├── config/                   # ⚙️ All configuration files
│   ├── extraction_patterns/  # Regex patterns for PDF extraction (20 companies)
│   └── mapping_rules/        # Data normalization mappings (5 companies complete)
├── mapping/                  # 🗺️ Data normalization system
│   └── mapping_engine.py     # Business logic transformation engine
├── data/                     # 📊 Data pipeline
│   ├── 00_raw_pdfs/          # Input: PDF files + markdown references
│   ├── 02_output/            # Extracted: Raw regex results
│   └── 03_mapped/            # Normalized: Standardized data
├── archive/                   # 🗃️ Utility tools
│   └── quick_csv2json.py     # CSV to mapping JSON converter
└── docs/                     # 📚 Documentation
    ├── FIELD_PATTERNS_GUIDE.md   # Field validation & troubleshooting reference
    └── AGENT_TOOLS.md            # This file - agent tool usage guide
```

### **📚 Documentation System**

**📖 This File (AGENT_TOOLS.md)**: Agent tool usage, development workflow, and technical methodology  
**🔍 FIELD_PATTERNS_GUIDE.md**: Field validation, pattern expectations, troubleshooting reference  
**📋 TODO Files**: Project status, company priorities, and detailed progress tracking  
**⚙️ config/README.md**: Configuration file structure and management
**👤 user_tools/README.md**: End-user pipeline tools and simple commands

> **Note**: This file contains **agent development tools** for internal use. For end-user tools, see `user_tools/` directory.

## 🚀 **Quick Start Guide**

### **First Commands for Any Session**
```bash
# 1. Check where you are - overall project status
python agent_tools/output_check.py --company allianz_E    # Check existing results
python agent_tools/output_check.py --company ak_E         # Check a working company

# 2. Identify what to work on next
ls TODO/                                       # See available company TODOs
cat TODO/TODO.md                              # Check project priorities

# 3. Pick a company and check current status  
python agent_tools/output_check.py --company target_company_E
```

### **"I Don't Know What Company to Work On"**
```bash
# Check which companies exist
ls data/00_raw_pdfs/                          # See all available companies
ls config/extraction_patterns/               # See which have extraction configurations
ls config/mapping_rules/                     # See which have mapping configurations

# Quick company assessment
python agent_tools/output_check.py --company company_E    # Check field completion rates
cat TODO/company_E_todo.md                    # See detailed status (if exists)

# Compare multiple companies at once
python agent_tools/output_check.py --company allianz_E ak_E turkiye_E  # Multi-company summary
```

### **"I Want to Improve a Specific Company"**
```bash
# 1. Check current status
python agent_tools/output_check.py --company target_E

# 2. Start with 0% fields (highest impact)
python agent_tools/field_dev.py --company target_E --field "Field_With_0_Percent"

# 3. Follow Phase 1-3 workflow below
# 4. After changes, regenerate results
python agent_tools/output_create.py --company target_E
```

## 🔄 **Agent Development Workflow**

### **Phase 1: Field Discovery** (Extraction)

#### **Step 1: Search for Field**
```bash
python agent_tools/field_dev.py --company target_company_E --field "Target_Field_Name"
```
**Purpose**: Find field occurrences across company PDFs  
**Output**: Context snippets showing where field appears

#### **Step 2: Analyze Context**
```bash
python agent_tools/field_dev.py --company target_company_E --field "Target_Field_Name" --context
```
**Purpose**: Line-based analysis with pattern suggestions  
**Output**: Surrounding lines + suggested regex patterns

#### **Step 3: Test Pattern**
```bash
python agent_tools/field_dev.py --company target_company_E --pattern "developed_regex_pattern"
```
**Purpose**: Validate regex across multiple PDFs  
**Output**: Success rate + sample matches

### **Phase 2: Pattern Implementation**

#### **Step 4: Update Configuration**
Manually edit `config/extraction_patterns/target_company_E.json`:

**Single Pattern (Standard)**
```json
{
  "Field_Name": {
    "pattern": "validated_regex_pattern",
    "group": 1,
    "description": "What this pattern extracts"
  }
}
```

**Multiple Patterns (Advanced)**
```json
{
  "Field_Name": {
    "patterns": [
      "primary_pattern",
      "fallback_pattern"
    ],
    "mode": "first"
  }
}
```

**List Collection (Multi-Value)**
```json
{
  "Field_Name": {
    "patterns": [
      "pattern_for_multiple_items"
    ],
    "mode": "all"
  }
}
```

### **Phase 3: Extraction Validation & Iteration**

#### **Step 5: Check Field Results**
```bash
# Single field
python agent_tools/output_check.py --company target_company_E --field "Field_Name"

# Multiple fields at once
python agent_tools/output_check.py --company target_company_E --field "Field_Name_1" "Field_Name_2" "Field_Name_3"
```
**Purpose**: Analyze existing results for specific field(s)  
**Output**: Success rate + sample values + failed cases for each field

#### **Step 6: Regenerate All Fields**
```bash
python agent_tools/output_create.py --company target_company_E
```
**Purpose**: Generate fresh extraction results after pattern changes  
**Output**: Complete JSON results + field success rates

#### **Step 7: Check Overall Status**
```bash
python agent_tools/output_check.py --company target_company_E
```
**Purpose**: View summary of all fields from existing data  
**Output**: Field success rates and completion statistics

#### **Step 8: Cross-Company Validation**
```bash
# Single field across multiple companies
python agent_tools/output_check.py --company allianz_E ak_E turkiye_E --field "Field_Name"

# Multiple fields across multiple companies  
python agent_tools/output_check.py --company allianz_E ak_E --field "Field_1" "Field_2" "Field_3"
```
**Purpose**: Validate field makes sense across companies  
**Output**: Comparison of field values and success rates

### **Phase 4: Data Normalization & Mapping**

#### **Step 9: Create Mapping Configuration**
```bash
# Create mapping rules for extracted data normalization
vim config/mapping_rules/target_company_E_map.json
```
**Purpose**: Define how to transform raw extracted data into standardized format
**Configuration**: JSON file with transformation rules
**Templates Available**: Use ak_E_map.json, allianz_E_map.json, etc. as templates

#### **Step 10: Test Data Mapping**
```bash
# Apply mapping to normalize data
python mapping/mapping_engine.py --input data/02_output/target_company_E.json --output data/03_mapped/target_company_E.json --config config/mapping_rules/target_company_E_map.json
```
**Purpose**: Transform raw extraction results into normalized, standardized format
**Output**: Standardized data ready for business intelligence
**Status**: Working for ak_E, allianz_E, anadolu_E, ankara_E, axa_E

#### **Step 11: Validate Mapping Results**
```bash
# Check mapped data output files
ls data/03_mapped/target_company_E.json
```
**Purpose**: Verify mapping produced output files
**Alternative**: Use user_tools/process_pipeline.py for end-to-end processing

## 🎯 **Field Development Strategy**

### **Priority Assessment**
1. **Check current status**: `python agent_tools/output_check.py --company target_E`
2. **Focus on 0% fields**: Highest impact improvements
3. **Target 80%+ success rate**: Quality threshold for production
4. **After changes**: `python agent_tools/output_create.py --company target_E` to regenerate

### **Search Methodology**
1. **Markdown Analysis**: `cat data/00_raw_pdfs/company_E/*.md` - understand document structure
2. **Field Name Search**: Use Turkish field names (e.g., "Poliçe No", "Araç Markası")
3. **Value-Based Search**: If field names fail, search for expected values
4. **Context Mapping**: Analyze sections between known fields

### **Pattern Development**
1. **Start Simple**: Basic field extraction first
2. **Add Complexity**: Handle edge cases and variations
3. **Test Thoroughly**: Validate across all company PDFs
4. **Cross-Validate**: Compare with similar companies

## 📝 **Configuration Flexibility**

### **Supported Modes**

#### **Single Pattern (Legacy Compatible)**
```json
{
  "Police_No": {
    "pattern": "Policy\\s*No[:\\s]*([0-9-]+)",
    "group": 1
  }
}
```

#### **First Match (Multiple Fallbacks)**
```json
{
  "Police_No": {
    "patterns": [
      "Policy\\s*No[:\\s]*([0-9-]+)",
      "Pol[:\\s]*([A-Z0-9-]+)"
    ],
    "mode": "first"
  }
}
```

#### **All Matches (List Collection)**
```json
{
  "All_Coverages": {
    "patterns": [
      "Coverage[:\\s]*([^\\n]+)"
    ],
    "mode": "all"
  }
}
```

### **Output Examples**

**Single Value**
```json
{
  "Police_No": {
    "doc1": "12345-67890",
    "doc2": "ABC-123456"
  }
}
```

**List Values**
```json
{
  "All_Coverages": {
    "doc1": ["Coverage A", "Coverage B", "Coverage C"],
    "doc2": ["Coverage X", "Coverage Y"]
  }
}
```

## 🔍 **Common Field Patterns**

### **Policy Information**
- **Policy Numbers**: `"Poliçe No[:\\s]*([0-9-]+)"`
- **Dates**: `"Başlangıç.*?([0-9]{2}/[0-9]{2}/[0-9]{4})"`
- **Previous Policy**: `"Önceki.*?Poliçe.*?([0-9-]+)"`

### **Customer Information**
- **TC Numbers**: `"TC.*?Kimlik.*?([0-9\\*]+)"` (often masked)
- **Names**: `"Sigortalı.*?Ad.*?([^\\n]+)"`
- **Addresses**: `"Adres[:\\s]*([^\\n]+(?:\\n[^A-Z][^\\n]*)*)"` (multiline)

### **Vehicle Information**  
- **License Plates**: `"Plaka[:\\s]*([0-9]{2}\\s*[A-Z]+\\s*[0-9]+)"`
- **Engine Numbers**: `"Motor.*?No[:\\s]*([A-Z0-9]+)"`
- **Vehicle Types**: `"Araç.*?Tip[:\\s]*([^\\n]+(?:\\n[^A-Z][^\\n]*)*)"` (multiline)

### **Coverage Information**
- **Coverage Amounts**: `"Teminat.*?([0-9,\\.]+\\s*TL)"`
- **Coverage Status**: `"(Dahil|Hariç|[0-9,\\.]+\\s*TL)"`
- **Discount Info**: `"([0-9]+\\.yıl.*?[%0-9]+.*?indirim)"`

## 🚀 **Development Examples**

### **Example 1: New Field Development**
```bash
# 1. Search field
python agent_tools/field_dev.py --company turkiye_E --field "Araç Markası"

# 2. Analyze context  
python agent_tools/field_dev.py --company turkiye_E --field "Araç Markası" --context

# 3. Test pattern
python agent_tools/field_dev.py --company turkiye_E --pattern "Araç Markası[:\\s]*\\n([^\\n]+)"

# 4. Edit config: config/extraction_patterns/turkiye_E.json
{
  "Arac_Marka_Tip": {
    "pattern": "Araç Markası[:\\s]*\\n([^\\n]+)",
    "group": 1
  }
}

# 5. Regenerate and validate results
python agent_tools/output_create.py --company turkiye_E
python agent_tools/output_check.py --company turkiye_E --field "Arac_Marka_Tip"
```

### **Example 2: Multi-Pattern Field (Complex Coverage)**
```bash
# 1. Search basic coverage
python agent_tools/field_dev.py --company allianz_E --field "Cam Kırılması"

# 2. Search detailed terms
python agent_tools/field_dev.py --company allianz_E --field "CAM KIRILMASI TEMİNATI"

# 3. Test combined pattern
python agent_tools/field_dev.py --company allianz_E --pattern "(Cam Kırılması\\s*\\nDahil)|(CAM KIRILMASI TEMİNATI[\\s\\S]*?uygulanmamaktadır)"

# 4. Configure for all matches
{
  "Teminat_Oto_Cam_Klozu": {
    "patterns": [
      "(Cam Kırılması\\s*\\n(?:Dahil|[0-9,\\.]+\\s*TL))",
      "(CAM KIRILMASI TEMİNATI\\s*\\nCam hasarına ilişkin[^.]+\\.)",
      "(Cam hasarlarında Allianz[\\s\\S]*?sınırlı olacaktır\\.)"
    ],
    "mode": "all"
  }
}

# 5. Regenerate and check results show list of all patterns  
python agent_tools/output_create.py --company allianz_E
python agent_tools/output_check.py --company allianz_E --field "Teminat_Oto_Cam_Klozu"
```

### **Example 3: Multiple TEMINAT Fields**
```bash
# Single company, multiple TEMINAT fields
python agent_tools/output_check.py --company allianz_E --field "Teminat_Oto_Cam_Klozu" "Teminat_IMM_Bedeni_Maddi_Ayrimsiz_Bedeli" "Teminat_Ikame_Arac"

# Cross-company TEMINAT field analysis
python agent_tools/output_check.py --company allianz_E ak_E turkiye_E anadolu_E --field "Teminat_Hasar_Kademesi_Bilgisi"

# Multiple companies, multiple TEMINAT fields
python agent_tools/output_check.py --company allianz_E ak_E --field "Teminat_Hasar_Kademesi_Bilgisi" "Teminat_Oto_Cam_Klozu"
```

### **Example 4: Cross-Company TEMINAT Analysis**
```bash
python agent_tools/output_check.py --company allianz_E ak_E turkiye_E anadolu_E --field "Teminat_Hasar_Kademesi_Bilgisi"
python agent_tools/output_check.py --company allianz_E ak_E --field "Teminat_Oto_Cam_Klozu" "Teminat_Ikame_Arac"
```

## 🎯 **Quality Guidelines**

### **Success Rate Targets**
- **✅ Excellent**: 95%+ success rate
- **✅ Good**: 80-95% success rate  
- **⚠️ Needs Work**: 60-80% success rate
- **❌ Failed**: <60% success rate

### **Pattern Quality Checks**
1. **Consistency**: Works across all company PDFs
2. **Accuracy**: Extracts correct values, not surrounding text
3. **Completeness**: Captures all variations of the field
4. **Robustness**: Handles edge cases and formatting differences

### **Field Validation**
1. **Business Logic**: Extracted values make sense
2. **Cross-Company**: Similar fields have similar value patterns
3. **Format Consistency**: Dates, numbers, text follow expected formats
4. **Missing Data**: Understand why some PDFs fail extraction

## 📋 **Iterative Development Process**

### **Single Field Development Cycle**
1. **Search** → Find field locations
2. **Context** → Understand surrounding structure  
3. **Pattern** → Develop and test regex
4. **Configure** → Update JSON config
5. **Validate** → Check results quality
6. **Iterate** → Refine until 80%+ success
7. **Cross-Check** → Compare with other companies
8. **Next Field** → Move to next 0% field

### **Company Development Cycle**
1. **Overview** → Check current field completion rates
2. **Prioritize** → Focus on 0% fields first, then low-success fields
3. **Markdown** → Review document structure and field locations
4. **Develop** → Apply single field cycle to each target field
5. **Validate** → Generate full company results
6. **Quality** → Ensure 80%+ average success rate
7. **Complete** → Move to next company

### **Decision Points**
- **Pattern Success ≥80%**: Move to next field
- **Pattern Success 60-80%**: Try to improve or accept
- **Pattern Success <60%**: Rethink approach or mark as unavailable
- **Field Not Found**: Try variations, value-based search, or mark unavailable
- **Field Inconsistent**: Consider multiple patterns or document limitations

## 🛠️ **Troubleshooting Guide**

### **Common Issues**

#### **Field Not Found**
```bash
# Try variations
python agent_tools/field_dev.py --company company_E --field "Police No"
python agent_tools/field_dev.py --company company_E --field "Poliçe"
python agent_tools/field_dev.py --company company_E --field "Policy"
```

#### **Pattern Fails**
```bash
# Test with simpler pattern
python agent_tools/field_dev.py --company company_E --pattern "simplified_pattern"

# Check for special characters
python agent_tools/field_dev.py --company company_E --pattern "pattern\\.with\\.escaped\\.dots"
```

#### **Low Success Rate**
```bash
# Check failed cases
python agent_tools/output_check.py --company company_E --field "Field_Name"
# Look at failed document names, find pattern

# Test pattern on specific failed PDF
python agent_tools/field_dev.py --company company_E --field "Field_Name" --context --max-files 1
```

### **Pattern Development Tips**

#### **Multiline Fields**
```regex
# Vehicle types often span multiple lines
"Araç Tipi\\s*\\n([^\\n]+(?:\\n[^A-Z][^\\n]*)*)"
```

#### **Optional Content**
```regex
# Some fields may have optional parts
"Field Name[:\\s]*([^\\n]+)(?:\\nOptional Part)?"
```

#### **Line-Based Issues**
```bash
# Use context analysis for alignment problems
python agent_tools/field_dev.py --company company_E --field "Field_Name" --context --lines-before 5 --lines-after 5
```

#### **Section Boundary Issues**
```bash
# Problem: Pattern bleeds into next section
# Solution: Use lookahead to stop at next heading

# Test current pattern
python agent_tools/field_dev.py --company company_E --field "SECTION_HEADING" --context --lines-after 8

# Add boundary detection for Turkish all-caps headings
python agent_tools/field_dev.py --company company_E --pattern "(HEADING\\s*\\n[^\\n]+)(?=\\s*\\n[A-ZÇĞIJKLMNOPRSŞTUÜVYZ]{3,})"

# Reference FIELD_PATTERNS_GUIDE.md for boundary pattern examples
```

## 📊 **Success Metrics**

### **Company Progress Tracking**
- **Field Completion**: % of fields with ≥80% success rate
- **Average Success**: Average success rate across working fields
- **PDF Coverage**: % of PDFs successfully processed
- **Quality Score**: Weighted score based on field importance

### **Project Progress**
- **Companies Completed**: Companies with ≥80% field completion
- **Total Field Coverage**: Fields working across all companies
- **Cross-Company Consistency**: Same fields working similarly
- **Critical Field Status**: High-priority fields (Policy, Customer, Vehicle)

## 🎉 **System Benefits**

- ✅ **Simple Workflow**: Only 2 tools, clear linear process
- ✅ **Flexible Patterns**: Single, multiple, or list collection modes
- ✅ **Quality Focus**: Built-in success rate tracking and validation
- ✅ **Cross-Company**: Easy comparison and validation across companies
- ✅ **Iterative**: Clear decision points and improvement cycles
- ✅ **Context-Efficient**: Focused output relevant to current task
- ✅ **Production Ready**: 80%+ success threshold for reliable extraction

This streamlined system eliminates complexity while providing powerful pattern development capabilities and clear quality metrics for reliable insurance PDF data extraction.

---

## 🗺️ **Data Mapping & Normalization**

### **Pipeline Architecture**
```
Raw PDFs → (extraction) → 02_output/ → (mapping) → 03_mapped/
```

### **Mapping Rules Configuration**
```json
{
  "company": "allianz_E",
  "field_mappings": {
    "Teminat_Yedek_Parca": {
      "type": "pattern_to_value",
      "mappings": [
        {"input_pattern": "orijinal parçalar kullanılır", "output": "Var"},
        {"input_pattern": null, "output": ""}
      ]
    }
  }
}
```

### **Null Handling Behavior**
- **Default**: `null` values remain `null` (preserved)  
- **Explicit Mapping**: Use `"input_pattern": null` to map `null → ""`
- **No Mapping Config**: Original values preserved unchanged

### **CSV to JSON Converter**
```bash
python archive/quick_csv2json.py  # Generates mapping files from reference CSVs
```
- Creates `config/mapping_rules/{company}_map.json` from `docs/{Company}_mapping.csv`
- Handles null mappings: empty `regexed_value` → `null` input pattern
- Generates business logic transformations from reference data