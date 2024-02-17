import pyzed.sl as sl
import sys


init = sl.InitParameters(depth_mode=sl.DEPTH_MODE.ULTRA,
                                 coordinate_units=sl.UNIT.METER,
                                 coordinate_system=sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP)
parse_args(init)
zed = sl.Camera()
status = zed.open(init)
if status != sl.ERROR_CODE.SUCCESS:
    print(repr(status))
    exit()

res = sl.Resolution()
res.width = 720
res.height = 404

point_cloud = sl.Mat(res.width, res.height, sl.MAT_TYPE.F32_C4, sl.MEM.CPU)

while True:
    if zed.grab() == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA,sl.MEM.CPU, res)
            print(point_cloud.get_data())
            