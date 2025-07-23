from gcodeparser import GcodeParser

input_file = input("Enter path to Gcode file: ").replace("\"", '') # ignore quotes if inserted by Windows
output_file = input("Enter path to save Gcode to (or leave blank to overwrite): ").replace("\"", '') or input_file # ignore quotes if inserted by Windows

translate_X = float(input("Enter a distance to translate in X (or leave blank for 0): ") or 0)
translate_Y = float(input("Enter a distance to translate in Y (or leave blank for 0): ") or 0)
translate_Z = float(input("Enter a distance to translate in Z (or leave blank for 0): ") or 0)
translate_E = float(input("Enter a distance to translate in E (or leave blank for 0): ") or 0)

# this section handles GcodeParser not understanding extra spaces in Gcode lines
all_lines = []
with open(input_file, 'r') as f:
	for line in f:
		line = "".join(line.split())
		all_lines.append(line)
spaces_removed = "\n".join(all_lines)

gcode_lines = GcodeParser(spaces_removed, include_comments=True).lines

translated_lines = []

for line in gcode_lines:
	X = line.get_param('X')
	if X is not None:
		line.update_param('X', round(X+translate_X, 3))

	Y = line.get_param('Y')
	if Y is not None:
		line.update_param('Y', round(Y+translate_Y, 3))

	Z = line.get_param('Z')
	if Z is not None:
		line.update_param('Z', round(Z+translate_Z, 3))

	E = line.get_param('E')
	if E is not None:
		line.update_param('E', round(E+translate_E, 4))

	translated_lines.append(line.gcode_str)

with open(output_file, 'w') as f:
	f.write('\n'.join(translated_lines))