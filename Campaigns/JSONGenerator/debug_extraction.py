"""Debug the extraction to see what's happening"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from extract_to_google_sheets import CampaignExtractor

docx_path = "Takeda_TAK-279-VT-2001-Vitiligo_Walgreens Email Outreach_English_v1.0_03DEC2025 (1).docx"

print("="*80)
print("DEBUG EXTRACTION")
print("="*80)

extractor = CampaignExtractor(docx_path)

print("\n1. Email Headers from Document:")
email_headers = extractor.extract_email_headers_from_doc()
print(f"   Result: {email_headers}")

print("\n2. Document Paragraphs (first 10):")
for i, para in enumerate(extractor.doc.paragraphs[:10]):
    text = para.text.strip()
    if text:
        print(f"   Para {i}: '{text[:80]}...' (Style: {para.style.name})")

print("\n3. Extracting content...")
emails = extractor.extract_all_emails()

print(f"\n4. Warnings ({len(extractor.warnings)}):")
for w in extractor.warnings:
    print(f"   - {w['field']}: {w['action']}")

print(f"\n5. Extracted Data for Row 1:")
if emails:
    for key, value in list(emails[0].items())[:10]:
        val_preview = value[:60] if value else "(empty)"
        print(f"   {key}: {val_preview}")

print("\n" + "="*80)

