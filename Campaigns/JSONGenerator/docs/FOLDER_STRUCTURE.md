# JSONGenerator Folder Structure

## 📁 Clean, Organized Structure

```
JSONGenerator/
│
├── 🚀 EXECUTION FILES (Double-click to run)
│   ├── Extract_Campaign_Content_GUI.bat          ⭐ Main GUI extractor
│   ├── Extract_Campaign_Content.bat              Command-line version
│   └── Create_Desktop_Shortcuts.bat              Create desktop shortcuts
│
├── 🐍 PYTHON SCRIPTS (Used automatically)
│   ├── extract_to_google_sheets.py               Main extraction engine
│   └── extract_gui.py                            GUI interface
│
├── 📖 DOCUMENTATION (Start here!)
│   ├── START_HERE.txt                            ⭐ Quick start guide
│   ├── SIMPLE_USAGE_GUIDE.md                     Step-by-step for all methods
│   ├── QUICK_START.md                            Quick reference
│   ├── README_EXTRACTOR.md                       Technical documentation
│   ├── COMPLETE_SYSTEM_OVERVIEW.md               Full system overview
│   ├── CHECKBOX_GUIDE.md                         How to use checkboxes
│   ├── WARNING_ALERTS_GUIDE.md                   Warning alerts feature
│   ├── WHATS_NEW.md                              New features summary
│   └── FOLDER_STRUCTURE.md                       This file
│
├── 📝 SOURCE CONTENT
│   └── Takeda_TAK-279-VT-2001-Vitiligo...docx   Source Word document
│
├── 🔧 CONFIGURATION & CODE
│   ├── requirements.txt                          Python dependencies
│   ├── campaign_JSON_script_v1.1.txt            Google Sheets script
│   └── Word_VBA_Macro.vba                       VBA code for Word button
│
└── 📦 Archive/                                   Old files & tests
    ├── test_*.py                                 Test scripts
    ├── TEST_*.json/.tsv                          Test outputs
    ├── *_extracted.json                          Old extractions
    ├── Campaign_content.pdf                      Reference PDF
    ├── __pycache__/                              Python cache
    └── README.md                                 Archive contents info
```

---

## 🎯 Quick Navigation

### I Want To...

**Extract campaign content:**
- → Double-click `Extract_Campaign_Content_GUI.bat`

**Learn how to use the system:**
- → Open `START_HERE.txt`

**Understand checkboxes:**
- → Read `CHECKBOX_GUIDE.md`

**See what's new:**
- → Read `WHATS_NEW.md`

**Add button to Word:**
- → Open `Word_VBA_Macro.vba` and follow instructions

**Create desktop shortcut:**
- → Double-click `Create_Desktop_Shortcuts.bat`

---

## 📊 File Categories

### Production Files (Keep These!)
- ✅ All `.bat` files
- ✅ All `.py` files
- ✅ All `.md` files
- ✅ `requirements.txt`
- ✅ `campaign_JSON_script_v1.1.txt`
- ✅ `Word_VBA_Macro.vba`
- ✅ Source `.docx` files

### Archived Files (In Archive folder)
- 📦 Test scripts (`test_*.py`)
- 📦 Test outputs (`TEST_*`)
- 📦 Old extraction outputs
- 📦 Reference documents
- 📦 Python cache

---

## 🧹 Maintenance

### Files That Get Created During Use:
When you run extractions, new files are created:
- `[filename]_extracted.json` - JSON output
- `[filename]_for_google_sheets.tsv` - Google Sheets format

**These are temporary and can be deleted after pasting into Google Sheets.**

### To Clean Up After Extractions:
You can move old extraction outputs to `Archive/` folder to keep things tidy.

---

## 💾 Total File Count

### Main Folder: ~23 files
- 3 Execution files (.bat)
- 2 Python scripts (.py)
- 9 Documentation files (.md + .txt)
- 3 Configuration files
- 1 Source document (.docx)
- 5 Other support files

### Archive Folder: ~10 files
- Test scripts and outputs
- Old extractions
- Reference materials

---

## 🎓 Recommended Reading Order

1. **START_HERE.txt** - Overview and quick start
2. **SIMPLE_USAGE_GUIDE.md** - Detailed step-by-step
3. **CHECKBOX_GUIDE.md** - How to mark selections
4. **WARNING_ALERTS_GUIDE.md** - Understanding warnings
5. **COMPLETE_SYSTEM_OVERVIEW.md** - Deep dive

---

**Folder is now clean and organized! All production files in main folder, all test/obsolete files in Archive.** ✨

