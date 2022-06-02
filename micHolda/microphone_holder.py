from cadquery import Sketch, Workplane, Vector, Sketch

# globals 
SIDE_WALL = 5 # mm
SIDE_DIAM = 74 
SIDE_THICK = 8 #mm
SIDE_FIX_L = 10.5
SIDE_FIX_DEPTH = 3
SIDE_INSET_DIAM = 10
SIDE_INSET_DEPTH = 1.5
AXIS_HEIGHT = 25
MIC_BIG_DIAM = 54
MIC_LOW_DIAM = 51
MIC_LOW_HEIGTH = 29
FIX_DIAM_INNER = 26
FIX_HEIGHT = 12
FIX_DIAM_OUTER = 40 


# TEST ZONE
# objects creatio
res = (
    cq.Workplane()
    .circle(FIX_DIAM_OUTER/2)
    .circle(FIX_DIAM_INNER/2)
    .extrude(FIX_HEIGHT, both=True)
    .edges().fillet(1)
)
def make_outer_ring():
    # outer fixage
    outer = (
        Workplane()
        .circle( SIDE_DIAM/2)
        .circle( (SIDE_DIAM - SIDE_THICK)/2)
        .extrude(FIX_HEIGHT, both=True)
    )

    fix_pad = (
        Workplane('XZ')
        .circle(SIDE_FIX_L)
        .extrude(SIDE_THICK)
        .edges().fillet(2)
        .faces("<Y").workplane()
        .rect(SIDE_FIX_L, SIDE_FIX_L)
        .cutBlind(-SIDE_FIX_DEPTH)
        #.faces(">Y").workplane()
        #.circle(SIDE_INSET_DIAM/2).cutBlind(-SIDE_INSET_DEPTH)
        .translate(Vector((0,SIDE_DIAM/2,0)))
    )
    fix_pad = fix_pad.union(fix_pad.mirror('XZ'))

    outer = outer.union(fix_pad)
    outer = ( outer.faces(">Y").workplane().circle(6.5/2).cutThruAll())
    return outer

def make_outer_fixes():
    sketch = (
            Sketch().rect(7,AXIS_HEIGHT*2,5)
            )

    res = (
            Workplane()
    )
    #return res
    return sketch

# show zone for objects
show_object(make_outer_fixes(), name='outer_fixes')
show_object(make_outer_ring(), name='Outer Ring')
#show_object(fix_pad, name='lateralFix')
