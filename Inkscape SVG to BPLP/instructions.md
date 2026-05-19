
Converting SVGs (usually downloaded sketches from Onshape) to BPLP:

1. Download and install [Inkscape](https://inkscape.org/), any version newer than 1.0.
2. Navigate to `C:\Users\<username>\AppData\Roaming\inkscape\extensions` and paste in `flatten.py` and `flatten-pt5.inx`.
3. Open Command Prompt and paste the following: `"C:\Program Files\Inkscape\bin\inkscape.com" "<input file path>.svg" --actions="select-by-element:path; org.ekips.filter.flatten-pt5.noprefs;" --export-type="svg" --export-filename="<output file path>.svg" -g`. *Note for experienced people: this will not work without the `-g` flag, it seems to be some weird Inkscape bug. No GUI, no worky.*
4. Close the open Inkscape window; it does not need to be saved.
5. In the `3D-print-processing-scripts` folder, run `inkscape_svg_to_bplp.py` with the output from step 4 as the input.
6. Open the resulting BPLP file in VisualMachines or a text editor and re-order the lines as necessary.
7. For future conversions, only steps 3-6 must be run.
