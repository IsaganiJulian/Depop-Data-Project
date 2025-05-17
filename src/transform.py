import pandas as pd
import uuid

# State mapping
STATE_MAP = {
        'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
    'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
    'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
    'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
    'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire',
    'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina',
    'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania',
    'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee',
    'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington',
    'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming',
    # Add full names to themselves for normalization
    'California': 'California', 'Utah': 'Utah', 'Kansas': 'Kansas', 'Washington': 'Washington'
    }     

# State sales tax
STATE_SALES_TAX = {
    'Alabama': 0.04,
    'Alaska': 0.0,
    'Arizona': 0.056,
    'Arkansas': 0.065,
    'California': 0.0725,
    'Colorado': 0.029,
    'Connecticut': 0.0635,
    'Delaware': 0.0,
    'Florida': 0.06,
    'Georgia': 0.04,
    'Hawaii': 0.04,
    'Idaho': 0.06,
    'Illinois': 0.0625,
    'Indiana': 0.07,
    'Iowa': 0.06,
    'Kansas': 0.065,
    'Kentucky': 0.06,
    'Louisiana': 0.0445,
    'Maine': 0.055,
    'Maryland': 0.06,
    'Massachusetts': 0.0625,
    'Michigan': 0.06,
    'Minnesota': 0.06875,
    'Mississippi': 0.07,
    'Missouri': 0.04225,
    'Montana': 0.0,
    'Nebraska': 0.055,
    'Nevada': 0.0685,
    'New Hampshire': 0.0,
    'New Jersey': 0.06625,
    'New Mexico': 0.05125,
    'New York': 0.04,
    'North Carolina': 0.0475,
    'North Dakota': 0.05,
    'Ohio': 0.0575,
    'Oklahoma': 0.045,
    'Oregon': 0.0,
    'Pennsylvania': 0.06,
    'Rhode Island': 0.07,
    'South Carolina': 0.06,
    'South Dakota': 0.045,
    'Tennessee': 0.07,
    'Texas': 0.0625,
    'Utah': 0.0485,
    'Vermont': 0.06,
    'Virginia': 0.043,
    'Washington': 0.065,
    'West Virginia': 0.06,
    'Wisconsin': 0.05,
    'Wyoming': 0.04
}

class DataCleaner:
    """ Initialize class"""
    def __init__(self, df):
        self.df = df

    def drop_sensitive(self):
        """ Drop sensitive columns"""
        columns=['Name', 'Buyer', 'Address Line 1', 'Address Line 2', 
                    'Estimated payout date', 'Payout arrival date'
        ]
        self.df = self.df.drop(columns = columns, errors='ignore')
        print("Finished dropping sensitive columns.")
        return self 
    
    def normalize_states(self, column='State'):
        """ List out the state's name"""
        self.df[column] = self.df[column].map(STATE_MAP).fillna(self.df[column])
        print("Finished normalizing state names.")
        return self

    def convert_dates(self):
        date_cols = [
            'Date of sale', 'Date of listing', 
            'Estimated payout date', 'Payout arrival date'
        ]
        for col in date_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
        print("Finished converting date columns to datetime.")
        return self

    def convert_numerics(self):
        numeric_cols = [
            'Item price', 'Buyer shipping cost', 'Total', 'USPS Cost', 
            'Depop fee', 'Depop Payments fee', 'Boosting fee', 
            'US Sales tax', 'Refunded to buyer amount', 'Fees refunded to seller'
        ]
        for col in numeric_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(
                    self.df[col].astype(str).str.replace('[\$,]', '', regex=True), 
                    errors='coerce')
        print("Finished converting numeric columns to float.")
        return self
    
    def fill_sales_tax_by_state(self, tax_col='US Sales tax', state_col = 'State'):
        """ 
        Fill the null values in the ' US Sales tax' column with the corresponding 
        sales tax from the STATE SALES TAX dictionary
        """
        def fill_func(row):
            if pd.isnull(row[tax_col]):
                return STATE_SALES_TAX.get(row[state_col], 0)
            else:
                return row[tax_col]
        if tax_col in self.df.columns and state_col in self.df.columns:
            self.df[tax_col] = self.df.apply(fill_func, axis =1)
        print(f"Filled missing '{tax_col}' with state sales tax rates.")
        return self
    
    def fill_columns_with_zero(self, columns=None):
        """ Fill columns with zero"""
        if columns is None:
            columns = ['Refunded to buyer amount', 'Fees refunded to seller', 
                       'Boosting fee', 'Buyer shipping cost', 'Total', 'USPS Cost', 
                       'Depop Payments fee']
        for col in columns:
            if col in self.df.columns:
                self.df[col] = self.df[col].fillna(0)
        print("Finished filling refund columns with zero")
        return self

    def fill_missing(self, value=''):
        """Fill na values"""
        self.df = self.df.fillna(value)
        print("Finished filling missing values.")
        return self
       
    def drop_duplicates(self):
        """ Drop duplicate"""
        self.df = self.df.drop_duplicates()
        print("Finished dropping duplicates.")
        return self
    
    def get_data(self):
        return self.df
    
if __name__ == "__main__":
    df = pd.read_csv("data/processed/combined.csv")
    cleaner = DataCleaner(df)
    cleaned_df = (
    cleaner
    .drop_sensitive()
    .normalize_states()
    .convert_dates()
    .convert_numerics()
    .fill_sales_tax_by_state()
    .fill_columns_with_zero()
    .fill_missing()
    .drop_duplicates()
    .get_data()
)
    # unique order ID
    cleaned_df['order_id'] = [uuid.uuid4() for _ in range(len(cleaned_df))]
    
    cleaned_df.to_csv("data/processed/cleaned.csv", index=False)
    print(cleaned_df.info())

    