from cadquery import Workplane, Vector


def make_lofting_wire(
        scale: float,
        center: cq.Vector,
        base: float = 23,
        crad: float = 6
        ):
    return cq.Wire.makeRect(
            scale * (base - 2 * crad),
            scale * (base - 2 * crad),
            center,
            normal=cq.Vector(0, 0, 1),
            ).offset2D(scale * crad)[0]


hook_profile = cq.Edge.makeSpline(
        [
            cq.Vector(base, 0, 0),
            cq.Vector(0.4 * base, 0, 9),
            cq.Vector(0.5 * base, 0, 17),
         ],
        tangents=(cq.Vector(-1, 0, 1), cq.Vector(0.5, 0, 1)), )

hook_lofting_wires = [
        make_lofting_wire(
            hook_profile.positionAt(t / 10).x / base,
            cq.Vector(
                -base / 2 + hook_profile.positionAt(t / 10).x / 2,
                0,
                hook_profile.positionAt(t / 10).z,
                ),
            ) for t in range(11) ]
hook = (
    cq.Workplane(cq.Solid.makeLoft(hook_lofting_wires))
    .edges(">Z")
    .fillet(1)
    .edges("<Z")
    .chamfer(0.5)
)

if "show_object" in locals():
    show_object(hook_lofting_wires, name="hook_lofting_wires")
    show_object(hook, name="hook")
