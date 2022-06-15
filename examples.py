import cadquery as cq

def discord_test_cross():
    res = (
            cq.Workplane()
            .sketch().circle(5)
            .rect(1.5,4.2, mode='s')
            .rect(4.2,1.5, mode='s')
            .finalize().extrude(5)
            )
    return res
def discord_rarray():
    res = (
            cq.Workplane()
            .sketch()
            .rarray(2,10,5,5).circle(2)
            .clean().finalize()
            .extrude(2)
        )
    return res

def discord_clip_test():
    clipW = 8
    clipT = 1.5
    clipR = 2
    clipBumpW = 2
    clipBumpH = 2
    clipBumpR = 0.5
    clipSkew =0 
    catchBump = 1
    clipSpan = 32.3
    clipH = 8
    clipCorr = clipT*clipSkew/clipSpan

    clip = (
            cq.Workplane('XZ')
            .move(-clipSpan/2)
            .line(catchBump, catchBump)
            .line(-catchBump, catchBump)
            .vLine(clipH-2*catchBump)
            .close()
            )
    clip = (cq.Workplane('XZ').move(-clipSpan/2)
    .line(catchBump, catchBump).line(-catchBump, catchBump)
    .vLine(clipH-2*catchBump).line(clipSpan, clipSkew)
    .vLine(-clipSkew-clipH+2*catchBump)
    .line(-catchBump, -catchBump).line(catchBump, -catchBump)
    .hLine(clipT).vLine(clipSkew+clipH+clipT+clipCorr)
    .line(-clipSpan-2*clipT, -clipSkew-clipCorr)
    .vLine(-clipT-clipH)
    .close().extrude(-clipW)
    )
    return clip

def distribute_example():
    res = (

            cq.Workplane()
            .sketch()
            .circle(10).wires()
            .distribute(5)
            .circle(1)
            .reset()
            .circle(7,mode='s')
            .wires()
            .distribute(3).rect(1,2,mode='a')
            .finalize()
            .extrude(2)
            )
    return res
def discord_test():
    box = (cq.Workplane("XY")
       .box(10,10,10)
       .faces(">Z")
       .shell(1)
        )
    box_with_sketch = (box.faces(">Z")
                    .sketch()
                    .circle(5)
                    .circle(2, mode='s')
                    #.rect(1,4,mode='a')
                    .finalize()
                    )
    extrude_value = box_with_sketch.extrude(-10)
    extrude_next = box_with_sketch.extrude(until="next")
    show_object(extrude_value)
    show_object(extrude_next.translate((13,0,0)))
def discord_sweep_example():

    arr2 = []

    def sinecurv(tmax,its):
        for i in range(0,its):
            cval = tmax*i/its
            arr2.append((sin(cval),cval))
        return arr2

    sinecurv(2*pi,40)

    f0 = (cq.Workplane("XY")
    .spline(arr2)
    )

    profile = cq.Wire.makeCircle(.4, center=f0.val().positionAt(0), normal=f0.val().tangentAt(0))
    f2 = cq.Solid.sweep(outerWire=profile,innerWires=[], path=f0.val())

    f1 = (cq.Workplane("XY")
    .circle(.4)
    .sweep(path=f0.val(),normal=f0.val().tangentAt(0))
    )

    show_object(f2,options={"alpha":0.1, "color": (65, 94, 55)})
    show_object(f1.translate((2,0,0)),options={"alpha":0.1, "color": (95, 44, 55)})
    show_object(f0.translate((3,0,0)),options={"alpha":0.1, "color": (65, 94, 155)})


def discord_sound_cone():
    import cadquery as cq
    import random
    from itertools import accumulate

    thickness = 10
    radius = 150
    numcircles = radius // thickness
    max_height = 50
    tower_count = 20
    cone_angle = 15
    main = cq.Assembly()
    for ring in range(numcircles):
        randomlist = random.sample(range(10, 30), tower_count)
        scale = 360 / sum(randomlist)
        arc_widths = [r * scale for r in randomlist]
        arc_positions = list(accumulate(arc_widths))
        for i in range(tower_count):
            tower_height = random.randrange(0, max_height)
            tower_wire = (
                cq.Workplane("XZ")
                .pushPoints([(ring * thickness, 0)])
                .rect(thickness, tower_height, centered=False)
                .rotate((0, 0, 0), (0, 1, 0), cone_angle)
                .val()
            )
            tower = (
                cq.Workplane("XY")
                .add(tower_wire)
                .toPending()
                .revolve(arc_widths[i], (0, 0, 0), (0, 0, -1))
                .rotate((0, 0, 0), (0, 0, 1), arc_positions[i])
            )
            main.add(tower)

    show_object(main, name="main")



