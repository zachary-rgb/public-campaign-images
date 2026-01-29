"""Test full extraction"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from extract_to_google_sheets import CampaignExtractor, GoogleSheetsExporter

docx_path = "Takeda_TAK-279-VT-2001-Vitiligo_Walgreens Email Outreach_English_v1.0_03DEC2025 (1).docx"

print("="*80)
print("FULL EXTRACTION TEST")
print("="*80)

extractor = CampaignExtractor(docx_path)
rows = extractor.extract_all_emails()

print(f"\nExtracted {len(rows)} rows")

for idx, row in enumerate(rows, 1):
    print(f"\n{'='*80}")
    print(f"ROW {idx}")
    print('='*80)
    print(f"Campaign Name: {row.get('Campaign Name', '(empty)')}")
    print(f"Message Name: {row.get('Message Name', '(empty)')}")
    print(f"Email Subject: {row.get('Email Subject', '(empty)')[:80]}")
    print(f"Banner Headline: {row.get('Banner Headline', '(empty)')[:80]}")
    print(f"Hero Image (URL): {row.get('Hero Image (URL)', '(empty)')}")

print(f"\n{'='*80}")
print(f"WARNINGS: {len(extractor.warnings)}")
print('='*80)
for w in extractor.warnings:
    print(f"  {w['field']}: {w['action']}")

print("\n" + "="*80)

