class Part():
     """
     class Part describes interaction between two parts

     all parameters of the part available as attributes
     """

     def __init__(self, params = {}):
         if isinstance(params, dict):
             if not ("name" in params.keys()):
                 self.name = 'DefaultPart_NameYourPart'
             self.__dict__.update(params)
             #for key,value in params.items():
                 # add key: value to self class 
                 # nocheck for key as str
                 # TODO convertion key from params to string 
                 #_____bad Cycle?
                 #self.__dict__.update(params)

         else:
             raise ValueError('Params of model should be passed as dict')

     def __str__(self):
         msg = []
         for key, value in self.__dict__.items():
             msg.append(f'{key}--\t->{value}')
         return str(msg)

     @property
     def body(self):
         return self.make()

     def make(self):

         """
         Method of creation of body of Part
         """
         msg = f'{self.name}.make() not implemented'
         raise NotImplementedError(msg)

     def get_dimentions(self, obj):
         """
         tuple of X,Y,Z len dimentions
         """
         box = obj.BoundingBox()

         return (box.xlen, box.ylen, box.zlen)

     def get_max_dimention(self, obj):
         """
         max bounding box dimention fior object
         """

         return max(*self.get_dimentions(obj))

     def cutout(self, anoutherPart,
             scale: float = 1.04,
             inPlace: bool = False
             ):
         """
         Cuts one Part from anouther 
         scaling intersected body.
         TODO
         reimplement: make intersected body by delta gap

         """
         #Intersection of two objects
         inter = self.body.intersect(anoutherPart.body)
         loc =  inter.val().Center()
         print('___' *5)
         print('Init loacation ', loc.toTuple())
         debug (inter)
         # SCALE applying to inrsection
         reloc =  inter.val().scale(scale)
         print('After scale loc ', reloc.Center().toTuple())
         trVec =  loc - reloc.Center()
         cutBody = reloc.translate(trVec)
         ## inPlace logic
         if inPlace:
             self.body -= cutBody
         return self.body - cutBody
