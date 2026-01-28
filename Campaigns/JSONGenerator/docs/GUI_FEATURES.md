# GUI Features - Campaign Content Extractor

## 🖥️ What You'll See in the GUI

### 1. Document Selection
- **Browse button** to select your Word document
- Auto-finds `.docx` files in current folder

### 2. ✨ NEW: Assess Document Button

**The game-changer for multi-email documents!**

Click "Assess Document" to:
- 📊 Scan document for email templates
- 🔍 Detect email headers (e.g., "Email 1: Long-form email")
- ✨ Dynamically create Campaign Name fields
- 📋 One field per email template found!

**Example:**
```
Before Assess:
[No fields visible]

After Assess (3 emails found):
✅ Found 3 email templates:
   • Email 1: Long-form email
   • Email 2: Short-form reminder
   • Email 3: Final follow-up

📧 Email 1: Long-form email
   Campaign Name: [Takeda Vitiligo WeConnect________________]

📧 Email 2: Short-form reminder
   Campaign Name: [Takeda Vitiligo SMS Campaign____________]

📧 Email 3: Final follow-up
   Campaign Name: [Takeda Vitiligo Final CTA______________]
```

**Benefits:**
- ✅ Different Campaign Names per email
- ✅ See exactly what's in your document
- ✅ Smart defaults pre-filled
- ✅ Edit any field individually
- ✅ Perfect for multi-template documents

**See `ASSESS_DOCUMENT_FEATURE.md` for complete guide!**

---

### 3. Dynamic Campaign Name Fields ✍️

After assessing, you get **one Campaign Name field per email template**:

**For Single Email:**
```
📧 Long-form email
Campaign Name: [Takeda Vitiligo WeConnect]
```

**For Multiple Emails:**
```
📧 Email 1: Long-form email
Campaign Name: [Takeda Vitiligo WeConnect]

📧 Email 2: Short reminder
Campaign Name: [Takeda Vitiligo SMS Campaign]
```

**You have full control!**
- Edit any Campaign Name individually
- Use same name for all (just keep defaults)
- Use different names per email (customize each)
- Message Names are auto-extracted from headers

### 3. User Input Fields ✍️

You still need to fill in:

| Field | Example | Purpose |
|-------|---------|---------|
| Language | `en-us` | English or Spanish (`en-es`) |
| URL/UTM | `https://...` | Campaign tracking URL |
| Sponsor Name | `Takeda` | Sponsor brand name |

### 4. Status Indicators ✅

The GUI shows real-time status:

- **✓ Color Detection** - GREEN text = Variable content, RED text = Standard (skipped)
- **✓ Checkbox Detection** - [X] markers identify selected options
- **⚠️ Warning Alerts** - Pop-up if checkboxes are missing

### 5. Output Preview 📄

After extraction, you'll see:
- Number of email templates extracted
- Preview of first row data
- Any warnings about missing selections
- File save locations

### 6. One-Click Copy 📋

The extracted content is **automatically copied to your clipboard**!

Just:
1. Click "Extract Content"
2. Open Google Sheets
3. Press `Ctrl+V` (or `Cmd+V` on Mac)
4. Done! ✨

---

## 🎯 Why Campaign Name & Message Name Are Manual Entry

**Benefits of Manual Entry:**

✅ **Full Control** - You decide the naming, not the document
✅ **Consistency** - Use your own standardized naming across campaigns  
✅ **Flexibility** - Same document, different names for testing/variants
✅ **No Dependency** - Works even if document headers aren't formatted perfectly

**Common Naming Examples:**

| Campaign Name | Message Name |
|---------------|--------------|
| Takeda Vitiligo WeConnect | Long-form email |
| Takeda Vitiligo WeConnect | Short-form reminder |
| Pfizer Diabetes Q1 2026 | Initial outreach |
| Novartis Heart Trial | Follow-up message |

**Pro Tip:** Use descriptive Message Names - they appear in warning alerts to help you identify which template needs attention!

---

## 🚀 Quick Start

1. Double-click `Extract_Campaign_Content_GUI.bat`
2. Browse to your Word document
3. **✨ NEW: Click "Assess Document"** to scan for email templates
4. **Edit Campaign Names** for each email (one field per template!)
5. Fill in Language, URL, and Sponsor
6. Click "Extract Content"
7. Go to Google Sheets and press `Ctrl+V`

That's it! Each email gets its own Campaign Name and auto-extracted Message Name! 🎉

**Pro Tip:** The Assess button creates dynamic fields based on what's in your document!

