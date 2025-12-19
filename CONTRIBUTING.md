# Contributing Writeups

This guide explains how to create, preview, and submit writeups for the NC3 CTF repository.

## Quick Start

1. **Generate a new writeup template**
2. **Write your solution**
3. **Preview locally with Hugo**
4. **Submit via Pull Request**

---

## Step 1: Create a New Writeup

Use the provided script to generate a properly formatted writeup template:

```bash
./generate-writeup.sh
```

You'll be prompted for:
- **Title**: Challenge name (e.g., "SantaShield Part 1")
- **Category**: Challenge category (e.g., "Boot2Root", "Crypto", "Web", "Forensics")
- **Date**: Completion date in ISO 8601 format (defaults to current date/time)

The script will create a structured directory under `<category>/<year>/<challenge-name>/` with an `index.md` template.

### Example

```
Title of the Challenge: SantaShield Part 1
Category of the Challenge: Boot2Root
Date of Completion (YYYY-MM-DDTHH:MM:SS+ZZ:ZZ) [Default: current date]: 

Writeup template created at ./boot2root/2025/santashield-part-1/index.md
```

---

## Step 2: Write Your Writeup

Edit the generated `index.md` file and fill in the sections:

```markdown
## Challenge Name:
[Your challenge name]

## Category:
[Category]

## Challenge Description:
[Describe the challenge objectives and context]

## Approach
[Detail your solution methodology, tools used, and key findings]

## Flag
[Include the captured flag]

## Reflections and Learnings
[Share insights, mistakes, and defensive takeaways]
```

### Best Practices

- **Use code blocks** with language specification (e.g., ````bash`, ```python`)
- **Add images** to `images/` folder and reference as `![description](images/filename.png)`
- **Include scripts** in `scripts/` folder and link with `[script.py](scripts/script.py)`
- **Write clear, narrative-driven content** that teaches others

Refer to [.github/copilot-instructions.md](.github/copilot-instructions.md) for full formatting standards.

---

## Step 3: Commit Your Changes

Once your writeup is complete, commit it to a new branch:

```bash
# Create a new branch for your writeup
git checkout -b 2025-add-<challenge-name>

# Stage your changes
git add <category>/<year>/<challenge-name>/

# Commit with a descriptive message
git commit -m "Add writeup for <challenge-name>"

# Push to GitHub
git push origin 2025-add-<challenge-name>
```

---

## Step 4: Preview Your Writeup Locally with Hugo

To see how your writeup will appear on the published blog, you need to run the Hugo site locally.

### Prerequisites

- **Hugo Extended** installed ([Installation Guide](https://gohugo.io/installation/))
- **Git** with submodule support

### Clone the Blog Repository

The blog is hosted in a separate repository that uses this CTF-NC3 repo as a Git submodule:

```bash
# Clone the blog repository
git clone https://github.com/onero/aCTF-Writeup.git
cd aCTF-Writeup
```

### Check Out Your Branch in the Submodule

The `NC3/` folder inside the blog repo is a Git submodule pointing to this repository. You need to check out your feature branch to preview your new writeup:

```bash
# Initialize and update the submodule
git submodule update --init --recursive

# Navigate into the NC3 submodule
cd content/NC3

# Check out your feature branch
git fetch origin
git checkout 2025-add-<challenge-name>

# Return to the blog root
cd ../..
```

### Serve the Hugo Site

Now you can run Hugo's built-in development server:

```bash
hugo server -D
```

Open your browser and navigate to:

```
http://localhost:1313
```

Your writeup should now be visible in the blog! Hugo will automatically reload when you make changes to the markdown files.

### Making Changes

If you need to edit your writeup:

1. Edit the file in `content/NC3/<category>/<year>/<challenge-name>/index.md`
2. Save the file
3. Hugo will auto-reload the preview in your browser
4. Commit changes as needed:

```bash
cd content/NC3
git add .
git commit -m "Update writeup with additional details"
git push origin 2025-add-<challenge-name>
```

---

## Step 5: Submit a Pull Request

Once you're satisfied with your writeup:

1. **Go to GitHub**: Navigate to [https://github.com/onero/CTF-NC3](https://github.com/onero/CTF-NC3)
2. **Open a Pull Request**: From your feature branch to `master`
3. **Add details**: Describe the challenge and your approach in the PR description
4. **Request review**: Tag team members for review
5. **Address feedback**: Make any requested changes
6. **Merge**: Once approved, your writeup will be merged and published!

---

## Troubleshooting

### Hugo Submodule Not Updating

If your changes aren't appearing:

```bash
cd content/NC3
git fetch origin
git checkout 2025-add-<challenge-name>
git pull origin 2025-add-<challenge-name>
```

### Port Already in Use

If port 1313 is occupied:

```bash
hugo server -D -p 1314
```

### Images Not Displaying

Ensure images are in the `images/` folder relative to your `index.md`:

```
boot2root/2025/santashield/
  ├── index.md
  └── images/
      └── screenshot.png
```

Reference them as:

```markdown
![Screenshot](images/screenshot.png)
```

---

## Need Help?

- **Formatting questions**: See [.github/copilot-instructions.md](.github/copilot-instructions.md)
- **Hugo issues**: Check [Hugo Documentation](https://gohugo.io/documentation/)
- **Team support**: Ask on [Discord](https://discord.gg/79snmecfW9)

Happy hacking! 🎄🔐
