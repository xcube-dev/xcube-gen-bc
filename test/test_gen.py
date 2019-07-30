import os
import unittest

from test.helpers import get_inputdata_file
from xcube.api.gen.gen import gen_cube
from xcube.util.dsio import rimraf


def clean_up():
    files = ['l2c-single.nc', 'l2c.nc', 'l2c.zarr']
    for file in files:
        rimraf(os.path.join('.', file))
        rimraf(os.path.join('.', file + 'temp.nc'))


class SnapProcessTest(unittest.TestCase):

    def setUp(self):
        clean_up()

    def tearDown(self):
        clean_up()

    # noinspection PyMethodMayBeStatic
    def test_process_inputs_single(self):
        status = process_inputs_wrapper(input_path=[get_inputdata_file('O_L2_0001_SNS_2017105100139_v1.0.nc')],
                                        output_path='l2c-single.nc',
                                        output_writer='netcdf4',
                                        append_mode=False)
        self.assertEqual(True, status)

    def test_process_inputs_append_multiple_nc(self):
        status = process_inputs_wrapper(input_path=[get_inputdata_file('O_L2_0001_SNS_*_v1.0.nc')],
                                        output_path='l2c.nc',
                                        output_writer='netcdf4',
                                        append_mode=True)
        self.assertEqual(True, status)

    def test_process_inputs_append_multiple_zarr(self):
        status = process_inputs_wrapper(input_path=[get_inputdata_file('O_L2_0001_SNS_*_v1.0.nc')],
                                        output_path='l2c.zarr',
                                        output_writer='zarr',
                                        append_mode=True)
        self.assertEqual(True, status)


# noinspection PyShadowingBuiltins
def process_inputs_wrapper(input_path=None,
                           output_path=None,
                           output_writer='netcdf4',
                           append_mode=False):
    return gen_cube(input_paths=input_path, input_processor='snap-olci-highroc-l2', output_region=(0., 50., 5., 52.5),
                    output_size=(2000, 1000), output_resampling='Nearest', output_path=output_path,
                    output_writer=output_writer,
                    output_variables=[('conc_chl', None), ('conc_tsm', None), ('kd489', None)], append_mode=append_mode,
                    dry_run=False, monitor=None)
