"""Test current extraction to see what's happening with [X] markers"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from extract_to_google_sheets import CampaignExtractor

docx_path = "Takeda_TAK-279-VT-2001-Vitiligo_Walgreens Email Outreach_English_v1.0_03DEC2025 (1).docx"

print("="*80)
print("TESTING CURRENT EXTRACTION")
print("="*80)

extractor = CampaignExtractor(docx_path)

# Check what's in Email Subject and Hero Image cells
for table_idx, table in enumerate(extractor.doc.tables):
    print(f"\nTable {table_idx + 1}:")
    for row in table.rows:
        cells = row.cells
        if len(cells) >= 2:
            label = cells[0].text.strip()
            content = cells[1].text.strip()
            
            if 'EMAIL SUBJECT' in label.upper():
                print(f"\n  {label}:")
                print(f"  Raw content: {repr(content[:300])}")
                
                # Check each line
                lines = content.split('\n')
                for i, line in enumerate(lines[:5]):
                    print(f"    Line {i+1}: {repr(line)}")
                    has_bracket_X = '[X]' in line or '[x]' in line
                    has_bracket_empty = '[ ]' in line
                    print(f"      Has [X]: {has_bracket_X}, Has [ ]: {has_bracket_empty}")
                
                # Try extraction
                result = extractor.extract_selected_option(content, label)
                print(f"  Extracted result: {repr(result[:100])}")
                
            if 'HERO' in label.upper() and 'IMAGE' in label.upper():
                print(f"\n  {label}:")
                print(f"  Raw content: {repr(content[:200])}")
                
                lines = content.split('\n')
                for i, line in enumerate(lines[:5]):
                    print(f"    Line {i+1}: {repr(line)}")
                    has_X = '[X]' in line or '[x]' in line
                    print(f"      Has [X] or [x]: {has_X}")
                
                result = extractor.extract_selected_option(content, label)
                print(f"  Extracted result: {repr(result[:100])}")

print("\n" + "="*80)
print("Extraction complete")
print(f"Total warnings: {len(extractor.warnings)}")
for w in extractor.warnings:
    print(f"  - {w['field']}")
print("="*80)

