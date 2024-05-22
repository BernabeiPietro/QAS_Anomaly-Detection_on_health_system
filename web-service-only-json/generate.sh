#!/bin/bash


# Set number of files 
num_files=1000
dimensione_file=1M
# Directory to store files 
output_dir="/usr/local/apache2/htdocs/"

# Create output directory if it doesn't exist
mkdir -p "$output_dir"

# Generate JSON files and list content in HTML file
html_content="<h1>Generated JSON Files</h1><ul>"

for i in $(seq 1 $num_files); do

  # Create filename
  filename="data_$i.json"

  dd if=/dev/urandom of="$output_dir/$filename" bs=1M count=10

  # Write JSON data to file
  #echo "$json_content" > "$output_dir/$filename"
  #fallocate -l ${dimensione_file} "$output_dir/null_$filename"
  # Add link to HTML list
  html_content="$html_content<li><a href='$filename'>data_$i.json</a></li>"
  #html_content="$html_content<li><a href='null_$filename'>null_data_$i.json</a></li>"
done

# Close HTML list and create HTML file
html_content="$html_content</ul>"
echo "$html_content" > "$output_dir/index.html"

echo "Generated $num_files JSON files and index.html in $output_dir"

