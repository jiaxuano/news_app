import unittest
from unittest.mock import patch
import pandas as pd
from main import load_data  # Make sure to replace 'your_script_name' with the actual name of your script

class TestDataLoading(unittest.TestCase):

    @patch('pandas.read_csv')
    def test_load_data(self, mock_read_csv):
        # Mock data
        test_data = pd.DataFrame({
            'publish_date': ['2023-04-01', '2023-03-31', '2023-04-02'],
            'title': ['Title1', 'Title2', 'Title3']
        })
        
        # Set the mock to return the test data
        mock_read_csv.return_value = test_data

        # Call the function
        df = load_data('Fannie Mae')

        # Assertions to check if the data is sorted correctly
        self.assertEqual(df.iloc[0]['title'], 'Title3')
        self.assertEqual(df.iloc[1]['title'], 'Title1')
        self.assertEqual(df.iloc[2]['title'], 'Title2')

if __name__ == '__main__':
    unittest.main()