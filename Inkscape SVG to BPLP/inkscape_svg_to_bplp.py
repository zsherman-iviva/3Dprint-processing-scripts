import xml.etree.ElementTree as ET

input_file = input("Enter path to discretized SVG file: ").replace("\"", '') # ignore quotes if inserted by Windows
output_file = input("Enter path to save BPLP to: ").replace("\"", '') # ignore quotes if inserted by Windows

while True:
	speed = input("Enter desired print speed (1-100, integers only, default 50): ") or 50
	try:
		speed = int(speed)
		if (0 < speed < 101) == False:
			raise TypeError
		break
	except:
		print("Input was not understood. Please choose a speed between 1 and 100.")


def path_to_LinePoint(X, Y):
	LinePoint = f"""
		<LinePoint>
			<X>{X}</X>
			<Y>{Y}</Y>
			<Z>0</Z>
		</LinePoint>
		"""
	return LinePoint


def process_path(root, d):

	global line_name

	lines = root.find("Lines")

	lines.append(ET.fromstring(f"""
		<Line>
			<Name>Line{line_name}</Name>
			<Points></Points>
			<Speed>{speed}</Speed>
		</Line>
	"""))
	line_name += 1

	split_line = d.split()
	
	last_points = root.findall("./Lines/Line/Points")[-1]
	last_points.append(ET.fromstring(path_to_LinePoint(split_line[1], split_line[2])))

	rest_of_line = split_line[3:]
	if len(rest_of_line) % 3 != 0:
		print(rest_of_line)
		raise ValueError

	num_points = int(len(rest_of_line) / 3)

	for i in range(num_points):
		last_points.append(ET.fromstring(path_to_LinePoint(rest_of_line[i*3+1], rest_of_line[i*3+2])))


def main():

	root = ET.Element('BioPlotterLineProject')
	tree = ET.ElementTree(root)

	root.append(ET.fromstring('<DoZTouch>false</DoZTouch>'))
	root.append(ET.fromstring('<CleanNozzleAtStart>false</CleanNozzleAtStart>'))
	root.append(ET.fromstring('<TransferHeight>0</TransferHeight>'))
	root.append(ET.fromstring('<Lines></Lines>'))

	global line_name
	line_name = 1


	
	svg_tree = ET.parse(input_file)
	svg_root = svg_tree.getroot()

	for g in svg_root.findall('{*}g'):
		for path in g.findall('{*}path'):
			d = path.get('d')
			process_path(root, d)

	ET.indent(root)
	tree.write(output_file, encoding="utf-8")

main()
