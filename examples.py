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
show_object(distribute_example())
