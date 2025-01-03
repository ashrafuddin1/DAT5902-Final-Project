import unittest
import pandas as pd
from headline_figure_code import prepare_data, filter_by_2022, add_income_group

class TestFunctions(unittest.TestCase):

    def setUp(self):
        self.test_file_path = 'test_data.csv'
        
    def test_prepare_data(self):
        """Ensures that the dataframe is loaded and cleaned properly e.g. removing unwanted columns"""
        clean_df = prepare_data(self.test_file_path)
        self.assertNotIn('World', clean_df['Entity'].values)
        self.assertFalse(clean_df.isnull().values.any())
        self.assertNotIn('Code', clean_df.columns)

    def test_filter_by_2022(self):
        """Checks that dataframe has been filtered by 2022."""
        clean_df = prepare_data(self.test_file_path)
        df_2022 = filter_by_2022(clean_df)
        self.assertTrue((df_2022['Year'] == 2022).all())
        self.assertEqual(len(df_2022), 4)

    def test_add_income_group(self):
        """Ensures income group column is added"""
        clean_df = prepare_data(self.test_file_path)
        df_2022 = filter_by_2022(clean_df)
        updated_df_2022 = add_income_group(df_2022)
        self.assertEqual(
            updated_df_2022[updated_df_2022['Entity'] == 'United States']['Income group'].values[0],
            'High Income'
        )

if __name__ == '__main__':
    unittest.main()