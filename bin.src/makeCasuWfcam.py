#!/usr/bin/env python

import os

from lsst.utils import getPackageDir
from lsst.afw.table import AmpInfoCatalog, AmpInfoTable, LL
from lsst.afw.geom import Box2I

GAIN = (4.6, 4.5, 4.7, 5.2)
SATURATION = (40000, 40000, 40000, 27900)
READNOISE = 25.0

def makeCasuWfcam():
    path = os.path.join(getPackageDir("obs_ukirt"), "casuWfcam", "camera")

    for detNum, (gain, sat) in enumerate(zip(GAIN, SATURATION), 1):
        det = AmpInfoCatalog(AmpInfoTable.makeMinimalSchema())
        amp = det.addNew()
        amp.setName(str(detNum))
        amp.setBBox(Box2I())
        amp.setGain(gain)
        amp.setReadNoise(READNOISE)
        amp.setSaturation(sat)
#        amp.setSuspectLevel(float("nan"))
        amp.setReadoutCorner(LL)
        amp.setLinearityType("none")
        amp.setHasRawInfo(False)

        det.writeFits(os.path.join(path, "%d.fits" % (detNum,)))


if __name__ == "__main__":
    makeCasuWfcam()
