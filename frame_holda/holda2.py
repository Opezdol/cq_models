from cadquery import Workplane, Location, Vector, Sketch, Plane
import sys
sys.path.append("..")
from helpers import Part

class Holda(Part):
    params = {
            "name": "Angle holda",
            "prof_width":20,
            "prof_height": 30, 
            "prof_thick": 4,
            "prof_fillet": 1, 
            "len": 70,
            "fillet": 1.2,
            "main_plane": 'YZ', 

            }
    def __init__(self):
        super().__init__(params = Holda.params)

    def make(self):
        sketch = (
                Sketch()
                .rect(self.prof_height+self.prof_thick*2,
                    self.prof_width+self.prof_thick*2)
                .wires()
                .offset(-self.prof_thick, mode='s')
                .reset()
        )
        def make_arm(f):
            center = f.Center().toTuple()
            normal = f.normalAt().toTuple()
            plane = Plane(origin = center, normal=normal)
            res = (
                    Workplane(plane)
                    .placeSketch(sketch)
                    .extrude(self.len)
            )
            return res.val()

        # base Cube
        baseCube = (
                Workplane()
                .rect(self.prof_width+self.prof_thick*2,
                    self.prof_width+self.prof_thick*2)
                .extrude(self.prof_height+self.prof_thick*2)
        )
        #Double angle
        double = (
                baseCube
                .faces(">X or >Y").each(make_arm, combine='a')
                )
        # Triple Angle
        base_oval = (
                Sketch()
                .circle(10)
                )
        triple = (
                double 
                # locate origin point
                #create baseZ plane for construction
                .faces('<Z').edges('<X').vertices('<Y')
                .workplane(centerOption='CenterOfMass')
                # rotate 45 && offset
                .transformed( rotate=(0,0,45+90), offset=(4,4,0))
                .tag('baseZ')
                # __LOFT ANGLE Form
                .placeSketch(base_oval,
                    base_oval.moved(Location(
                        Vector(2,2, self.prof_height*2/3))),
                    sketch.moved(Location(
                        Vector(0,0,self.prof_height+self.prof_thick*2)))
                    )

                # false for simple manage
                .loft(combine=False)
                #make extrusion at Z axis
                .workplaneFromTagged('baseZ')
                .transformed(offset=(0,0,self.prof_height+self.prof_thick*2))
                # Sharped Dressed man YAA! =))
                .tag('ZZtop')
                .placeSketch(sketch).extrude(self.len)
                )
        # combine both
        triple+=double
        #reinforcements
        triple = self._make_reinforcements(triple)
        # cut off 
        triple = self._cutoff(triple)

        # fillet double
        res = double.edges().fillet(self.fillet)
        # make fix holes
        res = (
                res.faces('<Z').workplane()
                .pushPoints([
                    (0,0),(self.len,0),(0,-self.len),
                    (self.len/2,0),(0,-self.len/2), 
                    ])
                .circle(3).cutBlind(-self.prof_thick,taper=40)
                )

        return (triple.clean()
                #.faces(">Z[-2]")
                )

    def _make_reinforcements(self, res):
        # Y reinforce
        cntrOff = 1 # center offset multiplier
        res  = (
                res
                .faces('>Y').edges('>Z')
                .workplane(centerOption='CenterOfMass')
                .center(self.prof_thick*cntrOff,0)
                .rect(self.prof_thick, self.len, centered=(True,False))
                .extrude('next', combine='a')
        )
        # X reinforce
        res  = (
                res
                .faces('>X').edges('>Z')
                .workplane(centerOption='CenterOfMass')
                .center(-self.prof_thick*cntrOff,0)
                .rect(self.prof_thick,self.len, centered=(True,False))
                .extrude('next')
        )
        # Z reinforce
        res = (
                res
                .workplaneFromTagged('ZZtop')
                .transformed(
                    offset=(0,-(self.prof_height+self.prof_thick),0),
                    rotate=(0,0,180+45)
                    )
                .rect(self.len,self.len, centered=(False, False))
                .extrude(-self.prof_thick)
        )

        # rotate to cut off
        res =  res.clean().val().rotate(
                Vector(0,0,0),
                Vector(1,1,0),
                90)
        return res 

    def _cutoff(self, res):
        box = res.BoundingBox()
        max_dimention = max(box.xlen,box.ylen, box.zlen) + 30
        print(max_dimention)
        cut_body = (
                Workplane('YZ')
                .rect(max_dimention, max_dimention)
                .extrude(max_dimention)
                )
        cut_body = cut_body.translate((60,0,0))
        #debug(cut_body,name='cutZone')
        res = res.cut(cut_body.val())
        return res.clean()




holda = Holda()
show_object(holda.body, name = holda.name)
