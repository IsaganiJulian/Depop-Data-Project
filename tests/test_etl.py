import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.extract import extract_data
from src.transform import DataCleaner
from src.quality import quality_checks


class TestExtract(unittest.TestCase):
    def test_extract_combines_multiple_csv_files(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            raw_dir = Path(tmp_dir)
            pd.DataFrame({"a": [1, 2]}).to_csv(raw_dir / "one.csv", index=False)
            pd.DataFrame({"a": [3]}).to_csv(raw_dir / "two.csv", index=False)

            result = extract_data(str(raw_dir))

            self.assertEqual(len(result), 3)
            self.assertListEqual(result["a"].tolist(), [1, 2, 3])


class TestTransform(unittest.TestCase):
    def test_fill_sales_tax_uses_amount_not_rate(self):
        df = pd.DataFrame(
            {
                "State": ["CA", "UT"],
                "Item price": [100.0, 50.0],
                "US Sales tax": [None, None],
            }
        )

        cleaned = (
            DataCleaner(df)
            .normalize_states()
            .convert_numerics()
            .fill_sales_tax_by_state()
            .get_data()
        )

        self.assertAlmostEqual(cleaned.loc[0, "US Sales tax"], 7.25)
        self.assertAlmostEqual(cleaned.loc[1, "US Sales tax"], 2.43)

class TestQualityChecks(unittest.TestCase):
    def test_valid_dataframe(self):
        df = pd.DataFrame({
            'Date of sale': ['2024-01-01'],
            'Item price': [10],
            'State': ['NY'],
            'Total': [10],
            'order_id': [1]
        })
        self.assertTrue(quality_checks(df))

    def test_missing_column(self):
        df = pd.DataFrame({
            'Item price': [10],
            'State': ['NY'],
            'Total': [10],
            'order_id': [1]
        })
        self.assertFalse(quality_checks(df))

    def test_duplicate_order_id(self):
        df = pd.DataFrame({
            'Date of sale': ['2024-01-01', '2024-01-01'],
            'Item price': [10, 10],
            'State': ['NY', 'NY'],
            'Total': [10, 10],
            'order_id': [1, 1]
        })
        self.assertFalse(quality_checks(df))

    def test_negative_item_price(self):
        df = pd.DataFrame({
            'Date of sale': ['2024-01-01'],
            'Item price': [-5],
            'State': ['NY'],
            'Total': [10],
            'order_id': [1]
        })
        self.assertFalse(quality_checks(df))


if __name__ == "__main__":
    unittest.main()
