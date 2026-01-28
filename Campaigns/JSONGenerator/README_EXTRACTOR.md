# Campaign Content Extractor for Google Sheets

Extracts Walgreens campaign content from Word documents and prepares it for direct paste into Google Sheets.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Extractor

```bash
cd JSONGenerator
python extract_to_google_sheets.py
```

### 3. Paste into Google Sheets

The script will:
- ✅ Extract all content from your Word doc
- ✅ Map it to your spreadsheet columns
- ✅ Copy to clipboard automatically
- ✅ Create a TSV file for manual import

Just press **Ctrl+V** (or **Cmd+V** on Mac) in your Google Sheet!

## Features

### 🔄 Automatic Content Extraction

Extracts from Word doc table structure:
- Email Subject Lines (takes first option)
- Banner Headlines (takes first option)
- Study Information
- CTAs (buttons)
- Eligibility
- What to Expect
- Closing
- Optional Resources
- Hero Image references

### 📧 Multiple Email Support

If your Word doc contains multiple email templates (Email 1, Email 2, etc.), the script extracts them all as separate rows.

### 🎯 Auto-Extract Campaign & Message Names

The system automatically extracts **Campaign Name** and **Message Name** from document headers:
- Looks for patterns like "Email 1: Long-form email"
- Campaign Name = "Email 1"
- Message Name = "Long-form email"
- **GUI displays both fields** in real-time during extraction
- No manual entry needed for these fields!

### 📋 Google Sheets Ready

Output format matches your campaign spreadsheet:
- Campaign Name (auto-extracted)
- Message Name (auto-extracted)
- Language
- Email Subject
- Banner Headline
- Study Information
- CTA 1
- Eligibility
- What to Expect
- CTA 2
- Closing
- Optional Resource
- Hero Image (URL)
- URL/UTM
- End Matter (Enter Sponsor)

### 🎯 Smart Options Handling

For fields with multiple options (subject lines, headlines), the script:
- Recognizes numbered lists (1., 2., 3.)
- Recognizes lettered lists (A., B., C.)
- Recognizes bullet points (-, •, ●)
- Automatically selects the first option

## Column Mapping

The script automatically maps these Word doc sections:

| Word Document Label | Google Sheet Column |
|-------------------|-------------------|
| Email Subject Line Options | Email Subject |
| Banner Headline Options | Banner Headline |
| Study Information | Study Information |
| CTA 1 / Button 1 | CTA 1 |
| CTA 2 / Button 2 | CTA 2 |
| Eligibility | Eligibility |
| What to Expect | What to Expect |
| Closing | Closing |
| Optional Resource | Optional Resource |
| Hero Space Image Options | Hero Image (URL) |

## Output Files

The script creates:

1. **`[filename]_for_google_sheets.tsv`**
   - Tab-separated values file
   - Open in Excel/Sheets and copy

2. **`[filename]_extracted.json`**
   - JSON format for reference
   - Contains all extracted data

3. **Clipboard** (automatic)
   - Ready to paste directly into Google Sheets

## Usage Examples

### Basic Usage

```bash
python extract_to_google_sheets.py
```

Follow the prompts to:
- Select Word document
- Add campaign metadata (optional)
- Get content copied to clipboard

### Adding Metadata

The script will ask for:
- **Campaign Name**: e.g., "Takeda Vitiligo"
- **Language**: `en-us` or `en-es`
- **URL/UTM**: Campaign tracking URL
- **Sponsor Name**: For end matter (e.g., "Takeda")

This metadata is added to all extracted rows.

## Troubleshooting

### "No .docx files found"

Make sure your Word document is in the `JSONGenerator` folder, or provide the full path when prompted.

### Clipboard not working

If clipboard copy fails:
1. Install pyperclip: `pip install pyperclip`
2. Or use the TSV file generated
3. Open TSV file and copy/paste manually

### Missing content

Check that your Word doc uses a table structure with:
- Left column: Section labels (e.g., "STUDY INFORMATION")
- Right column: Content

### Special characters display incorrectly

The script uses UTF-8 encoding. Make sure:
- Your Word doc is saved properly
- Google Sheets is set to UTF-8 import

## Integration with JSON Generator

After pasting into Google Sheets:

1. Review the pasted row(s)
2. Add Hero Image URLs if needed
3. Verify all content is correct
4. Check the box in Column A
5. Your `campaign_JSON_script_v1.1.txt` will generate the JSON!

## Support

For issues or questions, check:
- Word doc table structure matches expected format
- All dependencies are installed
- Using Python 3.7 or higher

