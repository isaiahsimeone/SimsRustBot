# Extract table data from this site - https://www.corrosionhour.com/rust-item-list/

# Inspect the table, ensure all cells under 'Display name', 'Short name', 'ID' are populated
# Sort by item ID Then, Copy the <tbody> tag to input.txt

#!/bin/bash

# Input HTML file
inputFile="input.html"
# Output file
outputFile="extracted_data.txt"

# Use grep to find lines containing the desired classes, then use sed to extract and format the text
grep -oP '(?<=class="ch-tbl-name">)[^<]+|(?<=class="ch-tbl-short-name">)[^<]+|(?<=class="ch-tbl-id sorting_1">)[^<]+' "$inputFile" | 
sed ':a;N;$!ba;s/\n/,/g' | 
sed 's/,/\n/g' | 
awk 'NR%3{printf "%s,",$0; next}1' |
sed 's/,$/\n/' > "$outputFile"

echo "Data extracted to $outputFile."
