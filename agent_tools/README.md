# Agent Tools - Development & Debugging

This directory contains internal development tools for creating and maintaining regex patterns for Turkish insurance policy PDF extraction. These tools are used by developers and agents to build patterns, analyze extraction quality, and debug issues.

## 🔧 **Tools Overview**

### **Core Tools**
- **enhanced_extractor.py** - Multi-pattern extraction engine
- **field_dev.py** - Pattern discovery and testing tool  
- **output_create.py** - Generate extraction results for all company fields
- **output_check.py** - Analyze and validate extraction results

## 📋 **Quick Reference**

### **Field Development Workflow**
```bash
# 1. Search for field occurrences
python agent_tools/field_dev.py --company ak_E --field "Target_Field_Name"

# 2. Analyze context and get pattern suggestions  
python agent_tools/field_dev.py --company ak_E --field "Target_Field_Name" --context

# 3. Test developed pattern
python agent_tools/field_dev.py --company ak_E --pattern "developed_regex_pattern"

# 4. Generate extraction results
python agent_tools/output_create.py --company ak_E

# 5. Check field quality
python agent_tools/output_check.py --company ak_E --field "Target_Field_Name"
```

### **Quality Analysis**
```bash
# Check company extraction status
python agent_tools/output_check.py --company ak_E

# Compare field across companies
python agent_tools/output_check.py --company ak_E allianz_E turkiye_E --field "Police_No"

# Check multiple fields
python agent_tools/output_check.py --company ak_E --field "Police_No" "Sigortali_Adi" "Arac_Plaka_No"
```

## 🎯 **Tool Details**

### **field_dev.py** - Pattern Development
Primary tool for developing extraction patterns.

**Key Features:**
- Field occurrence search across PDFs
- Context analysis with pattern suggestions
- Pattern testing and validation
- Multi-file support for comprehensive testing

**Usage Examples:**
```bash
# Search field in company PDFs
python agent_tools/field_dev.py --company turkiye_E --field "Araç Markası"

# Get context analysis
python agent_tools/field_dev.py --company turkiye_E --field "Araç Markası" --context

# Test pattern
python agent_tools/field_dev.py --company turkiye_E --pattern "Araç Markası[:\\s]*\\n([^\\n]+)"
```

### **output_create.py** - Batch Extraction
Generates extraction results for all configured fields in a company.

**Usage:**
```bash
# Generate all fields for a company
python agent_tools/output_create.py --company ak_E

# Custom output directory
python agent_tools/output_create.py --company ak_E --output-dir custom_output/
```

**Output:** JSON file in `data/02_output/company_E.json`

### **output_check.py** - Quality Analysis
Analyzes existing extraction results for quality and completeness.

**Usage:**
```bash
# Company overview
python agent_tools/output_check.py --company ak_E

# Specific field analysis
python agent_tools/output_check.py --company ak_E --field "Police_No"

# Cross-company comparison
python agent_tools/output_check.py --company ak_E allianz_E --field "Police_No"
```

### **enhanced_extractor.py** - Core Engine
The underlying extraction engine supporting multiple pattern configurations.

**Pattern Types Supported:**
- Single patterns with capture groups
- Multiple patterns with fallback hierarchy
- List collection patterns for multi-value fields

**Configuration Examples:**
```json
{
  "Single_Pattern": {
    "pattern": "Field[:\\s]*([^\\n]+)",
    "group": 1
  },
  "Multiple_Patterns": {
    "patterns": ["primary_pattern", "fallback_pattern"],
    "mode": "first"
  },
  "List_Collection": {
    "patterns": ["item_pattern"],
    "mode": "all"
  }
}
```

## 🎯 **Development Workflow**

### **New Field Development**
1. **Search**: Find field occurrences in PDFs
2. **Analyze**: Study context and patterns
3. **Develop**: Create regex pattern
4. **Test**: Validate across multiple PDFs
5. **Configure**: Add to company config file
6. **Validate**: Generate and check results
7. **Iterate**: Refine until 80%+ success rate

### **Quality Assurance**
1. **Regenerate**: Fresh extraction after pattern changes
2. **Validate**: Check success rates and sample values
3. **Cross-Check**: Compare similar fields across companies
4. **Document**: Update patterns and troubleshooting notes

### **Troubleshooting**
1. **Low Success**: Use context analysis to understand failures
2. **Pattern Issues**: Test simpler patterns and build complexity
3. **Edge Cases**: Analyze failed documents for pattern improvements
4. **Cross-Company**: Validate patterns work across similar companies

## 📊 **Success Metrics**

### **Quality Thresholds**
- **✅ Excellent**: 95%+ success rate
- **✅ Good**: 80-95% success rate  
- **⚠️ Needs Work**: 60-80% success rate
- **❌ Failed**: <60% success rate

### **Development Targets**
- **Field Completion**: 80%+ of fields working at good/excellent level
- **Company Coverage**: Patterns working across all company PDFs
- **Pattern Quality**: Robust handling of formatting variations
- **Documentation**: Clear pattern descriptions and troubleshooting notes

## 🔍 **Advanced Usage**

### **Pattern Development Tips**
```bash
# Handle multiline fields
python agent_tools/field_dev.py --company company_E --pattern "Field.*\\n([^\\n]+(?:\\n[^A-Z][^\\n]*)*)"

# Test with specific PDF count
python agent_tools/field_dev.py --company company_E --field "Field" --max-files 3

# Context analysis with extended range
python agent_tools/field_dev.py --company company_E --field "Field" --context --lines-before 5 --lines-after 5
```

### **Batch Operations**
```bash
# Process multiple companies
for company in ak_E allianz_E turkiye_E; do
  python agent_tools/output_create.py --company $company
done

# Generate reports for all companies
python agent_tools/output_check.py --company ak_E allianz_E anadolu_E ankara_E axa_E
```

## 📚 **Related Documentation**

- **[Agent Tools Guide](../docs/AGENT_TOOLS.md)** - Complete development workflow
- **[Field Patterns Guide](../docs/FIELD_PATTERNS_GUIDE.md)** - Pattern validation reference
- **[Configuration Guide](../config/README.md)** - Config file management
- **[User Tools](../user_tools/README.md)** - End-user interfaces

## ⚠️ **Important Notes**

- These tools are for **internal development only**
- End users should use **user_tools/** directory instead
- Always test patterns across multiple PDFs before deployment
- Maintain 80%+ success rate threshold for production patterns
- Document complex patterns and edge cases for future maintenance