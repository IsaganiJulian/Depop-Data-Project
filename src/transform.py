import pandas as pd

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
class DataCleaner:
    """ Initialize class"""
    def __init__(self, df):
        self.df = df

    def drop_sensitive(self, columns=['Name', 'Address Line 1', 'Address Line 2']):
        """ Drop sensitive columns"""
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
                self.df[col] = pd.to_numeric(self.df[col].str.replace('[\$,]', '', regex=True), errors='coerce')
        print("Finished converting numeric columns to float.")
        return self
    
    def fill_columns_with_zero(self, columns=None):
        """ Fill columns with zero"""
        if columns is None:
            columns = ['Refunded to buyer amount', 'Fees refunded to seller', 'Boosting fee']
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
    .fill_columns_with_zero()
    .fill_missing()
    .drop_duplicates()
    .get_data()
)
    cleaned_df.to_csv("data/processed/cleaned.csv", index=False)
    print(cleaned_df.head())
