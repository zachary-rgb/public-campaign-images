# Automatic GitHub Upload - Feature Guide

## Overview

The Campaign Content Extractor now **automatically uploads images to GitHub** when you click "Extract Content"! No more manual Git commands or GitHub Desktop steps needed.

---

## How It Works

### Simple Workflow:

1. **Assess Document** → Images detected and marked as preferred
2. **Choose upload option** → Select "Upload all" or "Upload preferred only"
3. **Click "Extract Content"** → Images automatically uploaded to GitHub! ✨

That's it! The script handles all Git operations automatically.

---

## What Happens During Upload

When you click "Extract Content" with images selected, you'll see:

```
================================================================================
PROCESSING IMAGES
================================================================================

Saved 3 image(s) to 'campaign_images/' folder:
  campaign_images\image_1.jpg
  campaign_images\image_2.png
  campaign_images\image_3.jpg

================================================================================
UPLOADING TO GITHUB
================================================================================

Project directory: C:\Users\zach.fabiano\Projects\Campaigns

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
✅ SUCCESS: Images uploaded to GitHub!
================================================================================

Your images are now available at:
  https://github.com/[your-repo]/campaign_images/

Uploaded files:
  - image_1.jpg
  - image_2.png
  - image_3.jpg
```

---

## Prerequisites

### Required:
1. **Git installed** on your computer
   - Download: https://git-scm.com/downloads
   - Or install GitHub Desktop (includes Git)

2. **Git repository initialized**
   - Your Campaigns folder should already be a Git repo
   - Command: `git init` (if not already done)

3. **GitHub authentication configured**
   - Option A: GitHub Desktop (easiest - handles auth automatically)
   - Option B: Personal Access Token
   - Option C: SSH keys

### Checking Prerequisites:

```bash
# Check Git is installed
git --version

# Check you're in a Git repository
git status

# Check remote is configured
git remote -v
```

---

## Where Images Are Uploaded

### Local Location:
```
C:\Users\zach.fabiano\Projects\Campaigns\
└── campaign_images\
    ├── image_1.jpg
    ├── image_2.png
    └── image_3.jpg
```

### GitHub Location:
```
https://github.com/[your-username]/Campaigns/
└── campaign_images/
    ├── image_1.jpg
    ├── image_2.png
    └── image_3.jpg
```

### Image URLs:
After upload, your images are accessible at:
```
https://raw.githubusercontent.com/[your-username]/Campaigns/main/campaign_images/image_1.jpg
https://raw.githubusercontent.com/[your-username]/Campaigns/main/campaign_images/image_2.png
```

Use these URLs in the "Hero Image (URL)" column in Google Sheets!

---

## Error Handling

The auto-upload feature includes robust error handling:

### Error 1: Git Not Found
```
ERROR: Git not found. Please install Git or use manual upload.
```
**Solution:** Install Git from https://git-scm.com/downloads

### Error 2: Not a Git Repository
```
ERROR: Not a Git repository. Initialize Git first or use manual upload.
```
**Solution:** 
```bash
cd C:\Users\zach.fabiano\Projects\Campaigns
git init
git remote add origin https://github.com/[your-username]/Campaigns.git
```

### Error 3: Push Failed
```
ERROR pushing to GitHub: [error message]

Fallback: Use GitHub Desktop or manual commands:
  git add campaign_images/
  git commit -m 'Add campaign images: [campaign name]'
  git push
```
**Solution:** Run the manual commands shown, or use GitHub Desktop

### Error 4: Authentication Required
```
ERROR: fatal: Authentication failed
```
**Solution:** 
- Use GitHub Desktop (easiest)
- Or configure Git credentials: `git config --global credential.helper manager`

### Error 5: Network Timeout
```
ERROR: Git push timed out. Check your internet connection.
```
**Solution:** Check internet connection and try again

---

## Manual Fallback

If auto-upload fails, the script provides fallback instructions:

### Using GitHub Desktop (Recommended):
1. Open GitHub Desktop
2. You'll see new files in "Changes"
3. Add commit message: "Add campaign images"
4. Click "Commit to main"
5. Click "Push origin"

### Using Command Line:
```bash
cd C:\Users\zach.fabiano\Projects\Campaigns
git add campaign_images/
git commit -m "Add campaign images"
git push
```

---

## Upload Options Behavior

### Option 1: Upload All Images
- Saves all detected images
- Automatically uploads ALL to GitHub
- Fast and simple

### Option 2: Upload Preferred Only
- Saves only images marked with [X]
- Automatically uploads ONLY PREFERRED to GitHub
- Selective and efficient

### Option 3: Skip Upload
- No images saved
- No GitHub upload
- For manual handling

---

## Commit Messages

The script automatically creates descriptive commit messages:

```
Add campaign images: Takeda Vitiligo WeConnect
Add campaign images: Pfizer Study Reminder
Add campaign images: GSK Patient Registry
```

Based on your Campaign Name from the GUI!

---

## Multiple Extractions

### Scenario: Extracting multiple campaigns

**First extraction:**
```
Campaign: Takeda Vitiligo WeConnect
Images: image_1.jpg, image_2.jpg
→ Committed: "Add campaign images: Takeda Vitiligo WeConnect"
→ Pushed to GitHub
```

