from gcodeparser import GcodeParser
import xml.etree.ElementTree as ET

input_file = input("Enter path to Gcode file: ").replace("\"", '') # ignore quotes if inserted by Windows
output_file = input("Enter path to save BPLP to: ").replace("\"", '') # ignore quotes if inserted by Windows

while True:
	separate_method = input("Separate lines by 1) (default) Don't separate / 2) Feedrate / 3) Layer: ") or 1
	try:
		separate_method = int(separate_method)
		if (0 < separate_method < 4) == False:
			raise TypeError
		break
	except:
		print("Input was not understood. Please type 1, 2, or 3 only.")

if separate_method == 1 or separate_method == 3:
	while True:
		speed = input("Enter desired print speed (1-100, default 50): ") or 50
		try:
			speed = int(speed)
			if (0 < speed < 101) == False:
				raise TypeError
			break
		except:
			print("Input was not understood. Please choose a speed between 1 and 100.")

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

def process_line(root, line, prev_X, prev_Y, prev_Z, prev_F):

	global relative
	global line_name

	match line.command_str:
		case "G1": # move and extrude
			lines = root.find("Lines")

			match separate_method:
				case 1: # no separation
					F = speed
					if len(lines) < 1: # if no lines,
						# create one
						lines.append(ET.fromstring(f"""
							<Line>
								<Name>Line{line_name}</Name>
								<Points></Points>
								<Speed>{speed}</Speed>
							</Line>
						"""))
				
				case 2: # separate by feedrate
					F = line.get_param("F")

					if F and F != prev_F: # create new line if desired feedrate has changed
						if F > 1000:
							F_bplp = 100 # 100% is max speed in BPLP files
						else:
							F_bplp = round(F/10)

						last_point = None
						if len(lines) > 0: # if no lines, can't get last point from previous line
							last_point = lines.findall('Line/Points/LinePoint')[-1]

						lines.append(ET.fromstring(f"""
							<Line>
								<Name>Line{line_name}</Name>
								<Points></Points>
								<Speed>{F_bplp}</Speed>
							</Line>
						"""))

						line_name += 1

						if last_point is not None:
							# add last point of previous line as first point in new line to maintain line continuity
							new_points_element = lines.findall('Line/Points')[-1]
							new_points_element.append(last_point)
				
				case 3: # separate by layer
					F = speed
					Z = line.get_param("Z")

					if Z and 0.04 < (Z - prev_Z) < 0.5: # create new line if this is likely a new layer based on Z change

						last_point = None
						if len(lines) > 0: # if no lines, can't get last point from previous line
							last_point = lines.findall('Line/Points/LinePoint')[-1]

						lines.append(ET.fromstring(f"""
							<Line>
								<Name>Line{line_name}</Name>
								<Points></Points>
								<Speed>{speed}</Speed>
							</Line>
						"""))

						line_name += 1

						if last_point is not None:
							# add last point of previous line as first point in new line to maintain line continuity
							new_points_element = lines.findall('Line/Points')[-1]
							new_points_element.append(last_point)

			if relative:
				X = prev_X + (line.get_param("X") or 0)
				Y = prev_Y + (line.get_param("Y") or 0)
				Z = prev_Z + (line.get_param("Z") or 0)
			else: # if absolute
				X = line.get_param("X") or prev_X
				Y = line.get_param("Y") or prev_Y
				Z = line.get_param("Z") or prev_Z

			prev_X = X
			prev_Y = Y
			prev_Z = Z
			prev_F = F

			try:
				last_points = root.findall("./Lines/Line/Points")[-1]
				last_points.append(ET.fromstring(coords_to_LinePoint(X, Y, Z)))
			except:
				print('Please ensure first G1 (move and extrude) command contains a feedrate (F), '
					'otherwise BPLP output may be different than expected.')

		case "G90": # absolute coordinates
			relative=False

		case "G91": # relative coordinates
			relative=True

		case _: # another command not specified
			pass

	return prev_X, prev_Y, prev_Z, prev_F


def main():

	root = ET.Element('BioPlotterLineProject')
	tree = ET.ElementTree(root)

	root.append(ET.fromstring('<DoZTouch>true</DoZTouch>'))
	root.append(ET.fromstring('<CleanNozzleAtStart>true</CleanNozzleAtStart>'))
	root.append(ET.fromstring('<TransferHeight>0</TransferHeight>'))
	root.append(ET.fromstring('<Lines></Lines>'))


	with open(input_file, 'r') as f:
		gcode = f.read()

	gcode_lines = GcodeParser(gcode).lines

	prev_X = 0.0
	prev_Y = 0.0
	prev_Z = 0.0
	prev_F = 0.0

	global relative
	relative = False

	global line_name
	line_name = 1

	for line in gcode_lines:
		prev_X, prev_Y, prev_Z, prev_F = process_line(root, line, prev_X, prev_Y, prev_Z, prev_F)

	ET.indent(root)
	tree.write(output_file, encoding="utf-8")

main()