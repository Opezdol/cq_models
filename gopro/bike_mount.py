from cadquery import Workplane, Vector, Face, Plane, Sketch, Location, Shape
from cadquery.selectors import NearestToPointSelector

class Part():
    """
    class Part describes interaction between two parts
    all parameters of the part available as attributes

    """
    def __init__(self, params = {}):

        if isinstance(params, dict):

            if not ("name" in params.keys()):
                self.name = 'DefaultPart_NameYourPart'

            for key,value in params.items():
                # add key: value to self class 
                # nocheck for key as str
                # TODO convertion key from params to string 
                self.__dict__.update(params)
        else:
            raise ValueError('Params of model should be passed as dict')
        self.body = self.make()



    def test(self):
        for key, value in self.__dict__.items():
            print(f'{key}--\t->{value}')

    def make(self):
        """
        Method of creation of Part body
        """
        msg = f'{self.name}.make() not implemented'
        raise NotImplementedError(msg)

    def cutout(self, anoutherPart):
        inter = self.body.intersect(anoutherPart.body)
        loc =  inter.val().Center()
        print('___' *5)
        print('Init loacation ', loc.toTuple())
        debug (inter)
        reloc =  inter.val().scale(1.04)
        print('After scale loc ', reloc.Center().toTuple())
        trVec =  loc - reloc.Center()
        cutBody = reloc.translate(trVec)
        self.body -= cutBody


class PlateAdhesive(Part):
    """ std plate for goPro mount """
    params = {
        "name": "PlateAdhesive",
        "base_width":38,        #*
        "base_length": 47,      #*
        "base_thick": 6,        #*
        "c_height": 2,          # mid guide
        "c_width": 4,           # mid guide
        "c_length": 34,         # mid guide
        "wing_l": 26,           # wing definition
        "wing_h": 7.5,          # wind definition
        "cut_width": 28.5,      # CutFrom in the center
        "cut_height": 4.5,      # |
        "cut_wing": 22.5,       # |
        "fillet": 2,
        "main_plain":'YZ',
        }

    def __init__(self):
        super().__init__(params = PlateAdhesive.params)

    def make(self):
        # Basis form definition
        res = (
                Workplane()
                .rect(self.base_width, self.base_length)
                .extrude(-self.base_thick)
                .faces('>Z').workplane().tag('base')
                .rect(self.base_width, self.wing_l).extrude(self.wing_h)
        )

        z_max = res.val().BoundingBox().zmax
        # mid cut 
        cutForm = (
                Workplane('XZ')
                .rect(self.cut_width, self.cut_height, centered=(True,False))
                .rect(self.cut_wing, (z_max+1),centered=(True,False))
                .extrude(self.base_length, both=True)
        )
        # make cut out with given form
        res = res.cut(cutForm)

        # fillets && champhers
        res = res.faces('<X or >X').edges('not <Z').fillet(self.fillet)
        res = res.edges('|Z').edges('>Z').chamfer(self.fillet)
        res = res.faces(">Y").edges(">Z").fillet(self.fillet-0.5)

        #correct position
        res = res.translate((0,0,self.base_thick))

        return res

class FixMount(Part):
    params = {
            "name": "FixMount",
            "d": 32,
            "delta_d": 10,
            "thick": 15,
            "up": 16,
            "intercut": 1,
            "fix_h":14,
            "fix_w":11,
            "leg_width":20,
            "pos_lateral": 25,
            "main_plane": "YZ",
            "fillet":1,
            "fillet_up":5,
    }
    def __init__(self):
        super().__init__(FixMount.params)
    def make(self):
        sketch = (
                Sketch()
                .circle((self.d + self.delta_d)/2)
                .rect((self.d+self.delta_d+self.fix_w*2),self.fix_h,mode='a')
                .push( [(0,self.d/2)])
                .rect( self.leg_width, self.up*2, mode='a')
                .clean()
                .reset()
                .circle(self.d/2, mode='s')
                .rect(self.d*2, self.intercut, mode='s')
                .reset()
                .clean()
        )
        #debug(sketch)
        def cut_hole(f):
#TODO Add params to main params dict!!!!
            center = f.Center()
            normal = f.normalAt()
            plane = Plane(origin=center, normal=normal)
            res = (
                    Workplane(plane).tag('base')
                    .circle(6.5/2).extrude(-15)
                    .workplaneFromTagged('base').rect(10.5,10.5).extrude(-2)
                    .workplaneFromTagged('base').rect(10.5,10.5).extrude(5)
            )
            return res.val()

        res = (
                Workplane(self.main_plane)
                .placeSketch(sketch)
                .extrude(self.thick)
                # FILLET lateral
                .faces('>X or <X').edges('not >Z').fillet(self.fillet)
                # Fillet upper laateral edge
                .faces('#Z').faces('>Z').edges("<Z").fillet(self.fillet_up)
                # fillet lower lateral edge
                .faces("+Z").faces('not >Z').faces('>Z').tag('fix')
                .edges('#Y').edges('not(>Y or <Y)')
                .fillet(8)
                # cut holes for bolts and inserts
                .faces(tag='fix')
                .each(cut_hole, combine='s')
                .clean()
                # Pin for part connection
                .faces(">Z").workplane(centerOption='CenterOfMass')
                .rect(self.thick,5).extrude(3.5)
            )
        res = res.translate((self.pos_lateral,0,-(self.d/2+self.up)))
        # Mirror fix holda
        #res =  res.union(res.mirror(self.main_plane))

        return res 

class PlateToFix(PlateAdhesive):
    params = {
            "name": "Plate To fix",
            "length": 21,
        }
    def __init__(self):
        super().__init__()
        self.__dict__.update(PlateToFix.params)
        self.update()
    def update(self):
        face = self.body.faces(">X")
        sketch = (
                Sketch()
                .push([(0,(self.base_thick-self.fillet)/2)])
                .rect(self.base_length-self.fillet*2,
                    (self.base_thick-self.fillet))
                .push([(0,self.wing_h/2)])
                .rect(self.wing_l - self.fillet*2, self.wing_h)
                .push([(0,self.wing_h)])
                .rect(5, self.wing_h)
                .clean()
                .reset()
                .vertices().fillet(self.fillet/2)
                )
        sk  = (
                Sketch()
                .rect(20,self.wing_h)
                .reset()
                .vertices().fillet(self.fillet)
                )
        self.body = (
                face.workplane()
                .placeSketch(sketch,
                    sk.moved(Location(
                        Vector(0,3, self.length/2))),
                    sk.moved(Location(
                        Vector(0,2, self.length)))
                    )

                .loft()
                )
        #self.body += self.body.mirror('YZ')


plate = PlateAdhesive()
fix = FixMount()
plate_to_fix = PlateToFix()
#### OBejcts operations
plate_to_fix.cutout(fix)
plate_to_fix.body += plate_to_fix.body.mirror('YZ')
#fix.body += fix.body.mirror('YZ')
#show_object(plate.body, name=plate.name)
show_object(fix.body, name=fix.name)
show_object(plate_to_fix.body, name=plate_to_fix.name)
