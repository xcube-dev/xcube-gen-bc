import os
import unittest
import xarray as xr
from xcube.api.gen.gen import gen_cube
from xcube.util.dsio import rimraf
from test.helpers import get_inputdata_file


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
        status = process_inputs_wrapper(input_path=[get_inputdata_file('O_L2_0001_SNS_2017104102450_v1.0.nc'),
                                                    get_inputdata_file('O_L2_0001_SNS_2017105095839_v1.0.nc'),
                                                    get_inputdata_file('O_L2_0001_SNS_2017105100139_v1.0.nc')],
                                        output_path='l2c.nc',
                                        output_writer='netcdf4',
                                        append_mode=True)
        self.assertEqual(True, status)

    def test_process_inputs_insert_multiple_nc(self):
        status = process_inputs_wrapper(input_path=[get_inputdata_file('O_L2_0001_SNS_*_v1.0.nc')],
                                        output_path='l2c.nc',
                                        output_writer='netcdf4',
                                        append_mode=True)
        self.assertEqual(False, status)

    # def test_not_implemented_insert_nc_cube(self):
    #      with self.assertRaises(NotImplementedError):
    #         gen_cube(input_paths=[get_inputdata_file('O_L2_0001_SNS_*_v1.0.nc')],
    #                  input_processor_name='snap-olci-highroc-l2',
    #                  output_region=(0., 50., 5., 52.5),
    #                  output_size=(2000, 1000),
    #                  output_resampling='Nearest',
    #                  output_path='l2c.nc',
    #                  output_writer_name='netcdf4',
    #                  output_variables=[('conc_chl', None), ('conc_tsm', None), ('kd489', None)],
    #                  append_mode=True,
    #                  dry_run=False,
    #                  monitor=None)

    def test_process_inputs_append_multiple_zarr(self):
        status = process_inputs_wrapper(input_path=[get_inputdata_file('O_L2_0001_SNS_*_v1.0.nc')],
                                        output_path='l2c.zarr',
                                        output_writer='zarr',
                                        append_mode=True)
        self.assertEqual(True, status)

    def test_correct_times_in_cube(self):
        status = process_inputs_wrapper(input_path=[get_inputdata_file('O_L2_0001_SNS_*_v1.0.nc')],
                                        output_path='l2c.zarr',
                                        output_writer='zarr',
                                        append_mode=True)
        self.assertEqual(True, status)
        ds = xr.open_zarr('l2c.zarr')
        self.assertEqual(f"['2017-04-14T10:27:39.819000320' '2017-04-15T10:01:37.405000192'\n "
                         f"'2017-04-15T10:01:57.892000256']", str(ds.time.values))

# noinspection PyShadowingBuiltins
def process_inputs_wrapper(input_path=None,
                           output_path=None,
                           output_writer='netcdf4',
                           append_mode=False):
    return gen_cube(input_paths=input_path, input_processor_name='snap-olci-highroc-l2',
                    output_region=(0., 50., 5., 52.5),
                    output_size=(2000, 1000), output_resampling='Nearest', output_path=output_path,
                    output_writer_name=output_writer,
                    output_variables=[('conc_chl', None), ('conc_tsm', None), ('kd489', None)], append_mode=append_mode,
                    dry_run=False, monitor=None)