**Second extraction:**
```
Campaign: Pfizer Diabetes Study
Images: image_3.jpg, image_4.png
→ Committed: "Add campaign images: Pfizer Diabetes Study"
→ Pushed to GitHub
```

Each extraction is a separate commit with clear naming!

---

## Git Repository Structure

### Before First Upload:
```
Campaigns/
├── JSONGenerator/
├── [Word documents]
└── .git/
```

### After First Upload:
```
Campaigns/
├── campaign_images/          ← NEW
│   ├── image_1.jpg
│   ├── image_2.png
│   └── image_3.jpg
├── JSONGenerator/
├── [Word documents]
└── .git/
```

### On GitHub:
```
https://github.com/[your-username]/Campaigns/
├── campaign_images/          ← Visible on GitHub!
│   ├── image_1.jpg
│   ├── image_2.png
│   └── image_3.jpg
└── JSONGenerator/
```

---

## Performance

### Upload Time:
- **Small images (< 1MB)**: 2-5 seconds
- **Medium images (1-3MB)**: 5-10 seconds
- **Large images (> 3MB)**: 10-20 seconds

### Factors:
- Internet connection speed
- Image file sizes
- Number of images
- GitHub server response time

---

## Security & Authentication

### GitHub Authentication Methods:

**Method 1: GitHub Desktop (Recommended)**
- Handles authentication automatically
- No manual setup needed
- Most user-friendly

**Method 2: Personal Access Token (PAT)**
```bash
# Configure Git to use PAT
git config --global credential.helper manager

# First push will prompt for credentials
# Use your PAT instead of password
```

**Method 3: SSH Keys**
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to GitHub: Settings → SSH Keys
```

---

## Troubleshooting

### Issue: "Nothing to commit"
**Cause:** Images already in repository
**Solution:** This is normal! Images were previously uploaded.

### Issue: "No upstream branch"
**Cause:** First push to a new branch
**Solution:** Script automatically handles this with `--set-upstream`

### Issue: Push takes too long
**Cause:** Large images or slow connection
**Solution:** 
- Compress images before inserting in Word doc
- Use smaller image files
- Check internet connection

### Issue: Authentication popup appears
**Cause:** Git credentials not stored
**Solution:**
1. Enter your GitHub credentials
2. Check "Remember me"
3. Future pushes will be automatic

---

## Best Practices

### 1. Check Git Status Before Extracting
```bash
git status
```
Make sure you're on the right branch and have no conflicts.

### 2. Use Descriptive Campaign Names
Good: "Takeda Vitiligo WeConnect Email 1"
Bad: "Test" or "Campaign"

This makes Git commit messages clear!

### 3. Review Images Before Extract
- Use "Preview Detected Images" button
- Verify preferred selections
- Ensure image quality is good

### 4. Monitor Output Log
- Watch for success/error messages
- Note GitHub URLs provided
- Keep track of uploaded files

### 5. Keep Images Organized
- Use [X] markers consistently
- Name images descriptively in Word doc
- Delete old campaign images periodically

---

## FAQ

**Q: Does this work with any Git repository?**
A: Yes! Works with GitHub, GitLab, Bitbucket, or any Git remote.

**Q: Can I disable auto-upload?**
A: Currently, it's automatic for "Upload all" and "Upload preferred". Use "Skip" option to avoid upload.

**Q: What if I want to review before pushing?**
A: The script commits locally first. You can review with `git log` and force push later if needed.

**Q: Can I change the commit message?**
A: Currently auto-generated. You can amend with: `git commit --amend -m "New message"`

**Q: Will this overwrite existing images?**
A: No. Git tracks changes. New versions are added as updates.

**Q: What happens if extraction fails mid-upload?**
A: Images are saved locally first. Even if push fails, you have the files and can push manually.

**Q: Can I upload to a different repository?**
A: Currently uploads to the current repository. For different repo, change `git remote` configuration.

---

## Advanced Usage

### Upload to Specific Branch
```bash
# Before extraction, switch branch
git checkout -b campaign-images

# Extract (auto-uploads to current branch)

# Merge to main later
git checkout main
git merge campaign-images
```

### Upload to Different Remote
```bash
# Add second remote
git remote add images https://github.com/zachary-rgb/public-campaign-images.git

# Modify script or manually push
git push images main
```

### Review Before Pushing
1. Let script commit (it will try to push)
2. If push fails, you can review:
   ```bash
   git log -1
   git show HEAD
   ```
3. Then manually push when ready

---

## Summary

**Auto-Upload Benefits:**
- ⚡ **Fast**: No manual commands needed
- 🎯 **Accurate**: Commit messages include campaign name
- 🛡️ **Safe**: Error handling with fallback options
- 📊 **Tracked**: All uploads are Git commits
- 🔄 **Consistent**: Same process every time

**Trigger:**
- Click "Extract Content" button
- Images saved → Automatically uploaded to GitHub
- All in one step!

**Location:**
- Local: `campaign_images/` folder
- GitHub: `https://github.com/[your-repo]/campaign_images/`

---

**Version:** 1.0  
**Date:** January 28, 2026  
**Feature Status:** ✅ Complete & Production Ready

