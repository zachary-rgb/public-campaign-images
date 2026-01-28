# Git Prerequisite Checks - Feature Documentation

## Overview

The Campaign Content Extractor now **checks Git prerequisites during document assessment** to ensure auto-upload will work before you extract!

---

## What It Does

When you click **"Assess Document"**, the system now automatically checks:

1. ✅ **Git is installed**
2. ✅ **Current folder is a Git repository**
3. ✅ **Git remote is configured** (for push to GitHub)
4. ✅ **Git user is configured** (name and email)
5. ⚠️ **Uncommitted changes** (optional warning)

---

## When It Runs

### Timing:
```
User clicks "Assess Document"
    ↓
Extract email templates
    ↓
Detect images
    ↓
>>> CHECK GIT PREREQUISITES <<<  ← NEW!
    ↓
Show assessment results
```

**Before extraction!** So you know about issues early.

---

## What You'll See

### ✅ All Good (Everything Works):

```
Checking Git prerequisites for auto-upload...
  [OK] Git installed: git version 2.43.0
  [OK] Git repository initialized
  [OK] Git remote configured: origin
  [OK] Git user configured

  >> Git auto-upload ready!
```

### ❌ Git Not Installed:

```
Checking Git prerequisites for auto-upload...
  [X] Git not installed
      Install from: https://git-scm.com/downloads

⚠️ WARNING POPUP:
┌─────────────────────────────────────┐
│ Git Setup Required                  │
├─────────────────────────────────────┤
│ Git Auto-Upload Not Available:      │
│                                     │
│   • Git not installed               │
│                                     │
│ Images will be saved locally but    │
│ not auto-uploaded to GitHub.        │
│                                     │
│ Fix Git issues to enable auto-upload│
└─────────────────────────────────────┘
```

### ❌ Not a Git Repository:

```
Checking Git prerequisites for auto-upload...
  [OK] Git installed: git version 2.43.0
  [X] Not a Git repository
      Run: git init

⚠️ WARNING POPUP:
Git Auto-Upload Not Available:
  • Not a Git repository

Fix: Run "git init" in project folder
```

### ⚠️ No Remote Configured:

```
Checking Git prerequisites for auto-upload...
  [OK] Git installed: git version 2.43.0
  [OK] Git repository initialized
  [!] No Git remote configured
      Images will be committed locally only
      To add remote: git remote add origin [URL]
  [OK] Git user configured

  >> Git setup complete but no remote - images will commit locally only

⚠️ LOG WARNING (no popup blocking)
```

### ⚠️ User Not Configured:

```
Checking Git prerequisites for auto-upload...
  [OK] Git installed: git version 2.43.0
  [OK] Git repository initialized
  [OK] Git remote configured: origin
  [!] Git user not fully configured
      Run: git config user.name "Your Name"
      Run: git config user.email "your.email@example.com"

⚠️ LOG WARNING
```

### ⚠️ Uncommitted Changes:

```
Checking Git prerequisites for auto-upload...
  [OK] Git installed: git version 2.43.0
  [OK] Git repository initialized
  [OK] Git remote configured: origin
  [OK] Git user configured
  [!] 5 uncommitted file(s) in repository
      Consider committing before adding images

  >> Git auto-upload ready!

⚠️ LOG WARNING
```

---

## Error vs Warning

### 🔴 Errors (Block Auto-Upload):
- Git not installed
- Not a Git repository

**Result:** Images saved locally, auto-upload skipped, manual instructions provided

### 🟡 Warnings (Allow Auto-Upload):
- No Git remote configured
- Git user not configured
- Uncommitted changes

**Result:** Auto-upload attempted, may work with limitations

---

## During Extraction

### If Git Errors Detected:

```
================================================================================
PROCESSING IMAGES
================================================================================

Saved 3 image(s) to 'campaign_images/' folder:
  campaign_images\image_1.jpg
  campaign_images\image_2.png
  campaign_images\image_3.jpg

================================================================================
GIT AUTO-UPLOAD SKIPPED
================================================================================

Images saved locally but NOT uploaded to GitHub.
Git setup issues detected during assessment:
  • Git not installed

Fix Git issues and re-extract to enable auto-upload.

Manual upload: Use GitHub Desktop to commit and push
```

### If Git Warnings Only:

```
================================================================================
UPLOADING TO GITHUB
================================================================================

[Automatic upload proceeds normally]
```

---

## Fixing Issues

### Issue 1: Git Not Installed

**Solution:**
1. Download Git: https://git-scm.com/downloads
2. Install Git
3. Restart GUI
4. Re-assess document

**Verify:**
```bash
git --version
```

### Issue 2: Not a Git Repository

**Solution:**
```bash
cd C:\Users\[your-path]\Projects\Campaigns
git init
git remote add origin https://github.com/[your-username]/[repo-name].git
```

**Verify:**
```bash
git status
```

### Issue 3: No Remote Configured

**Solution:**
```bash
git remote add origin https://github.com/[your-username]/[repo-name].git
```

**Verify:**
```bash
git remote -v
```

### Issue 4: Git User Not Configured

