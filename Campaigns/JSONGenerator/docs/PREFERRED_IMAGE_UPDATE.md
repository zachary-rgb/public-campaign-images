# Preferred Image Upload - Update Summary

## What Changed

The image upload feature has been **enhanced** to use the same `[X]` checkbox workflow you already use for text content!

---

## New Behavior

### Before (Old):
- "Let me select which images to upload"
- Manual checkbox selection in GUI popup
- No connection to document markup

### After (New):
- **"Upload preferred images only (marked with [X] in doc)"**
- Automatically detects `[X]` markers near images in Word document
- Only images marked with `[X]` are pre-selected
- Consistent with your existing checkbox workflow!

---

## How It Works

### Step 1: Mark Images in Word Document

In your Word document, add `[X]` near the images you want to upload:

**Example:**
```
HERO SPACE IMAGE OPTIONS

[X] Image 1: Study participants
    [Image embedded here]

[ ] Image 2: Doctor consultation  
    [Image embedded here]

[X] Image 3: Patient testimonial
    [Image embedded here]
```

### Step 2: Assess Document

Click "Assess Document" and you'll see:

```
Detecting images in document...
  Found 3 image(s):
     image_1.jpg (JPEG, 245.8 KB) [X] PREFERRED
     image_2.png (PNG, 102.3 KB)
     image_3.jpg (JPEG, 189.5 KB) [X] PREFERRED
  -> 2 image(s) marked as preferred with [X]
```

### Step 3: Choose "Upload preferred images only"

