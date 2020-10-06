# This file is part of <REPLACE WHEN RENAMED>.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Unit tests for the metrics measurement system: PA1, PA2, PF1.
"""

import unittest
import yaml
import os
import random

from lsst.utils import getPackageDir
from lsst.afw.table import SimpleCatalog
from metric_pipeline_tasks import PA1Task

random.seed(8675309)

DATADIR = os.path.join(getPackageDir('metric_pipeline_tasks'), 'tests', 'data')


class Pa1Test(unittest.TestCase):

    def load_data(self, key):
        '''Helper to load data to process and the expected value.'''
        cat_file, expected_file = self.file_map[key]
        catalog = SimpleCatalog.readFits(os.path.join(DATADIR, cat_file))
        with open(os.path.join(DATADIR, expected_file), 'r') as fh:
            expected = yaml.load(fh, Loader=yaml.FullLoader)
        return catalog, expected

    @classmethod
    def setUpClass(cls):
        '''This gets called once so can be used to set up
           state that is used by all test methods.'''
        super().setUpClass()
        cls.file_map = {('PA1', 'i'): ('matchedCatalog_0_85_i.fits.gz', 'PA1_expected_0_85_i.yaml'),
                        ('PA1', 'r'): ('matchedCatalog_0_85_r.fits.gz', 'PA1_expected_0_85_r.yaml')}

    @classmethod
    def tearDownClass(cls):
        '''Delete any variables set in setUpClass.'''
        del cls.file_map
        super().tearDownClass()

    def test_pa1(self):
        """Test calculation of am1 on a known catalog."""
        config = PA1Task.ConfigClass()
        task = PA1Task(config=config)
        for band in ('i', 'r'):
            catalog, expected = self.load_data(('PA1', band))
            result = task.run(catalog, 'validate_drp.PA1')
            self.assertEqual(result.measurement, expected)


if __name__ == "__main__":
    unittest.main()