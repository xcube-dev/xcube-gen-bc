import os
import unittest
from io import StringIO
from unittest.mock import patch

import xarray as xr
from xcube.core.dsio import rimraf
from xcube.core.gen.gen import gen_cube

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
                                        input_processor_name='snap-olci-highroc-l2',
                                        output_path='l2c-single.nc',
                                        output_writer='netcdf4',
                                        append_mode=False)
        self.assertEqual(True, status)

    def test_process_inputs_append_multiple_nc(self):
        status = process_inputs_wrapper(input_path=[get_inputdata_file('O_L2_0001_SNS_2017104102450_v1.0.nc'),
                                                    get_inputdata_file('O_L2_0001_SNS_2017105095839_v1.0.nc'),
                                                    get_inputdata_file('O_L2_0001_SNS_2017105100139_v1.0.nc')],
                                        input_processor_name='snap-olci-highroc-l2',
                                        output_path='l2c.nc',
                                        output_writer='netcdf4',
                                        append_mode=True)
        self.assertEqual(True, status)

    def test_process_inputs_insert_multiple_nc(self):
        with patch('sys.stdout', new=StringIO()) as output:
            process_inputs_wrapper(input_path=[get_inputdata_file('O_L2_0001_SNS_*_v1.0.nc')],
                                   input_processor_name='snap-olci-highroc-l2',
                                   output_path='l2c.nc',
                                   output_writer='netcdf4',
                                   append_mode=True, monitor=print, no_sort_mode=False)
            self.assertEqual(output.getvalue()[-69:],
                             '3 of 3 datasets processed successfully, 0 were dropped due to errors\n')

    def test_process_inputs_append_multiple_zarr(self):
        status = process_inputs_wrapper(input_path=[get_inputdata_file('O_L2_0001_SNS_*_v1.0.nc')],
                                        input_processor_name='snap-olci-highroc-l2',
                                        output_path='l2c.zarr',
                                        output_writer='zarr',
                                        append_mode=True)
        self.assertEqual(True, status)

    def test_process_inputs_cmems_daily_nc(self):
        status = process_inputs_wrapper(
            input_path=[get_inputdata_file('OCEANCOLOUR_ATL_CHL_L4_REP_OBSERVATIONS_009_098-TDS-2017-11-10.nc')],
            input_processor_name='cmems',
            output_path='l2c.zarr',
            output_writer='zarr',
            append_mode=True)
        self.assertEqual(True, status)
        ds = xr.open_zarr('l2c.zarr')
        self.assertEqual('2017-11-10T12:00:00.000000000', str(ds.time[0].values))
        self.assertEqual('2017-11-11T00:00:00.000000000', ds.attrs['time_coverage_end'])
        self.assertEqual('2017-11-10T00:00:00.000000000', ds.attrs['time_coverage_start'])

    def test_process_inputs_cmems_hourly_nc(self):
        status = process_inputs_wrapper(
            input_path=[get_inputdata_file('NORTHWESTSHELF_ANALYSIS_FORECAST_WAV_004_014-TDS-2019-08-21-15.nc')],
            input_processor_name='cmems',
            output_path='l2c.zarr',
            output_writer='zarr',
            append_mode=True)
        self.assertEqual(True, status)
        ds = xr.open_zarr('l2c.zarr')
        self.assertEqual('2019-08-21T15:30:00.000000000', str(ds.time[0].values))
        self.assertEqual('2019-08-21T16:00:00.000000000', ds.attrs['time_coverage_end'])
        self.assertEqual('2019-08-21T15:00:00.000000000', ds.attrs['time_coverage_start'])
        self.assertIn('lon', ds.dims)
        self.assertIn('lat', ds.dims)

    def test_process_bc_s2_inputs_single(self):
        status = gen_cube(
            input_paths=[get_inputdata_file('S2A_MSIL1C_20150929T100016_N0204_R122_T34VCK_20150929T100239.nc')],
            input_processor_name='bc-s2-l2',
            output_path='l2c-single.zarr',
            output_variables=[('conc_chl', (None)),
                              ('conc_tsm', (None)),
                              ('rhow_B4', (None))],
            output_resampling='Nearest',
            output_region=(17.5, 57.6, 19.4, 58.6),
            no_sort_mode=False, dry_run=False, monitor=None,
            output_writer_name='zarr')
        self.assertEqual(True, status)
        ds = xr.open_zarr('l2c-single.zarr')
        self.assertEqual('2015-09-29T10:00:16.027000064', str(ds.time[0].values))

# noinspection PyShadowingBuiltins
def process_inputs_wrapper(input_path=None,
                           input_processor_name=None,
                           output_path=None,
                           output_writer='netcdf4',
                           append_mode=False,
                           no_sort_mode=False,
                           monitor=None):
    return gen_cube(input_paths=input_path, input_processor_name=input_processor_name,
                    output_region=(0., 50., 5., 52.5),
                    output_size=(2000, 1000), output_resampling='Nearest', output_path=output_path,
                    output_writer_name=output_writer,
                    output_variables=[('conc_chl', None), ('conc_tsm', None)], append_mode=append_mode,
                    no_sort_mode=no_sort_mode, dry_run=False, monitor=monitor)
