
# Setting up this Project on GitHub

It looks like **Git** is not currently installed or configured in your environment. Follow these steps to get your project on GitHub:

## 1. Install Git
If you haven't already, download and install Git from [git-scm.com](https://git-scm.com/downloads).

## 2. Initialize the Repository
Open your terminal (Command Prompt or PowerShell) and navigate to the project folder:
```bash
cd faceless_video_studio
```

Initialize Git:
```bash
git init
```

## 3. Commit Your Files
Add all files to the staging area:
```bash
git add .
```

Commit the files:
```bash
git commit -m "Initial commit of Faceless Video Studio"
```

## 4. Create a Repository on GitHub
1.  Log in to [GitHub](https://github.com).
2.  Click the **+** icon in the top-right corner and select **New repository**.
3.  Name your repository (e.g., `faceless-video-studio`).
4.  Do **not** initialize with README, .gitignore, or License (we already have them).
5.  Click **Create repository**.

## 5. Push to GitHub
Copy the commands shown on the GitHub setup page under "…or push an existing repository from the command line". They will look like this:

```bash
git remote add origin https://github.com/YOUR_USERNAME/faceless-video-studio.git
git branch -M main
git push -u origin main
```

## 6. Verification
Refresh your GitHub repository page. You should now see all your files listed there!
