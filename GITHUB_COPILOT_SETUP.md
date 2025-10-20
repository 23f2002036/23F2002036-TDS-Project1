# How to Verify GitHub Copilot Pro Free Access in VS Code

This guide helps you check whether your GitHub Copilot Pro free access is properly linked to your VS Code installation.

## Prerequisites

- Visual Studio Code installed on your system
- A GitHub account with Copilot Pro access (free or paid)
- GitHub Copilot extension installed in VS Code

## Step-by-Step Verification

### 1. Check Your GitHub Copilot Subscription Status

First, verify your subscription on GitHub:

1. Go to [GitHub Copilot Settings](https://github.com/settings/copilot)
2. Sign in with your GitHub account
3. Check if you see:
   - "GitHub Copilot is active for your account" or
   - "You have access to GitHub Copilot through [organization/education/free trial]"
4. Verify the subscription type (Individual, Business, or Enterprise)

### 2. Install GitHub Copilot Extension in VS Code

1. Open VS Code
2. Click on the Extensions icon in the left sidebar (or press `Ctrl+Shift+X` / `Cmd+Shift+X`)
3. Search for "GitHub Copilot"
4. Install the following extensions:
   - **GitHub Copilot** (by GitHub)
   - **GitHub Copilot Chat** (by GitHub) - optional but recommended

### 3. Sign In to GitHub in VS Code

1. After installing the extension, you'll see a notification to sign in
2. Click "Sign in to GitHub" or go to the Accounts icon (👤) in the bottom-left corner
3. Select "Sign in with GitHub to use GitHub Copilot"
4. Your browser will open - authorize VS Code to access your GitHub account
5. Return to VS Code after authorization

### 4. Verify Copilot is Active

There are several ways to confirm Copilot is working:

#### Method 1: Check the Status Bar
- Look at the bottom-right corner of VS Code
- You should see a GitHub Copilot icon or text label
- If it's active (not grayed out or showing an error symbol), Copilot is working
- Click the icon/label to see detailed status and options

#### Method 2: Check Extension Status
1. Go to Extensions (`Ctrl+Shift+X` / `Cmd+Shift+X`)
2. Find "GitHub Copilot" in your installed extensions
3. It should show "Active" or no error messages

#### Method 3: Test with Code Suggestions
1. Create a new file (e.g., `test.py` or `test.js`)
2. Start typing a function comment, like:
   ```python
   # Function to calculate factorial of a number
   ```
3. Press Enter and wait 1-2 seconds
4. If Copilot is working, you'll see gray suggested code appear
5. Press `Tab` to accept the suggestion or `Esc` to dismiss it

#### Method 4: Check Copilot Chat (if installed)
1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
2. Type "GitHub Copilot: Open Chat"
3. If the chat panel opens, Copilot Chat is working
4. Try asking a question like "How do I create a function in Python?"

### 5. Verify Account Connection

1. Click on the Accounts icon (👤) in the bottom-left corner of VS Code
2. You should see your GitHub username listed
3. Hover over it to see text indicating Copilot access is enabled

### 6. Check Copilot Settings

1. Open VS Code Settings (`Ctrl+,` / `Cmd+,`)
2. Search for "copilot"
3. Verify that:
   - "GitHub Copilot: Enable" is checked
   - Other relevant settings match your preferences

## Troubleshooting

### Issue: Copilot Icon Shows "X" or Red Status

**Solution:**
1. Click the Copilot icon in the status bar
2. Read the error message
3. Common fixes:
   - Sign out and sign back in to GitHub
   - Check your internet connection
   - Restart VS Code
   - Verify your GitHub Copilot subscription is still active

### Issue: No Suggestions Appearing

**Solution:**
1. Check if Copilot is enabled for the file type:
   - Click the Copilot icon
   - Check if suggestions are disabled for this language
2. Verify Copilot is not in "disabled" mode
3. Check your settings: Search for "GitHub Copilot: Enable" in settings
4. Try reloading VS Code window (`Ctrl+Shift+P` > "Reload Window")

### Issue: "Not Authorized" or "Subscription Required"

**Solution:**
1. Verify your GitHub account has active Copilot access at [GitHub Copilot Settings](https://github.com/settings/copilot)
2. If you have free access through education or organization:
   - Ensure you're signed in with the correct GitHub account
   - Verify your student/organization status is still valid
3. Sign out of GitHub in VS Code and sign back in
4. Uninstall and reinstall the GitHub Copilot extension if issues persist

### Issue: Already Signed In But Copilot Not Working

**Solution:**
1. Sign out of GitHub: Click Accounts (👤) > Your GitHub username > Sign out
2. Restart VS Code completely
3. Sign in again to GitHub
4. Authorize GitHub Copilot when prompted

### Issue: Multiple GitHub Accounts

**Solution:**
1. Make sure you're signed in with the account that has Copilot access
2. Sign out of all GitHub accounts in VS Code
3. Sign in with the correct account
4. VS Code may prompt which account to use for Copilot - select the one with access

## Additional Resources

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [VS Code GitHub Copilot Extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)
- [GitHub Copilot Pricing and Plans](https://github.com/features/copilot/plans)
- [GitHub Education Benefits](https://education.github.com/benefits)

## Quick Reference Commands

| Action | Command (Windows/Linux) | Command (Mac) |
|--------|------------------------|---------------|
| Open Command Palette | `Ctrl+Shift+P` | `Cmd+Shift+P` |
| Open Extensions | `Ctrl+Shift+X` | `Cmd+Shift+X` |
| Open Settings | `Ctrl+,` | `Cmd+,` |
| Accept Copilot Suggestion | `Tab` | `Tab` |
| Reject Copilot Suggestion | `Esc` | `Esc` |
| Next Suggestion | `Alt+]` | `Option+]` |
| Previous Suggestion | `Alt+[` | `Option+[` |

## Verification Checklist

Use this checklist to ensure everything is set up correctly:

- [ ] GitHub account has active Copilot subscription (verified at github.com/settings/copilot)
- [ ] GitHub Copilot extension installed in VS Code
- [ ] Signed in to GitHub in VS Code (check Accounts icon)
- [ ] Copilot icon in status bar shows active status (not grayed out or with X)
- [ ] Code suggestions appear when typing
- [ ] No error messages in Copilot status or output panel
- [ ] Settings show "GitHub Copilot: Enable" is checked

If all items are checked, your GitHub Copilot Pro free access is properly linked to VS Code! 🎉

## Support

If you're still experiencing issues after following this guide:
1. Check the [GitHub Copilot Status Page](https://www.githubstatus.com/)
2. Visit [GitHub Community Discussions](https://github.com/community/community/discussions/categories/copilot)
3. Contact GitHub Support if you have an active subscription
