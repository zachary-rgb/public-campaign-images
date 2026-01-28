"""
Test warning alerts for missing checkbox selections
"""

from pathlib import Path
from extract_to_google_sheets import CampaignExtractor

def test_warning_alerts():
    """Test that warnings are generated for missing checkboxes"""
    print("=" * 80)
    print("TESTING WARNING ALERTS FOR MISSING CHECKBOXES")
    print("=" * 80)
    
    # Find a real docx file
    docx_files = list(Path(".").glob("*.docx"))
    if not docx_files:
        print("[ERROR] No .docx files found for testing")
        return
    
    extractor = CampaignExtractor(str(docx_files[0]))
    
    # Test 1: Multi-option field WITHOUT checkbox
    print("\nTest 1: Multi-option field WITHOUT checkbox")
    test_text = """1. First option
2. Second option
3. Third option"""
    
    result = extractor.extract_selected_option(test_text, "Email Subject Line")
    print(f"Input: {test_text}")
    print(f"Extracted: '{result}'")
    print(f"Warnings generated: {len(extractor.warnings)}")
    if extractor.warnings:
        print(f"Warning: {extractor.warnings[-1]}")
    print("[PASS]" if len(extractor.warnings) > 0 else "[FAIL - Expected warning]")
    
    # Test 2: Multi-option field WITH checkbox
    print("\n" + "-" * 80)
    print("\nTest 2: Multi-option field WITH checkbox")
    extractor.warnings.clear()  # Reset warnings
    test_text2 = """[X] 1. First option
[ ] 2. Second option
[ ] 3. Third option"""
    
    result2 = extractor.extract_selected_option(test_text2, "Banner Headline")
    print(f"Input: {test_text2}")
    print(f"Extracted: '{result2}'")
    print(f"Warnings generated: {len(extractor.warnings)}")
    print("[PASS]" if len(extractor.warnings) == 0 else "[FAIL - Should not warn]")
    
    # Test 3: Single paragraph (no options)
    print("\n" + "-" * 80)
    print("\nTest 3: Single paragraph (no multi-option)")
    extractor.warnings.clear()  # Reset warnings
    test_text3 = """If you struggle with vitiligo and are 18 years of age or older,
you may be matched to an active clinical trial."""
    
    result3 = extractor.extract_selected_option(test_text3, "Eligibility")
    print(f"Input: {test_text3}")
    print(f"Extracted: '{result3}'")
    print(f"Warnings generated: {len(extractor.warnings)}")
    print("[PASS]" if len(extractor.warnings) == 0 else "[FAIL - Should not warn for single paragraph]")
    
    # Test 4: Format warnings display
    print("\n" + "-" * 80)
    print("\nTest 4: Warning Message Format")
    extractor.warnings.clear()
    
    # Generate multiple warnings
    extractor.extract_selected_option("1. Opt A\n2. Opt B", "Email Subject")
    extractor.extract_selected_option("1. Opt X\n2. Opt Y", "Banner Headline")
    extractor.extract_selected_option("A. Opt 1\n B. Opt 2", "Hero Image")
    
    print(extractor.format_warnings())
    print(f"\n[INFO] Generated {len(extractor.warnings)} warnings")
    print("[PASS]" if len(extractor.warnings) == 3 else "[FAIL]")
    
    # Test 5: has_warnings() method
    print("\n" + "-" * 80)
    print("\nTest 5: has_warnings() method")
    print(f"extractor.has_warnings() = {extractor.has_warnings()}")
    print("[PASS]" if extractor.has_warnings() == True else "[FAIL]")
    
    print("\n" + "=" * 80)
    print("WARNING ALERTS TESTING COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    test_warning_alerts()

