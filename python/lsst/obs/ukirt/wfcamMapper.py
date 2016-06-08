#!/usr/bin/env python

from lsst.daf.butlerUtils import CameraMapper
from lsst.daf.persistence import ButlerLocation
import lsst.afw.image.utils as afwImageUtils
import lsst.afw.image as afwImage
import lsst.afw.geom as afwGeom
import lsst.afw.coord as afwCoord
import lsst.pex.policy as pexPolicy

class CasuWfcamMapper(CameraMapper):
    """Provides abstract-physical mapping for UKIRT+WFCAM data from CASU"""
    packageName = "obs_ukirt"

    def __init__(self, **kwargs):
        policyFile = pexPolicy.DefaultPolicyFile("obs_ukirt", "CasuWfcamMapper.paf", "policy")
        policy = pexPolicy.Policy(policyFile)
        CameraMapper.__init__(self, policy, policyFile.getRepositoryPath(), **kwargs)

        # Ensure each dataset type of interest knows about the full range of keys available from the registry
        keys = {
            'project': str,
            'object': str,
            'obsType': str,
            'visit': int,
            'grp': int,
            'dateObs': str,
            'expTime': float,
            'filter': str,
            'date': str,
        }
        for name in ("raw",
                     # processCcd outputs
                     "calexp", "src", "icMatch", "icMatchFull",
                     "srcMatch", "srcMatchFull",
                     # Warp
                     "deepCoadd_tempExp",
                     ):
            self.mappings[name].keyDict.update(keys)

        # The order of these defineFilter commands matters as their IDs are used to generate at least some
        # object IDs (e.g. on coadds) and changing the order will invalidate old objIDs

        afwImageUtils.resetFilters()
        afwImageUtils.defineFilter(name='Z', lambdaEff=950, alias=[])
        afwImageUtils.defineFilter(name='Y', lambdaEff=1100, alias=[])
        afwImageUtils.defineFilter(name='J', lambdaEff=1300, alias=[])
        afwImageUtils.defineFilter(name='H', lambdaEff=1600, alias=[])
        afwImageUtils.defineFilter(name='K', lambdaEff=2000, alias=[])

        self.filters = {}
        for f in "ZYJHK":
            self.filters[f] = f

        #
        # The number of bits allocated for fields in object IDs, appropriate for
        # the default-configured Rings skymap.
        #
        CasuWfcamMapper._nbit_tract = 16
        CasuWfcamMapper._nbit_patch  = 5
        CasuWfcamMapper._nbit_filter = 6
        CasuWfcamMapper._nbit_id = 64 - (CasuWfcamMapper._nbit_tract + 2*CasuWfcamMapper._nbit_patch +
                                         CasuWfcamMapper._nbit_filter)
        if len(afwImage.Filter.getNames()) >= 2**CasuWfcamMapper._nbit_filter:
            raise RuntimeError("You have more filters defined than fit into the %d bits allocated" %
                               CasuWfcamMapper._nbit_filter)

    def map(self, datasetType, dataId, write=False):
        """Need to strip 'flags' argument from map

        We want the 'flags' argument passed to the butler to work (it's
        used to change how the reading/writing is done), but want it
        removed from the mapper (because it doesn't correspond to a
        registry column).
        """
        copyId = dataId.copy()
        copyId.pop("flags", None)
        location = super(CasuWfcamMapper, self).map(datasetType, copyId, write=write)

        if 'flags' in dataId:
            location.getAdditionalData().set('flags', dataId['flags'])

        return location

    def map_linearize(self, dataId, write=False):
        """Map a linearizer."""
        raise RuntimeError("No linearization available.")

    def bypass_defects(self, datasetType, pythonType, location, dataId):
        """since we have no defects, return an empty list.  Fix this when defects exist """
        return []

    # def std_raw(self, item, dataId):
    #     md = item.getMetadata()
    #     # afw doesn't understand ZPN
    #     md.set("CTYPE1", "RA---TAN")
    #     md.set("CTYPE2", "DEC--TAN")
    #     md.remove("PV2_1")
    #     md.remove("PV2_2")
    #     md.remove("PV2_3")
    #    return CameraMapper.std_raw(self, item, dataId)

    def std_raw(self, image, dataId):
        """Standardize a raw dataset by converting it to an Exposure instead of an Image"""
        if isinstance(image, afwImage.DecoratedImageU) or isinstance(image, afwImage.DecoratedImageI) or \
                isinstance(image, afwImage.DecoratedImageF) or isinstance(image, afwImage.DecoratedImageD):
            exposure = afwImage.makeExposure(afwImage.makeMaskedImage(image.getImage()))
        else:
            exposure = image
        md = image.getMetadata()

        if False:
            wcs = afwImage.makeWcs(md, True)

            # The CASU WCSes use ZPN; our stuff wants TAN
            # This won't work near the pole, but should be decent away from it.
            box = afwGeom.BoxD(image.getImage().getBBox())
            refPix = box.getCenter()
            refSky = wcs.pixelToSky(refPix)
            refSkyOffsetX = wcs.pixelToSky(refPix + afwGeom.Extent2D(1.0, 0.0))
            refSkyOffsetY = wcs.pixelToSky(refPix + afwGeom.Extent2D(0.0, 1.0))
            xPixelScale = refSky.angularSeparation(refSkyOffsetX).asDegrees()
            yPixelScale = refSky.angularSeparation(refSkyOffsetY).asDegrees()

            xPixelScale = yPixelScale = wcs.pixelScale().asDegrees()
        else:
            refPix = afwGeom.Point2D(md.get("CRPIX1"), md.get("CRPIX2"))
            refSky = afwCoord.IcrsCoord(md.get("CRVAL1")*afwGeom.degrees,
                                        md.get("CRVAL2")*afwGeom.degrees)
            xPixelScale = yPixelScale = (0.2*afwGeom.arcseconds).asDegrees()

