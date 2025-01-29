import xml.etree.ElementTree as ET
import copy

input_file = input("Enter path to BPLP file to multiply: ").replace("\"", '') # ignore quotes if inserted by Windows
output_file = input("Enter path to save BPLP to (or leave blank to overwrite): ").replace("\"", '') or input_file # ignore quotes if inserted by Windows

n_instances = int(input("Enter the desired total number of instances (or leave blank for 2, which is one copy): ") or 2)
translate_X = float(input("Enter a distance to translate in X (or leave blank for 0): ") or 0)
translate_Y = float(input("Enter a distance to translate in Y (or leave blank for 0): ") or 0)
translate_Z = float(input("Enter a distance to translate in Z (or leave blank for 0): ") or 0)


def rename_line(line, new_number):
	name = line.find('Name')

	if name.text[-1].isdigit:
		head = name.text.rstrip('0123456789')
		tail = str(new_number)
		name.text = head+tail
	else:
		name.text += new_number


def translate_xyz(lines, translate_X, translate_Y, translate_Z):
	for line in lines:

		for X_coord in line.iter('X'):
			new_X_coord = float(X_coord.text) + translate_X
			X_coord.text = str(new_X_coord)

		for Y_coord in line.iter('Y'):
			new_Y_coord = float(Y_coord.text) + translate_Y
			Y_coord.text = str(new_Y_coord)

		for Z_coord in line.iter('Z'):
			new_Z_coord = float(Z_coord.text) + translate_Z
			Z_coord.text = str(new_Z_coord)


def main():
	tree = ET.parse(input_file)
	root = tree.getroot()

	all_lines = root.find('Lines')
	original_lines = root.findall('.//Line')
	new_lines = original_lines # copy.deepcopy(original_lines)

	all_lines.clear()

	for i in range(n_instances):
		new_lines = copy.deepcopy(new_lines)

		for line_id, line in enumerate(new_lines):

			new_number = (line_id+1)+i*len(new_lines)
			#print('line id: ' + str(line_id) + ' | i: ' + str(i) + ' | len(new_lines): ' + str(len(new_lines)) + ' | new number: ' + str(new_number))
			rename_line(line, new_number)
			#print(line.find('Name').text)
			
		translate_xyz(new_lines, translate_X, translate_Y, translate_Z)

		for line in new_lines:
			all_lines.append(line)

	ET.indent(root)
	tree.write(output_file, encoding="utf-8")


main()