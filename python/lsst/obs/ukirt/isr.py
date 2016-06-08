import numpy
import lsst.pipe.base
import lsst.ip.isr

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

        # XXX check (set?) WCS
        # XXX set zero point

        return lsst.pipe.base.Struct(exposure=ccdExposure)