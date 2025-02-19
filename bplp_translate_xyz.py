import xml.etree.ElementTree as ET

input_file = input("Enter path to BPLP file: ").replace("\"", '') # ignore quotes if inserted by Windows
output_file = input("Enter path to save BPLP to (or leave blank to overwrite): ").replace("\"", '') or input_file # ignore quotes if inserted by Windows

translate_X = float(input("Enter a distance to translate in X (or leave blank for 0): ") or 0)
translate_Y = float(input("Enter a distance to translate in Y (or leave blank for 0): ") or 0)
translate_Z = float(input("Enter a distance to translate in Z (or leave blank for 0): ") or 0)

tree = ET.parse(input_file)
root = tree.getroot()

for X_coord in root.iter('X'):
	new_X_coord = round((float(X_coord.text) + translate_X), 2)
	X_coord.text = str(new_X_coord)

for Y_coord in root.iter('Y'):
	new_Y_coord = round((float(Y_coord.text) + translate_Y), 2)
	Y_coord.text = str(new_Y_coord)

for Z_coord in root.iter('Z'):
	new_Z_coord = round((float(Z_coord.text) + translate_Z), 2)
	Z_coord.text = str(new_Z_coord)

tree.write(output_file, xml_declaration=True)