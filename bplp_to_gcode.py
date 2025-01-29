import xml.etree.ElementTree as ET

input_file = input("Enter path to BPLP file: ").replace("\"", '') # ignore quotes if inserted by Windows
output_file = input("Enter path to save Gcode to: ").replace("\"", '') # ignore quotes if inserted by Windows

def LinePoint_to_gcode(LinePoint, prev_X, prev_Y, prev_Z):
	X = ""
	Y = ""
	Z = ""

	current_X = LinePoint.find("X").text
	current_Y = LinePoint.find("Y").text
	current_Z = LinePoint.find("Z").text

	if prev_X != current_X:
		X = "X" + str(current_X)
	if prev_Y != current_Y:
		Y = "Y" + str(current_Y)
	if prev_Z != current_Z:
		Z = "Z" + str(current_Z)

	if X+Y+Z == "":
		gcode = ""
	else:
		gcode = ["G1", X, Y, Z]
		gcode = [i for i in gcode if i]
		gcode = " ".join(gcode) + "\n"

	return gcode, current_X, current_Y, current_Z


def main():

	tree = ET.parse(input_file)
	root = tree.getroot()

	prev_X = 0
	prev_Y = 0
	prev_Z = 0

	with open(output_file, "w") as file:
		for LinePoint in root.findall('.//LinePoint'):
			gcode, prev_X, prev_Y, prev_Z = LinePoint_to_gcode(LinePoint, prev_X, prev_Y, prev_Z)
			file.write(gcode)

main()