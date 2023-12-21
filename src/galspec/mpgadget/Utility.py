import numpy,galspec

def get_fixed_format_snapshot_number(snap_num:int):
    return '{:03}'.format(snap_num)


def get_snapshot_number_from_time(time:float):
    snap_num,snap_time = numpy.loadtxt(galspec.CONFIG.MPGADGET_SNAPSHOT_TXT_DIR).T

    # Direct comparision will have issues due to floating point precisions
    # So take few decimal points for accuracy
    da = 4    #decimal accuracy
    time_ac = int(time*(10**da))
    snap_time_ac = numpy.int32(snap_time*(10**da))

    if not time_ac in snap_time_ac:
        raise ValueError("No snapshot is available for the time " + str(time)) 

    time_index = numpy.where(snap_time_ac == time_ac)
    return numpy.int32(snap_num[time_index])[0]


def get_time_from_snapshot_number(snap_num:int):
    return galspec.InitConfig().PART(snap_num).Header.time

