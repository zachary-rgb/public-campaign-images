# Simple Usage Guide - No Command Line Required!

## 🎯 Three Super Simple Ways to Extract Content

You don't need to know anything about command lines or terminals. Just pick one of these easy methods:

---

## ⭐ Method 1: Double-Click GUI (EASIEST!)

### Steps:
1. **Double-click** `Extract_Campaign_Content_GUI.bat`
2. A friendly window opens
3. Fill in the campaign details
4. Click "Extract Content"
5. **Done!** Content is automatically copied to clipboard
6. Go to Google Sheets and press **Ctrl+V**

### Screenshot of what you'll see:
```
┌─────────────────────────────────────────────┐
│  Campaign Content Extractor                 │
│                                             │
│  1. Select Word Document                    │
│    [Your_Document.docx        ] [Browse...] │
│                                             │
│  2. Campaign Metadata                       │
│    Campaign Name: [Takeda Vitiligo...]      │
│    Language:      [en-us ▼]                 │
│    URL/UTM:       [https://...]             │
│    Sponsor Name:  [Takeda]                  │
│                                             │
│         [ 3. Extract Content ]              │
│                                             │
│  Output:                                    │
│  ┌─────────────────────────────────────┐   │
│  │ [Extraction results appear here]    │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

**Advantages:**
- ✅ Most user-friendly
- ✅ See all options at once
- ✅ No typing required
- ✅ Works by just double-clicking

---

## Method 2: Double-Click Batch File

### Steps:
1. **Double-click** `Extract_Campaign_Content.bat`
2. Answer a few questions in the window that opens
3. Content is extracted and copied to clipboard
4. Press any key to close
5. Go to Google Sheets and press **Ctrl+V**

**Advantages:**
- ✅ Super simple - just double-click
- ✅ No GUI needed
- ✅ Quick for repeat use

---

## Method 3: Extract Button in Word Document

You can add an "Extract" button right inside your Word document!

### One-Time Setup:

1. **Open your Word document**
2. Press **Alt+F11** (opens VBA Editor)
3. Click **Insert** > **Module**
4. Open the file `Word_VBA_Macro.vba` in Notepad
5. **Copy all the code** and paste it into the VBA window
6. Close VBA Editor (click the X)
7. In Word, click **Insert** > **Shapes** > **Rectangle**
8. Draw a button shape
9. Type text in the button: "Extract Campaign Content"
10. **Right-click** the button > **Assign Macro**
11. Select **ExtractCampaignContent**
12. Click OK

### Using It:
1. **Click the button** in your Word doc
2. Script runs automatically
3. Content extracted and copied to clipboard!
4. Go to Google Sheets and press **Ctrl+V**

**Advantages:**
- ✅ Extract directly from Word
- ✅ No need to open other programs
- ✅ Button stays in the document

---

## 📊 What Happens After Extraction?

No matter which method you use:

1. ✅ **Content is copied to clipboard** - Ready to paste
2. ✅ **TSV file created** - Backup if clipboard fails
3. ✅ **JSON file created** - For reference
4. ✅ **Success message shown** - You know it worked

---

## 🔄 Complete Workflow

### Start to Finish:

```
Word Document
     ↓
Double-Click → Extract_Campaign_Content_GUI.bat
     ↓
Fill in details → Click Extract
     ↓
Content copied to clipboard ✓
     ↓
Open Google Sheets
     ↓
Click empty row → Press Ctrl+V
     ↓
Content pasted! ✓
     ↓
Add Hero Image URLs
     ↓
Check box in Column A
     ↓
JSON Generated! ✓
```

---

## 🆘 Troubleshooting

### "Python is not recognized..."
- Install Python from Microsoft Store or python.org
- Make sure "Add to PATH" is checked during install

### GUI doesn't open
- Try Method 2 (batch file) instead
- Or check if Python is installed

### Content not in clipboard
- No problem! Open the `.tsv` file created
- Copy from there and paste into Google Sheets

### Button in Word doesn't work
- Make sure document is saved first
- Check that Python scripts are in same folder
- Try Method 1 (GUI) instead

---

## 📁 Files You Need

These files should all be in your `JSONGenerator` folder:

**For GUI (Method 1):**
- ✅ `Extract_Campaign_Content_GUI.bat` (Double-click this)
- ✅ `extract_gui.py` (Used by the batch file)
- ✅ `extract_to_google_sheets.py` (Core extraction code)

**For Batch File (Method 2):**
- ✅ `Extract_Campaign_Content.bat` (Double-click this)
- ✅ `extract_to_google_sheets.py` (Core extraction code)

**For Word Button (Method 3):**
- ✅ `Word_VBA_Macro.vba` (Copy code from here)
- ✅ `test_extraction.py` (Used by the macro)

All of these are already created and ready to use! ✨

---

## 🎓 Quick Tips

- **First time?** Use Method 1 (GUI) - it's the easiest
- **Regular use?** Use Method 2 (batch file) - it's faster
- **Working in Word?** Use Method 3 (button) - most convenient

**Most Popular:** Method 1 (GUI) - Just double-click and fill in the form!

---

## 🚀 Ready to Start?

1. Find `Extract_Campaign_Content_GUI.bat` in your JSONGenerator folder
2. Double-click it
3. Follow the prompts
4. Paste into Google Sheets

That's it! No command line needed. 🎉

