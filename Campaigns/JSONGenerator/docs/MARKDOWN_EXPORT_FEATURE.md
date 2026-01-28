# ✨ Markdown Export with Source Formatting

## 🎯 What's New

The extractor now **preserves source formatting** and exports to **Markdown format**!

---

## 📋 What Gets Preserved

### Formatting from Word Document:

- **Bold text** → `**bold**`
- *Italic text* → `*italic*`
- ***Bold italic*** → `***bold italic***`
- _Underlined text_ → `_underlined_`
- Bulleted lists → `- item`
- Numbered lists → `1. item`
- Paragraphs → Separate blocks

---

## 📂 Output Files

### When You Extract Content, You Get 3 Files:

**1. TSV File (Google Sheets)**
```
filename_for_google_sheets.tsv
```
- Tab-separated values
- Ready to paste into Google Sheets
- **Best for:** Spreadsheet import

**2. JSON File (Structured Data)**
```
filename_extracted.json
```
- Structured data format
- All fields in JSON
- **Best for:** Programmatic access

**3. Markdown File (Formatted) ✨ NEW!**
```
filename_formatted.md
```
- Preserves bold, italic, lists
- Human-readable format
- **Best for:** Documentation, review, sharing

---

## 📖 Markdown File Structure

### Example Output:

```markdown
# Campaign Content Export

## Email 1: Long-form email

**Campaign:** Takeda Vitiligo WeConnect

---

### Email Subject Line

**Your Experience with Vitiligo Matters**

### Language

en-us

### Hero Image (URL)

Option 1

### Banner Headline

**Join the WeConnect Registry** - *Make Your Voice Heard*

### Study Information

Dear Participant,

We invite you to join our **vitiligo research study**. This important work will help:

- Improve treatment options
- Understand patient experiences
- Advance medical knowledge

### CTA 1

**Learn more** [INSERT CTA BUTTON]

### CTA 2

***Enroll Today***

Click here to get started

### Closing

Thank you for your interest.

*Sincerely,*
**Research Team**

---

```

---

## 🎨 Formatting Examples

### How Word Formatting Converts to Markdown:

| Word Document | Markdown Output |
|---------------|-----------------|
| **Bold text** | `**Bold text**` |
| *Italic text* | `*Italic text*` |
| **_Bold italic_** | `***Bold italic***` |
| <u>Underline</u> | `_Underline_` |
| • Bullet | `- Bullet` |
| 1. Numbered | `1. Numbered` |

### Real Example:

**Word Document:**
```
Study Benefits:
• Improved treatment options
• Better understanding
• Contribute to research
```

**Markdown Output:**
```markdown
Study Benefits:
- Improved treatment options
- Better understanding
- Contribute to research
```

---

## 🚀 How to Use

### Automatic (No Extra Steps!)

1. **Run extraction as usual** (GUI or CLI)
2. **Markdown file is automatically created**
3. **Find it in the same folder** as TSV/JSON

### GUI:
```
[+] TSV file created: Campaign_for_google_sheets.tsv
[+] JSON file created: Campaign_extracted.json
[+] Markdown file created: Campaign_formatted.md  ← NEW!
```

### CLI:
```
[+] Also saved as JSON: Campaign_extracted.json
[+] Also saved as Markdown: Campaign_formatted.md  ← NEW!
```

---

## 💡 Use Cases

### 1. **Content Review**
- Share markdown file with stakeholders
- Easy to read in GitHub, Notion, or any markdown viewer
- Preserves formatting for accurate review

### 2. **Documentation**
- Keep formatted copy of campaign content
- Archive with proper formatting
- Easy to search and reference

### 3. **Collaboration**
- Share via Slack, Teams, or email
- Colleagues can read without Word/Excel
- Formatting preserved for clarity

### 4. **Version Control**
- Track changes in Git
- Readable diffs
- Better than binary Word files

### 5. **Publishing**
- Convert to HTML easily
- Use in static site generators
- Present to clients in formatted way

---

## 🔍 Technical Details

### New Methods Added:

**1. `extract_text_with_formatting(cell)` in CampaignExtractor**
```python
def extract_text_with_formatting(self, cell) -> str:
    """
    Extract text from cell with markdown formatting preserved.
    Converts Word formatting to Markdown:
    - Bold → **text**
    - Italic → *text*
    - Lists → - item or 1. item
    """
```

