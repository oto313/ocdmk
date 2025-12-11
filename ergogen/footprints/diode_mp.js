// LED MP-2016-1100-50-90 footprint for Ergogen
// 2016 (2.0mm x 1.6mm) SMD LED package

module.exports = {
  params: {
    designator: 'LED',
    side: 'F',
    reversible: false,
    show_3d: false,
    from: undefined,
    to: undefined
  },
  body: p => {
    function genPads(side) {
      return `
        (pad 1 smd custom (at -0.86 0 ${p.rot}) (size 0.1 0.1) (layers ${side}.Cu ${side}.Paste ${side}.Mask)
          ${p.from.str}
          (clearance 0.1) (zone_connect 0)
          (options (clearance outline) (anchor rect))
          (primitives
            (gr_poly (pts
              (xy -0.125 0.175) (xy -0.375 0.175) (xy -0.375 -0.175) (xy -0.125 -0.175) 
              (xy -0.125 -0.7) (xy 0.375 -0.7) (xy 0.375 0.7) (xy -0.125 0.7))
              (width 0.01))))

        (pad 2 smd custom (at 0.6 0 ${p.rot}) (size 0.1 0.1) (layers ${side}.Cu ${side}.Paste ${side}.Mask)
          ${p.to.str}
          (clearance 0.1) (zone_connect 0)
          (options (clearance outline) (anchor rect))
          (primitives
            (gr_poly (pts
              (xy -0.635 -0.7) (xy -0.635 0.7) (xy 0.385 0.7) (xy 0.385 0.175) 
              (xy 0.635 0.175) (xy 0.635 -0.175) (xy 0.385 -0.175) (xy 0.385 -0.7))
              (width 0.01))))
      `;
    }

    let pads = genPads(p.side);
    if (p.reversible) {
      pads += genPads(p.side === "F" ? "B" : "F");
    }

    const standard = `
      (module LED_MP-2016-1100-50-90 (layer ${p.side}.Cu) (tedit 5B24D78E)
        ${p.at /* parametric position */}

        ${'' /* reference */}
        (fp_text reference "${p.ref}" (at 0 -1.5548 ${p.rot}) (layer ${p.side}.SilkS) ${p.ref_hide}
          (effects (font (size 0.48 0.48) (thickness 0.15)))
        )
        (fp_text value "LED_MP-2016-1100-50-90" (at 5.2206 1.5548 ${p.rot}) (layer ${p.side}.Fab)
          (effects (font (size 0.48 0.48) (thickness 0.15)))
        )

        ${'' /* solder paste polygons */}
        (fp_poly (pts
          (xy -0.985 -0.5) (xy -0.485 -0.5) (xy -0.485 0.5) (xy -0.985 0.5))
          (layer ${p.side}.Paste) (width 0.01))
        (fp_poly (pts
          (xy -0.035 -0.5) (xy 0.965 -0.5) (xy 0.965 0.5) (xy -0.035 0.5))
          (layer ${p.side}.Paste) (width 0.01))

        ${'' /* silkscreen */}
        (fp_line (start -1 -1.02) (end 1 -1.02) (layer ${p.side}.SilkS) (width 0.127))
        (fp_line (start 1 1.02) (end -1 1.02) (layer ${p.side}.SilkS) (width 0.127))
        (fp_circle (center 1.935 0) (end 2.035 0) (layer ${p.side}.SilkS) (width 0.2))

        ${'' /* solder mask openings */}
        (fp_poly (pts
          (xy -1.085 0.275) (xy -1.335 0.275) (xy -1.335 -0.275) (xy -1.085 -0.275) 
          (xy -1.085 -0.8) (xy -0.385 -0.8) (xy -0.385 0.8) (xy -1.085 0.8))
          (layer ${p.side}.Mask) (width 0.01))
        (fp_poly (pts
          (xy -0.135 -0.8) (xy -0.135 0.8) (xy 1.085 0.8) (xy 1.085 0.275) 
          (xy 1.335 0.275) (xy 1.335 -0.275) (xy 1.085 -0.275) (xy 1.085 -0.8))
          (layer ${p.side}.Mask) (width 0.01))

        ${'' /* courtyard */}
        (fp_line (start -1.485 -1.05) (end -1.485 1.05) (layer ${p.side}.CrtYd) (width 0.05))
        (fp_line (start -1.485 1.05) (end 1.485 1.05) (layer ${p.side}.CrtYd) (width 0.05))
        (fp_line (start 1.485 -1.05) (end -1.485 -1.05) (layer ${p.side}.CrtYd) (width 0.05))
        (fp_line (start 1.485 1.05) (end 1.485 -1.05) (layer ${p.side}.CrtYd) (width 0.05))

        ${'' /* fabrication layer */}
        (fp_line (start -1 -0.8) (end 1 -0.8) (layer ${p.side}.Fab) (width 0.127))
        (fp_line (start -1 0.8) (end -1 -0.8) (layer ${p.side}.Fab) (width 0.127))
        (fp_line (start 1 -0.8) (end 1 0.8) (layer ${p.side}.Fab) (width 0.127))
        (fp_line (start 1 0.8) (end -1 0.8) (layer ${p.side}.Fab) (width 0.127))
        (fp_circle (center 1.935 0) (end 2.035 0) (layer ${p.side}.Fab) (width 0.2))

        ${pads}

        ${'' /* 3D model (optional) */}
        ${p.show_3d ? `
        (model \${KIPRJMOD}/PATH_TO_3D_MODEL.step
          (offset (xyz 0 0 0))
          (scale (xyz 1 1 1))
          (rotate (xyz 0 0 0))
        )` : ''}
      )
    `

    return standard;
  }
}