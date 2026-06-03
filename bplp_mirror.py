import xml.etree.ElementTree as ET

input_file = input("Enter path to BPLP file: ").replace("\"", '') # ignore quotes if inserted by Windows
output_file = input("Enter path to save BPLP to (or leave blank to overwrite): ").replace("\"", '') or input_file # ignore quotes if inserted by Windows

axis = str(input("Mirror axis? x/y (default x): ") or "x")
translate_dist = float(input("Enter a distance to translate around " + axis + " axis (or leave blank for 0): ") or 0)


tree = ET.parse(input_file)
root = tree.getroot()

for X_coord in root.iter('X'):
	match axis:
		case "x":
			new_X_coord = round((-float(X_coord.text) + translate_dist), 2)
			X_coord.text = str(new_X_coord)
		case _:
			pass

for Y_coord in root.iter('Y'):
	match axis:
		case "y":
			new_Y_coord = round((-float(Y_coord.text) + translate_dist), 2)
			Y_coord.text = str(new_Y_coord)
		case _:
			pass

tree.write(output_file, xml_declaration=True)