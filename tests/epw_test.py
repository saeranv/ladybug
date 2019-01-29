# coding=utf-8

import unittest
import os
import pytest

from ladybug.epw import EPW
from ladybug.datacollection import HourlyContinuousCollection, MonthlyCollection
from ladybug.designday import DesignDay
from ladybug.analysisperiod import AnalysisPeriod


class EPWTestCase(unittest.TestCase):
    """Test for (ladybug/epw.py)"""

    # preparing to test.
    def setUp(self):
        """set up."""
        pass

    def tearDown(self):
        """Nothing to tear down as nothing gets written to file."""
        pass

    def test_import_epw(self):
        """Test import standard epw."""
        relative_path = './tests/epw/chicago.epw'
        abs_path = os.path.abspath(relative_path)
        epw_rel = EPW(relative_path)
        epw = EPW(abs_path)

        assert epw_rel.file_path == os.path.normpath(relative_path)
        assert epw_rel.location.city == 'Chicago Ohare Intl Ap'
        assert epw.file_path == abs_path
        assert epw.location.city == 'Chicago Ohare Intl Ap'
        # Check that calling location getter only retrieves location
        assert epw.is_data_loaded is False
        dbt = epw.dry_bulb_temperature
        skyt = epw.sky_temperature  # test sky temperature calculation
        assert epw.is_data_loaded is True
        assert len(dbt) == 8760
        assert len(skyt) == 8760

    def test_import_tokyo_epw(self):
        """Test import standard epw from another location."""
        path = './tests/epw/tokyo.epw'
        epw = EPW(path)
        assert epw.is_header_loaded is False
        assert epw.location.city == 'Tokyo'
        assert epw.is_header_loaded is True
        assert epw.is_data_loaded is False
        dbt = epw.dry_bulb_temperature
        assert epw.is_data_loaded is True
        assert len(dbt) == 8760

    def test_epw_from_missing_values(self):
        """Test import custom epw with wrong types."""
        epw = EPW.from_missing_values()
        assert epw.is_header_loaded is True
        assert epw.is_data_loaded is True
        assert len(epw.dry_bulb_temperature) == 8760
        assert list(epw.dry_bulb_temperature.values) == [99.9] * 8760

    def test_json_methods(self):
        """Test JSON serialization methods"""
        relative_path = './tests/epw/chicago.epw'
        epw = EPW(relative_path)

        epw_json = epw.to_json()
        rebuilt_epw = EPW.from_json(epw_json)
        assert epw_json == rebuilt_epw.to_json()

    def test_invalid_epw(self):
        """Test the import of incorrect file type and a non-existent epw file."""
        path = './tests/epw/non-exitent.epw'
        with pytest.raises(Exception):
            epw = EPW(path)
            epw.location

        path = './tests/stat/chicago.stat'
        with pytest.raises(Exception):
            epw = EPW(path)
            epw.location

    def test_import_data(self):
        """Test the imported data properties."""
        relative_path = './tests/epw/chicago.epw'
        epw = EPW(relative_path)
        assert isinstance(epw.years, HourlyContinuousCollection)
        assert isinstance(epw.dry_bulb_temperature, HourlyContinuousCollection)
        assert isinstance(epw.dew_point_temperature, HourlyContinuousCollection)
        assert isinstance(epw.relative_humidity, HourlyContinuousCollection)
        assert isinstance(epw.atmospheric_station_pressure, HourlyContinuousCollection)
        assert isinstance(epw.extraterrestrial_horizontal_radiation, HourlyContinuousCollection)
        assert isinstance(epw.extraterrestrial_direct_normal_radiation, HourlyContinuousCollection)
        assert isinstance(epw.horizontal_infrared_radiation_intensity, HourlyContinuousCollection)
        assert isinstance(epw.global_horizontal_radiation, HourlyContinuousCollection)
        assert isinstance(epw.direct_normal_radiation, HourlyContinuousCollection)
        assert isinstance(epw.diffuse_horizontal_radiation, HourlyContinuousCollection)
        assert isinstance(epw.global_horizontal_illuminance, HourlyContinuousCollection)
        assert isinstance(epw.direct_normal_illuminance, HourlyContinuousCollection)
        assert isinstance(epw.diffuse_horizontal_illuminance, HourlyContinuousCollection)
        assert isinstance(epw.zenith_luminance, HourlyContinuousCollection)
        assert isinstance(epw.wind_direction, HourlyContinuousCollection)
        assert isinstance(epw.wind_speed, HourlyContinuousCollection)
        assert isinstance(epw.total_sky_cover, HourlyContinuousCollection)
        assert isinstance(epw.opaque_sky_cover, HourlyContinuousCollection)
        assert isinstance(epw.visibility, HourlyContinuousCollection)
        assert isinstance(epw.ceiling_height, HourlyContinuousCollection)
        assert isinstance(epw.present_weather_observation, HourlyContinuousCollection)
        assert isinstance(epw.present_weather_codes, HourlyContinuousCollection)
        assert isinstance(epw.precipitable_water, HourlyContinuousCollection)
        assert isinstance(epw.aerosol_optical_depth, HourlyContinuousCollection)
        assert isinstance(epw.snow_depth, HourlyContinuousCollection)
        assert isinstance(epw.days_since_last_snowfall, HourlyContinuousCollection)
        assert isinstance(epw.albedo, HourlyContinuousCollection)
        assert isinstance(epw.liquid_precipitation_depth, HourlyContinuousCollection)
        assert isinstance(epw.liquid_precipitation_quantity, HourlyContinuousCollection)
        assert isinstance(epw.sky_temperature, HourlyContinuousCollection)

    def test_set_data(self):
        """Test the ability to set the data of any of the epw hourly data."""
        relative_path = './tests/epw/chicago.epw'
        epw = EPW(relative_path)
        epw.dry_bulb_temperature[12] = 20
        assert epw.dry_bulb_temperature[12] == 20
        epw.dry_bulb_temperature.values = list(range(8760))
        assert epw.dry_bulb_temperature.values == tuple(range(8760))

        # Test if the set data is not annual
        with pytest.raises(Exception):
            epw.dry_bulb_temperature = list(range(365))

    def test_import_design_conditions(self):
        """Test the functions that import design conditions."""
        relative_path = './tests/epw/chicago.epw'
        epw = EPW(relative_path)
        assert isinstance(epw.heating_design_condition_dictionary, dict)
        assert len(epw.heating_design_condition_dictionary.keys()) == 15
        assert isinstance(epw.cooling_design_condition_dictionary, dict)
        assert len(epw.cooling_design_condition_dictionary.keys()) == 32
        assert isinstance(epw.extreme_design_condition_dictionary, dict)
        assert len(epw.extreme_design_condition_dictionary.keys()) == 16

    def test_set_design_conditions(self):
        """Test the functions that set design conditions."""
        relative_path = './tests/epw/chicago.epw'
        epw = EPW(relative_path)

        heat_dict = dict(epw.heating_design_condition_dictionary)
        heat_dict['DB996'] = -25
        epw.heating_design_condition_dictionary = heat_dict
        assert epw.heating_design_condition_dictionary['DB996'] == -25

        # Check for when the dictionary has a missing key
        wrong_dict = dict(heat_dict)
        del wrong_dict['DB996']
        with pytest.raises(Exception):
            epw.heating_design_condition_dictionary = wrong_dict

        # Check for when the wrong type is assigned
        heat_list = list(epw.heating_design_condition_dictionary.keys())
        with pytest.raises(Exception):
            epw.heating_design_condition_dictionary = heat_list

        cool_dict = dict(epw.cooling_design_condition_dictionary)
        cool_dict['DB004'] = 40
        epw.cooling_design_condition_dictionary = cool_dict
        assert epw.cooling_design_condition_dictionary['DB004'] == 40

        extremes_dict = dict(epw.extreme_design_condition_dictionary)
        extremes_dict['WS010'] = 20
        epw.extreme_design_condition_dictionary = extremes_dict
        assert epw.extreme_design_condition_dictionary['WS010'] == 20

    def test_import_design_days(self):
        """Test the functions that import design days."""
        relative_path = './tests/epw/chicago.epw'
        epw = EPW(relative_path)
        assert isinstance(epw.annual_heating_design_day_996, DesignDay)
        assert epw.annual_heating_design_day_996.dry_bulb_condition.dry_bulb_max == -20.0
        assert isinstance(epw.annual_heating_design_day_990, DesignDay)
        assert epw.annual_heating_design_day_990.dry_bulb_condition.dry_bulb_max == -16.6
        assert isinstance(epw.annual_cooling_design_day_004, DesignDay)
        assert epw.annual_cooling_design_day_004.dry_bulb_condition.dry_bulb_max == 33.3
        assert isinstance(epw.annual_cooling_design_day_010, DesignDay)
        assert epw.annual_cooling_design_day_010.dry_bulb_condition.dry_bulb_max == 31.6

    def test_import_extreme_weeks(self):
        """Test the functions that import the extreme weeks."""
        relative_path = './tests/epw/chicago.epw'
        epw = EPW(relative_path)
        ext_cold = list(epw.extreme_cold_weeks.values())[0]
        ext_hot = list(epw.extreme_hot_weeks.values())[0]
        assert isinstance(ext_cold, AnalysisPeriod)
        assert len(ext_cold.doys_int) == 7
        assert (ext_cold.st_month, ext_cold.st_day, ext_cold.end_month,
                ext_cold.end_day) == (1, 27, 2, 2)
        assert isinstance(ext_hot, AnalysisPeriod)
        assert len(ext_hot.doys_int) == 7
        assert (ext_hot.st_month, ext_hot.st_day, ext_hot.end_month,
                ext_hot.end_day) == (7, 13, 7, 19)

    def test_import_typical_weeks(self):
        """Test the functions that import the typical weeks."""
        relative_path = './tests/epw/chicago.epw'
        epw = EPW(relative_path)
        typ_weeks = list(epw.typical_weeks.values())
        assert len(typ_weeks) == 4
        for week in typ_weeks:
            assert isinstance(week, AnalysisPeriod)
            assert len(week.doys_int) == 7

    def test_set_extreme_typical_weeks(self):
        """Test the functions that set the extreme  and typical weeks."""
        relative_path = './tests/epw/chicago.epw'
        epw = EPW(relative_path)
        a_per_cold = AnalysisPeriod(1, 1, 0, 1, 7, 23)
        a_per_hot = AnalysisPeriod(7, 1, 0, 7, 7, 23)
        a_per_typ = AnalysisPeriod(5, 1, 0, 5, 7, 23)
        epw.extreme_cold_weeks = {'Extreme Cold Week': a_per_cold}
        epw.extreme_hot_weeks = {'Extreme Hot Week': a_per_hot}
        epw.typical_weeks = {'Typical Week': a_per_typ}
        assert list(epw.extreme_cold_weeks.values())[0] == a_per_cold
        assert list(epw.extreme_hot_weeks.values())[0] == a_per_hot
        assert list(epw.typical_weeks.values())[0] == a_per_typ

        # Test one someone sets an analysis_period longer than a week.
        a_per_wrong = AnalysisPeriod(1, 1, 0, 1, 6, 23)
        with pytest.raises(Exception):
            epw.extreme_cold_weeks = {'Extreme Cold Week': a_per_wrong}

        # Test when someone sets the wrong type of data
        with pytest.raises(Exception):
            epw.extreme_cold_weeks = a_per_cold

    def test_import_ground_temperatures(self):
        """Test the functions that import ground temperature."""
        relative_path = './tests/epw/chicago.epw'
        epw = EPW(relative_path)
        assert len(epw.monthly_ground_temperature.keys()) == 3
        assert tuple(epw.monthly_ground_temperature.keys()) == (0.5, 2.0, 4.0)
        assert isinstance(epw.monthly_ground_temperature[0.5], MonthlyCollection)
        assert epw.monthly_ground_temperature[0.5].values == \
            (-1.89, -3.06, -0.99, 2.23, 10.68, 17.2,
             21.6, 22.94, 20.66, 15.6, 8.83, 2.56)
        assert epw.monthly_ground_temperature[2].values == \
            (2.39, 0.31, 0.74, 2.45, 8.1, 13.21,
             17.3, 19.5, 19.03, 16.16, 11.5, 6.56)
        assert epw.monthly_ground_temperature[4].values == \
            (5.93, 3.8, 3.34, 3.98, 7.18, 10.62,
             13.78, 15.98, 16.49, 15.25, 12.51, 9.17)

    def test_set_ground_temperatures(self):
        """Test the functions that set ground temperature."""
        relative_path = './tests/epw/chicago.epw'
        epw = EPW(relative_path)
        grnd_dict = dict(epw.monthly_ground_temperature)
        grnd_dict[0.5].values = list(range(12))
        epw.monthly_ground_temperature = grnd_dict
        assert epw.monthly_ground_temperature[0.5].values == tuple(range(12))

        # test when the type is not a monthly collection.
        grnd_dict = dict(epw.monthly_ground_temperature)
        grnd_dict[0.5] = list(range(12))
        with pytest.raises(Exception):
            epw.monthly_ground_temperature = grnd_dict

        # Test when type is not a dictionary

    def test_epw_header(self):
        """Check that the process of parsing the EPW header hasn't changed it."""
        relative_path = './tests/epw/chicago.epw'
        epw = EPW(relative_path)
        for i in range(len(epw.header)):
            line1, line2 = epw.header[i], epw._header[i]
            if i in (0, 1, 4, 5, 6, 7):
                # These lines should match exactly
                assert line1 == line2
            elif i in (2, 3):
                # The order of data in these lines can change and  spaces can get deleted
                assert len(line1.split(',')) == len(line2.split(','))

    def test_save_epw(self):
        """Test save epw_rel."""
        path = './tests/epw/tokyo.epw'
        epw = EPW(path)

        modified_path = './tests/epw/tokyo_modified.epw'
        epw.save(modified_path)
        assert os.path.isfile(modified_path)
        assert os.stat(modified_path).st_size > 1
        os.remove(modified_path)

    def test_save_epw_from_missing_values(self):
        """Test import custom epw with wrong types."""
        epw = EPW.from_missing_values()
        file_path = './tests/epw/missing.epw'
        epw.save(file_path)
        assert os.path.isfile(file_path)
        assert os.stat(file_path).st_size > 1
        os.remove(file_path)

    def test_save_wea(self):
        """Test save wea_rel."""
        path = './tests/epw/chicago.epw'
        epw = EPW(path)
        wea_path = './tests/wea/chicago_epw.wea'
        epw.to_wea(wea_path)
        assert os.path.isfile(wea_path)
        assert os.stat(wea_path).st_size > 1

        # check the order of the data in the file
        with open(wea_path) as wea_f:
            line = wea_f.readlines()
            assert float(line[6].split(' ')[-2]) == epw.direct_normal_radiation[0]
            assert float(line[6].split(' ')[-1]) == epw.diffuse_horizontal_radiation[0]
            assert float(line[17].split(' ')[-2]) == epw.direct_normal_radiation[11]
            assert float(line[17].split(' ')[-1]) == epw.diffuse_horizontal_radiation[11]

        os.remove(wea_path)


if __name__ == "__main__":
    unittest.main()
