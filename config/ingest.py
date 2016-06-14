from lsst.obs.ukirt.ingest import CasuWfcamParseTask
config.parse.retarget(CasuWfcamParseTask)

config.parse.hdu = 1  # PHU
config.parse.extnames = list("1234")

config.parse.translation = {
    'project': 'PROJECT',
    'object': 'OBJECT',
    'obsType': 'OBSTYPE',
    #'visit': 'OBSNUM',
    'ccd': 'CAMNUM',
    'grp': 'GRPNUM',
    'dateObs': 'DATE-OBS',
    'expTime': 'EXPTIME',
    'filter': 'FILTER',
}
config.parse.defaults = {
    'ccd': '0',
}

config.parse.translators = {
    'visit': 'translate_visit',
    'date': 'translate_date',
    'project': 'translate_project',
}

config.register.columns = {
    'project': 'text',  # Time-allocation code (e.g., "U/15A/UA03")
    'object': 'text',  # Object name from telescope
    'obsType': 'text',  # BIAS|DARK|SKYFLAT|DOMEFLAT|OBJECT|SKY|FOCUS
    'visit': 'int',  # Observation number, from 'OBSNUM' in the header
    'ccd': 'int',  # Detector number (no, these aren't CCDs, but that's what the system expects)
    'grp': 'int',  # Group number applied to all members (will probably match visit)
    'dateObs': 'text',  # Date time (UTC) of start of observation
    'expTime': 'double',  # Integration time per exposure [s]
    'filter': 'text',  # Filter name
    'date': 'text',  # Date of observation
}
config.register.unique = ['visit', 'ccd',]
config.register.visit = ['project', 'object', 'obsType', 'visit', 'grp', 'dateObs', 'expTime', 'filter',
                         'date']
