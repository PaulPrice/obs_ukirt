import lsst.afw.cameraGeom.cameraConfig
assert type(config)==lsst.afw.cameraGeom.cameraConfig.CameraConfig, 'config is of type %s.%s instead of lsst.afw.cameraGeom.cameraConfig.CameraConfig' % (type(config).__module__, type(config).__name__)
config.name = 'CasuWfcam'

pixelScale = 0.2 # arcsec/pix
pixelSize = 0.01 # mm/pix; not sure, this is a guess

config.plateScale = pixelScale/pixelSize
config.radialCoeffs = None
config.transformDict.nativeSys = 'FocalPlane'
config.transformDict.transforms = {}
# config.transformDict.transforms['Focal_Plane_Pixels'] = lsst.afw.geom.transformConfig.TransformConfig()
# config.transformDict.transforms['Focal_Plane_Pixels'].transform['multi'].transformDict = None
# config.transformDict.transforms['Focal_Plane_Pixels'].transform['affine'].translation = [0.0, 0.0]
# config.transformDict.transforms['Focal_Plane_Pixels'].transform['affine'].linear = [1.0, 0.0, 0.0, 1.0]
# config.transformDict.transforms['Focal_Plane_Pixels'].transform['radial'].coeffs = None
# config.transformDict.transforms['Focal_Plane_Pixels'].transform.name = 'affine'
config.transformDict.transforms['Pupil'] = lsst.afw.geom.transformConfig.TransformConfig()
config.transformDict.transforms['Pupil'].transform['multi'].transformDict = None
config.transformDict.transforms['Pupil'].transform['affine'].translation = [0.0, 0.0]
config.transformDict.transforms['Pupil'].transform['affine'].linear = [1.0, 0.0, 0.0, 1.0]
config.transformDict.transforms['Pupil'].transform['radial'].coeffs = [0.0, pixelScale/3600]
config.transformDict.transforms['Pupil'].transform.name = 'radial'
config.detectorList = {}

# These are likely subject to observing strategy, as we're working with reconstructed images from CASU,
# and they probably change their reduction recipe according to the observing strategy. Hopefully this
# isn't too important, and we can manage.
pixelScale = 0.4  # arcsec/pix; raw data
rawSize = 2048  # raw data, pixels
processedSize = 4151  # processed data, pixels
centerToChip = 6.41  # arcmin
chipSize = 13.65  # arcmin
offset = (centerToChip + 0.5*chipSize)*60/0.4*processedSize/rawSize
offset = 0.0

config.detectorList[0] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
config.detectorList[0].bbox_x0 = 0
config.detectorList[0].bbox_y0 = 0
config.detectorList[0].bbox_x1 = processedSize
config.detectorList[0].bbox_y1 = processedSize
config.detectorList[0].name = '1'
config.detectorList[0].pixelSize_x = 1.0
config.detectorList[0].transformDict.nativeSys = None
config.detectorList[0].transformDict.transforms = None
config.detectorList[0].refpos_x = 0.5*processedSize
config.detectorList[0].refpos_y = 0.5*processedSize
config.detectorList[0].pixelSize_y = 1.0
config.detectorList[0].detectorType = 0
config.detectorList[0].offset_x = +offset
config.detectorList[0].offset_y = -offset
config.detectorList[0].transposeDetector = None
config.detectorList[0].yawDeg = 0.0
config.detectorList[0].rollDeg = 0.0
config.detectorList[0].serial = '1'
config.detectorList[0].pitchDeg = 0.0
config.detectorList[0].id = 1

config.detectorList[1] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
config.detectorList[1].bbox_x0 = 0
config.detectorList[1].bbox_y0 = 0
config.detectorList[1].bbox_x1 = processedSize
config.detectorList[1].bbox_y1 = processedSize
config.detectorList[1].name = '2'
config.detectorList[1].pixelSize_x = 1.0
config.detectorList[1].transformDict.nativeSys = None
config.detectorList[1].transformDict.transforms = None
config.detectorList[1].refpos_x = 0.5*processedSize
config.detectorList[1].refpos_y = 0.5*processedSize
config.detectorList[1].pixelSize_y = 1.0
config.detectorList[1].detectorType = 0
config.detectorList[1].offset_x = -offset
config.detectorList[1].offset_y = -offset
config.detectorList[1].transposeDetector = None
config.detectorList[1].yawDeg = 0.0
config.detectorList[1].rollDeg = 0.0
config.detectorList[1].serial = '2'
config.detectorList[1].pitchDeg = 0.0
config.detectorList[1].id = 2

config.detectorList[2] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
config.detectorList[2].bbox_x0 = 0
config.detectorList[2].bbox_y0 = 0
config.detectorList[2].bbox_x1 = processedSize
config.detectorList[2].bbox_y1 = processedSize
config.detectorList[2].name = '3'
config.detectorList[2].pixelSize_x = pixelSize
config.detectorList[2].transformDict.nativeSys = None
config.detectorList[2].transformDict.transforms = None
config.detectorList[2].refpos_x = 0.0 # 0.5*processedSize
config.detectorList[2].refpos_y = 0.0 # 0.5*processedSize
config.detectorList[2].pixelSize_y = pixelSize
config.detectorList[2].detectorType = 0
config.detectorList[2].offset_x = -offset
config.detectorList[2].offset_y = +offset
config.detectorList[2].transposeDetector = None
config.detectorList[2].yawDeg = 0.0
config.detectorList[2].rollDeg = 0.0
config.detectorList[2].serial = '3'
config.detectorList[2].pitchDeg = 0.0
config.detectorList[2].id = 3

config.detectorList[3] = lsst.afw.cameraGeom.cameraConfig.DetectorConfig()
config.detectorList[3].bbox_x0 = 0
config.detectorList[3].bbox_y0 = 0
config.detectorList[3].bbox_x1 = processedSize
config.detectorList[3].bbox_y1 = processedSize
config.detectorList[3].name = '4'
config.detectorList[3].pixelSize_x = 1.0
config.detectorList[3].transformDict.nativeSys = None
config.detectorList[3].transformDict.transforms = None
config.detectorList[3].refpos_x = 0.5*processedSize
config.detectorList[3].refpos_y = 0.5*processedSize
config.detectorList[3].pixelSize_y = 1.0
config.detectorList[3].detectorType = 0
config.detectorList[3].offset_x = +offset
config.detectorList[3].offset_y = +offset
config.detectorList[3].transposeDetector = None
config.detectorList[3].yawDeg = 0.0
config.detectorList[3].rollDeg = 0.0
config.detectorList[3].serial = '4'
config.detectorList[3].pitchDeg = 0.0
config.detectorList[3].id = 4

