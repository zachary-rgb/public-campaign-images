# Automatic Image URL Insertion - Feature Documentation

## Overview

The Campaign Content Extractor now **automatically inserts GitHub image URLs** into your extracted data! No more manual copying of URLs - they're inserted directly into the "Hero Image (URL)" column when you extract!

---

## How It Works

### Complete Workflow:

```
1. Assess Document
   ↓
2. Images detected & Git checked
   ↓
3. Click "Extract Content"
   ↓
4. Images saved to campaign_images/
   ↓
5. Images auto-uploaded to GitHub
   ↓
6. >>> GITHUB URLs GENERATED <<<  ← NEW!
   ↓
7. >>> URLS INSERTED INTO DATA <<<  ← NEW!
   ↓
8. TSV/JSON/Markdown exported with URLs
   ↓
9. Clipboard copy includes URLs!
```

**Everything automated - just paste into Google Sheets!** 🎉

---

## What You'll See

### During Extraction:

```
================================================================================
UPLOADING TO GITHUB
================================================================================

[1/4] Checking Git installation...
  ✓ Git found: git version 2.43.0

[2/4] Checking Git repository...
  ✓ Repository status: OK

[3/4] Adding images to Git...
  ✓ Added 3 file(s) to Git staging

[4/4] Committing and pushing to GitHub...
  ✓ Committed: Add campaign images: Takeda Vitiligo WeConnect
  ✓ Pushing to GitHub...

================================================================================
SUCCESS: Images uploaded to GitHub!
================================================================================

Generating image URLs for: zachary-rgb/Campaigns

Generated GitHub URLs:
  image_1.jpg
    -> https://raw.githubusercontent.com/zachary-rgb/Campaigns/main/campaign_images/image_1.jpg
  image_2.png
    -> https://raw.githubusercontent.com/zachary-rgb/Campaigns/main/campaign_images/image_2.png
  image_3.jpg
    -> https://raw.githubusercontent.com/zachary-rgb/Campaigns/main/campaign_images/image_3.jpg

Updating extracted data with GitHub image URLs...
  Updated row 1: https://raw.githubusercontent.com/zachary-rgb/Campaigns/...
  Updated row 2: https://raw.githubusercontent.com/zachary-rgb/Campaigns/...
  Updated row 3: https://raw.githubusercontent.com/zachary-rgb/Campaigns/...
  ✓ Image URLs inserted into Hero Image (URL) column!

[+] TSV file created: Takeda_for_google_sheets.tsv
[+] JSON file created: Takeda_extracted.json
[+] Markdown file created: Takeda_formatted.md
[SUCCESS] Content copied to clipboard!
```

---

## In Your Google Sheets

When you paste (Ctrl+V), the data looks like this:

| Campaign Name | Message Name | Email Subject Line | ... | **Hero Image (URL)** |
|--------------|--------------|-------------------|-----|---------------------|
| Takeda Vitiligo | Email 1: Long-form | Consider Joining... | ... | **https://raw.githubusercontent.com/zachary-rgb/Campaigns/main/campaign_images/image_1.jpg** |
| Takeda Vitiligo | Email 2: Reminder | Your Experience... | ... | **https://raw.githubusercontent.com/zachary-rgb/Campaigns/main/campaign_images/image_2.png** |

**URLs are already there!** ✅

---

## URL Format

### Standard Format:
```
https://raw.githubusercontent.com/{username}/{repo}/main/campaign_images/{image_name}
```

### Example:
```
https://raw.githubusercontent.com/zachary-rgb/Campaigns/main/campaign_images/image_1.jpg
```

