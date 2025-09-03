#!/usr/bin/env python3
"""
HTML template generation module for dashboards.
Handles all HTML, CSS, and JavaScript generation.
"""

import json
from typing import Dict, Any
from dashboard_data import DashboardData


class HTMLGenerator:
    """Generates HTML templates for dashboards."""
    
    def generate_dashboard(self, data: DashboardData, output_path: str) -> str:
        """Generate complete HTML dashboard."""
        
        # Get configuration based on mode
        config = self._get_mode_config(data.mode)
        
        # Generate HTML content
        html_content = self._generate_html_template(data, config)
        
        # Write to file
        self._save_html(html_content, output_path)
        
        return html_content
    
    def _get_mode_config(self, mode: str) -> Dict[str, Any]:
        """Get configuration based on dashboard mode."""
        if mode == "regex":
            return {
                'title': 'PDF Regex Pattern Analysis Dashboard',
                'subtitle': 'Interactive visualization of field extraction success rates across insurance companies',
                'header_gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                'accent_color': '#007bff',
                'stats_bg': '#e7f3ff',
                'stats_border': '#b3d7ff',
                'text_color': '#007bff',
                'primary_section': 'PATTERN',
                'primary_title': 'Regex Patterns',
                'values_title': 'Extracted Values',
                'matrix_title': 'Field Success Rate Matrix',
                'matrix_desc': 'Success percentage for each field across companies (click cell for details)',
                'dashboard_desc': 'Green = completed (all 100% or N/A)',
                'color_scheme': 'regex',
                'js_class': 'Dashboard'
            }
        else:  # mapped
            return {
                'title': 'PDF Mapped Data Analysis Dashboard',
                'subtitle': 'Interactive visualization of business logic mapping results across insurance companies',
                'header_gradient': 'linear-gradient(135deg, #28a745 0%, #20c997 100%)',
                'accent_color': '#28a745',
                'stats_bg': '#d4edda',
                'stats_border': '#c3e6cb',
                'text_color': '#155724',
                'primary_section': 'MAPPING',
                'primary_title': 'Business Logic Rules',
                'values_title': 'Mapped Values',
                'matrix_title': 'Field Mapping Success Matrix',
                'matrix_desc': 'Success percentage for mapped fields across companies (click cell for details)',
                'dashboard_desc': 'Shows results from 03_mapped/ with business logic transformations',
                'color_scheme': 'mapped',
                'js_class': 'MappedDashboard'
            }
    
    def _generate_html_template(self, data: DashboardData, config: Dict[str, Any]) -> str:
        """Generate the complete HTML template."""
        
        # Prepare data for embedding
        primary_json = json.dumps(data.primary_data, ensure_ascii=False, indent=2)
        secondary_json = json.dumps(data.secondary_data, ensure_ascii=False, indent=2)
        companies_json = json.dumps(data.companies)
        fields_json = json.dumps(data.fields)
        
        # Get CSS and JS
        css_content = self._generate_css(config)
        js_content = self._generate_javascript(config)
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{config['title']}</title>
    <style>
{css_content}
    </style>
</head>
<body>
    <div class="header">
        <h1>{config['title']}</h1>
        <p>{config['subtitle']}</p>
        <div class="header-info">
            <div class="generated-info">
                <strong>[REPORT] Dashboard Info:</strong><br>
                Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}<br>
                Companies: {len(data.companies)} | Fields: {len(data.fields)}<br>
                [SUCCESS] {config['dashboard_desc']}
            </div>
            <div class="color-legend">
                <strong>[STYLE] Color Scheme:</strong><br>
                {self._get_legend_html(config['color_scheme'])}
            </div>
        </div>
    </div>

    <div class="main-container">
        <div class="matrix-section">
            <div class="matrix-header">
                <h2>[TARGET] {config['matrix_title']}</h2>
                <p>{config['matrix_desc']}</p>
            </div>
            <div class="matrix-container">
                <table class="matrix-table" id="matrixTable">
                    <thead>
                        <tr id="matrixHeader">
                            <th class="field-header">Field Name</th>
                        </tr>
                    </thead>
                    <tbody id="matrixBody">
                    </tbody>
                </table>
            </div>
        </div>

        <div class="side-panel">
            <div class="filter-section">
                <h3>[FILTER] Filters</h3>
                
                <div class="filter-group">
                    <label for="companyFilter">Company:</label>
                    <select id="companyFilter" class="filter-select">
                        <option value="">All Companies</option>
                    </select>
                </div>

                <div class="filter-group">
                    <label for="fieldFilter">Field:</label>
                    <select id="fieldFilter" class="filter-select">
                        <option value="">All Fields</option>
                    </select>
                </div>

                <div class="stats-info" id="statsInfo">
                    Select filters to view detailed information
                </div>
            </div>

            <div class="primary-section">
                <div class="section-header">
                    <h3>[{config['primary_section']}] {config['primary_title']}</h3>
                </div>
                <div class="section-content" id="primaryContent">
                    <div class="no-data">Select a field to view {config['primary_title'].lower()}</div>
                </div>
            </div>

            <div class="values-section">
                <div class="section-header">
                    <h3>[VALUES] {config['values_title']}</h3>
                </div>
                <div class="section-content" id="valuesContent">
                    <div class="no-data">Select a field to view values</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const EMBEDDED_PRIMARY_DATA = {primary_json};
        const EMBEDDED_SECONDARY_DATA = {secondary_json};
        const EMBEDDED_COMPANIES = {companies_json};
        const EMBEDDED_FIELDS = {fields_json};
        const DASHBOARD_MODE = "{data.mode}";

