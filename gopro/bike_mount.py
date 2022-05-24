from cadquery import Workplane, Vector, Face, Plane, Sketch, Location

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
            "fix_h":12,
            "fix_w":11,
            "leg_width":20,
            "pos_lateral": 25,
            "main_plane": "YZ",
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
        )
        res = (
                Workplane(self.main_plane)
                .placeSketch(sketch)
                .extrude(self.thick)
        )
        #res = res.translate((self.pos_lateral,0,-(self.d/2+self.up)))
        # Mirror fix holda
        #res =  res.union(res.mirror(self.main_plane))

        return res


plate = PlateAdhesive()
fix = FixMount()
show_object(plate.body)
show_object(fix.body)