**Features:**
- Detects bold, italic, underline from Word
- Converts to markdown syntax
- Preserves list formatting
- Handles mixed formatting (bold+italic)

**2. `to_markdown(rows, output_file)` in GoogleSheetsExporter**
```python
def to_markdown(self, rows: List[Dict[str, str]], output_file: str) -> str:
    """Export to Markdown format with preserved formatting"""
```

**Features:**
- Creates structured markdown document
- One section per email
- Headings for each field
- Proper markdown hierarchy

---

## 📊 File Comparison

### TSV (Spreadsheet):
```
Campaign Name	Message Name	Email Subject Line
Takeda Vitiligo	Email 1	Your Experience Matters
```
- ✅ Best for: Google Sheets import
- ✅ Format: Tab-separated
- ❌ No formatting preserved

### JSON (Data):
```json
{
  "Campaign Name": "Takeda Vitiligo",
  "Message Name": "Email 1",
  "Email Subject Line": "Your Experience Matters"
}
```
- ✅ Best for: Programming
- ✅ Format: Structured data
- ❌ Not human-friendly

### Markdown (Formatted): ✨
```markdown
## Email 1: Long-form email

**Campaign:** Takeda Vitiligo

### Email Subject Line

**Your Experience** with Vitiligo Matters
```
- ✅ Best for: Human reading
- ✅ Format: Human-readable
- ✅ **Formatting preserved!**

---

## 🎨 Viewing Markdown Files

### Desktop Apps:
- **Typora** - Beautiful markdown editor
- **Obsidian** - Knowledge base viewer
- **Visual Studio Code** - Built-in preview

### Online:
- **GitHub** - Auto-renders markdown
- **GitLab** - Auto-renders markdown
- **Notion** - Import markdown files

### Windows:
- **Notepad++** - Syntax highlighting
- **VS Code** - Best preview
- **Any text editor** - Still readable!

---

## 🔧 Customization

### Want Different Markdown Styles?

Edit the `to_markdown()` method in `extract_to_google_sheets.py`:

```python
# Change heading levels
f.write(f"## Email {idx}: {message_name}\n\n")  # H2
# To:
f.write(f"# Email {idx}: {message_name}\n\n")   # H1

# Add metadata table
f.write(f"| Field | Value |\n")
f.write(f"|-------|-------|\n")
f.write(f"| Campaign | {campaign_name} |\n\n")

# Add custom sections
f.write(f"### Notes\n\n")
f.write(f"_Add your review notes here_\n\n")
```

---

## 📝 Example Workflow

### Step-by-Step:

1. **Extract content** from Word doc
2. **Get 3 output files:**
   - TSV → Paste into Google Sheets
   - JSON → Use in scripts
   - **Markdown → Share for review** ✨

3. **Share markdown file** with team:
   - Email attachment
   - Slack/Teams message
   - GitHub repository
   - Notion page

4. **Receive feedback** (easy to read!)

5. **Make updates** in Word doc

6. **Re-extract** → New markdown with changes

---

## ✅ Benefits

| Aspect | Benefit |
|--------|---------|
| **Formatting** | Bold, italic, lists preserved |
| **Readability** | Human-friendly format |
| **Portability** | Works everywhere (GitHub, Notion, etc.) |
| **Searchable** | Plain text, easy to grep/search |
| **Version Control** | Git-friendly, readable diffs |
| **Collaboration** | Share without Word/Excel |
| **Documentation** | Archive with proper formatting |

---

## 🎉 Summary

**Before:** Only TSV and JSON (no formatting)

**After:** TSV + JSON + **Markdown with formatting!**

**What You Get:**
- ✅ **TSV** for Google Sheets
- ✅ **JSON** for programming
- ✅ **Markdown** for humans ← NEW!

**Formatting Preserved:**
- ✅ Bold text
- ✅ Italic text
- ✅ Lists
- ✅ Paragraphs
- ✅ Mixed styles

**Your content extraction is now even more powerful and shareable!** 📝✨

---

## 💻 Quick Example

**Run extraction:**
```bash
> python extract_to_google_sheets.py
```

**Output:**
```
[+] TSV file created: Campaign_for_google_sheets.tsv
[+] JSON file created: Campaign_extracted.json
[+] Markdown file created: Campaign_formatted.md  ← Open this!
```

**Open `Campaign_formatted.md` in any markdown viewer and see your formatted content!** 🎨

