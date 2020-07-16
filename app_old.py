import json
import pivotpy as pp
vr=pp.export_vasprun(path="E:/Research/graphene_example/ISPIN_1/bands/vasprun.xml")
dp=json.dumps(vr.bands.evals.tolist())
import numpy as np
x=np.array(json.loads(dp))
x==vr.bands.evals

