# Image Upload Feature Guide

## Overview

The Campaign Content Extractor now includes automatic image detection and upload options. When you assess a document, the script will detect all embedded images and give you flexible options for handling them.

---

## How It Works

### 1. **Automatic Image Detection**

When you click **"Assess Document"**, the script:
- Scans the Word document for all embedded images
- Extracts image metadata (format, size)
- Displays the count and details in the GUI

### 2. **Image Upload Options**

You get three choices:

#### Option A: Upload All Images
✅ **Best for:** Documents where all images are needed

- Saves all detected images to `campaign_images/` folder
- Provides Git commands for uploading to GitHub
- File naming: `image_1.jpg`, `image_2.png`, etc.

#### Option B: Select Specific Images
🎯 **Best for:** Documents with some unnecessary images

- Opens a selector window with checkboxes
- Choose which images to save
- Only selected images are saved to `campaign_images/` folder

#### Option C: Skip Image Upload
⏭️ **Best for:** Manual image handling

- Images are detected but not saved
- You can handle images separately later

---

## Step-by-Step Usage

### Step 1: Assess Your Document
1. Open the GUI (`GUI.bat` or `Extract_Campaign_Content_GUI.bat`)
2. Select your Word document
3. Click **"Assess Document"**

### Step 2: Review Image Detection
The output window will show:
```
Detecting images in document...
  Found 3 image(s):
     image_1.jpg (JPEG, 245.8 KB)
     image_2.png (PNG, 102.3 KB)
     image_3.jpg (JPEG, 189.5 KB)
```

### Step 3: Choose Upload Option
A new section appears: **"Image Upload Options"**

**Radio buttons:**
- ⚪ Upload all images to GitHub automatically
- ⚪ Let me select which images to upload
- ⚪ Skip image upload (I'll handle manually)

**Button:**
- 📋 **Preview Detected Images** - See detailed list of all images

### Step 4: (Optional) Select Specific Images
If you chose **"Let me select which images to upload"**:
1. A popup window opens
2. Checkboxes for each image are shown
3. Uncheck any images you don't want
4. Click **"Confirm Selection"**

### Step 5: Extract Content
Click **"4. Extract Content"** as usual. The images will be handled according to your selection.

---

## After Extraction

### If You Selected "Upload All" or "Select"

The extraction output will include:
```
================================================================================
UPLOADING IMAGES
================================================================================

Saved 3 image(s) to 'campaign_images/' folder:
  campaign_images\image_1.jpg
  campaign_images\image_2.png
  campaign_images\image_3.jpg

Next steps for GitHub upload:
  1. Open terminal in project folder
  2. Run: git add campaign_images/*
  3. Run: git commit -m 'Add campaign images'
  4. Run: git push origin main

Or use GitHub Desktop to upload the images folder
```

---

## Uploading Images to GitHub

### Method 1: Command Line (Git)

1. Open terminal/PowerShell in your Campaigns folder
2. Run these commands:
   ```bash
   git add campaign_images/*
   git commit -m "Add campaign images for [Campaign Name]"
   git push origin main
   ```

### Method 2: GitHub Desktop (Recommended)

1. Open **GitHub Desktop**
2. You'll see new files in the "Changes" panel:
   - `campaign_images/image_1.jpg`
   - `campaign_images/image_2.png`
   - etc.
3. Add a commit message: "Add campaign images"
4. Click **"Commit to main"**
5. Click **"Push origin"** (or "Publish branch" if first time)

### Method 3: Upload via GitHub Website

1. Go to https://github.com/zachary-rgb/public-campaign-images
2. Click **"Add file"** > **"Upload files"**
3. Drag the `campaign_images` folder contents
4. Add commit message
5. Click **"Commit changes"**

---

## Image Naming & Organization

### Default Naming
Images are automatically named: `image_1.jpg`, `image_2.png`, etc.

### Renaming (Optional)
You can rename files before uploading:
1. Navigate to `campaign_images/` folder
2. Rename files to descriptive names:
   - `hero_vitiligo_study.jpg`
   - `logo_takeda.png`
   - `banner_weconnect.jpg`
3. Then upload to GitHub

### Folder Structure
```
Campaigns/
├── campaign_images/          ← All images saved here
│   ├── image_1.jpg
│   ├── image_2.png
│   └── image_3.jpg
├── JSONGenerator/
│   ├── extract_gui.py
│   └── extract_to_google_sheets.py
└── [your Word documents]
```

---

## Preview Images Feature

Click **"Preview Detected Images"** to see:
- Filename for each image
- Format (JPEG, PNG, GIF, etc.)
- File size in KB
- Selection status (Selected/Skipped)

Example preview:
```
image_1.jpg
   Format: JPEG
   Size: 245.8 KB
   Status: Selected

image_2.png
   Format: PNG
   Size: 102.3 KB
   Status: Skipped
```

---

## Technical Details

### Supported Image Formats
- ✅ JPEG/JPG
- ✅ PNG
- ✅ GIF
- ✅ BMP
- ✅ TIFF
- ✅ WebP

### What Gets Detected
- ✅ Inline images in paragraphs
- ✅ Images in table cells
- ✅ Images in headers/footers
- ✅ Grouped images

### What Doesn't Get Detected
- ❌ Images inserted as OLE objects
- ❌ Images from external links/URLs
- ❌ Background images (watermarks)

---

## Troubleshooting

### "No images detected in document"
**Cause:** Document doesn't have embedded images, or they're external links.
**Solution:** Check if images are actually embedded in the Word doc.

### Images not saving to folder
**Cause:** Permission issues or disk full.
**Solution:** Check folder permissions and available disk space.

### Git push fails
**Cause:** Not authenticated or wrong repository.
**Solution:** 
1. Verify you're in the correct folder
2. Check if you're logged into GitHub
3. Use GitHub Desktop if command line fails

### Image quality issues
**Cause:** Images in Word docs are compressed.
**Solution:** Use original high-resolution images and upload separately.

---

## Best Practices

### 1. Review Before Uploading
- Always click **"Preview Detected Images"** first
- Verify the image count matches your expectations
- Check file sizes (large files may slow down loading)

### 2. Organize Images
- Rename images with descriptive names before uploading
- Group campaign images in subfolders if needed
- Delete old campaign images periodically

### 3. Use Select Option
- If document has logos, headers, or decorative images you don't need
- Select only the content images relevant to the campaign
- Saves storage space and keeps repository clean

### 4. GitHub Repository
- Keep your image repository public for easy access
- Use descriptive commit messages
- Tag major campaigns for easy reference

---

## FAQ

**Q: Can I upload images to a different repository?**
A: Yes! The images are saved locally first. You can manually upload to any location.

**Q: What if I forgot to select the right images?**
A: Re-run the assessment and extraction. The `campaign_images/` folder will be updated.

**Q: Can I use these images in the Google Sheet?**
A: Yes! Once on GitHub, copy the image URLs and paste into the "Hero Image (URL)" column.

**Q: Do images affect the TSV/JSON output?**
A: No. Image handling is separate. The extraction process remains the same.

**Q: Can I automate the GitHub push?**
A: Not currently. Manual upload gives you control to review before publishing.

---

## Related Documentation

- **GUI_FEATURES.md** - Complete GUI feature reference
- **ASSESS_DOCUMENT_FEATURE.md** - Document assessment guide
- **QUICK_START.md** - Getting started guide

---

## Need Help?

If you encounter issues:
1. Check the output log in the GUI
2. Verify images are embedded in Word doc
3. Ensure you have Git/GitHub access
4. Try GitHub Desktop if command line fails

---

**Version:** 1.0  
**Last Updated:** January 2026