### Why This Format?
- `raw.githubusercontent.com` - Direct access to file content
- Shows the actual image (not GitHub's HTML page)
- Works in Google Sheets and other applications
- No authentication needed for public repos

---

## How URLs Are Matched to Rows

### Single Email + Single Image:
```
1 email template → 1 image → URLs in row 1
```

### Multiple Emails + Multiple Images:
```
Email 1 → image_1.jpg → URL in row 1
Email 2 → image_2.png → URL in row 2
Email 3 → image_3.jpg → URL in row 3
```

### Multiple Emails + Single Image:
```
Email 1 → image_1.jpg → URL in row 1
Email 2 → image_1.jpg → Same URL in row 2 (shared)
```

### Multiple Emails + More Images:
```
Email 1 → image_1.jpg → URL in row 1
Email 2 → image_2.png → URL in row 2
Email 3 → image_1.jpg → URL in row 3 (uses first image)
```

---

## Benefits

✅ **No Manual Work** - URLs inserted automatically  
✅ **Correct Format** - Uses raw.githubusercontent.com  
✅ **Ready to Use** - Just paste into spreadsheet  
✅ **Multiple Images** - Handles any number of images  
✅ **Multiple Emails** - Works with multi-email campaigns  
✅ **Clear Logging** - See exactly what URLs were generated  
✅ **Error Tolerant** - Falls back gracefully if repo can't be detected  

---

## Technical Details

### New Methods Added:

**1. `get_github_repo_url()`**
- Extracts GitHub username and repo name from Git remote
- Handles both HTTPS and SSH URL formats
- Returns `(username, repo_name)` tuple

**2. `generate_github_image_urls()`**
- Creates raw.githubusercontent.com URLs for all images
- Uses username, repo, branch, and image filenames
- Returns dict mapping filename to URL

**3. `update_rows_with_image_urls()`**
- Inserts URLs into "Hero Image (URL)" column
- Handles multiple rows and images intelligently
- Logs each update for visibility

### Modified Methods:

**`auto_upload_to_github()`**
- Now returns `(success: bool, image_urls: dict)`
- Generates URLs after successful upload
- Provides clear logging of generated URLs

### URL Generation Process:

```python
# 1. Get repository info
username, repo = get_github_repo_url()
# Example: ("zachary-rgb", "Campaigns")

# 2. Generate URLs
base = f"https://raw.githubusercontent.com/{username}/{repo}/main/campaign_images"
url = f"{base}/{image_filename}"

# 3. Insert into rows
row['Hero Image (URL)'] = url
```

---

## Supported Git Remote Formats

### HTTPS Format:
```
https://github.com/username/repo.git
https://github.com/username/repo
```

### SSH Format:
```
git@github.com:username/repo.git
git@github.com:username/repo
```

Both formats are automatically detected and parsed!

---

## Error Handling

### If Git Repo Can't Be Detected:

```
Generating image URLs for: zachary-rgb/Campaigns

  Note: Could not determine GitHub repo for URL generation
  You can manually add image URLs to spreadsheet

[+] TSV file created: ...
```

**Result:** Data exported without URLs, manual insertion needed.

### If Git Upload Fails:

```
GIT AUTO-UPLOAD SKIPPED

Images saved locally but NOT uploaded to GitHub.
```

**Result:** No URLs generated (images aren't on GitHub yet).

---

## Manual Override

### If You Need Different URLs:

1. Let auto-insert do its thing
2. Paste into Google Sheets
3. Manually edit URLs in "Hero Image (URL)" column

### Common Manual Edits:
- Change branch: `main` → `develop`
- Change folder: `campaign_images` → `images/campaign`
- Use CDN: Switch to CDN URL

---

## Multiple Images Per Email

### Scenario: 3 Images for 1 Email

**Current Behavior:**
- First image URL inserted into row
- Other images available but not auto-inserted

**To Use Other Images:**
1. Check the extraction log for all URLs
2. Manually copy additional URLs
3. Use in other columns or additional rows

**Future Enhancement Idea:**
- Insert multiple images as comma-separated list
- Create multiple rows per email (one per image)
- User preference for which image to use

---

## Verification

### Check URLs Are Valid:

1. **Copy URL from spreadsheet**
2. **Paste into browser**
3. **Should see the actual image**

If you see GitHub's HTML page instead:
- URL format is wrong
- Should use `raw.githubusercontent.com`
- Not `github.com/blob/`

---

## Troubleshooting

### URLs Not Generated:

**Possible Causes:**
1. Git remote not configured
2. Not a GitHub repository
3. Git upload failed
4. Remote URL in unexpected format

**Solutions:**
1. Check Git remote: `git remote -v`
2. Verify GitHub URL
3. Check upload succeeded
4. Review extraction log for errors

### Wrong URLs Generated:

**Possible Causes:**
1. Wrong branch (using `main` but you use `master`)
2. Wrong folder structure
3. Repo renamed

**Solutions:**
1. Manually edit URLs in spreadsheet
2. Update Git remote
3. Check GitHub repo structure

### URLs Work But Images Don't Display:

**Possible Causes:**
1. Repository is private
2. Images not actually uploaded
3. Browser cache issue

**Solutions:**
1. Make repo public or use authenticated URLs
2. Check GitHub repo - are images there?
3. Clear browser cache or try incognito

---

## Examples

### Example 1: Single Email Campaign

**Document:** 1 email with 1 hero image  
**Extract:** 1 row generated  
**URL:** Inserted into row 1  
**Result:** Perfect - just paste!

### Example 2: Multi-Email Campaign

**Document:** 3 emails, each with different image  
**Extract:** 3 rows generated  
**URLs:** Inserted into rows 1, 2, 3  
**Result:** Each email has its own image URL!

### Example 3: Shared Image

**Document:** 2 emails sharing same image  
**Extract:** 2 rows generated  
**URL:** Same URL in both rows  
**Result:** Both emails point to same image

---

## Workflow Comparison

### Before This Feature:

1. Extract content ✅
2. Images uploaded to GitHub ✅
3. **Open GitHub in browser** ❌
4. **Navigate to campaign_images/** ❌
5. **Click each image** ❌
6. **Copy raw URL** ❌
7. **Paste into spreadsheet** ❌
8. **Repeat for each image** ❌

**Time:** ~5 minutes per campaign

### After This Feature:

1. Extract content ✅
2. Images uploaded to GitHub ✅
3. **URLs automatically inserted** ✅
4. **Paste into spreadsheet** ✅

**Time:** ~10 seconds

**Time Saved:** 4+ minutes per campaign! 🎯

---

## FAQ

**Q: Does this work with any Git repository?**
A: Currently optimized for GitHub. Other Git hosts may require adjustments.

**Q: Can I change the branch from `main`?**
A: Not currently, but URLs can be manually edited after extraction.

**Q: What if I have multiple GitHub accounts?**
A: Uses the repository configured in Git remote for current folder.

**Q: Do URLs expire?**
A: No, as long as repository and images remain on GitHub.

**Q: Can I use custom domain instead of raw.githubusercontent.com?**
A: Yes, manually edit URLs after insertion.

**Q: What if repository is renamed?**
A: Old URLs break. Update Git remote and re-extract.

---

## Best Practices

### 1. Verify Repository Before Extract
```bash
git remote -v
```
Make sure it points to correct GitHub repo.

### 2. Check URLs After First Use
- Copy one URL
- Paste in browser
- Verify image displays

### 3. Keep Repository Public
- For easy access
- No authentication needed
- URLs work everywhere

### 4. Use Descriptive Image Names
- Consider renaming images in folder
- Makes URLs more meaningful
- Easier to manage

---

## Future Enhancements (Ideas)

1. **Support for other branches** - User selects branch
2. **CDN integration** - Auto-generate CDN URLs
3. **Image optimization** - Resize/compress during upload
4. **Multiple image columns** - Insert into multiple columns
5. **GitLab/Bitbucket support** - Other Git hosts
6. **Custom URL patterns** - User-defined URL format
7. **Image preview** - Show thumbnails in GUI

---

## Summary

**Feature:** Automatic GitHub image URL insertion  
**Benefit:** Save 4+ minutes per campaign  
**Usage:** Just extract - URLs are auto-inserted  
**Result:** Paste into spreadsheet with URLs already there!  

**Status:** ✅ Complete and working  
**Version:** 2.2  
**Date:** January 28, 2026  

---

**No more manual URL copying - it's all automatic!** 🚀✨

