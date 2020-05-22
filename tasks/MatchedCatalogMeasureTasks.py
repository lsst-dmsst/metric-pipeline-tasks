import astropy.units as u
import numpy as np
from lsst.pipe.base import Struct, Task
from lsst.pex.config import Config, Field
from lsst.verify import Measurement, ThresholdSpecification
import lsst.pex.config as pexConfig
from sst_metrics_utils.filtermatches import filterMatches
from lsst.validate.drp.repeatability import calcPhotRepeat

class NumSourcesTask(Task):

    ConfigClass = Config
    _DefaultName = "numSourcesTask"

    def run(self, matchedCatalog, metric_name):
        self.log.info(f"Counting sources in matched catalog")
        nSources = len(matchedCatalog)
        meas = Measurement("nsrcMeas", nSources * u.count)
        return Struct(measurement=meas)


class PA1TaskConfig(Config):
    brightSnrMin = Field(doc="Minimum median SNR for a source to be considered bright.",
                                   dtype=float, default=50)
    brightSnrMax = Field(doc="Maximum median SNR for a source to be considered bright.",
                                   dtype=float, default=np.Inf)


class PA1Task(Task):

    ConfigClass = PA1TaskConfig
    _DefaultName = "PA1Task"

    def __init__(self, config: PA1TaskConfig, *args, **kwargs):
        super().__init__(*args, config=config, **kwargs)
        self.brightSnrMin = self.config.brightSnrMin
        self.brightSnrMax = self.config.brightSnrMax

    def run(self, matchedCatalog, metric_name):
        self.log.info(f"Measuring PA1")

        filteredCat = filterMatches(matchedCatalog) #, extended=False, isPrimary=False)
        magKey = filteredCat.schema.find('slot_PsfFlux_mag').key

        # Require at least nMinPA1=10 objects to calculate the repeatability:
        nMinPA1 = 50
        if filteredCat.count > nMinPA1:
            pa1 = calcPhotRepeat(filteredCat, magKey)
            return Struct(measurement=Measurement("PA1", pa1['repeatability']))
        else:
            return Struct(measurement=Measurement("PA1", np.nan*u.mmag))
