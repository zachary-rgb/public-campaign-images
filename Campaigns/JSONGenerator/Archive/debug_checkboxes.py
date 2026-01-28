"""Debug checkbox detection"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from extract_to_google_sheets import CampaignExtractor

docx_path = "Takeda_TAK-279-VT-2001-Vitiligo_Walgreens Email Outreach_English_v1.0_03DEC2025 (1).docx"

print("="*80)
print("DEBUG CHECKBOX DETECTION")
print("="*80)

extractor = CampaignExtractor(docx_path)

# Find Email Subject and Banner Headline cells
print("\nScanning tables for Email Subject and Banner Headline...")

for table_idx, table in enumerate(extractor.doc.tables):
    print(f"\nTable {table_idx+1}:")
    for row_idx, row in enumerate(table.rows):
        cells = row.cells
        if len(cells) >= 2:
            label = cells[0].text.strip()
            content = cells[1].text.strip()
            
            if 'EMAIL SUBJECT' in label.upper() or 'BANNER HEADLINE' in label.upper():
                print(f"\n  Found: {label}")
                print(f"  Content length: {len(content)}")
                print(f"  First 200 chars: {repr(content[:200])}")
                
                # Check for specific characters
                has_2611 = '\u2611' in content  # ☑
                has_2610 = '\u2610' in content  # ☐
                has_bracket_X = '[X]' in content or '[x]' in content
                
                print(f"  Has ☑ (U+2611): {has_2611}")
                print(f"  Has ☐ (U+2610): {has_2610}")
                print(f"  Has [X] or [x]: {has_bracket_X}")
                
                # Show each line
                lines = content.split('\n')
                print(f"  Lines ({len(lines)}):")
                for i, line in enumerate(lines[:5]):
                    print(f"    {i+1}: {repr(line[:80])}")

print("\n" + "="*80)

