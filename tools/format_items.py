# Assuming your file is named 'items.txt'
input_file_path = 'items.txt'
output_file_path = 'transformed_items.txt'

with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
    for line in input_file:
        # Strip newline and any trailing spaces
        line = line.strip()
        
        # Split the line by comma and strip spaces
        name, id = [x.strip() for x in line.split(',')]
        
        # Format the line according to the specified transformation
        transformed_line = f'("{id}", "{name}"),\n'
        
        # Write the transformed line to the output file
        output_file.write(transformed_line)

print(f"Transformation complete. Check '{output_file_path}' for the results.")