**Solution:**
```bash
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

**Verify:**
```bash
git config user.name
git config user.email
```

### Issue 5: Uncommitted Changes

**Solution:**
```bash
git add .
git commit -m "Commit message"
```

Or use GitHub Desktop to commit

---

## Benefits

### 1. Early Warning
- Know about Git issues **before extraction**
- No surprises at the end
- Fix problems early

### 2. Clear Instructions
- Shows exactly what's wrong
- Provides specific commands to run
- Links to download pages

### 3. Non-Blocking
- Warnings don't stop extraction
- Still get your content
- Can fix Git later

### 4. Better User Experience
- No confusion about why upload failed
- Clear status updates
- Helpful error messages

### 5. Graceful Degradation
- If Git unavailable, saves locally
- Manual upload option always available
- System doesn't break

---

## Technical Details

### Implementation:

**New Method:**
```python
def check_git_prerequisites(self):
    """Check Git configuration"""
    # Checks Git install, repo status, remote, user config
    # Returns dict with status and messages
```

**Integration Points:**
1. Called in `assess_document()` after image detection
2. Results stored in `self.git_status`
3. Checked in `_do_extraction()` before auto-upload

**Checks Performed:**
```python
git_status = {
    'git_installed': bool,
    'is_repo': bool,
    'has_remote': bool,
    'can_commit': bool,
    'warnings': list,
    'errors': list
}
```

### Commands Run:

```bash
git --version                    # Check install
git rev-parse --git-dir         # Check repo
git remote -v                   # Check remote
git config user.name            # Check user name
git config user.email           # Check user email
git status --porcelain          # Check uncommitted
```

All with 5-second timeout for safety.

---

## Workflow Diagram

```
┌─────────────────────────────────────┐
│ User Clicks "Assess Document"       │
└──────────────┬──────────────────────┘
               ↓
┌──────────────────────────────────────┐
│ Extract Email Templates              │
└──────────────┬───────────────────────┘
               ↓
┌──────────────────────────────────────┐
│ Detect Images                        │
└──────────────┬───────────────────────┘
               ↓
┌──────────────────────────────────────┐
│ >>> CHECK GIT PREREQUISITES <<<      │
│   - Git installed?                   │
│   - Is repo?                         │
│   - Has remote?                      │
│   - User configured?                 │
│   - Uncommitted changes?             │
└──────────────┬───────────────────────┘
               ↓
       ┌───────┴───────┐
       │               │
  [Errors]        [Warnings/OK]
       │               │
       ↓               ↓
  Show Alert      Log Warnings
       │               │
       └───────┬───────┘
               ↓
┌──────────────────────────────────────┐
│ Show Assessment Results              │
└──────────────┬───────────────────────┘
               ↓
┌──────────────────────────────────────┐
│ User Clicks "Extract Content"        │
└──────────────┬───────────────────────┘
               ↓
┌──────────────────────────────────────┐
│ Extract Content & Save Images        │
└──────────────┬───────────────────────┘
               ↓
       ┌───────┴───────┐
       │               │
  [Git Errors]    [Git OK]
       │               │
       ↓               ↓
  Skip Upload    Auto-Upload
  Show Manual    to GitHub
  Instructions        │
       │               │
       └───────┬───────┘
               ↓
┌──────────────────────────────────────┐
│ Done!                                │
└──────────────────────────────────────┘
```

---

## FAQ

**Q: Does this check happen every time I assess?**
A: Yes! Every time you click "Assess Document", Git is checked.

**Q: Can I skip the check?**
A: No, but it's fast (< 1 second) and helps prevent issues.

**Q: What if I don't have Git installed?**
A: You'll get a clear warning. Images will save locally but won't auto-upload.

**Q: Can I still extract without Git?**
A: Yes! Extraction always works. Only auto-upload requires Git.

**Q: What if I fix Git issues after assessment?**
A: Re-assess the document to verify Git is now working.

**Q: Do warnings block extraction?**
A: No, only errors block auto-upload. Extraction always works.

**Q: Can I use GitHub Desktop instead of Git CLI?**
A: GitHub Desktop includes Git CLI, so it will be detected!

---

## Testing

### Test 1: All Good
1. Have Git installed
2. Be in Git repo with remote
3. Assess document
4. Should see all OK checkmarks

### Test 2: Git Not Installed
1. Uninstall/hide Git temporarily
2. Assess document
3. Should see error popup
4. Should offer install link

### Test 3: Not a Repo
1. Use non-Git folder
2. Assess document
3. Should see error popup
4. Should offer `git init` command

### Test 4: No Remote
1. Be in Git repo without remote
2. Assess document
3. Should see warning (not error)
4. Should offer `git remote add` command

---

## Summary

**Feature:** Git prerequisite checks during document assessment  
**Purpose:** Early warning about Git issues  
**Benefit:** Fix problems before extraction  
**Impact:** Better user experience, fewer surprises  

**Checks:**
- ✅ Git installed
- ✅ Git repository
- ✅ Remote configured
- ✅ User configured
- ⚠️ Uncommitted changes

**Status:** ✅ Complete and tested  
**Version:** 2.0  
**Date:** January 28, 2026  

---

**No more wondering why auto-upload failed - you'll know before you extract!** 🎯

