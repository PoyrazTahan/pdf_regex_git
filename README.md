# Turkish Insurance PDF Data Extraction System

## 🎯 **Overview**

Comprehensive system for extracting and normalizing structured data from Turkish insurance policy PDFs across 20+ insurance companies. Processes ~30 standardized fields per company with high accuracy using regex patterns and data normalization.

## 👥 **For Different Users**

### **🔧 Agent/Developer Tools**
**For internal development, pattern creation, and debugging:**
- 📖 **[Agent Tools Guide](docs/AGENT_TOOLS.md)** - Complete development workflow and tool usage
- 🔧 **[Agent Tools Directory](agent_tools/README.md)** - Development tool reference
- 🔍 **[Field Patterns Guide](docs/FIELD_PATTERNS_GUIDE.md)** - Field validation and troubleshooting reference
- ⚙️ **[Config Management](config/README.md)** - Configuration file structure and management

### **👤 End-User Tools** ✅
**For simple, production-ready data processing:**
- 📋 **[User Tools Guide](user_tools/README.md)** - Simple commands for data extraction and normalization  
- 🚀 **Quick Start**: `python user_tools/process_pipeline.py --visualize`
- 📊 **Dashboard**: Interactive visualization at `data/static_dashboard.html`

## 🏗️ **System Architecture**

```
pdf_regex/
├── user_tools/                     # 👤 End-user pipeline tools
├── agent_tools/                    # 🔧 Internal development & debugging  
├── config/                         # ⚙️ All configuration files
│   ├── extraction_patterns/        # Regex patterns (20 companies)
│   └── mapping_rules/              # Data normalization rules
├── mapping/                        # 🗺️ Data normalization system
├── data/                           # 📊 Data pipeline
│   ├── 00_raw_pdfs/               # Input: PDF files
│   ├── 02_output/                 # Extracted: Raw data
│   └── 03_mapped/                 # Normalized: Standardized data
└── docs/                          # 📚 Documentation
```

## 📊 **Current Status**

### **Extraction (Phase 1)**
- ✅ **20 Companies**: Complete regex patterns for all major Turkish insurers
- ✅ **~30 Fields**: Policy info, customer data, vehicle details, coverage information
- ✅ **High Accuracy**: 80%+ success rates for production fields

### **Normalization (Phase 2)**
- ✅ **5 Companies Complete**: AK, Allianz, Anadolu, Ankara, AXA fully mapped and validated
- ✅ **System Architecture**: Scalable mapping engine ready for all companies
- 🚧 **15 Companies Pending**: Template ready for rapid expansion

### **Companies Supported**
- AK Sigorta, Allianz, Anadolu, Ankara, AXA, Doğa, Gulf, HDI, MAPFRE, MG
- Neova, Orient, Quick, Ray, Sompo, Türkiye, Türkiye Katılım, Türk Nippon, Unico, Zurich

## 🚀 **Quick Examples**

### **Agent Development**
```bash
# Pattern development and testing
python agent_tools/field_dev.py --company ak_E --field "Policy_Number"
python agent_tools/output_create.py --company ak_E

# Data normalization  
python mapping/mapping_engine.py --input data/02_output/ak_E.json --output data/03_mapped/ak_E.json --config config/mapping_rules/ak_E_map.json
```

### **End-User**
```bash
# Complete pipeline with dashboard
python user_tools/process_pipeline.py --visualize

# Process specific company
python user_tools/process_pipeline.py --company ak_E

# Dashboard output: data/static_dashboard.html (self-contained)
```

## 📈 **Data Processing Pipeline**

1. **📄 Input**: Turkish insurance policy PDFs + metadata
2. **🔍 Extraction**: Regex-based structured data extraction  
3. **🗺️ Normalization**: Transform to standardized business format
4. **📊 Output**: Clean, consistent data ready for analysis

## 🎯 **Key Features**

- **Multi-Pattern Support**: Fallback hierarchies for robust extraction
- **Turkish Language**: Specialized handling of Turkish characters and formats
- **Business Logic**: Intelligent mapping of complex insurance terms
- **Quality Assurance**: Built-in validation and error reporting
- **Scalable Architecture**: Easy to add new companies and fields

## 📚 **Documentation**

- **[Agent Tools Guide](docs/AGENT_TOOLS.md)** - Complete development workflow
- **[Field Patterns Reference](docs/FIELD_PATTERNS_GUIDE.md)** - Field expectations and troubleshooting
- **[Configuration Guide](config/README.md)** - Config file management
- **[Mapping System](docs/MAPPING_DISCUSSION.md)** - Data normalization architecture
- **[Project Reorganization](docs/REORGANIZATION_PLAN.md)** - System architecture planning

## 🛠️ **Development Status**

This is an active development project with continuous improvements to:
- Pattern accuracy and coverage
- New company integration
- Data normalization quality
- User experience and tooling

**Current Focus**: Scaling data normalization to all 20 companies and building user-friendly interfaces.