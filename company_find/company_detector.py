import os
import fitz
import glob

COMPANY_PATTERNS = {
    'ak': ['ak sigorta', 'ak insurance', 'ak sig'],
    'allianz': ['allianz', 'allianz sigorta'],
    'anadolu': ['anadolu sigorta', 'anadolu sig'],
    'ankara': ['ankara sigorta', 'ankara sig'],
    'axa': ['axa', 'axa sigorta'],
    'doga': ['doğa sigorta', 'doga sigorta'],
    'gulf': ['gulf sigorta', 'gulf sig', 'gig sigorta', 'gig sig'],
    'hdi': ['hdi sigorta', 'hdi sig'],
    'mapfre': ['mapfre', 'mapfre sigorta'],
    'mg': ['mg sigorta', 'mg sig', 'magdeburger sigorta', 'magdeburger'],
    'neova': ['neova sigorta', 'neova sig'],
    'orient': ['orient sigorta', 'orient sig'],
    'Quick': ['quick sigorta', 'quick sig'],
    'ray': ['ray sigorta', 'ray sig'],
    'sompo': ['sompo sigorta', 'sompo sig'],
    'turkiye': ['türkiye sigorta', 'turkiye sigorta'],
    'turkiyekatilim': ['türkiye katılım', 'turkiye katilim'],
    'turknippon': ['türk nippon', 'turk nippon'],
    'unico': ['unico sigorta', 'unico sig'],
    'zurich': ['zurich', 'zurich sigorta']
}

def detect_company(pdf_path):
    """Simple exact matching algorithm - counts frequency of company patterns"""
    
    with fitz.open(pdf_path) as doc:
        content = " ".join(page.get_text() for page in doc).lower()
    
    company_counts = {}
    
    for company, patterns in COMPANY_PATTERNS.items():
        total_count = 0
        for pattern in patterns:
            total_count += content.count(pattern.lower())
        company_counts[company] = total_count
    
    # Return company with highest frequency, None if no matches
    max_count = max(company_counts.values())
    if max_count == 0:
        return None
        
    return max(company_counts, key=company_counts.get)

def test_all_pdfs(folder_path):
    """Recursively test all PDFs in folder and compare detected vs actual company names"""
    
    pdf_files = glob.glob(os.path.join(folder_path, "**", "*.pdf"), recursive=True)
    
    correct = 0
    total = 0
    results = []
    
    for pdf_file in pdf_files:
        # Extract actual company from path (format: company_E/company_E_numbers.pdf)
        path_parts = pdf_file.split('/')
        company_dir = path_parts[-2]  # e.g., "ak_E"
        actual_company = company_dir.split('_E')[0]  # Remove "_E" suffix
        
        detected_company = detect_company(pdf_file)
        is_correct = detected_company == actual_company
        
        results.append({
            'file': os.path.basename(pdf_file),
            'actual': actual_company,
            'detected': detected_company,
            'correct': is_correct
        })
        
        total += 1
        if is_correct:
            correct += 1
        
        status = "✅" if is_correct else "❌"
        print(f"{status} {os.path.basename(pdf_file)}: {actual_company} -> {detected_company}")
    
    accuracy = (correct / total) * 100 if total > 0 else 0
    
    print(f"\n=== RESULTS ===")
    print(f"Total PDFs: {total}")
    print(f"Correct: {correct}")
    print(f"Accuracy: {accuracy:.1f}%")
    
    # Show mismatches
    mismatches = [r for r in results if not r['correct']]
    if mismatches:
        print(f"\n=== MISMATCHES ({len(mismatches)}) ===")
        for m in mismatches[:10]:  # Show first 10
            print(f"{m['file']}: Expected '{m['actual']}', Got '{m['detected']}'")
    
    return results

if __name__ == "__main__":
    # Test single file
    test_file = "/Users/dogapoyraztahan/_repos/policy_assistant/pdf_regex_git/data/00_raw_pdfs/ak_E/ak_E_128027105_407994597.pdf"
    result = detect_company(test_file)
    print(f"Single file test: {result}")
    
    # Test all PDFs
    folder = "/Users/dogapoyraztahan/_repos/policy_assistant/pdf_regex_git/data/00_raw_pdfs"
    test_all_pdfs(folder)