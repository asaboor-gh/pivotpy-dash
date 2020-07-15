import json
import pivotpy as pp
vr=pp.export_vasprun(path="E:/Research/graphene_example/ISPIN_1/bands/vasprun.xml")
dp=json.dumps(vr.bands.evals.tolist())
import numpy as np
x=np.array(json.loads(dp))
x==vr.bands.evals


import json
from json import JSONEncoder
class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        import numpy as np
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyArrayEncoder, self).default(obj)
def evr_to_json(evr):
    import json
    return json.dumps(evr.tdos,cls=NumpyArrayEncoder)
    

def evr_from_json(jsonified_evr):
    pass



from json import JSONDecoder

# Serialization
numpyData = vr
encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)  # use dump() to write array into file
print("Printing JSON serialized NumPy array")
print(encodedNumpyData)

print("Decode JSON serialized NumPy array")
decodedArrays = json.loads(encodedNumpyData,cls=ListToNumpyEncoder)

finalNumpyArray = numpy.asarray(decodedArrays)
print("NumPy Array")
print(finalNumpyArray)

def get_all_values(ndict):
    import numpy as np
    import pivotpy as pp
    for key, value in ndict.items():
        if type(value) is dict or type(value) is pp.Dic2Dot:
            value = dict(**value)
            for k1,v1 in value.items():
                if type(v1) is dict or type(v1) is pp.Dic2Dot:
                    v1 = dict(**v1)
                    for k2,v2 in v1.items():
                        if type(v2) == np.ndarray:
                            ndict[key][k1][k2] = v2.tolist()
                elif type(v1) == np.ndarray:
                    ndict[key][k1] = v1.tolist()
        elif type(value) == np.ndarray:
            ndict[key] = value.tolist()
    return dict(ndict)

