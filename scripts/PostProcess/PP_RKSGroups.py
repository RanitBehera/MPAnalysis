import numpy
# PP prefic for Post Process functions

def PP_LengthByType(RSG):
    def ReturnCount(ptype:pt,ihid):
        ihid_mask = (ptype.InternalHaloID()==ihid)
        pos = ptype.Position()[ihid_mask]
        rvir_mask = (numpy.linalg.norm(pos-HPOS,axis=1)<RVIR)
        ids = ptype.ID()[ihid_mask][rvir_mask]
        return len(ids)
    


def PP_LengthByTypeInRvir()