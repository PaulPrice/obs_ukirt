import numpy
import lsst.pipe.base
import lsst.ip.isr
from lsst.afw.table import ReferenceMatch, ReferenceMatchVector
from lsst.afw.table import SimpleCatalog, SimpleTable
from lsst.afw.table import SourceCatalog, SourceTable, Point2DKey
from lsst.afw.coord import IcrsCoord
from lsst.afw.geom import degrees
from lsst.afw.geom import Point2D
import lsst.afw.image as afwImage
import lsst.afw.geom as afwGeom
import lsst.afw.coord as afwCoord
from lsst.meas.astrom import FitTanSipWcsTask, setMatchDistance


class IsrTask(lsst.ip.isr.IsrTask):
    def __init__(self, *args, **kwargs):
        """Don't configure sub-tasks"""
        lsst.pipe.base.Task.__init__(self, *args, **kwargs)

    def readIsrData(self, dataRef, rawExposure):
        """There is no ISR data"""
        return lsst.pipe.base.Struct()

    def run(self, ccdExposure):
        """Mask negative pixels"""
        ccd = ccdExposure.getDetector()
        ccdExposure = self.convertIntToFloat(ccdExposure)

        self.updateVariance(ccdExposure, ccd[0])  # Treating as having only a single amplifier

        image = ccdExposure.getMaskedImage().getImage()
        mask = ccdExposure.getMaskedImage().getMask()
        bad = mask.getPlaneBitMask("BAD")
        if False:
            mask.getArray()[:] = numpy.where(image <= 0, bad, 0)  # XXX this causes bad things to happen

        #from lsst.afw.image.utils import clipImage
        #clipImage(image,0,10)
        #exit()


        """ transfer wcs system to TAN """
        matches = ReferenceMatchVector()
        md  = ccdExposure.getMetadata()
        wcs = ccdExposure.getWcs()

        refSchema = SimpleTable.makeMinimalSchema()
        Point2DKey.addFields(refSchema, "centroid", "centroid position", "pixel")
        refCatalog = SimpleCatalog(refSchema)
        schema = SourceTable.makeMinimalSchema()
        centroidKey = Point2DKey.addFields(schema, "centroid", "centroid position", "pixel")
        imgCatalog = SourceCatalog(schema)
        imgCatalog.defineCentroid("centroid")

#        for i in numpy.linspace(10, md.get("ZNAXIS1")-10, 20):
#            for j in numpy.linspace(10, md.get("ZNAXIS2")-10, 20):
        for i in numpy.linspace(10, 4000, 10):
            for j in numpy.linspace(10, 4000, 10):
                imgcrd = Point2D(i,j)  
                skycrd = wcs.pixelToSky(afwGeom.Point2D(i, j))
                # Create the reference catalog (with coordinates on the sky)
                refSrc = refCatalog.addNew()
                refSrc.setCoord(skycrd)
                # Create the position catalog (with positions on the image)
                imgSrc = imgCatalog.addNew()
                imgSrc.set(centroidKey, imgcrd)
                # matches
                matches.push_back(ReferenceMatch(refSrc, imgSrc, float("NaN")))

        # make initial wcs
        refPix = afwGeom.Point2D(0.5*ccdExposure.getWidth(), 0.5*ccdExposure.getHeight())
        refSky = wcs.pixelToSky(refPix)
        xPixelScale = yPixelScale = (0.2*afwGeom.arcseconds).asDegrees()
        initanWcs = afwImage.makeWcs(refSky, refPix, xPixelScale, 0.0, 0.0, yPixelScale)
        # obtain modified wcs with matched catalogs
        fitter = FitTanSipWcsTask()
        fitRes = fitter.fitWcs(
            matches = matches,
            initWcs = initanWcs,
            refCat = refCatalog,
            sourceCat = imgCatalog,
        )
        ccdExposure.setWcs(fitRes.wcs)


        """ Set zero point, ZP error, exptime """
    	zp = md.get("MAGZPT")
    	ccdExposure.getCalib().setFluxMag0(10.0**(0.4*zp))

        return lsst.pipe.base.Struct(exposure=ccdExposure)