{js_content}

        // Initialize dashboard when page loads
        document.addEventListener('DOMContentLoaded', () => {{
            new {config['js_class']}();
        }});
    </script>
</body>
</html>"""
    
    def _generate_css(self, config: Dict[str, Any]) -> str:
        """Generate CSS styles."""
        color_classes = self._get_color_classes(config['color_scheme'])
        
        return f"""        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }}

        .header {{
            background: {config['header_gradient']};
            color: white;
            padding: 1rem;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .main-container {{
            display: flex;
            flex: 1;
            gap: 10px;
            padding: 10px;
            overflow: hidden;
        }}

        .matrix-section {{
            flex: 2;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }}

        .matrix-header {{
            background: #f8f9fa;
            padding: 15px;
            border-bottom: 1px solid #e9ecef;
        }}

        .matrix-container {{
            flex: 1;
            overflow: auto;
            position: relative;
        }}

        .matrix-table {{
            border-collapse: separate;
            border-spacing: 0;
            min-width: 100%;
        }}

        .matrix-table th,
        .matrix-table td {{
            border: 1px solid #dee2e6;
            padding: 8px 12px;
            text-align: center;
            white-space: nowrap;
            min-width: 80px;
            max-width: 120px;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .matrix-table th {{
            background: #f8f9fa;
            font-weight: 600;
            position: sticky;
            top: 0;
            z-index: 10;
        }}

        .matrix-table th.field-header {{
            background: #e9ecef;
            position: sticky;
            left: 0;
            z-index: 11;
            text-align: left;
            min-width: 200px;
            max-width: 200px;
        }}

        .matrix-table td.field-name {{
            background: #f8f9fa;
            font-weight: 500;
            position: sticky;
            left: 0;
            z-index: 9;
            text-align: left;
            min-width: 200px;
            max-width: 200px;
        }}

        .percentage-cell {{
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .percentage-cell:hover {{
            transform: scale(1.05);
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }}

{color_classes}
        
        .completed-company {{ background-color: #d4edda !important; font-weight: bold; border: 2px solid #28a745; }}
        .completed-field {{ background-color: #d4edda !important; font-weight: bold; border: 2px solid #28a745; }}

        .side-panel {{
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}

        .filter-section,
        .primary-section,
        .values-section {{
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            overflow: hidden;
        }}

        .filter-section {{
            padding: 20px;
        }}

        .primary-section,
        .values-section {{
            flex: 1;
            display: flex;
            flex-direction: column;
        }}

        .section-header {{
            background: #f8f9fa;
            padding: 15px;
            border-bottom: 1px solid #e9ecef;
            font-weight: 600;
        }}

        .section-content {{
            flex: 1;
            padding: 15px;
            overflow: auto;
        }}

        .filter-group {{
            margin-bottom: 20px;
        }}

        .filter-group label {{
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: #495057;
        }}

        .filter-select {{
            width: 100%;
            padding: 10px;
            border: 1px solid #ced4da;
            border-radius: 4px;
            font-size: 14px;
            background: white;
        }}

        .filter-select:focus {{
            outline: none;
            border-color: #80bdff;
            box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
        }}

        .code-block {{
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 4px;
            padding: 12px;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 12px;
            white-space: pre-wrap;
            word-wrap: break-word;
            overflow-x: auto;
            max-height: 300px;
            overflow-y: auto;
        }}

        .content-item {{
            margin-bottom: 15px;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 4px;
            border-left: 4px solid {config['accent_color']};
        }}

        .content-company {{
            font-weight: 600;
            color: {config['accent_color']};
            margin-bottom: 5px;
        }}

        .content-pattern {{
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 11px;
            background: white;
            padding: 8px;
            border-radius: 3px;
            word-break: break-all;
            border: 1px solid #dee2e6;
            margin-bottom: 5px;
        }}

        .content-type {{
            font-size: 10px;
            color: #6c757d;
            background: #e9ecef;
            padding: 2px 6px;
            border-radius: 3px;
            display: inline-block;
            margin-bottom: 5px;
        }}

        .no-data {{
            text-align: center;
            color: #6c757d;
            font-style: italic;
            padding: 20px;
        }}

        .stats-info {{
            background: {config['stats_bg']};
            border: 1px solid {config['stats_border']};
            border-radius: 4px;
            padding: 10px;
            margin-bottom: 15px;
            font-size: 14px;
        }}

        .header-info {{
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
        }}

        .generated-info {{
            background: {config['stats_bg']};
            border: 1px solid {config['stats_border']};
            border-radius: 4px;
            padding: 8px;
            font-size: 11px;
            color: {config['text_color']};
            flex: 1;
            line-height: 1.3;
        }}

        .color-legend {{
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 4px;
            padding: 8px;
            font-size: 10px;
            color: #495057;
            flex: 1;
            line-height: 1.3;
        }}

        .legend-item {{
            display: inline-block;
            margin: 2px 5px;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 10px;
        }}"""
    
    def _get_color_classes(self, scheme: str) -> str:
        """Get color scheme CSS classes."""
        if scheme == "mapped":
            return """        /* Green color scheme for mapped data */
        .success-100 { background-color: #d4edda; color: #155724; }
        .success-90 { background-color: #d1ecf1; color: #0c5460; }
        .success-80 { background-color: #d1ecf1; color: #0c5460; }
        .success-70 { background-color: #bee5eb; color: #0c5460; }
        .success-60 { background-color: #bee5eb; color: #0c5460; }
        .success-50 { background-color: #b3d7ff; color: #0c5460; }
        .success-40 { background-color: #fff3cd; color: #856404; }
        .success-30 { background-color: #ffeaa7; color: #b8860b; }
        .success-20 { background-color: #ffd93d; color: #b8860b; }
        .success-10 { background-color: #ffb347; color: #8b4513; }
        .success-0 { background-color: #f8f9fa; color: #6c757d; }
        .not-available { background-color: #e9ecef; color: #6c757d; font-style: italic; }"""
        else:  # regex
            return """        /* Blue color scheme for regex patterns */
        .teminat-100 { background-color: #d4edda; color: #155724; }
        .teminat-90 { background-color: #d1ecf1; color: #0c5460; }
        .teminat-80 { background-color: #d1ecf1; color: #0c5460; }
        .teminat-70 { background-color: #bee5eb; color: #0c5460; }
        .teminat-60 { background-color: #bee5eb; color: #0c5460; }
        .teminat-50 { background-color: #b3d7ff; color: #0c5460; }
        .teminat-40 { background-color: #fff3cd; color: #856404; }
        .teminat-30 { background-color: #ffeaa7; color: #b8860b; }
        .teminat-20 { background-color: #ffd93d; color: #b8860b; }
        .teminat-10 { background-color: #ffb347; color: #8b4513; }
        .teminat-0 { background-color: #f8f9fa; color: #6c757d; }
        
        .other-100 { background-color: #d4edda; color: #155724; }
        .other-90 { background-color: #fff3cd; color: #856404; }
        .other-80 { background-color: #ffeaa7; color: #b8860b; }
        .other-70 { background-color: #ffd93d; color: #b8860b; }
        .other-60 { background-color: #ffb347; color: #8b4513; }
        .other-white { background-color: #ffffff; color: #333333; border: 1px solid #dee2e6; }
        .other-0 { background-color: #f8f9fa; color: #6c757d; }
        .not-applicable { background-color: #e9ecef; color: #6c757d; font-style: italic; }"""
    
    def _get_legend_html(self, scheme: str) -> str:
        """Get legend HTML based on color scheme."""
        if scheme == "mapped":
            return """<span class="legend-item success-100">100%</span>
                <span class="legend-item success-90">90-99%</span>
                <span class="legend-item success-50">50-89%</span>
                <span class="legend-item success-40">40-49%</span>
                <span class="legend-item success-20">20-39%</span>
                <span class="legend-item success-10">10-19%</span>
                <span class="legend-item success-0">0% (-)</span><br>
                <strong>Green:</strong> Successful mapping | <strong>All data shown:</strong> No N/M placeholders"""
        else:  # regex
            return """<span class="legend-item teminat-100">100%</span>
                <span class="legend-item other-90">90-99% Other</span>
                <span class="legend-item teminat-50">50-99% Teminat</span>
                <span class="legend-item teminat-40">40-49% Teminat</span>
                <span class="legend-item other-white">1-59% Other</span>
                <span class="legend-item other-0">0% (-)</span>
                <span class="legend-item not-applicable">N/A</span><br>
                <strong>Teminat:</strong> Orange <50% | <strong>Others:</strong> Orange 60-99%, White 1-59%"""
    
    def _generate_javascript(self, config: Dict[str, Any]) -> str:
        """Generate JavaScript based on dashboard mode."""
        if config['color_scheme'] == "mapped":
            return self._get_mapped_javascript()
        else:
            return self._get_regex_javascript()
    
    def _get_regex_javascript(self) -> str:
        """JavaScript for regex dashboards."""
        return """        class Dashboard {
            constructor() {
                this.outputData = EMBEDDED_PRIMARY_DATA;
                this.configData = EMBEDDED_SECONDARY_DATA;
                this.companies = EMBEDDED_COMPANIES;
                this.allFields = EMBEDDED_FIELDS;
                this.selectedCompany = '';
                this.selectedField = '';
                
                this.initializeEventListeners();
                this.initialize();
            }

            initializeEventListeners() {
                document.getElementById('companyFilter').addEventListener('change', (e) => {
                    this.selectedCompany = e.target.value;
                    this.updateDisplays();
                });

                document.getElementById('fieldFilter').addEventListener('change', (e) => {
                    this.selectedField = e.target.value;
                    this.updateDisplays();
                });
            }

            initialize() {
                this.populateFilters();
                this.renderMatrix();
                this.updateDisplays();
            }

            populateFilters() {
                const companySelect = document.getElementById('companyFilter');
                this.companies.sort().forEach(company => {
                    const option = document.createElement('option');
                    option.value = company;
                    option.textContent = company.replace('_E', '').toUpperCase();
                    companySelect.appendChild(option);
                });

                const fieldSelect = document.getElementById('fieldFilter');
                this.allFields.forEach(field => {
                    const option = document.createElement('option');
                    option.value = field;
                    option.textContent = field;
                    fieldSelect.appendChild(option);
                });
            }

            calculateSuccessRate(company, field) {
                if (!this.configData[company] || !this.configData[company].hasOwnProperty(field)) {
                    return { rate: 0, isNA: true };
                }

                if (!this.outputData[company] || !this.outputData[company][field]) {
                    return { rate: 0, isNA: false, successful: 0, total: 0 };
                }

                const fieldData = this.outputData[company][field];
                const totalDocs = Object.keys(fieldData).length;
                const successfulDocs = Object.values(fieldData).filter(value => value !== null && value !== undefined && value !== '').length;
                
                if (totalDocs === 0) {
                    return { rate: 0, isNA: false, successful: 0, total: 0 };
                }

                return { 
                    rate: Math.round((successfulDocs / totalDocs) * 100),
                    isNA: false,
                    successful: successfulDocs,
                    total: totalDocs
                };
            }

            getPercentageClass(rate, isNA, field) {
                if (isNA) return 'not-applicable';
                
                const isTeminat = field.startsWith('Teminat');
                
                if (rate === 100) {
                    return isTeminat ? 'teminat-100' : 'other-100';
                }
                
                if (isTeminat) {
                    if (rate >= 90) return 'teminat-90';
                    if (rate >= 80) return 'teminat-80';
                    if (rate >= 70) return 'teminat-70';
                    if (rate >= 60) return 'teminat-60';
                    if (rate >= 50) return 'teminat-50';
                    if (rate >= 40) return 'teminat-40';
                    if (rate >= 30) return 'teminat-30';
                    if (rate >= 20) return 'teminat-20';
                    if (rate >= 10) return 'teminat-10';
                    if (rate > 0) return 'teminat-10';
                    return 'teminat-0';
                } else {
                    if (rate >= 90) return 'other-90';
                    if (rate >= 80) return 'other-80';
                    if (rate >= 70) return 'other-70';
                    if (rate >= 60) return 'other-60';
                    if (rate > 0) return 'other-white';
                    return 'other-0';
                }
            }

            isCompanyCompleted(company) {
                return this.allFields.every(field => {
                    const result = this.calculateSuccessRate(company, field);
                    return result.isNA || result.rate === 100;
                });
            }

            isFieldCompleted(field) {
                return this.companies.every(company => {
                    const result = this.calculateSuccessRate(company, field);
                    return result.isNA || result.rate === 100;
                });
            }

            renderMatrix() {
                const header = document.getElementById('matrixHeader');
                const body = document.getElementById('matrixBody');

                header.innerHTML = '<th class="field-header">Field Name</th>';
                body.innerHTML = '';

                this.companies.sort().forEach(company => {
                    const th = document.createElement('th');
                    th.textContent = company.replace('_E', '').toUpperCase();
                    th.title = company;
                    
                    if (this.isCompanyCompleted(company)) {
                        th.classList.add('completed-company');
                        th.title += ' - [SUCCESS] COMPLETED (All fields 100% or N/A)';
                    }
                    
                    header.appendChild(th);
                });

                this.allFields.forEach(field => {
                    const row = document.createElement('tr');
                    
                    const fieldCell = document.createElement('td');
                    fieldCell.className = 'field-name';
                    fieldCell.textContent = field;
                    fieldCell.title = field;
                    
                    if (this.isFieldCompleted(field)) {
                        fieldCell.classList.add('completed-field');
                        fieldCell.title += ' - [SUCCESS] COMPLETED (All companies 100% or N/A)';
                    }
                    
                    row.appendChild(fieldCell);

                    this.companies.sort().forEach(company => {
                        const cell = document.createElement('td');
                        const result = this.calculateSuccessRate(company, field);
                        
                        cell.className = `percentage-cell ${this.getPercentageClass(result.rate, result.isNA, field)}`;
                        cell.textContent = result.isNA ? 'N/A' : (result.rate === 0 ? '-' : `${result.rate}%`);
                        cell.title = result.isNA ? 'Field not available' : `${result.successful}/${result.total} documents`;
                        
                        cell.addEventListener('click', () => {
                            this.selectCell(company, field);
                        });
                        
                        row.appendChild(cell);
                    });

                    body.appendChild(row);
                });
            }

            selectCell(company, field) {
                document.getElementById('companyFilter').value = company;
                document.getElementById('fieldFilter').value = field;
                this.selectedCompany = company;
                this.selectedField = field;
                this.updateDisplays();
            }

            updateDisplays() {
                this.updateStats();
                this.updatePrimarySection();
                this.updateValuesSection();
            }

            updateStats() {
                const statsDiv = document.getElementById('statsInfo');
                
                if (!this.selectedField && !this.selectedCompany) {
                    const completedCompanies = this.companies.filter(company => this.isCompanyCompleted(company));
                    const completedFields = this.allFields.filter(field => this.isFieldCompleted(field));
                    
                    statsDiv.innerHTML = `
                        <strong>[REPORT] Completion Status</strong><br>
                        [SUCCESS] Completed Companies: ${completedCompanies.length}/${this.companies.length}<br>
                        [SUCCESS] Completed Fields: ${completedFields.length}/${this.allFields.length}<br>
                        <small style="color: #6c757d;">Green highlighted headers indicate 100% completion</small>
                    `;
                    return;
                }

                let stats = '';
                
                if (this.selectedField && this.selectedCompany) {
                    const result = this.calculateSuccessRate(this.selectedCompany, this.selectedField);
                    stats = `<strong>${this.selectedCompany}</strong> - <strong>${this.selectedField}</strong><br>`;
                    stats += result.isNA ? 'Field not available' : `Success Rate: ${result.rate}% (${result.successful}/${result.total})`;
                } else if (this.selectedField) {
                    const validCompanies = this.companies.filter(company => {
                        const result = this.calculateSuccessRate(company, this.selectedField);
                        return !result.isNA;
                    });
                    stats = `<strong>${this.selectedField}</strong><br>Available in ${validCompanies.length}/${this.companies.length} companies`;
                } else if (this.selectedCompany) {
                    const validFields = this.allFields.filter(field => {
                        const result = this.calculateSuccessRate(this.selectedCompany, field);
                        return !result.isNA;
                    });
                    stats = `<strong>${this.selectedCompany}</strong><br>Has ${validFields.length}/${this.allFields.length} fields`;
                }

                statsDiv.innerHTML = stats;
            }

            updatePrimarySection() {
                const primaryDiv = document.getElementById('primaryContent');
                
                if (!this.selectedField) {
                    primaryDiv.innerHTML = '<div class="no-data">Select a field to view regex patterns</div>';
                    return;
                }

                let content = '';
                let hasApplicableField = false;
                
                const targetCompanies = this.selectedCompany ? [this.selectedCompany] : this.companies;
                
                targetCompanies.sort().forEach(company => {
                    const config = this.configData[company];
                    if (config && config.hasOwnProperty(this.selectedField)) {
                        hasApplicableField = true;
                        if (config[this.selectedField] && config[this.selectedField].pattern) {
                            content += `
                                <div class="content-item">
                                    <div class="content-company">${company.replace('_E', '').toUpperCase()}</div>
                                    <div class="content-pattern">${this.escapeHtml(config[this.selectedField].pattern)}</div>
                                    ${config[this.selectedField].description ? `<div style="margin-top: 5px; font-size: 12px; color: #6c757d;">${this.escapeHtml(config[this.selectedField].description)}</div>` : ''}
                                </div>
                            `;
                        } else {
                            content += `
                                <div class="content-item">
                                    <div class="content-company">${company.replace('_E', '').toUpperCase()}</div>
                                    <div class="content-pattern" style="color: #6c757d; font-style: italic;">No pattern implemented yet</div>
                                </div>
                            `;
                        }
                    }
                });

                if (content === '') {
                    if (hasApplicableField) {
                        content = '<div class="no-data">No regex patterns found for selected criteria</div>';
                    } else {
                        content = '<div class="no-data">N/A - Field not applicable for selected companies</div>';
                    }
                }

                primaryDiv.innerHTML = content;
            }

            updateValuesSection() {
                const valuesDiv = document.getElementById('valuesContent');
                
                if (!this.selectedField) {
                    valuesDiv.innerHTML = '<div class="no-data">Select a field to view extracted values</div>';
                    return;
                }

                let content = '';
                let hasApplicableField = false;
                
                const targetCompanies = this.selectedCompany ? [this.selectedCompany] : this.companies;
                
                targetCompanies.sort().forEach(company => {
                    const config = this.configData[company];
                    if (config && config.hasOwnProperty(this.selectedField)) {
                        hasApplicableField = true;
                        const fieldData = this.outputData[company] && this.outputData[company][this.selectedField];
                        if (fieldData) {
                            const entries = Object.entries(fieldData)
                                .map(([doc, value]) => `"${doc}": ${value === null ? 'null' : `"${this.escapeHtml(String(value))}"`}`)
                                .join(',\\n');
                            
                            if (entries) {
                                content += `<div class="content-item">
                                    <div class="content-company">${company.replace('_E', '').toUpperCase()}</div>
                                    <pre class="code-block">{\\n${entries}\\n}</pre>
                                </div>`;
                            }
                        } else {
                            content += `<div class="content-item">
                                <div class="content-company">${company.replace('_E', '').toUpperCase()}</div>
                                <pre class="code-block" style="color: #6c757d; font-style: italic;">No extracted data available</pre>
                            </div>`;
                        }
                    }
                });

                if (content === '') {
                    if (hasApplicableField) {
                        content = '<div class="no-data">No extracted values found for selected criteria</div>';
                    } else {
                        content = '<div class="no-data">N/A - Field not applicable for selected companies</div>';
                    }
                }

                valuesDiv.innerHTML = content;
            }

            escapeHtml(text) {
                const div = document.createElement('div');
                div.textContent = text;
                return div.innerHTML;
            }
        }"""
    
    def _get_mapped_javascript(self) -> str:
        """JavaScript for mapped dashboards."""
        return """        class MappedDashboard {
            constructor() {
                this.mappedData = EMBEDDED_PRIMARY_DATA;
                this.mappingConfig = EMBEDDED_SECONDARY_DATA;
                this.companies = EMBEDDED_COMPANIES;
                this.allFields = EMBEDDED_FIELDS;
                this.selectedCompany = '';
                this.selectedField = '';
                
                this.initializeEventListeners();
                this.initialize();
            }

            initializeEventListeners() {
                document.getElementById('companyFilter').addEventListener('change', (e) => {
                    this.selectedCompany = e.target.value;
                    this.updateDisplays();
                });

                document.getElementById('fieldFilter').addEventListener('change', (e) => {
                    this.selectedField = e.target.value;
                    this.updateDisplays();
                });
            }

            initialize() {
                this.populateFilters();
                this.renderMatrix();
                this.updateDisplays();
            }

            populateFilters() {
                const companySelect = document.getElementById('companyFilter');
                this.companies.sort().forEach(company => {
                    const option = document.createElement('option');
                    option.value = company;
                    option.textContent = company.replace('_E', '').toUpperCase();
                    companySelect.appendChild(option);
                });

                const fieldSelect = document.getElementById('fieldFilter');
                this.allFields.forEach(field => {
                    const option = document.createElement('option');
                    option.value = field;
                    option.textContent = field;
                    fieldSelect.appendChild(option);
                });
            }

            calculateMappingSuccess(company, field) {
                // Always show data if it exists - no N/M placeholders!
                if (!this.mappedData[company] || !this.mappedData[company][field]) {
                    return { rate: 0, hasMapping: false, isNA: true, successful: 0, total: 0 };
                }

                const fieldData = this.mappedData[company][field];
                const totalDocs = Object.keys(fieldData).length;
                const successfulDocs = Object.values(fieldData).filter(value => 
                    value !== null && value !== undefined && value !== ''
                ).length;
                
                const hasMapping = this.mappingConfig[company] && 
                                 this.mappingConfig[company].field_mappings && 
                                 this.mappingConfig[company].field_mappings.hasOwnProperty(field);
                
                return { 
                    rate: totalDocs > 0 ? Math.round((successfulDocs / totalDocs) * 100) : 0,
                    hasMapping: hasMapping,
                    successful: successfulDocs,
                    total: totalDocs,
                    isNA: false
                };
            }

            getPercentageClass(rate, hasMapping, isNA) {
                if (isNA) return 'not-available';
                
                if (rate === 100) return 'success-100';
                if (rate >= 90) return 'success-90';
                if (rate >= 80) return 'success-80';
                if (rate >= 70) return 'success-70';
                if (rate >= 60) return 'success-60';
                if (rate >= 50) return 'success-50';
                if (rate >= 40) return 'success-40';
                if (rate >= 30) return 'success-30';
                if (rate >= 20) return 'success-20';
                if (rate >= 10) return 'success-10';
                if (rate > 0) return 'success-10';
                return 'success-0';
            }

            isCompanyCompleted(company) {
                return this.allFields.every(field => {
                    const result = this.calculateMappingSuccess(company, field);
                    return result.isNA || result.rate === 100;
                });
            }

            isFieldCompleted(field) {
                return this.companies.every(company => {
                    const result = this.calculateMappingSuccess(company, field);
                    return result.isNA || result.rate === 100;
                });
            }

            renderMatrix() {
                const header = document.getElementById('matrixHeader');
                const body = document.getElementById('matrixBody');

                header.innerHTML = '<th class="field-header">Field Name</th>';
                body.innerHTML = '';

                this.companies.sort().forEach(company => {
                    const th = document.createElement('th');
                    th.textContent = company.replace('_E', '').toUpperCase();
                    th.title = company;
                    
                    if (this.isCompanyCompleted(company)) {
                        th.classList.add('completed-company');
                        th.title += ' - [SUCCESS] COMPLETED (All fields mapped or N/A)';
                    }
                    
                    header.appendChild(th);
                });

                this.allFields.forEach(field => {
                    const row = document.createElement('tr');
                    
                    const fieldCell = document.createElement('td');
                    fieldCell.className = 'field-name';
                    fieldCell.textContent = field;
                    fieldCell.title = field;
                    
                    if (this.isFieldCompleted(field)) {
                        fieldCell.classList.add('completed-field');
                        fieldCell.title += ' - [SUCCESS] COMPLETED (All companies mapped or N/A)';
                    }
                    
                    row.appendChild(fieldCell);

                    this.companies.sort().forEach(company => {
                        const cell = document.createElement('td');
                        const result = this.calculateMappingSuccess(company, field);
                        
                        cell.className = `percentage-cell ${this.getPercentageClass(result.rate, result.hasMapping, result.isNA)}`;
                        
                        let cellText, cellTitle;
                        if (result.isNA) {
                            cellText = 'N/A';
                            cellTitle = 'No data available';
                        } else {
                            cellText = result.rate === 0 ? '-' : `${result.rate}%`;
                            cellTitle = `${result.successful}/${result.total} documents`;
                            if (result.hasMapping) {
                                cellTitle += ' (with mapping rules)';
                            } else {
                                cellTitle += ' (raw regex values)';
                            }
                        }
                        
                        cell.textContent = cellText;
                        cell.title = cellTitle;
                        
                        cell.addEventListener('click', () => {
                            this.selectCell(company, field);
                        });
                        
                        row.appendChild(cell);
                    });

                    body.appendChild(row);
                });
            }

            selectCell(company, field) {
                document.getElementById('companyFilter').value = company;
                document.getElementById('fieldFilter').value = field;
                this.selectedCompany = company;
                this.selectedField = field;
                this.updateDisplays();
            }

            updateDisplays() {
                this.updateStats();
                this.updatePrimarySection();
                this.updateValuesSection();
            }

            updateStats() {
                const statsDiv = document.getElementById('statsInfo');
                
                if (!this.selectedField && !this.selectedCompany) {
                    const completedCompanies = this.companies.filter(company => this.isCompanyCompleted(company));
                    const completedFields = this.allFields.filter(field => this.isFieldCompleted(field));
                    const companiesWithMappings = this.companies.filter(company => this.mappingConfig[company]);
                    
                    statsDiv.innerHTML = `
                        <strong>[REPORT] Mapping Status</strong><br>
                        [SUCCESS] Companies with mappings: ${companiesWithMappings.length}/${this.companies.length}<br>
                        [SUCCESS] Completed companies: ${completedCompanies.length}/${this.companies.length}<br>
                        [SUCCESS] Completed fields: ${completedFields.length}/${this.allFields.length}<br>
                        <small style="color: #6c757d;">All available data shown (no N/M placeholders)</small>
                    `;
                    return;
                }

                let stats = '';
                
                if (this.selectedField && this.selectedCompany) {
                    const result = this.calculateMappingSuccess(this.selectedCompany, this.selectedField);
                    stats = `<strong>${this.selectedCompany}</strong> - <strong>${this.selectedField}</strong><br>`;
                    if (result.isNA) {
                        stats += 'No data available';
                    } else {
                        stats += `Success: ${result.rate}% (${result.successful}/${result.total})`;
                        if (result.hasMapping) {
                            stats += '<br><small>Using business logic mapping</small>';
                        } else {
                            stats += '<br><small>Showing raw regex values</small>';
                        }
                    }
                } else if (this.selectedField) {
                    const companiesWithData = this.companies.filter(company => {
                        const result = this.calculateMappingSuccess(company, this.selectedField);
                        return !result.isNA;
                    });
                    stats = `<strong>${this.selectedField}</strong><br>Available in ${companiesWithData.length}/${this.companies.length} companies`;
                } else if (this.selectedCompany) {
                    const fieldsWithData = this.allFields.filter(field => {
                        const result = this.calculateMappingSuccess(this.selectedCompany, field);
                        return !result.isNA;
                    });
                    stats = `<strong>${this.selectedCompany}</strong><br>Has data for ${fieldsWithData.length}/${this.allFields.length} fields`;
                }

                statsDiv.innerHTML = stats;
            }

            updatePrimarySection() {
                const primaryDiv = document.getElementById('primaryContent');
                
                if (!this.selectedField) {
                    primaryDiv.innerHTML = '<div class="no-data">Select a field to view mapping rules</div>';
                    return;
                }

                let content = '';
                
                const targetCompanies = this.selectedCompany ? [this.selectedCompany] : this.companies;
                
                targetCompanies.sort().forEach(company => {
                    const mappingConfig = this.mappingConfig[company];
                    if (mappingConfig && mappingConfig.field_mappings && mappingConfig.field_mappings[this.selectedField]) {
                        const fieldMapping = mappingConfig.field_mappings[this.selectedField];
                        
                        content += `
                            <div class="content-item">
                                <div class="content-company">${company.replace('_E', '').toUpperCase()}</div>
                                <div class="content-type">${fieldMapping.type || 'unknown'}</div>`;
                        
                        if (fieldMapping.mappings && fieldMapping.mappings.length > 0) {
                            fieldMapping.mappings.forEach((mapping, index) => {
                                const inputPattern = mapping.input_pattern === null ? 'null' : (mapping.input_pattern || 'N/A');
                                const output = mapping.output || 'N/A';
                                content += `
                                    <div class="content-pattern">
                                        <strong>Rule ${index + 1}:</strong> "${this.escapeHtml(inputPattern)}" → "${this.escapeHtml(output)}"
                                        ${mapping.description ? `<br><em>${this.escapeHtml(mapping.description)}</em>` : ''}
                                    </div>`;
                            });
                        } else {
                            content += '<div class="content-pattern" style="color: #6c757d; font-style: italic;">No mapping rules defined</div>';
                        }
                        
                        content += '</div>';
                    } else {
                        const hasData = this.mappedData[company] && this.mappedData[company][this.selectedField];
                        if (hasData) {
                            content += `
                                <div class="content-item">
                                    <div class="content-company">${company.replace('_E', '').toUpperCase()}</div>
                                    <div class="content-pattern" style="color: #6c757d; font-style: italic;">No mapping rules - showing raw regex values</div>
                                </div>
                            `;
                        }
                    }
                });

                if (content === '') {
                    content = '<div class="no-data">No mapping configuration or data available for selected field/companies</div>';
                }

                primaryDiv.innerHTML = content;
            }

            updateValuesSection() {
                const valuesDiv = document.getElementById('valuesContent');
                
                if (!this.selectedField) {
                    valuesDiv.innerHTML = '<div class="no-data">Select a field to view mapped values</div>';
                    return;
                }

                let content = '';
                
                const targetCompanies = this.selectedCompany ? [this.selectedCompany] : this.companies;
                
                targetCompanies.sort().forEach(company => {
                    const fieldData = this.mappedData[company] && this.mappedData[company][this.selectedField];
                    if (fieldData) {
                        const entries = Object.entries(fieldData)
                            .map(([doc, value]) => `"${doc}": ${value === null ? 'null' : `"${this.escapeHtml(String(value))}"`}`)
                            .join(',\\n');
                        
                        if (entries) {
                            content += `<div class="content-item">
                                <div class="content-company">${company.replace('_E', '').toUpperCase()}</div>
                                <pre class="code-block">{\\n${entries}\\n}</pre>
                            </div>`;
                        }
                    }
                });

                if (content === '') {
                    content = '<div class="no-data">No mapped data available for selected field/companies</div>';
                }

                valuesDiv.innerHTML = content;
            }

            escapeHtml(text) {
                const div = document.createElement('div');
                div.textContent = text;
                return div.innerHTML;
            }
        }"""
    
    def _save_html(self, html_content: str, output_path: str) -> None:
        """Save HTML content to file."""
        from pathlib import Path
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"\n[SUCCESS] Dashboard generated successfully!")
            print(f"[FILE] Output file: {output_file}")
            print(f"[BROWSER] Open in browser: file://{output_file.absolute()}")
        except Exception as e:
            raise Exception(f"Error writing HTML file: {e}")


if __name__ == "__main__":
    # Test HTML generation
    import sys
    from dashboard_data import DataLoader
    
    if len(sys.argv) < 2:
        print("Usage: python dashboard_html.py [regex|mapped]")
        sys.exit(1)
    
    # Load data
    loader = DataLoader()
    data = loader.load_data(sys.argv[1])
    
    # Generate HTML
    generator = HTMLGenerator()
    output_file = f"test_{data.mode}_dashboard.html"
    generator.generate_dashboard(data, output_file)