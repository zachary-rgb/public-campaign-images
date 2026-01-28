# Warning Alerts for Missing Checkbox Selections

## 🚨 New Feature: Automatic Warning Detection

The extraction system now **automatically detects** when multi-option fields don't have a checkbox `[X]` marked and alerts you!

---

## ✅ How It Works

### When Extracting Content:

The system checks each field with multiple options (1., 2., 3., etc.):

| Scenario | What Happens |
|----------|--------------|
| **Has `[X]` checkbox** | ✅ Extracts selected option(s) - No warning |
| **No `[X]` checkbox** | ⚠️ Warns you + Uses first option as default |
| **Single paragraph** | ✅ Extracts all text - No warning |

---

## 📋 Example Scenarios

### ✅ Scenario 1: Proper Selection (No Warning)

**In Word Document:**
```
EMAIL SUBJECT LINE OPTIONS
[X] 1. Consider Joining a Vitiligo Patient Registry
[ ] 2. Your Experience with Vitiligo Matters
[ ] 3. Learn About Research Opportunities
```

**Result:**
- ✅ Extracts: "Consider Joining a Vitiligo Patient Registry"
- ✅ No warning
- ✅ Success!

---

### ⚠️ Scenario 2: Missing Selection (Warning!)

**In Word Document:**
```
EMAIL SUBJECT LINE OPTIONS
1. Consider Joining a Vitiligo Patient Registry
2. Your Experience with Vitiligo Matters
3. Learn About Research Opportunities
```

**Result:**
- ⚠️ **WARNING ALERT:** "No checkbox found for 'Email Subject Line'"
- ⚠️ Action: Using first option as default
- ⚠️ Extracted: "Consider Joining a Vitiligo Patient Registry" (first option)

**Warning Display:**
```
================================================================================
WARNING: Missing Checkbox Selections
================================================================================

The following fields have multiple options but no checkbox [X] was found:

  1. Email Subject Line
     > Using first option as default

--------------------------------------------------------------------------------
Recommendation: Review these fields in the Word document and add [X] to mark
the preferred option, then run the extraction again.
================================================================================
```

---

### ✅ Scenario 3: Single Paragraph (No Warning)

**In Word Document:**
```
ELIGIBILITY
If you struggle with vitiligo and are 18 years of age or older,
you may be matched to an active clinical trial.
```

**Result:**
- ✅ Extracts: Full paragraph
- ✅ No warning (not a multi-option field)
- ✅ Correct behavior!

---

## 🖥️ Where You'll See Warnings

### 1. In the GUI (Pop-up Dialog)

When using `Extract_Campaign_Content_GUI.bat`:

```
┌────────────────────────────────────────────┐
│  ⚠️ Missing Selections Detected            │
│                                            │
│  WARNING: Missing Checkbox Selections!     │
│                                            │
│  These fields have multiple options but    │
│  no [X] checkbox:                          │
│                                            │
│  • Email Subject Line                      │
│  • Banner Headline                         │
│                                            │
│  Action Taken: Using first option          │
│  as default.                               │
│                                            │
│  Recommendation: Add [X] to mark your      │
│  preferred options in the Word document,   │
│  then extract again.                       │
│                                            │
│            [ OK ]                           │
└────────────────────────────────────────────┘
```

### 2. In the GUI Output Window

The warnings also appear in the scrolling output:

```
[SUCCESS] Extracted 1 email template(s)

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
WARNING: Missing Checkbox Selections Detected!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  [!] Email Subject Line
      > Using first option as default
  [!] Banner Headline
      > Using first option as default

Recommendation: Add [X] to mark selections in Word doc, then re-extract.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```

### 3. In Command Line

When using `Extract_Campaign_Content.bat`:

```
[+] Extracted 1 email template(s)

================================================================================
WARNING: Missing Checkbox Selections
================================================================================

The following fields have multiple options but no checkbox [X] was found:

  1. Email Subject Line
     > Using first option as default
  2. Banner Headline
     > Using first option as default

--------------------------------------------------------------------------------
Recommendation: Review these fields in the Word document and add [X] to mark
the preferred option, then run the extraction again.
================================================================================
```

---

## 🎯 Which Fields Trigger Warnings?

Warnings are only generated for fields that:
1. ✅ Have multiple options (numbered 1., 2., 3. or lettered A., B., C.)
2. ✅ Are marked as GREEN (variable content)
3. ❌ Don't have any `[X]` checkbox

### Fields That Can Trigger Warnings:

- **Email Subject Line Options** (if multiple)
- **Banner Headline Options** (if multiple)
- **Hero Space Image Options** (if multiple)
- **CTA Options** (if multiple)

### Fields That WON'T Trigger Warnings:

- **Eligibility** (single paragraph)
- **Study Information** (single paragraph)
- **What to Expect** (single paragraph)
- **Closing** (single paragraph)
- **RED sections** (Walgreens standard - skipped anyway)

---

## 🔧 What To Do When You See a Warning

### Option 1: Add Checkboxes (Recommended)

1. **Open the Word document**
2. **Find the fields mentioned in the warning**
3. **Add `[X]` before your preferred option:**
   ```
   [X] 1. Your preferred option
   [ ] 2. Not this one
   [ ] 3. Not this one either
   ```
4. **Save the document**
5. **Run the extractor again**
6. ✅ No more warnings!

### Option 2: Accept Default (First Option)

If the first option is what you want anyway:
1. **Proceed with the extraction**
2. The first option will be used
3. Content still gets pasted into Google Sheets
4. ✅ Everything works, but you should still add `[X]` for clarity

### Option 3: Manually Edit in Google Sheets

If you see the warning but want to proceed:
1. **Let it extract** (uses first option)
2. **Paste into Google Sheets**
3. **Manually change** the field to your preferred option
4. ⚠️ Not recommended - error-prone and more work

---

## 📊 Test Results

We've tested the warning system thoroughly:

| Test Scenario | Result |
|--------------|--------|
| Multi-option WITH `[X]` | ✅ PASS - No warning |
| Multi-option WITHOUT `[X]` | ✅ PASS - Warning generated |
| Single paragraph (no options) | ✅ PASS - No warning |
| Multiple missing selections | ✅ PASS - All warnings shown |
| Warning message format | ✅ PASS - Clear and helpful |

**Status: 5/5 tests passed!** ✅

---

## 💡 Benefits of This Feature

1. **Quality Control** - Catch missing selections before pasting into Google Sheets
2. **Transparency** - Know exactly which fields defaulted to first option
3. **Traceability** - Clear documentation of what was extracted
4. **Error Prevention** - Reduce manual corrections in Google Sheets
5. **User-Friendly** - Clear warnings with actionable recommendations

---

## 🎓 Summary

| Situation | Warning? | What Gets Extracted |
|-----------|----------|-------------------|
| Multi-option field WITH `[X]` | ❌ No | Selected option(s) |
| Multi-option field WITHOUT `[X]` | ⚠️ Yes | First option (default) |
| Single paragraph field | ❌ No | All text |
| RED section (standard) | ❌ No | Skipped entirely |

---

## 🚀 Try It Now!

1. **Create a test Word doc** with multi-option field (no checkboxes)
2. **Run the extractor**
3. **See the warning** in action!
4. **Add `[X]` checkboxes**
5. **Run again** - no warnings!

---

## 📝 Related Documentation

- **CHECKBOX_GUIDE.md** - How to use checkboxes
- **WHATS_NEW.md** - All new features summary
- **test_warning_alerts.py** - Test suite for this feature

---

**The warning system is live and ready to help ensure accurate extractions!** ✨

