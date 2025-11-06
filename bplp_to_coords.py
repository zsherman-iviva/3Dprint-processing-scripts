import xml.etree.ElementTree as ET

input_file = input("Enter path to BPLP file: ").replace("\"", '') # ignore quotes if inserted by Windows
output_file = input("Enter path to save txt to: ").replace("\"", '') # ignore quotes if inserted by Windows
include_z = input("Include Z coordinates? y/n (default y): ") or "y"

def LinePoint_to_coords(LinePoint):
	X = LinePoint.find("X").text
	Y = LinePoint.find("Y").text
	Z = LinePoint.find("Z").text

	return X, Y, Z

def main():

	tree = ET.parse(input_file)
	root = tree.getroot()

	with open(output_file, "w") as file:
		for LinePoint in root.findall('.//LinePoint'):
			X, Y, Z = LinePoint_to_coords(LinePoint)
			if include_z == "y":
				file.write((X + "," + Y + "," + Z + "\n"))
			else:
				file.write((X + "," + Y + "\n"))

main()