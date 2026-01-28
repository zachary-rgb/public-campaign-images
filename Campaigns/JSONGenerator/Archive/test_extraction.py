"""
Quick test of the extraction functionality
Runs without interactive prompts
"""

from extract_to_google_sheets import CampaignExtractor, GoogleSheetsExporter
from pathlib import Path

def test_extraction():
    """Test extraction on the Takeda Vitiligo document"""
    
    # Find the Word document
    docx_files = list(Path(".").glob("*.docx"))
    if not docx_files:
        print("[!] No Word documents found")
        return
    
    docx_path = str(docx_files[0])
    print("=" * 100)
    print("TESTING EXTRACTION")
    print("=" * 100)
    print(f"\n[+] Processing: {Path(docx_path).name}")
    
    # Sample metadata
    metadata = {
        'Campaign Name': 'Takeda Vitiligo WeConnect',
        'Language': 'en-us',
        'URL/UTM': 'https://example.com/register',
        'End Matter (Enter Sponsor)': 'Takeda'
    }
    
    print("\n[+] Using test metadata:")
    for key, value in metadata.items():
        print(f"    {key}: {value}")
    
    # Extract
    print("\n" + "=" * 100)
    print("EXTRACTING...")
    print("=" * 100)
    
    extractor = CampaignExtractor(docx_path)
    rows = extractor.extract_all_emails(metadata)
    
    print(f"\n[+] SUCCESS! Extracted {len(rows)} email template(s)")
    
    # Preview
    exporter = GoogleSheetsExporter(CampaignExtractor.STANDARD_COLUMNS)
    exporter.display_preview(rows)
    
    # Export
    output_file = 'TEST_extraction_output.tsv'
    exporter.to_tsv(rows, output_file)
    print(f"\n[+] TSV saved: {output_file}")
    
    # Try clipboard
    if exporter.to_clipboard(rows):
        print("[+] Content copied to clipboard! Ready to paste in Google Sheets.")
    
    # Save JSON
    import json
    json_file = 'TEST_extraction_output.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    print(f"[+] JSON saved: {json_file}")
    
    print("\n" + "=" * 100)
    print("TEST COMPLETE - Ready to paste into Google Sheets!")
    print("=" * 100)

if __name__ == "__main__":
    test_extraction()

