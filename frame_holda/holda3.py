from cadquery import Workplane, Location, Vector, Sketch, Plane
import sys
sys.path.append("..")
from helpers import Part

class Holda_1D(Part):
    params = {
            "name": "Angle holda",
            "prof_width":20,
            "prof_height": 30, 
            "prof_thick": 4,
            "prof_fillet": 1, 
            "prof_radius": 5,
            "len": 70,
            "fillet": 1.2,
            "main_plane": 'YZ', 
            "main_angle": 120,  # defines Z axis direction

            }
    def __init__(self):
        super().__init__(params = Holda.params)

    def get_profile(self, profile:str = '')-> Sketch:
        """
        Returns Sketch of the profile
        """
        match profile:
            case 'square':
                return (
                        Sketch()
                        .rect(self.prof_height+self.prof_thick*2,
                            self.prof_width+self.prof_thick*2)
                        .wires()
                        .offset(-self.prof_thick, mode='s')
                        .reset()
                        )
            case 'round':
                return (
                        Sketch()
                        .circle(self.prof_radius)
                        )


    def make(self):
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
        """
        Lock 3D axis interpositions
        """

        # Y reinforce
        cntrOff = 1 # center offset multiplier
        sketch = (
                Sketch()
                .rect(self.prof_thick, self.len)
                )
        res  = (
                res
                # max Y workplane on top edge
                .faces('>Y').edges('>Z')
                .workplane(centerOption='CenterOfMass').tag('ymax')
                # move center
                .center(self.prof_thick*cntrOff,self.len/2)
                .placeSketch(sketch)
                .extrude('next', combine='a')
                # horizontal reinforce
                .workplaneFromTagged('ymax')
                .transformed(rotate=(0,0,90), offset=(-self.len/2,
                    -self.prof_thick/2,0))
                .placeSketch(sketch)
                #.rect(self.prof_thick, self.len, centered=(True,False))
                .extrude('next', combine='a')
        )
        #debug (res, name='Yreinforce')
        # X reinforce
        res  = (
                res
                .faces('>X').edges('>Z')
                .workplane(centerOption='CenterOfMass')
                .center(-self.prof_thick*cntrOff,0)
                .rect(self.prof_thick,self.len, centered=(True,False))
                .extrude('next')
        )

        return res 


    def _cutoff(self, obj, cutDist = 60 ):
        # rotate object defore plane cutoff 
        # we can rotate plane to it with, but i Rotated object
        obj = obj.val().rotate(
            Vector(0,0,0),
            Vector(1,1,0),
            self.main_angle)

        #Max dimentions for volume cutoff
        max_dimention = self.get_max_dimention(obj)*2

        #print(max_dimention)
        cut_body = (
                Workplane('YZ')
                .rect(max_dimention, max_dimention)
                .extrude(max_dimention)
                )
        cut_body = cut_body.translate((cutDist,0,0))
        #debug(cut_body,name='cutZone')
        res = obj.cut(cut_body.val())
        return res.clean()




holda = Holda()
show_object(holda.body, name = holda.name)
