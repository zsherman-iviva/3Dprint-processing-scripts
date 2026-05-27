import ezdxf
from ezdxf.addons.drawing import Frontend, RenderContext, svg, layout, config
from ezdxf.math import ConstructionPolyline

input_file = input("Enter path to DXF file (must have been exported with mm units): ").replace("\"", '') # ignore quotes if inserted by Windows
output_file = input("Enter path to save DXF to: ").replace("\"", '') # ignore quotes if inserted by Windows

doc = ezdxf.readfile(input_file)
msp = doc.modelspace()

all_entities = msp.query("*")
original_layer = msp.query("*").first.dxf.layer # using the layer that came from Onshape (could alternatively use layer 0)

for entity in all_entities:
	if entity.dxftype() == "SPLINE":
		if entity is not None:
			polyline = ConstructionPolyline(entity.flattening(1))
			msp.add_lwpolyline(polyline, dxfattribs={"layer": original_layer})
			msp.delete_entity(entity)


all_entities = msp.query("*")
all_polyline_coords = []

for entity in all_entities:
	all_polyline_coords.append([])
	for x, y in entity.vertices():
		all_polyline_coords[-1].append(tuple([round(float(x), 2),round(float(y), 2)]))

print(all_polyline_coords)

doc.saveas(output_file)