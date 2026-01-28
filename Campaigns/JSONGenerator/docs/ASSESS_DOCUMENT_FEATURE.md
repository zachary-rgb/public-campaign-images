# ✨ NEW FEATURE: Assess Document Button

## 🎯 What It Does

The **"Assess Document"** button scans your Word document and **dynamically creates Campaign Name fields** - one for each email template found!

This allows you to assign **different Campaign Names** to each email in a multi-template document.

---

## 🚀 How to Use

### Step 1: Select Document
```
1. Select Word Document
   [Browse...] [Assess Document] ← Click this!
```

### Step 2: Click "Assess Document"
- Scans the document for email headers
- Looks for patterns like: "Email 1: Long-form email"
- Counts how many email templates exist

### Step 3: Review Assessment Results
```
2. Document Assessment & Campaign Names

   ✅ Found 3 email templates:
      • Email 1: Long-form email
      • Email 2: Short-form reminder
      • Email 3: Final follow-up
```

### Step 4: Enter Campaign Names
```
Enter Campaign Name for each email template:

📧 Email 1: Long-form email
   Campaign Name: [Takeda Vitiligo WeConnect________________]

📧 Email 2: Short-form reminder
   Campaign Name: [Takeda Vitiligo SMS Campaign____________]

📧 Email 3: Final follow-up
   Campaign Name: [Takeda Vitiligo Final CTA______________]
```

### Step 5: Extract Content
- Click "4. Extract Content"
- Each email gets its specific Campaign Name
- Message Names are still auto-extracted

---

## 📊 Example Workflow

### Document Structure:
```
Email 1: Long-form email
[table with content]

Email 2: Short-form reminder
[table with content]

Email 3: Final follow-up
[table with content]
```

### After Assessing:
- 3 Campaign Name fields appear
- Each field is editable
- Smart defaults are pre-filled

### You Enter:
```
Email 1: "Takeda Vitiligo WeConnect - Initial"
Email 2: "Takeda Vitiligo WeConnect - Reminder"
Email 3: "Takeda Vitiligo WeConnect - Final"
```

### Output to Google Sheets:
```
Row 1: Campaign Name = "Takeda Vitiligo WeConnect - Initial"
       Message Name = "Long-form email"

Row 2: Campaign Name = "Takeda Vitiligo WeConnect - Reminder"
       Message Name = "Short-form reminder"

Row 3: Campaign Name = "Takeda Vitiligo WeConnect - Final"
       Message Name = "Final follow-up"
```

---

## 💡 Use Cases

### Use Case 1: Different Campaign Phases
```
Email 1: Takeda Vitiligo Phase 1
Email 2: Takeda Vitiligo Phase 2
Email 3: Takeda Vitiligo Phase 3
```

### Use Case 2: Testing Variants
```
Email 1: Takeda Vitiligo Variant A
Email 2: Takeda Vitiligo Variant B
Email 3: Takeda Vitiligo Control
```

### Use Case 3: Multiple Products
```
Email 1: Takeda Vitiligo Campaign
Email 2: Takeda Psoriasis Campaign
Email 3: Takeda Eczema Campaign
```

### Use Case 4: Same Campaign Name (Default)
```
Email 1: Takeda Vitiligo WeConnect
Email 2: Takeda Vitiligo WeConnect
Email 3: Takeda Vitiligo WeConnect
```
(Just keep the defaults if all emails are part of the same campaign!)

---

## 🎨 Smart Defaults

### For Single Email:
```
Campaign Name: Takeda Vitiligo WeConnect
```

### For Multiple Emails:
```
Email 1: Takeda Vitiligo WeConnect
Email 2: Takeda Vitiligo WeConnect (Email 2)
Email 3: Takeda Vitiligo WeConnect (Email 3)
```

**You can edit any of these!** They're just suggestions to save time.

---

## ⚙️ Technical Details

### What Gets Assessed:
- ✅ Number of email templates
- ✅ Email headers (e.g., "Email 1: Long-form email")
- ✅ Message Names extracted from headers

### What You Control:
- ✅ Campaign Name for each email (editable)
- ✅ Language (applies to all)
- ✅ URL/UTM (applies to all)
- ✅ Sponsor Name (applies to all)

### What's Automatic:
- ✅ Message Name extraction
- ✅ Content extraction
- ✅ Color detection
- ✅ Checkbox detection
- ✅ Warning system

---

## 🔄 Comparison: Before vs After

### Before (Original Behavior):
```
Single "Campaign Name" field
All emails get the same Campaign Name
Message Names auto-extracted
```

**Best for:** Documents with emails from same campaign

### After (With Assess Button):
```
Click "Assess Document"
Dynamic Campaign Name fields appear
Each email can have different Campaign Name
Message Names still auto-extracted
```

**Best for:** Documents with emails from different campaigns/phases/variants

---

## 📝 Notes

### When to Use Assess:
- ✅ Document has multiple email templates
- ✅ Each email needs a different Campaign Name
- ✅ Testing variants or phases
- ✅ Multiple products in one document

### When to Skip Assess:
- ✅ Document has single email
- ✅ All emails are same campaign
- ✅ Campaign Names don't matter (testing)

### Optional Feature:
- You can still extract without assessing
- Default Campaign Name will be used for all emails
- Assess is **optional** but powerful!

---

## 🎉 Benefits

1. **Flexibility** - Different Campaign Names per email
2. **Accuracy** - Each email properly identified
3. **Time Saving** - Smart defaults pre-filled
4. **Clarity** - See exactly what's in the document
5. **Power User** - Advanced control when needed
6. **Backward Compatible** - Still works without assessing

---

## 🚀 Quick Reference

| Action | Result |
|--------|--------|
| **Browse** | Select document |
| **Assess Document** | Scan & create Campaign Name fields |
| **Edit Fields** | Customize Campaign Names |
| **Extract Content** | Process with individual names |
| **Skip Assess** | Use default behavior (single name) |

---

## 💬 Example Messages

**Assessment Success:**
```
✅ Found 3 email templates!

Campaign Name fields have been created below.
Review and edit as needed, then click 'Extract Content'.
```

**No Headers Found:**
```
Could not find email template headers in the document.

Looking for headers like:
  • Email 1: Long-form email
  • Email 2: Short reminder

The document may have a different structure.
```

**Extraction with Assessment:**
```
Using assessed email templates (3 found):

  Email 1:
    Campaign Name: Takeda Vitiligo WeConnect - Initial
    Message Name:  Long-form email

  Email 2:
    Campaign Name: Takeda Vitiligo WeConnect - Reminder
    Message Name:  Short-form reminder
```

---

## 🎯 Summary

**The Assess Document button gives you:**
- 📊 Document insights (how many emails)
- ✍️ Individual Campaign Name control
- 🎯 Precise targeting per email
- 🚀 Faster workflow with smart defaults
- 💪 Power user features when needed

**Your extraction workflow is now even more powerful and flexible!** 🎉

