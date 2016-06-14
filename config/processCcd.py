from lsst.obs.ukirt.isr import IsrTask
config.isr.retarget(IsrTask)

if False:
    config.charImage.detectAndMeasure.detection.doTempLocalBackground = True
    config.charImage.detectAndMeasure.detection.tempLocalBackground.binSize = 64
    config.calibrate.detectAndMeasure.detection.doTempLocalBackground = True
    config.calibrate.detectAndMeasure.detection.tempLocalBackground.binSize = 64

if False:
    from lsst.meas.astrom import ANetAstrometryTask  # We need to blind-solve because we don't trust the Wcs
    config.calibrate.astrometry.retarget(ANetAstrometryTask)
    config.calibrate.astrometry.solver.useWcsRaDecCenter = False
    config.calibrate.astrometry.solver.useWcsParity = False
    config.calibrate.astrometry.solver.useWcsPixelScale = False
    refObjLoader = config.calibrate.astrometry.solver
else:
    refObjLoader = config.calibrate.astrometry.refObjLoader
    config.calibrate.doAstrometry = False
    config.calibrate.doPhotoCal = False

# Cosmic rays
config.charImage.repair.cosmicray.nCrPixelMax = 1000000

# Our 2MASS catalog only contains J-band mags
for ff in "ZYJHK":
    refObjLoader.filterMap[ff] = "J"
