# ✅ Update: Campaign Name (Manual) + Message Name (Auto-Extracted)

## 🎯 What Changed

**Campaign Name** is now a **manual input field** while **Message Name** is **auto-extracted** from document headers.

### Before:
- Campaign Name: Auto-extracted from document headers (read-only)
- Message Name: Auto-extracted from document headers (read-only)
- User had no control over these values

### After:
- Campaign Name: **Manual entry** by user (full control)
- Message Name: **Auto-extracted** from document headers (e.g., "Email 1: Long-form email" → "Long-form email")
- User controls campaign naming, automation handles message identification
- Best of both worlds!

---

## 📋 GUI Updates

### Metadata Input Section:

```
2. Campaign Metadata
   
   Campaign Name:  [Takeda Vitiligo WeConnect     ] ← ✍️ Editable!
   Message Name:   (Auto-extracted)                 ← 📋 Auto-populated after extraction
   ─────────────────────────────────────────────────
   ℹ Message Name is extracted from document headers
   
   Language:       [en-us ▼]
   URL/UTM:        [                             ]
   Sponsor Name:   [Takeda                       ]
```

**Campaign Name is editable** - type your campaign identifier!
**Message Name auto-populates** - extracted from document (e.g., "Long-form email")

---

## 🎨 Default & Auto-Extracted Values

### Manual Input (Editable):

| Field | Default Value | You Can Change To |
|-------|---------------|-------------------|
| Campaign Name | `Takeda Vitiligo WeConnect` | Any campaign identifier |
| Language | `en-us` | `en-us` or `en-es` |
| Sponsor Name | `Takeda` | Any sponsor brand |

### Auto-Extracted (From Document):

| Field | Extracted From | Example Result |
|-------|----------------|----------------|
| Message Name | Document headers | `Long-form email` (from "Email 1: Long-form email") |

Just:
1. Open the GUI
2. Edit Campaign Name if needed
3. Click "Extract Content"
4. Message Name automatically appears from document!

---

## 📝 Command-Line Updates

The interactive command-line mode asks for Campaign Name, then auto-extracts Message Name:

```
CAMPAIGN METADATA
================================================================================
This information will be added to all extracted emails.
(Message Name will be auto-extracted from document headers)

> Campaign Name (e.g., Takeda Vitiligo WeConnect): [enter your value]
> Language (en-us or en-es) [en-us]: [press enter for default]
> URL/UTM (leave empty if in document): [optional]
> Sponsor Name (for end matter) [Takeda]: [press enter for default]

...extraction begins...
Found email headers: "Email 1: Long-form email", "Email 2: Short reminder"
```

---

## ⚠️ Warning Messages Still Work!

Even though Campaign Name and Message Name are manual, the warning system still tracks which content sections have issues:

### Warning Example:

```
WARNING: Missing Checkbox Selections!

These fields have multiple options but no [X] checkbox:

Long-form email:
  • Email Subject Line
  • Banner Headline

Action Taken: Using first option as default.
```

The Message Name you entered is displayed in warnings to help you identify which template needs attention.

---

## 🎯 Why This Change?

### Benefits:

1. **Campaign Control** - You decide the campaign naming, consistent across all messages
2. **Automatic Message ID** - System extracts message type from document structure
3. **Consistency** - Same campaign name for "Long-form email", "Short reminder", etc.
4. **Best of Both Worlds** - Manual control where needed, automation where helpful

### Use Cases:

**Scenario:** One campaign with 3 email types
- Document has: "Email 1: Long-form email", "Email 2: Short reminder", "Email 3: Follow-up"
- You enter Campaign Name once: "Takeda Vitiligo WeConnect"
- System extracts 3 rows with same Campaign Name but different Message Names
- Perfect for multi-message campaigns! ✨

**Other Benefits:**
- **Testing variants:** Same campaign name, different tests
- **Consistency:** Campaign name stays uniform across message types
- **Clarity:** Warnings reference Message Name so you know which email has issues

---

## 🚀 How to Use

### GUI Mode:
1. Double-click `Extract_Campaign_Content_GUI.bat`
2. **Edit Campaign Name** to your campaign identifier (e.g., "Takeda Vitiligo WeConnect")
3. Fill in other fields (Language, URL, Sponsor)
4. Click "Extract Content"
5. **Message Name auto-populates** from document headers
6. Done! Campaign Name from you, Message Name from document ✨

### Command-Line Mode:
1. Run `python extract_to_google_sheets.py`
2. Enter Campaign Name when prompted
3. Script automatically extracts Message Names from document
4. Multiple rows created (one per email template)

---

## 💡 Pro Tips

### Naming Conventions:

**Campaign Name Examples (You Enter):**
- `Takeda Vitiligo WeConnect`
- `Pfizer Diabetes Study Q1 2026`
- `Novartis Heart Health Trial`

**Message Name Examples (Auto-Extracted):**
- Document: "Email 1: Long-form email" → Extracts: `Long-form email`
- Document: "Email 2: Short-form reminder" → Extracts: `Short-form reminder`
- Document: "Email 3: Final call to action" → Extracts: `Final call to action`

### Quick Workflow:

1. **Enter Campaign Name once** in the GUI
2. **Let system extract Message Names** from document headers
3. **Campaign Name stays consistent** across all message types
4. **Message Names identify** which email template has warnings/issues

---

## 🎉 Result

You now have the **perfect balance**:
- ✍️ **Manual Campaign Name** - You control the campaign identifier
- 📋 **Auto Message Name** - System extracts from document structure
- ✅ Automatic content extraction
- ✅ Color detection (GREEN=variable, RED=standard)
- ✅ Checkbox detection with warnings
- ✅ Google Sheets-ready output
- ✅ Clear warning messages by Message Name

**Example Final Output:**

| Campaign Name | Message Name | Email Subject Line | ... |
|---------------|--------------|-------------------|-----|
| Takeda Vitiligo WeConnect | Long-form email | Your Experience Matters | ... |
| Takeda Vitiligo WeConnect | Short reminder | Quick reminder | ... |
| Takeda Vitiligo WeConnect | Final follow-up | Last chance | ... |

**Your campaign, smart automation, perfect results!** 🚀


