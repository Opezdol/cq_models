import cadquery as cq

#dim-s
WIDTH =30
HEIGHT = 20
WALL = 3.6 # wall thick
FILLET = 2
ARMLEN = 30 # arm holda len dimention

RECT = 10.5
INSET = 8 # len of headcap incision
INSET_R = 6.5/2 # diam/2
def placeOnFace(face):
    # get positiojn data from face
    pos = cq.Vector(face.Center())
    norm = cq.Vector(face.normalAt())
    # create plane for workplane
    plane = cq.Plane(origin=pos, normal = norm)
    #__________SKETCH_____________
    sketch = (
            cq.Sketch()
            .rect(WIDTH+WALL, HEIGHT+WALL)
            .rect(WIDTH,HEIGHT, mode='s')
            .vertices()
            .fillet(FILLET)
            )
    #__________SKETCH END_________

    res = (
            cq.Workplane(plane)
            .placeSketch(sketch)
            .extrude(ARMLEN)
            )
    #return Solid
    return res.val()

def placeCutout(face):
    pos = cq.Vector(face.Center())
    norm = cq.Vector(face.normalAt())
    plane = cq.Plane(origin= pos, normal=norm)
    res = (
            cq.Workplane()
            .rect(RECT,RECT)
            .extrude(-3.5)
            .circle(INSET_R)
            .extrude(-(HEIGHT-INSET))
            )

    debug(res,name='cutout')
    #print([s for s in dir(res) if not s.startswith('_')])
    return res.rotateAboutCenter(
            axisEndPoint=cq.Vector(0,0,1).cross(norm),
            angleDegrees=90
            ).val().locate(cq.Location(pos))

def apply_each_face(f):
    res =  cq.Workplane(
            cq.Plane(

                f.Center(),
                    f.normalAt().add(
                        cq.Vector(
                            f.normalAt().x +1,
                            f.normalAt().y +1,
                            f.normalAt().z +1)
                        ).cross(f.normalAt()),
                    f.normalAt()), origin=f.Center())
    return res

holda = (
        cq.Workplane()
        .box(HEIGHT+WALL,HEIGHT+WALL,WIDTH+WALL)
        .faces('>Y or >X')
        .tag('fix')
        .each(placeOnFace)
        #test placeCutout
        .faces("<Y or <X").each(placeCutout,combine='s', useLocalCoordinates=False)
        .edges('>(-1,-1,0) or >(1,1,0)').fillet(FILLET)
        )
show_object(holda)
