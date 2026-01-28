# Checkbox & Color Detection Guide

## 🎨 How the Enhanced Extractor Works

The extraction script now automatically detects:
1. **GREEN text** = Variable content (extracts based on selection)
2. **RED text** = Walgreens standard content (skipped/not extracted)
3. **Checkboxes** `[X]` = Selected options

---

## ✅ Preparing Your Word Document

### Step 1: Understand the Colors

In your Walgreens Word document:

| Color | Meaning | What Script Does |
|-------|---------|-----------------|
| **GREEN** | Variable content - sponsor chooses | Looks for `[X]` checkbox or extracts first option |
| **RED** | Walgreens standard - not editable | Skips this section completely |
| **BLACK** | Neutral content | Extracts as-is |

### Step 2: Mark Selected Options with Checkboxes

For sections with multiple options (like Email Subject, Banner Headline), the sponsor should mark their choice:

#### ✅ Supported Checkbox Formats:

```
[X] Option 1 - Selected
[x] Option 2 - Selected (lowercase x works too)
☑ Option 3 - Selected (Unicode checkbox)
✓ Option 4 - Selected (Checkmark)
✔ Option 5 - Selected (Heavy checkmark)
```

#### Example in Word Document:

```
EMAIL SUBJECT LINE OPTIONS (GREEN TEXT)
[X] 1. Consider Joining a Vitiligo Patient Registry
[ ] 2. Your Experience with Vitiligo Matters—Join the WeConnect Registry
[ ] 3. Learn About Research Opportunities for Vitiligo
```

**What gets extracted:** "Consider Joining a Vitiligo Patient Registry"

---

## 📋 Complete Example

### In Your Word Document:

```
┌─────────────────────────────────────────────────────────┐
│ EMAIL SUBJECT LINE OPTIONS                              │ ← GREEN TEXT
│   [X] 1. Consider Joining a Vitiligo Patient Registry  │ ← SELECTED
│   [ ] 2. Your Experience with Vitiligo Matters          │
│   [ ] 3. Learn About Research Opportunities             │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ SALUTATION                                              │ ← RED TEXT
│   Dear [Patient First Name]                             │ ← SKIPPED (Standard)
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ BANNER HEADLINE OPTIONS                                 │ ← GREEN TEXT
│   [X] 1. Join a Patient Registry for Adults Living...  │ ← SELECTED
│   [ ] 2. Vitiligo: Empower Yourself with Knowledge     │
│   [ ] 3. Support Vitiligo Research                     │
│   [ ] 4. Help us advance Vitiligo treatment            │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ STUDY INFORMATION                                       │ ← GREEN TEXT
│   Living with vitiligo can be a deeply personal        │ ← NO CHECKBOX
│   journey — one that affects more than just the skin.  │    (Single block)
│   We understand the challenges...                       │ ← ALL TEXT EXTRACTED
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ CTA 1 (Optional)                                        │ ← GREEN TEXT
│   Learn more [INSERT CTA BUTTON]                        │ ← ALL TEXT EXTRACTED
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ ELIGIBILITY                                             │ ← GREEN TEXT
│   If you struggle with vitiligo and are 18 years       │ ← NO CHECKBOX
│   of age or older, you may be matched to an active     │    (Single paragraph)
│   clinical trial.                                       │ ← ALL TEXT EXTRACTED
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ HERO SPACE IMAGE OPTIONS                                │ ← GREEN TEXT
│   [ ] Option 1                                          │
│   [X] Option 2: Client Preferred                        │ ← SELECTED
│   [ ] Option 3                                          │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ END MATTER (cannot be edited)                           │ ← RED TEXT
│   The safety and scientific validity of a clinical...  │ ← SKIPPED (Standard)
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 What Gets Extracted

From the example above:

| Section | Extracted Content |
|---------|------------------|
| Email Subject | "Consider Joining a Vitiligo Patient Registry" |
| Salutation | *Skipped (RED)* |
| Banner Headline | "Join a Patient Registry for Adults Living..." |
| Study Information | *Full paragraph* (all text) |
| CTA 1 | "Learn more [INSERT CTA BUTTON]" |
| Eligibility | *Full paragraph* (all text) |
| Hero Image | "Option 2: Client Preferred" |
| End Matter | *Skipped (RED)* |

---

## 📝 Instructions for Content Reviewers

### For Sections with Multiple Options (GREEN):

1. **Look for numbered or bulleted lists**
2. **Type `[X]` before your selected option**
3. **Leave `[ ]` for non-selected options**

Example:
```
[X] 1. Option I want
[ ] 2. Option I don't want
[ ] 3. Another option I don't want
```

### For Sections with Single Text Block (GREEN):

Just leave the text as-is. The entire block will be extracted.

Example:
```
ELIGIBILITY (GREEN)
If you struggle with vitiligo and are 18 years of age or older, 
you may be matched to an active clinical trial.
```
→ All of this text is extracted ✓

### For RED Sections:

Don't edit or mark anything. These are Walgreens standards and will be automatically skipped.

---

## 🔍 How to Check Text Color in Word

1. Select the section label text
2. Look at the Font Color button in the ribbon
3. **GREEN** = Variable content
4. **RED** = Standard content (will be skipped)

---

## ⚠️ Important Notes

### Multiple Selections

You can select **multiple options** by marking several with `[X]`:

```
[X] 1. First choice
[X] 2. Second choice also good
[ ] 3. Not this one
```

Both options 1 and 2 will be extracted and combined.

### No Checkbox = First Option

If you forget to add checkboxes to a GREEN multi-option section, the script will automatically use the **first option** (original behavior).

### Case Insensitive

These all work:
- `[X]` (uppercase)
- `[x]` (lowercase)
- `☑` (Unicode checkbox)
- `✓` or `✔` (checkmarks)

---

## ✨ Summary

| Field Type | Color | Has Options? | How to Mark | What Gets Extracted |
|------------|-------|--------------|-------------|-------------------|
| Email Subject | GREEN | Yes (1,2,3) | Add `[X]` | Selected option only |
| Banner Headline | GREEN | Yes (1,2,3,4) | Add `[X]` | Selected option only |
| Study Information | GREEN | No (paragraph) | Nothing | All text |
| CTA 1 | GREEN | No (single line) | Nothing | All text |
| Eligibility | GREEN | No (paragraph) | Nothing | All text |
| What to Expect | GREEN | No (paragraph) | Nothing | All text |
| CTA 2 | GREEN | No (single line) | Nothing | All text |
| Closing | GREEN | No (paragraph) | Nothing | All text |
| Hero Image | GREEN | Yes (Options) | Add `[X]` | Selected option only |
| Salutation | RED | N/A | Nothing | **Skipped** |
| End Matter | RED | N/A | Nothing | **Skipped** |

---

## 🚀 Ready to Extract!

Once your Word document has:
1. ✅ Checkboxes `[X]` marking selected options
2. ✅ GREEN sections are ready for extraction
3. ✅ RED sections are left as-is

Just double-click `Extract_Campaign_Content_GUI.bat` and the script will:
- ✅ Skip all RED sections
- ✅ Extract selected options from GREEN multi-option fields
- ✅ Extract all text from GREEN single-paragraph fields
- ✅ Copy everything to clipboard ready for Google Sheets!

