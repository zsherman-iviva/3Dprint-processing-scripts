import xml.etree.ElementTree as ET

import ezdxf
from ezdxf.addons.drawing import Frontend, RenderContext, svg, layout, config
from ezdxf.math import ConstructionPolyline

input_file = input("Enter path to DXF file (must have been exported with mm units): ").replace("\"", '') # ignore quotes if inserted by Windows
output_file = input("Enter path to save BPLP to: ").replace("\"", '') # ignore quotes if inserted by Windows

flattening_distance = 0.15 # maximum distance from the center of the curve to the center of the line segment between two approximation points to determine if a segment should be subdivided

while True:
	speed = input("Enter desired print speed (1-100, integers only, default 50): ") or 50
	try:
		speed = int(speed)
		if (0 < speed < 101) == False:
			raise TypeError
		break
	except:
		print("Input was not understood. Please choose a speed between 1 and 100.")


def coords_to_LinePoint(X, Y):
	LinePoint = f"""
		<LinePoint>
			<X>{X}</X>
			<Y>{Y}</Y>
			<Z>0</Z>
		</LinePoint>
		"""
	return LinePoint


def process_entity(root, coord_list):

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

	last_points = root.findall("./Lines/Line/Points")[-1]

	for x, y in coord_list:
		last_points.append(ET.fromstring(coords_to_LinePoint(x, y)))

def dxf_to_coords(input_file):
	doc = ezdxf.readfile(input_file)
	msp = doc.modelspace()

	all_entities = msp.query("*")
	original_layer = msp.query("*").first.dxf.layer # using the layer that came from Onshape (could alternatively use layer 0, or probably omit altogether)

	all_paths = []

	for entity in all_entities:
		all_paths.append(ezdxf.path.make_path(entity))
		msp.delete_entity(entity)

	# render all paths onto modelspace
	ezdxf.path.render_lwpolylines(msp, all_paths, distance=float(flattening_distance), segments=1, dxfattribs={"layer": original_layer})

	all_entities = msp.query("*")
	all_polyline_coords = []

	for entity in all_entities:
		all_polyline_coords.append([])

		for x, y in entity.vertices():
			x = round(float(x), 2)
			y = round(float(y), 2)

			all_polyline_coords[-1].append(tuple([x,y]))

	return all_polyline_coords


def main():

	root = ET.Element('BioPlotterLineProject')
	tree = ET.ElementTree(root)

	root.append(ET.fromstring('<DoZTouch>false</DoZTouch>'))
	root.append(ET.fromstring('<CleanNozzleAtStart>false</CleanNozzleAtStart>'))
	root.append(ET.fromstring('<TransferHeight>0</TransferHeight>'))
	root.append(ET.fromstring('<Lines></Lines>'))

	global line_name
	line_name = 1

	all_polyline_coords = dxf_to_coords(input_file)

	for coord_list in all_polyline_coords:
		process_entity(root, coord_list)

	ET.indent(root)
	tree.write(output_file, encoding="utf-8")

main()