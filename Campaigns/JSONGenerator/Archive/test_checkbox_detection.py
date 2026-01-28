"""
Test checkbox and color detection features
"""

from pathlib import Path
import sys

# Test checkbox detection
def test_checkbox_detection():
    print("=" * 80)
    print("TESTING CHECKBOX DETECTION")
    print("=" * 80)
    
    # Find a real docx file to initialize with
    docx_files = list(Path(".").glob("*.docx"))
    if not docx_files:
        print("[ERROR] No .docx files found for testing")
        return
    
    from extract_to_google_sheets import CampaignExtractor
    extractor = CampaignExtractor(str(docx_files[0]))
    
    # Test 1: [X] checkbox
    test1 = """[X] 1. Consider Joining a Vitiligo Patient Registry
[ ] 2. Your Experience with Vitiligo Matters
[ ] 3. Learn About Research Opportunities"""
    
    result1 = extractor.extract_selected_option(test1)
    print("\nTest 1: [X] Checkbox")
    print(f"Input:\n{test1}")
    print(f"\nExtracted: '{result1}'")
    print(f"Expected: 'Consider Joining a Vitiligo Patient Registry'")
    print("[PASS]" if "Consider Joining" in result1 else "[FAIL]")
    
    # Test 2: Unicode checkbox
    test2 = """[X] Option 1: First choice
[ ] Option 2: Second choice
[ ] Option 3: Third choice"""
    
    result2 = extractor.extract_selected_option(test2)
    print("\n" + "-" * 80)
    print("\nTest 2: Unicode Checkbox [X]")
    print(f"Input:\n{test2}")
    print(f"\nExtracted: '{result2}'")
    print(f"Expected: 'Option 1: First choice'")
    print("[PASS]" if "Option 1" in result2 else "[FAIL]")
    
    # Test 3: Multiple selections
    test3 = """[X] 1. First selected option
[X] 2. Second selected option  
[ ] 3. Not selected"""
    
    result3 = extractor.extract_selected_option(test3)
    print("\n" + "-" * 80)
    print("\nTest 3: Multiple [X] Checkboxes")
    print(f"Input:\n{test3}")
    print(f"\nExtracted: '{result3}'")
    print(f"Expected: Both options 1 and 2")
    print("[PASS]" if "First selected" in result3 and "Second selected" in result3 else "[FAIL]")
    
    # Test 4: No checkbox - should extract first option
    test4 = """1. First option (no checkbox)
2. Second option
3. Third option"""
    
    result4 = extractor.extract_selected_option(test4)
    print("\n" + "-" * 80)
    print("\nTest 4: No Checkbox (Fallback to First)")
    print(f"Input:\n{test4}")
    print(f"\nExtracted: '{result4}'")
    print(f"Expected: 'First option (no checkbox)'")
    print("[PASS]" if "First option" in result4 else "[FAIL]")
    
    # Test 5: Single paragraph (no options) - should extract all
    test5 = """If you struggle with vitiligo and are 18 years of age or older, 
you may be matched to an active clinical trial."""
    
    result5 = extractor.extract_selected_option(test5)
    print("\n" + "-" * 80)
    print("\nTest 5: Single Paragraph (No Options)")
    print(f"Input:\n{test5}")
    print(f"\nExtracted: '{result5}'")
    print(f"Expected: Full text")
    print("[PASS]" if "18 years of age" in result5 else "[FAIL]")
    
    # Test 6: Checkmark variations
    test6 = """[X] Option with checkmark
[ ] Option without checkmark"""
    
    result6 = extractor.extract_selected_option(test6)
    print("\n" + "-" * 80)
    print("\nTest 6: Checkmark Variation")
    print(f"Input:\n{test6}")
    print(f"\nExtracted: '{result6}'")
    print(f"Expected: 'Option with checkmark'")
    print("[PASS]" if "Option with checkmark" in result6 else "[FAIL]")
    
    print("\n" + "=" * 80)
    print("CHECKBOX DETECTION TESTS COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    test_checkbox_detection()

