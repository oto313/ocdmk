// USB-C 2.0 Receptacle Connector - 12402012E212A (Amphenol)
// Ergogen footprint module

module.exports = {
  params: {
    designator: 'USB',
    side: 'F',
    reversible: false,
    // Net assignments
    GND: { type: 'net', value: 'GND' },
    VBUS: { type: 'net', value: 'VBUS' },
    CC1: { type: 'net', value: 'CC1' },
    CC2: { type: 'net', value: 'CC2' },
    DP1: { type: 'net', value: 'DP1' },
    DN1: { type: 'net', value: 'DN1' },
    DP2: { type: 'net', value: 'DP2' },
    DN2: { type: 'net', value: 'DN2' },
    SBU1: { type: 'net', value: 'SBU1' },
    SBU2: { type: 'net', value: 'SBU2' }
  },
  body: p => {
    const standard_opening = `
    (footprint "12402012E212A_AMP"
      (layer "${p.side}.Cu")
      (attr smd)
      ${p.at}
      (tags "USB-C 2.0 Receptacle")
      
      (fp_text reference "${p.ref}" (at 0 -5.5 ${p.rot}) (layer "${p.side}.SilkS") ${p.ref_hide}
        (effects (font (size 1 1) (thickness 0.15))))
      (fp_text value "USB-C" (at 0 5.5 ${p.rot}) (layer "${p.side}.Fab")
        (effects (font (size 1 1) (thickness 0.15))))
      
      `;

    const silkscreen = `
      (fp_line (start -4.5974 -1.761308) (end -4.5974 -0.106891) (stroke (width 0.1524) (type solid)) (layer "${p.side}.SilkS"))
      (fp_line (start -4.5974 2.266293) (end -4.5974 3.7973) (stroke (width 0.1524) (type solid)) (layer "${p.side}.SilkS"))
      (fp_line (start -4.5974 3.7973) (end 4.5974 3.7973) (stroke (width 0.1524) (type solid)) (layer "${p.side}.SilkS"))
      (fp_line (start 4.5974 -0.106891) (end 4.5974 -1.761308) (stroke (width 0.1524) (type solid)) (layer "${p.side}.SilkS"))
      (fp_line (start 4.5974 3.7973) (end 4.5974 2.266293) (stroke (width 0.1524) (type solid)) (layer "${p.side}.SilkS"))
      (fp_text user "*" (at -5.74 -3.6703 ${p.rot}) (layer "${p.side}.SilkS")
        (effects (font (size 1 1) (thickness 0.15))))
      `;

    const courtyard = `
      (fp_line (start -5.0693 -4.4084) (end -5.0693 -1.7922) (stroke (width 0.1524) (type solid)) (layer "${p.side}.CrtYd"))
      (fp_line (start -5.0693 -1.7922) (end -4.7244 -1.7922) (stroke (width 0.1524) (type solid)) (layer "${p.side}.CrtYd"))
      (fp_line (start -5.0693 -0.075999) (end -5.0693 2.235401) (stroke (width 0.1524) (type solid)) (layer "${p.side}.CrtYd"))
      (fp_line (start -5.0693 2.235401) (end -4.7244 2.235401) (stroke (width 0.1524) (type solid)) (layer "${p.side}.CrtYd"))
      (fp_line (start -4.7244 -1.7922) (end -4.7244 -0.075999) (stroke (width 0.1524) (type solid)) (layer "${p.side}.CrtYd"))
      (fp_line (start -4.7244 -0.075999) (end -5.0693 -0.075999) (stroke (width 0.1524) (type solid)) (layer "${p.side}.CrtYd"))
      (fp_line (start -4.7244 2.235401) (end -4.7244 3.9243) (stroke (width 0.1524) (type solid)) (layer "${p.side}.CrtYd"))
      (fp_line (start -4.7244 3.9243) (end 4.7244 3.9243) (stroke (width 0.1524) (type solid)) (layer "${p.side}.CrtYd"))
      (fp_line (start -3.758801 -4.4958) (end -3.758801 -4.4084) (stroke (width 0.1524) (type solid)) (layer "${p.side}.CrtYd"))
      (fp_line (start -3.758801 -4.4084) (end -5.0693 -4.4084) (stroke (width 0.1524) (type solid)) (layer "${p.side}.CrtYd"))
      (fp_line (start 3.758799 -4.4958) (end -3.758801 -4.4958) (stroke (width 0.1524) (type solid)) (layer "${p.side}.CrtYd"))
      (fp_line (start 3.758799 -4.4084) (end 3.758799 -4.4958) (stroke (width 0.1524) (type solid)) (layer "${p.side}.CrtYd"))
      (fp_line (start 4.7244 -1.7922) (end 5.0693 -1.7922) (stroke (width 0.1524) (type solid)) (layer "${p.side}.CrtYd"))
      (fp_line (start 4.7244 -0.075999) (end 4.7244 -1.7922) (stroke (width 0.1524) (type solid)) (layer "${p.side}.CrtYd"))
      (fp_line (start 4.7244 2.235401) (end 5.0693 2.235401) (stroke (width 0.1524) (type solid)) (layer "${p.side}.CrtYd"))
      (fp_line (start 4.7244 3.9243) (end 4.7244 2.235401) (stroke (width 0.1524) (type solid)) (layer "${p.side}.CrtYd"))
      (fp_line (start 5.0693 -4.4084) (end 3.758799 -4.4084) (stroke (width 0.1524) (type solid)) (layer "${p.side}.CrtYd"))
      (fp_line (start 5.0693 -1.7922) (end 5.0693 -4.4084) (stroke (width 0.1524) (type solid)) (layer "${p.side}.CrtYd"))
      (fp_line (start 5.0693 -0.075999) (end 4.7244 -0.075999) (stroke (width 0.1524) (type solid)) (layer "${p.side}.CrtYd"))
      (fp_line (start 5.0693 2.235401) (end 5.0693 -0.075999) (stroke (width 0.1524) (type solid)) (layer "${p.side}.CrtYd"))
      `;

    const fabrication = `
      (fp_line (start -4.4704 -3.6703) (end -4.4704 3.6703) (stroke (width 0.0254) (type solid)) (layer "${p.side}.Fab"))
      (fp_line (start -4.4704 3.6703) (end 4.4704 3.6703) (stroke (width 0.0254) (type solid)) (layer "${p.side}.Fab"))
      (fp_line (start 4.4704 -3.6703) (end -4.4704 -3.6703) (stroke (width 0.0254) (type solid)) (layer "${p.side}.Fab"))
      (fp_line (start 4.4704 3.6703) (end 4.4704 -3.6703) (stroke (width 0.0254) (type solid)) (layer "${p.side}.Fab"))
      `;

    const mounting_holes = `
      (pad "" np_thru_hole oval (at -4.32 -3.1003 ${p.rot}) (size 0.9906 2.1082) (drill oval 0.6096 1.7018) (layers "*.Cu" "*.Mask"))
      (pad "" np_thru_hole oval (at -4.32 1.079701 ${p.rot}) (size 0.9906 1.8034) (drill oval 0.6096 1.397) (layers "*.Cu" "*.Mask"))
      (pad "" np_thru_hole circle (at -2.889999 -2.6003 ${p.rot}) (size 0.6604 0.6604) (drill 0.6604) (layers "*.Cu" "*.Mask"))
      (pad "" np_thru_hole circle (at 2.889999 -2.6003 ${p.rot}) (size 0.6604 0.6604) (drill 0.6604) (layers "*.Cu" "*.Mask"))
      (pad "" np_thru_hole oval (at 4.32 -3.1003 ${p.rot}) (size 0.9906 2.1082) (drill oval 0.6096 1.7018) (layers "*.Cu" "*.Mask"))
      (pad "" np_thru_hole oval (at 4.32 1.079701 ${p.rot}) (size 0.9906 1.8034) (drill oval 0.6096 1.397) (layers "*.Cu" "*.Mask"))
      `;

    const pad_defs = [
      { name: "A1", x: -3.200001, net: p.GND },
      { name: "A4", x: -2.4, net: p.VBUS },
      { name: "A5", x: -1.25, net: p.CC1 },
      { name: "A6", x: -0.25, net: p.DP1 },
      { name: "A7", x: 0.25, net: p.DN1 },
      { name: "A8", x: 1.25, net: p.SBU1 },
      { name: "A4", x: 2.4, net: p.VBUS },
      { name: "B1", x: 3.199999, net: p.GND },
      { name: "B5", x: 1.749999, net: p.CC2 },
      { name: "B6", x: 0.750001, net: p.DP2 },
      { name: "B7", x: -0.750001, net: p.DN2 },
      { name: "B8", x: -1.749999, net: p.SBU2 }
    ];

    function genPads(side) {
      return pad_defs.map(pad =>
        `(pad "${pad.name}" smd rect (at ${pad.x} -3.6703 ${p.rot}) (size ${["A1","A4","B1"].includes(pad.name) ? "0.6096 1.143" : "0.3048 1.143"}) (layers "${side}.Cu" "${side}.Paste" "${side}.Mask") ${pad.net.str})`
      ).join("\n");
    }

    let pads = genPads(p.side);
    if (p.reversible) {
      pads += "\n" + genPads(p.side === "F" ? "B" : "F");
    }

    const closing = `
    )
    `;

    return standard_opening + silkscreen + courtyard + fabrication + mounting_holes + pads + closing;
  }
}