Select the middle option:
- ⚪ Upload all images to GitHub automatically
- **🔘 Upload preferred images only (marked with [X] in doc)**  ← Select this!
- ⚪ Skip image upload (I'll handle manually)

### Step 4: Review (Optional)

A popup shows all images with:
- ✅ **Preferred images already checked** (green text)
- ☐ Non-preferred images unchecked
- You can still override by checking/unchecking

### Step 5: Extract

Only the preferred (checked) images are saved!

---

## Three Upload Options Explained

| Option | When to Use | What Gets Uploaded |
|--------|-------------|-------------------|
| **Upload all** | Need all images | All detected images |
| **Upload preferred only** | Marked favorites with [X] | Only images with [X] markers |
| **Skip** | Manual handling | Nothing (you handle later) |

---

## Detection Logic

### Where [X] Markers Are Detected:

✅ **In same paragraph as image:**
```
[X] Hero image showing study participants
[Image here]
```

✅ **In same table cell as image:**
```
┌──────────────────────────┐
│ [X] Option 1             │
│ [Image here]             │
└──────────────────────────┘
```

✅ **Text near image:**
```
Image Options:
[X] Selected option - [Image]
[ ] Not selected - [Image]
```

### Supported Checkbox Markers:
- `[X]` or `[x]`
- `[✓]` or `[√]` or `[✔]`
- `☑` or `✓` or `✔`

---

## Example Workflow

### In Word Document:

```
Email 1: Long-form email

HERO SPACE IMAGE OPTIONS

[X] Option 1: Diverse group studying
    Image: diverse_group.jpg

[ ] Option 2: Doctor consultation
    Image: doctor.jpg

[X] Option 3: Patient testimonial
    Image: patient.jpg
```

### In GUI After Assessment:

```
Detecting images in document...
  Found 3 image(s):
     image_1.jpg (JPEG, 245.8 KB) [X] PREFERRED
     image_2.jpg (JPEG, 180.2 KB)
     image_3.jpg (JPEG, 201.5 KB) [X] PREFERRED
  -> 2 image(s) marked as preferred with [X]
```

### After Extraction (with "preferred only"):

```
Saved 2 image(s) to 'campaign_images/' folder:
  campaign_images\image_1.jpg  (diverse_group)
  campaign_images\image_3.jpg  (patient testimonial)
  
Skipped 1 non-preferred image(s)
```

---

## Benefits

### ✅ Consistent Workflow
- Uses same `[X]` markers as subject lines, headlines, etc.
- No new syntax to learn
- Sponsors already know this pattern

### ✅ Document-Driven
- Selection happens in Word doc
- No manual clicking in GUI
- Repeatable and documented

### ✅ Flexible Override
- Can still check/uncheck in popup if needed
- Not locked to document selections
- Best of both worlds

### ✅ Clear Visibility
- See which images are preferred in assessment log
- Preview shows preferred status
- No surprises about what gets uploaded

---

## GUI Changes Summary

### Assessment Log:
- Now shows `[X] PREFERRED` next to marked images
- Displays count of preferred images
- Example: `-> 2 image(s) marked as preferred with [X]`

### Radio Button:
- Old: "Let me select which images to upload"
- New: **"Upload preferred images only (marked with [X] in doc)"**

### Image Selector Popup:
- Shows preferred count at top
- Pre-checks only preferred images
- Preferred images in green text
- Non-preferred images in black (unchecked)

### Preview Window:
- Shows `[X] PREFERRED` marker
- Displays context text (text near image)
- Shows selection status

---

## Code Changes

### In `extract_to_google_sheets.py`:

1. **Enhanced `detect_images_in_document()` method:**
   - Scans paragraphs and table cells for images
   - Checks for `[X]` markers in same location
   - Marks images as "preferred" if `[X]` found
   - Stores context text for display

2. **New `has_checkbox_marker()` method:**
   - Detects various checkbox markers
   - Same logic as text option detection
   - Supports `[X]`, `[x]`, `[✓]`, `☑`, etc.

### In `extract_gui.py`:

1. **Updated radio button text**
2. **Enhanced assessment log** to show preferred markers
3. **Updated image selector** to pre-select preferred only
4. **Enhanced preview** to show preferred status

---

## Testing Checklist

### ✅ Basic Functionality
- [x] Images with `[X]` detected as preferred
- [x] Images without `[X]` detected as non-preferred
- [x] Log shows preferred count
- [x] Selector pre-checks only preferred images

### ✅ Edge Cases
- [x] Document with no `[X]` markers (none selected)
- [x] Document with all images marked `[X]` (all selected)
- [x] Mixed: some preferred, some not
- [x] No images in document (no options shown)

### ✅ Override Capability
- [x] Can manually check non-preferred images
- [x] Can manually uncheck preferred images
- [x] Changes persist after "Confirm Selection"

---

## Backward Compatibility

✅ **Fully Compatible**
- Old documents still work (all images treated as non-preferred)
- "Upload all" option unchanged
- "Skip" option unchanged
- No breaking changes

---

## Migration Guide

### For Existing Users:

**No migration needed!** Your existing workflow continues to work.

**To use new feature:**
1. Open your Word document
2. Add `[X]` markers near preferred images
3. Save document
4. Extract as usual with "Upload preferred only" option

### For New Users:

1. Mark preferred images with `[X]` in Word doc
2. Click "Assess Document" in GUI
3. Choose "Upload preferred images only"
4. Extract and upload

---

## Sponsor Instructions

Add this to your Word document template:

```
INSTRUCTIONS FOR IMAGE SELECTION:

Mark your preferred images with [X]:
  [X] = Upload this image to GitHub
  [ ] = Skip this image

Example:
  [X] Option 1: This image will be uploaded
  [ ] Option 2: This image will be skipped
```

---

## FAQ

**Q: What if I don't add [X] markers?**
A: All images are treated as non-preferred. Use "Upload all" to upload everything.

**Q: Can I override the [X] selections?**
A: Yes! The popup lets you check/uncheck any images.

**Q: Do I have to use [X] for every image?**
A: No. Only mark the ones you want. Unmarked images won't be uploaded (unless you manually check them).

**Q: What if [X] is in a different cell than the image?**
A: The script checks paragraphs and table cells. If image and [X] are far apart, they may not be linked. Keep them close together.

**Q: Can I still use "Upload all"?**
A: Absolutely! "Upload all" works regardless of [X] markers.

---

## Examples

### Example 1: Email with Multiple Hero Options

**Word Document:**
```
HERO SPACE IMAGE OPTIONS (choose one)

[X] Diverse community members
    [Image: community.jpg]

[ ] Healthcare professional
    [Image: doctor.jpg]

[ ] Research laboratory
    [Image: lab.jpg]
```

**Result:** Only `community.jpg` uploaded

### Example 2: Multiple Emails with Images

**Word Document:**
```
Email 1: Long-form

[X] Hero image: Study overview
    [Image: overview.jpg]

Email 2: Reminder

[X] Hero image: Quick facts
    [Image: facts.jpg]
```

**Result:** Both `overview.jpg` and `facts.jpg` uploaded

### Example 3: Logo + Hero

**Word Document:**
```
LOGO OPTIONS

[ ] Logo: Takeda blue
    [Image: logo_blue.png]

[ ] Logo: Takeda red
    [Image: logo_red.png]

HERO IMAGE

[X] Study participants
    [Image: hero.jpg]
```

**Result:** Only `hero.jpg` uploaded (logos skipped)

---

## Summary

The **Preferred Image Upload** feature makes image selection consistent with your existing `[X]` checkbox workflow. Mark images in the Word document, and the script automatically detects and uploads only those marked as preferred.

**Status:** ✅ Complete and tested  
**Backward Compatible:** ✅ Yes  
**Documentation:** ✅ Complete  
**Ready to Use:** ✅ Yes  

---

**Version:** 2.0  
**Date:** January 28, 2026  
**Update Type:** Enhancement (non-breaking)

