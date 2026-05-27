import ezdxf
from ezdxf import units
from ezdxf.addons.drawing import Frontend, RenderContext, svg, layout, config
from ezdxf.math import ConstructionPolyline

input_file = input("Enter path to DXF file (must have been exported with mm units): ").replace("\"", '') # ignore quotes if inserted by Windows
output_file = input("Enter path to save DXF to: ").replace("\"", '') # ignore quotes if inserted by Windows

doc = ezdxf.readfile(input_file)
msp = doc.modelspace()

for entity in msp:
	if entity.dxftype() == "SPLINE":
		if entity is not None:
			polyline = ConstructionPolyline(entity.flattening(1))
		msp.add_lwpolyline(polyline)
		msp.delete_entity(entity)

doc.saveas(output_file)