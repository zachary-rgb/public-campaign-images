# Image Upload - Quick Reference Card

## Quick Start

1. **Click "Assess Document"** → Images detected automatically
2. **Choose upload option:**
   - ⚪ Upload all
   - ⚪ Select specific images
   - ⚪ Skip (manual)
3. **Click "Extract Content"** → Images saved to `campaign_images/`
4. **Upload to GitHub:**
   ```bash
   git add campaign_images/*
   git commit -m "Add campaign images"
   git push origin main
   ```

---

## Three Upload Options

| Option | When to Use | What Happens |
|--------|-------------|--------------|
| **Upload All** | All images needed | Saves all images to `campaign_images/` |
| **Select Images** | Some images unnecessary | Opens selector, saves only checked images |
| **Skip** | Manual handling | Images detected but not saved |

---

## Buttons

- **Assess Document** - Detects images + creates campaign fields
- **Preview Detected Images** - Shows list of all images found
- **Confirm Selection** - (In selector popup) Saves your choices

---

## Output Example

```
Detecting images in document...
  Found 3 image(s):
     image_1.jpg (JPEG, 245.8 KB)
     image_2.png (PNG, 102.3 KB)
     image_3.jpg (JPEG, 189.5 KB)
```

After extraction:
```
Saved 3 image(s) to 'campaign_images/' folder:
  campaign_images\image_1.jpg
  campaign_images\image_2.png
  campaign_images\image_3.jpg
```

---

## GitHub Upload Methods

### Method 1: Git Command Line
```bash
cd C:\Users\[your-path]\Campaigns
git add campaign_images/*
git commit -m "Add campaign images"
git push origin main
```

### Method 2: GitHub Desktop (Easiest!)
1. Open GitHub Desktop
2. See new files in "Changes"
3. Add commit message
4. Click "Commit to main"
5. Click "Push origin"

### Method 3: GitHub Website
1. Go to your repository
2. Click "Add file" > "Upload files"
3. Drag `campaign_images` folder
4. Commit changes

---

## File Locations

```
Your Project/
├── campaign_images/      ← Images saved here
│   ├── image_1.jpg
│   ├── image_2.png
│   └── image_3.jpg
├── JSONGenerator/
└── [Word docs]
```

---

## Supported Formats

✅ JPEG/JPG | ✅ PNG | ✅ GIF | ✅ BMP | ✅ TIFF | ✅ WebP

---

## Tips

💡 **Rename images** before uploading for better organization  
💡 Use **"Select"** option to filter out logos/decorative images  
💡 Click **"Preview"** to verify what's detected  
💡 Images don't affect TSV/JSON output - it's separate  

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No images detected | Check if images are embedded (not linked) |
| Can't save images | Check folder permissions |
| Git push fails | Use GitHub Desktop instead |

---

## Need More Help?

📖 See **IMAGE_UPLOAD_FEATURE.md** for detailed guide

---

**Quick Reference v1.0 | January 2026**

