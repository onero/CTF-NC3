#!/bin/bash

# Function to convert a string to lowercase and replace spaces with hyphens
slugify() {
    echo "$1" | awk '{print tolower($0)}' | sed -r 's/\s+/-/g'
}

# Prompt for challenge details
read -p "Title of the Challenge: " title
read -p "Category of the Challenge: " category
read -p "Date of Completion (YYYY-MM-DDTHH:MM:SS+ZZ:ZZ) [Default: current date]: " date

# Default date if not provided
if [ -z "$date" ]; then
    date=$(date +"%Y-%m-%dT%H:%M:%S")
    tz=$(date +%z | sed 's/\(.\{3\}\)/\1:/')
    date="$date$tz"
fi

# Convert title and category to URL-friendly slugs
title_slug=$(slugify "$title")
category_slug=$(slugify "$category")

# Map category slug to repository folder names
declare -A CATEGORY_MAP
CATEGORY_MAP[
    "crypto"
]="crypto"
CATEGORY_MAP[
    "web"
]="web"
CATEGORY_MAP[
    "malware"
]="malware"
CATEGORY_MAP[
    "forensics"
]="forensics"
CATEGORY_MAP[
    "kom-godt-i-gang"
]="kom-godt-i-gang"
CATEGORY_MAP[
    "boot2root"
]="boot2root"
CATEGORY_MAP[
    "det-store-nissehack"
]="Det-store-nissehack"

# Resolve category directory using mapping, fallback to slug
repo_category_dir=${CATEGORY_MAP[$category_slug]:-$category_slug}
category_dir="./$repo_category_dir"

# Determine year from provided date (fallback to current year)
year=$(date -d "$date" +%Y 2>/dev/null)
if [ -z "$year" ]; then
    year=$(date +%Y)
fi

# Directory path with year
year_dir="$category_dir/$year"
challenge_dir="$year_dir/$title_slug"

# Create category directory if it doesn't exist
if [ ! -d "$year_dir" ]; then
    mkdir -p "$year_dir"
fi

# Create challenge directory
mkdir -p "$challenge_dir"

# Create index.md with provided details
cat << EOF > "$challenge_dir/index.md"
+++
title = '$title'
categories = ['$category']
date = $date
scrollToTop = true
+++

## Challenge Name:

$title

## Category:

$category

## Challenge Description:

## Approach

## Flag

\`\`\`text

\`\`\`

## Reflections and Learnings
EOF

echo "Writeup template created at $challenge_dir/index.md"
