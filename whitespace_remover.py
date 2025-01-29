input_file = input("Enter path to Gcode file: ").replace("\"", '') # ignore quotes if inserted by Windows
output_file = input("Enter path to save BPLP to: ").replace("\"", '') # ignore quotes if inserted by Windows

all_lines = []

with open(input_file, 'r') as f:
	for line in f:
		line = "".join(line.split())
		all_lines.append(line)

spaces_removed = "\n".join(all_lines)

with open(output_file, 'w') as o:
	o.write(spaces_removed)