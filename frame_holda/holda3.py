from cadquery import Workplane, Location, Vector, Sketch, Plane
import sys
sys.path.append("..")
from helpers import Part

class Holda_1D(Part):
    params = {
            "name": "1D holda cap",
            "prof_width":20,
            "prof_height": 30,
            "prof_thick": 3.2,
            "prof_fillet": 1,
            "prof_radius": 12,
            "len": 70,
            "fillet": 1.2,
            "main_plane": 'YZ', 
            "radius":20,
            "delta": 25,

            }
    def __init__(self):
        super().__init__(params = Holda_1D.params)

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
                        .circle(self.radius)
                        )


    def make(self):
        """
        Here we make body of any part
        """

        plane = Workplane('YZ').tag('base') # X - oriented
        #circle sketch
        circle = (
                Sketch()
                .circle(self.prof_radius)
                )
        #profile  = self.get_profile('round')
        profile = self.get_profile('square')
        # loft profile
        obj = (
                # sphere base
                plane.sphere(self.prof_radius)
                #circle to loft
                .workplaneFromTagged('base')
                .placeSketch(circle,
                    profile.moved(Location(Vector((0,0,self.delta*0.33)))),
                    profile.moved(Location(Vector((0,0,self.delta*0.69)))),
                    profile.moved(Location(Vector((0,0,self.delta)))),
                    )
                .loft()
                )
        obj = (
                obj
                .faces('>X').workplane().tag('outer')
                .placeSketch(profile)
                .extrude(self.len)
                )
        return obj.clean()

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

class Holda_2D(Holda_1D):
    def __init__(self, angle: float = 120.0) -> None:
        super().__init__()
        self.x = super().make()
        self.angle = angle
        self.name = 'Holda 2D angled'
        self.fillet =3.7
    def make(self):
        res = self.x.rotate(
                axisStartPoint=(0,0,0),
                axisEndPoint=(0,0,1),
                angleDegrees= self.angle,
                )
        res  = res.union(self.x)
        return res##self.make_reinforcement(res)


    def make_reinforcement(self, obj):
        baseplane = obj.workplaneFromTagged('outer')
        # transform plane
        base = baseplane.transformed(
                rotate=(0,self.angle/2,0))
        base = base.transformed(
                offset=(0,0,50)).tag('inter')
        base = (
                base.rect(40,5)
                .extrude(40,'a')
                # fillet
                #.faces(">Z[2]")
                #.edges("<Y or <X").fillet(self.fillet)
                #.faces(">Z[3]").edges('<Y or <X')
                #.fillet(self.fillet)
                )

        show_object(base)

        return obj



holda = Holda_2D(90)
print(holda)
show_object(holda.body, name = holda.name)
