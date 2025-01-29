from gcodeparser import GcodeParser

input_file = input("Enter path to relative Gcode file: ").replace("\"", '') # ignore quotes if inserted by Windows
output_file = input("Enter path to save absolute Gcode file to: ").replace("\"", '') # ignore quotes if inserted by Windows


def process_line(line, prev_X, prev_Y, prev_Z, prev_F):

	match line.command_str:
		case "G1" | "G0": # move and extrude or travel
			print(line)
			X = round((prev_X + (line.get_param("X") or 0)), 2)
			print(line.get_param('X'))
			Y = round(prev_Y + (line.get_param("Y") or 0), 2)
			Z = round(prev_Z + (line.get_param("Z") or 0), 2)
			F = line.get_param("F")

			prev_X = X
			prev_Y = Y
			prev_Z = Z
			prev_F = F

		case "G91": # todo
			pass

	return prev_X, prev_Y, prev_Z, prev_F


def main():

	absolute_gcode_lines = []

	# this section handles GcodeParser not understanding extra spaces in Gcode lines
	all_lines = []
	with open(input_file, 'r') as f:
		for line in f:
			line = "".join(line.split())
			all_lines.append(line)
	spaces_removed = "\n".join(all_lines)

	gcode_lines = GcodeParser(spaces_removed, include_comments=False).lines

	prev_X = 0.0
	prev_Y = 0.0
	prev_Z = 0.0
	prev_F = 0.0

	for line in gcode_lines:
		prev_X, prev_Y, prev_Z, prev_F = process_line(line, prev_X, prev_Y, prev_Z, prev_F)

		line.update_param("X", prev_X)
		line.update_param("Y", prev_Y)
		line.update_param("Z", prev_Z)
		line.update_param("F", prev_F)
		
		absolute_gcode_lines.append(line.gcode_str)

	with open(output_file, 'w') as f:
		f.write('\n'.join(absolute_gcode_lines))

main()