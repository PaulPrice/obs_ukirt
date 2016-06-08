from lsst.pipe.tasks.ingest import ParseTask

class CasuWfcamParseTask(ParseTask):
    def translate_date(self, md):
        dateObs = md.get("DATE-OBS").strip()
        return dateObs[:dateObs.find("T")]

    def translate_project(self, md):
        return md.get("PROJECT").replace("/", "_")

    @staticmethod
    def getExtensionName(md):
        try:
            return str(md.get("CAMNUM"))
        except:
            return None