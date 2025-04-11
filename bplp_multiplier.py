import xml.etree.ElementTree as ET
import copy

input_file = input("Enter path to BPLP file to multiply: ").replace("\"", '') # ignore quotes if inserted by Windows
output_file = input("Enter path to save BPLP to (or leave blank to overwrite): ").replace("\"", '') or input_file # ignore quotes if inserted by Windows

n_instances = int(input("Enter the desired total number of instances (or leave blank for 2, which is one copy): ") or 2)
translate_X = float(input("Enter a distance to translate in X (or leave blank for 0): ") or 0)
translate_Y = float(input("Enter a distance to translate in Y (or leave blank for 0): ") or 0)
translate_Z = float(input("Enter a distance to translate in Z (or leave blank for 0): ") or 0)
Z_hop = float(input("Enter the desired Z hop between instances (or leave blank for 0): ") or 0)


def rename_line(line, new_number):
	name = line.find('Name')

	if name.text[-1].isdigit():
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


def coords_to_LinePoint(X, Y, Z):

	X = round(X, 2)
	Y = round(Y, 2)
	Z = round(Z, 2)

	LinePoint = f"""
		<LinePoint>
			<X>{X}</X>
			<Y>{Y}</Y>
			<Z>{Z}</Z>
		</LinePoint>
		"""
	return LinePoint


def main():
	tree = ET.parse(input_file)
	root = tree.getroot()

	all_lines = root.find('Lines')
	num_lines = len(all_lines)
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
		
		if len(all_lines) >= len(new_lines): # only translate subsequent instances, leave original instance alone
			translate_xyz(new_lines, translate_X, translate_Y, translate_Z)

		for line in new_lines:
			all_lines.append(line)

		new_lines = copy.deepcopy(new_lines) # not sure why having this line here makes it work, but it does...

		#print(len(new_lines[0].findall("Points/LinePoint"))) # prints number of linepoints in new_lines

		if Z_hop > 0:
			first_linepoint = all_lines.findall('.//Points')[-1].find('LinePoint')
			last_linepoint = all_lines.findall('.//LinePoint')[-1]

			first_X = float(first_linepoint.find("X").text)
			first_Y = float(first_linepoint.find("Y").text)
			first_Z = float(first_linepoint.find("Z").text)

			last_X = float(last_linepoint.find("X").text)
			last_Y = float(last_linepoint.find("Y").text)
			last_Z = float(last_linepoint.find("Z").text)

			last_instance = all_lines.findall('.//Points')[-num_lines]
			last_line = all_lines.findall('.//Points')[-1]

			if i > 0: # if not the first instance
				last_instance.insert(0, ET.fromstring(coords_to_LinePoint(first_X+0.2, first_Y, first_Z+Z_hop))) # need to add >0.1 mm (or other Minimum Length), otherwise Bioplotter will ignore line

			if i < (n_instances - 1): # if not the last instance
				last_line.append(ET.fromstring(coords_to_LinePoint(last_X+0.2, last_Y, last_Z+translate_Z+Z_hop))) # need to add >0.1 mm (or other Minimum Length), otherwise Bioplotter will ignore line

	ET.indent(root)
	tree.write(output_file, encoding="utf-8")


main()