#        import pdb;pdb.set_trace()

        exposure.setMetadata(md)

        newWcs = afwImage.makeWcs(refSky, refPix, xPixelScale, 0.0, 0.0, yPixelScale)
        exposure.setWcs(newWcs)

        return self._standardizeExposure(self.exposures['raw'], exposure, dataId,
                                         trimmed=False)



    def _defectLookup(self, dataId):
        """ This function needs to return a non-None value otherwise the mapper gives up
        on trying to find the defects.  I wanted to be able to return a list of defects constructed
        in code rather than reconstituted from persisted files, so I return a dummy value.
        """
        return "hack"

    def _extractAmpId(self, dataId):
        return 0

    def _extractDetectorName(self, dataId):
        return int("%(ccd)d" % dataId)

    def _computeCcdExposureId(self, dataId):
        """Compute the 64-bit (long) identifier for a CCD exposure.

        @param dataId (dict) Data identifier with visit, ccd
        """
        pathId = self._transformId(dataId)
        visit = pathId['visit']
        ccd = pathId['ccd']
        return visit*10 + ccd

    def bypass_ccdExposureId(self, datasetType, pythonType, location, dataId):
        return self._computeCcdExposureId(dataId)

    def bypass_ccdExposureId_bits(self, datasetType, pythonType, location, dataId):
        """How many bits are required for the maximum exposure ID"""
        return 32 # just a guess, but this leaves plenty of space for sources

    def _computeCoaddExposureId(self, dataId, singleFilter):
        """Compute the 64-bit (long) identifier for a coadd.

        @param dataId (dict)       Data identifier with tract and patch.
        @param singleFilter (bool) True means the desired ID is for a single- 
                                   filter coadd, in which case dataId
                                   must contain filter.
        """

        tract = long(dataId['tract'])
        if tract < 0 or tract >= 2**CasuWfcamMapper._nbit_tract:
            raise RuntimeError('tract not in range [0,%d)' % (2**CasuWfcamMapper._nbit_tract))
        patchX, patchY = map(int, dataId['patch'].split(','))
        for p in (patchX, patchY):
            if p < 0 or p >= 2**CasuWfcamMapper._nbit_patch:
                raise RuntimeError('patch component not in range [0, %d)' % 2**CasuWfcamMapper._nbit_patch)
        oid = (((tract << CasuWfcamMapper._nbit_patch) + patchX) << CasuWfcamMapper._nbit_patch) + patchY
        if singleFilter:
            return (oid << CasuWfcamMapper._nbit_filter) + afwImage.Filter(dataId['filter']).getId()
        return oid

    def bypass_deepCoaddId_bits(self, *args, **kwargs):
        """The number of bits used up for patch ID bits"""
        return 64 - CasuWfcamMapper._nbit_id

    def bypass_deepCoaddId(self, datasetType, pythonType, location, dataId):
        return self._computeCoaddExposureId(dataId, True)

    def bypass_deepMergedCoaddId_bits(self, *args, **kwargs):
        """The number of bits used up for patch ID bits"""
        return 64 - CasuWfcamMapper._nbit_id

    def bypass_deepMergedCoaddId(self, datasetType, pythonType, location, dataId):
        return self._computeCoaddExposureId(dataId, False)

    # The following allow grabbing a 'psf' from the butler directly, without having to get it from a calexp
    def map_psf(self, dataId, write=False):
        if write:
            raise RuntimeError("Writing a psf directly is no longer permitted: write as part of a calexp")
        copyId = dataId.copy()
        copyId['bbox'] = afwGeom.Box2I(afwGeom.Point2I(0,0), afwGeom.Extent2I(1,1))
        return self.map_calexp_sub(copyId)

    def std_psf(self, calexp, dataId):
        return calexp.getPsf()

    @classmethod
    def getCameraName(cls):
        return "casuWfcam"
