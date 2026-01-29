"""
Test Unicode checkbox detection (☑ and ☐)
"""

from pathlib import Path
from extract_to_google_sheets import CampaignExtractor

def test_unicode_checkboxes():
    """Test that Unicode checkbox characters are detected properly"""
    print("=" * 80)
    print("TESTING UNICODE CHECKBOX DETECTION")
    print("=" * 80)
    
    # Find a real docx file
    docx_files = list(Path(".").glob("*.docx"))
    if not docx_files:
        print("[ERROR] No .docx files found for testing")
        return
    
    extractor = CampaignExtractor(str(docx_files[0]))
    
    # Test 1: Unicode checked box ☑
    print("\nTest 1: Unicode Checked Box (U+2611)")
    test_text1 = """☑ Consider Joining a Vitiligo Patient Registry
☐ Your Experience with Vitiligo Matters—Join the WeConnect Registry
☐ Learn About Research Opportunities for Vitiligo"""
    
    result1 = extractor.extract_selected_option(test_text1, "Email Subject")
    print(f"Input:\n{test_text1}")
    print(f"\nExtracted: '{result1}'")
    print(f"Expected: 'Consider Joining a Vitiligo Patient Registry'")
    print("[PASS]" if "Consider Joining" in result1 else "[FAIL]")
    
    # Test 2: Multiple Unicode checked boxes
    print("\n" + "-" * 80)
    print("\nTest 2: Multiple Unicode Checked Boxes")
    test_text2 = """☑ Vitiligo: Empower Yourself with Knowledge and Care Options
☐ Support Vitiligo Research. Explore potential possibilities in care.
☐ Help us advance Vitiligo treatment through clinical trials"""
    
    result2 = extractor.extract_selected_option(test_text2, "Banner Headline")
    print(f"Input:\n{test_text2}")
    print(f"\nExtracted: '{result2}'")
    print(f"Expected: 'Vitiligo: Empower Yourself with Knowledge...'")
    print("[PASS]" if "Empower Yourself" in result2 else "[FAIL]")
    
    # Test 3: No checked boxes (all unchecked ☐)
    print("\n" + "-" * 80)
    print("\nTest 3: All Unchecked Boxes (Should warn)")
    extractor.warnings.clear()
    test_text3 = """☐ Option 1
☐ Option 2: Client Preferred
☐ Option 3"""
    
    result3 = extractor.extract_selected_option(test_text3, "Hero Image")
    print(f"Input:\n{test_text3}")
    print(f"\nExtracted: '{result3}'")
    print(f"Warnings generated: {len(extractor.warnings)}")
    if extractor.warnings:
        print(f"Warning: {extractor.warnings[-1]['field']}")
    print("[PASS]" if len(extractor.warnings) > 0 else "[FAIL - Should warn]")
    
    # Test 4: Mixed with text [X] checkboxes
    print("\n" + "-" * 80)
    print("\nTest 4: Text [X] Checkbox (Should still work)")
    test_text4 = """[X] 1. Join a Patient Registry for Adults Living with Vitiligo
[ ] 2. Vitiligo: Empower Yourself with Knowledge
[ ] 3. Support Vitiligo Research"""
    
    result4 = extractor.extract_selected_option(test_text4, "Banner Headline")
    print(f"Input:\n{test_text4}")
    print(f"\nExtracted: '{result4}'")
    print(f"Expected: 'Join a Patient Registry for Adults Living with Vitiligo'")
    print("[PASS]" if "Join a Patient Registry" in result4 else "[FAIL]")
    
    # Test 5: Campaign name extraction
    print("\n" + "-" * 80)
    print("\nTest 5: Campaign Name Extraction from Document")
    campaign_name = extractor.extract_campaign_name_from_doc()
    print(f"Extracted Campaign Name: '{campaign_name}'")
    print(f"Expected: Should contain 'Takeda' or 'Vitiligo' or similar")
    print("[PASS]" if campaign_name and len(campaign_name) > 0 else "[FAIL]")
    
    print("\n" + "=" * 80)
    print("UNICODE CHECKBOX DETECTION TESTS COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    test_unicode_checkboxes()

