# Quick Start Guide - Campaign Content Extractor

## ✅ READY TO USE!

All dependencies are installed and the extraction is working!

## 🌟 SIMPLEST WAYS TO USE (No Command Line!)

### Option 1: GUI - Just Double-Click! (EASIEST!)

1. **Double-click** `Extract_Campaign_Content_GUI.bat`
2. A friendly window opens
3. **NEW!** Click "Assess Document" to scan for email templates
4. **Edit Campaign Names** - one field per email template!
5. Fill in Language, URL, and Sponsor details
6. Click "Extract Content" button
7. **Done!** Go to Google Sheets and press **Ctrl+V**

**The GUI Shows:**
- ✨ **NEW: Assess Document** button - scans & creates dynamic fields
- ✍️ Campaign Name fields (one per email, fully editable)
- 📋 Message Names (auto-extracted from document)
- ✅ Color detection (GREEN=Variable, RED=Standard)
- ✅ Checkbox detection ([X] markers)
- ⚠️ Warning alerts if selections are missing

**Best for:** First-time users, visual interface preferred, full control over naming, multiple email templates

**Pro Tip:** Click "Assess Document" first to see how many emails are in your document!

### Option 2: Batch File - Double-Click!

1. **Double-click** `Extract_Campaign_Content.bat`
2. Answer the prompts in the window
3. Press any key to close
4. Go to Google Sheets and press **Ctrl+V**

**Best for:** Quick repeat extractions

### Option 3: Button in Word Document

Add an extract button right in your Word doc!
See `SIMPLE_USAGE_GUIDE.md` for setup instructions.

**Best for:** Extracting while editing the Word doc

---

## 💻 Advanced: Command Line Mode

### Interactive Mode

```bash
cd JSONGenerator
python extract_to_google_sheets.py
```

The script will:
1. Find your Word document automatically
2. Ask for campaign metadata (name, language, URL, sponsor)
3. Extract all content
4. **Copy directly to your clipboard**
5. Create TSV and JSON files

Then just **Ctrl+V** in Google Sheets!

### Option 2: Test Mode (No prompts)

```bash
cd JSONGenerator
python test_extraction.py
```

Uses predefined test metadata and extracts immediately.

## What Gets Extracted

From your Word document table:

| Word Doc Section | Google Sheets Column |
|-----------------|---------------------|
| Email Subject Line Options | Email Subject (first option) |
| Banner Headline Options | Banner Headline (first option) |
| Study Information | Study Information (full text) |
| CTA 1 | CTA 1 |
| CTA 2 | CTA 2 |
| Eligibility | Eligibility |
| What to Expect | What to Expect |
| Closing | Closing |
| Optional Resource | Optional Resource |
| Hero Space Image Options | Hero Image (URL) |

Plus your metadata:
- Campaign Name
- Message Name
- Language
- URL/UTM
- End Matter (Enter Sponsor)

## Output Files

Each run creates:

1. **`*_for_google_sheets.tsv`** - Ready to paste into Google Sheets
2. **`*_extracted.json`** - Structured data for reference
3. **Clipboard** - Automatically copied, just paste!

## Example Output

From the test run, we extracted:

```
Campaign Name: Takeda Vitiligo WeConnect
Message Name: Email 1
Language: en-us
Email Subject: Reminder: Enrollment is open for vitiligo clinical trials
Banner Headline: Learn about clinical trials that may help vitiligo treatments
Study Information: Living with vitiligo can be challenging...
CTA 1: Learn more [INSERT CTA BUTTON]
Eligibility: If you struggle with vitiligo and are 18 years or older...
...and more
```

## Next Steps After Pasting

1. ✅ Paste content into Google Sheets
2. 📝 Review extracted content
3. 🖼️ Add actual Hero Image URLs (currently shows "Option 1")
4. 🔗 Verify URL/UTM if needed
5. ☑️ Check the box in Column A to generate JSON!

## Troubleshooting

### No clipboard copy?
- Content is still in the TSV file
- Open `*_for_google_sheets.tsv` and copy manually

### Content looks wrong?
- Check Word doc uses table format (left = label, right = content)
- See `TEST_extraction_output.json` to verify what was extracted

### Multiple emails in one doc?
- The script automatically detects "Email 1:", "Email 2:", etc.
- Each becomes a separate row in the output

## Files Created

✅ `extract_to_google_sheets.py` - Main extraction script
✅ `test_extraction.py` - Quick test script
✅ `requirements.txt` - Python dependencies (already installed)
✅ `README_EXTRACTOR.md` - Full documentation
✅ `QUICK_START.md` - This file

## Need Help?

Check the full documentation: `README_EXTRACTOR.md`

