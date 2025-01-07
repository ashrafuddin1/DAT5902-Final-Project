import unittest
import pandas as pd
import matplotlib.pyplot as plt
import os
from  analysis import prepare_data, filter_by_2022, add_income_group, add_emissions_per_gdp, plot_scatter, add_regression_line, create_headline_plot, create_bottom_10_barplot, create_top_10_barplot

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

    def test_add_emissions_per_gdp(self):
        """Ensures emissions per gdp column is added"""
        clean_df = prepare_data(self.test_file_path)
        df_2022 = filter_by_2022(clean_df)
        updated_df_2022 = add_income_group(df_2022)
        updated_df_2022 = add_emissions_per_gdp(updated_df_2022)

        self.assertIn('CO₂ emissions per $100,000 GDP', updated_df_2022.columns)
        # Checking the caluclation is correct
        first_row = updated_df_2022.iloc[0]
        expected_value = (first_row['Annual CO₂ emissions (per capita)'] / first_row['GDP per capita']) * 100000
        self.assertAlmostEqual(
            first_row['CO₂ emissions per $100,000 GDP'], expected_value, places=2,
            msg="CO₂ emissions per $100,000 GDP calculation is incorrect"
        )

    def test_create_headline_plot(self):
        """Ensures headline plot runs and was saved to a file"""
        clean_df = prepare_data(self.test_file_path)
        df_2022 = filter_by_2022(clean_df)
        updated_df_2022 = add_income_group(df_2022)
        try:
            create_headline_plot(updated_df_2022)
        except:
            self.fail("Headline plot creation failed")

        self.assertTrue(os.path.exists("headline_figure.png"), "The headline figure file was not created.")
 

    def test_create_top_10_and_bottom_10_barplot(self):
        """Makes sure the create_top_10_barplot and create_bottom_10_barplot functions runs and are saved to a file"""
        clean_df = prepare_data(self.test_file_path)
        df_2022 = filter_by_2022(clean_df)
        updated_df_2022 = add_income_group(df_2022)
        updated_df_2022 = add_emissions_per_gdp(updated_df_2022)
        try:
            create_top_10_barplot(updated_df_2022)
            create_bottom_10_barplot(updated_df_2022)
        except:
            self.fail("Barplot creation failed")

        self.assertTrue(os.path.exists("top10_figure.png"), "The top 10 figure file was not created.")
        self.assertTrue(os.path.exists("bottom10_figure.png"), "The bottom 10 figure file was not created.")

if __name__ == '__main__':
    unittest.main()