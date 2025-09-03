"""
Agent Tools Package

Internal development and debugging tools for Turkish insurance policy PDF extraction.
These tools are used by developers to create and maintain regex patterns, 
analyze extraction quality, and debug issues.

Available Tools:
- enhanced_extractor.py: Core extraction engine supporting multi-pattern configurations
- field_dev.py: Pattern discovery, context analysis, and testing tool
- output_create.py: Generate extraction results for all fields in a company
- output_check.py: Analyze and validate existing extraction results

For end-user tools, see user_tools/ directory.
"""

__version__ = "1.0.0"
__author__ = "Turkish Insurance PDF Extraction System"