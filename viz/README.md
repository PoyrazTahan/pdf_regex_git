# 📊 Dashboard Visualization System

Clean, modular dashboard generation system for Turkish insurance PDF data analysis with proper separation of concerns.

## 🏗️ **Simplified Architecture**

### **Clean Modular Design**
```
viz/
├── dashboard.py          # 🎯 Main entry point with modes
├── dashboard_data.py     # 📊 Data loading logic  
├── dashboard_html.py     # 🎨 HTML generation logic
└── README.md             # 📚 Documentation
```

**Three-Layer Architecture:**
- **Entry Point** (`dashboard.py`): Command-line interface and coordination
- **Data Layer** (`dashboard_data.py`): Pure data loading and processing
- **Presentation Layer** (`dashboard_html.py`): Pure HTML/CSS/JavaScript generation

## 🚀 **Usage**

### **Single Entry Point**
```bash
# Generate individual dashboards
python viz/dashboard.py regex                    # Regex pattern analysis
python viz/dashboard.py mapped                   # Mapped data analysis

# Generate both dashboards
python viz/dashboard.py both                     # Generate both at once

# Custom output filename
python viz/dashboard.py regex -o my_patterns.html

# Verbose mode
python viz/dashboard.py both -v

# Help
python viz/dashboard.py --help
```

## 📋 **Dashboard Types**

### **1. Regex Dashboard** (`static_dashboard.html`)
- **Command**: `python viz/dashboard.py regex`
- **Data Source**: `02_output/` (raw extraction results)
- **Config Source**: `extraction_patterns/` (regex patterns)  
- **Color Scheme**: Blue gradient with Teminat vs Other field differentiation
- **Purpose**: Pattern development and extraction validation
- **Size**: ~689KB (20 companies, all extraction data)

### **2. Mapped Dashboard** (`static_map_dashboard.html`)
- **Command**: `python viz/dashboard.py mapped`
- **Data Source**: `03_mapped/` (business logic results)
- **Config Source**: `mapping_rules/` (transformation rules)
- **Color Scheme**: Green gradient (success-focused)
- **Purpose**: Business intelligence validation
- **Size**: ~244KB (5 companies with mapping configs)

## 🎯 **Key Features**

### **✅ Clean Architecture**
- **Single Responsibility**: Each module has one clear job
- **Separation of Concerns**: Data loading completely separate from HTML generation
- **Easy to Extend**: Add new dashboard modes by extending both data and HTML layers

### **✅ Simple Interface**
- **One Command**: `python viz/dashboard.py [mode]`
- **Clear Modes**: `regex`, `mapped`, or `both`
- **Helpful Options**: Custom output, verbose mode, built-in help

### **✅ Fixed Data Display**
- **No N/M Placeholders**: Always shows actual data when available
- **Clear Indicators**: Tooltips show "with mapping rules" vs "raw regex values"
- **Complete Transparency**: Full visibility into data transformation pipeline

### **✅ Optimized Codebase**
- **Total Lines**: ~1150 lines across 3 focused modules
- **Maintainable**: Edit data logic or HTML templates independently
- **Testable**: Clear interfaces make unit testing straightforward

## 🔧 **Module Details**

### **dashboard.py** (~100 lines)
```python
# Entry point with argument parsing and coordination
def generate_dashboard(mode: str, output_file: str = None) -> str
def main():  # Handles argparse, validates modes, coordinates execution
```

### **dashboard_data.py** (~150 lines)  
```python
# Pure data loading logic
class DataLoader:
    def load_data(self, mode: str) -> DashboardData
    def _load_regex_data(self) -> DashboardData      # 02_output + extraction_patterns
    def _load_mapped_data(self) -> DashboardData     # 03_mapped + mapping_rules

@dataclass  
class DashboardData:  # Clean data container
    primary_data: Dict[str, Any]      # Main dataset (output or mapped)
    secondary_data: Dict[str, Any]    # Config data (patterns or mapping rules)  
    companies: List[str]              # Valid companies
    fields: List[str]                 # All available fields
    mode: str                         # 'regex' or 'mapped'
    stats: Dict[str, Any]            # Summary statistics
```

### **dashboard_html.py** (~900 lines)
```python
# Pure HTML/CSS/JavaScript generation
class HTMLGenerator:
    def generate_dashboard(self, data: DashboardData, output_path: str) -> str
    def _get_mode_config(self, mode: str) -> Dict[str, Any]      # Mode-specific settings
    def _generate_html_template(...) -> str                      # Complete HTML structure
    def _generate_css(...) -> str                                # Responsive CSS + color schemes
    def _generate_javascript(...) -> str                         # Interactive functionality
```

## 📊 **Color Schemes & Behavior**

### **Regex Dashboard (Blue Theme)**
- **Teminat Fields**: Orange gradient for <50%, blue gradient for ≥50%
- **Other Fields**: Orange gradient for 60-99%, white for 1-59%  
- **N/A Fields**: Gray italic (non-applicable fields)
- **JavaScript**: `Dashboard` class with regex-specific logic

### **Mapped Dashboard (Green Theme)**
- **All Fields**: Unified green success gradient
- **Data Policy**: Shows all available data - no N/M placeholders
- **Mapping Status**: Clear tooltips indicate transformation source
- **JavaScript**: `MappedDashboard` class with mapping-specific logic

## 🎉 **Benefits**

### **For Development**
- **Focused Editing**: Change data loading without touching HTML
- **Easy Debugging**: Clear module boundaries make issues easy to trace
- **Consistent Interface**: Single command for all dashboard operations

### **For Business Intelligence**
- **No Confusion**: Always see actual data, never placeholders
- **Clear Status**: Know exactly when you're seeing transformed vs raw values
- **Complete Visibility**: Full transparency in data transformation pipeline

### **For Maintenance**
- **Simple Structure**: Only 4 files total
- **Clear Responsibilities**: Each module has obvious purpose
- **Easy Extension**: Well-defined interfaces for adding new features

## 🔄 **Data Flow**

```
Raw PDFs → (extraction) → 02_output/ → (mapping) → 03_mapped/
            ↓                         ↓
    dashboard.py regex           dashboard.py mapped
    (Pattern development)        (Business validation)
```

**Generated Files:**
- `data/static_dashboard.html` (689KB) - Regex pattern analysis
- `data/static_map_dashboard.html` (244KB) - Mapped data analysis

Both files are **completely self-contained** with no external dependencies!

## 🚀 **Quick Reference**

```bash
# Most common usage
python viz/dashboard.py both                     # Generate both dashboards
python viz/dashboard.py regex                    # Pattern development  
python viz/dashboard.py mapped                   # Business validation

# Advanced usage
python viz/dashboard.py regex -o patterns.html   # Custom filename
python viz/dashboard.py both -v                  # Verbose output
python viz/dashboard.py --help                   # Full help text
```

## 📏 **Code Metrics**

| **Module** | **Lines** | **Purpose** | **Dependencies** |
|---|---|---|---|
| `dashboard.py` | ~100 | Entry point & coordination | `dashboard_data`, `dashboard_html` |
| `dashboard_data.py` | ~150 | Data loading & processing | Standard library only |
| `dashboard_html.py` | ~900 | HTML/CSS/JS generation | `dashboard_data` types |
| **Total** | **~1150** | **Complete system** | **Minimal external deps** |

The simplified architecture is **clean, maintainable, and powerful** with maximum functionality in minimum complexity! 🎉