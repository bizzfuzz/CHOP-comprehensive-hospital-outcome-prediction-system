class df_helper:
    def column_decimal_rounding(self, df, column, decimals):
        df[column] = round(df[column], decimals)
        return df
    
    def convert_inches_to_meters(self, df, column, decimals):
        df[column] = df[column].astype(float)/39.3700787
        return self.column_decimal_rounding(df, column, decimals)

    def convert_lbs_to_kg(self, df, column, decimals):
        df[column] = df[column].astype(float)*0.453592
        return self.column_decimal_rounding(df, column, decimals)
    
    def drop_columns(self, df, columns):
        df.drop(columns=columns, axis=1, inplace=True)
        return df
    def rename_column(self, df, old_col, new_col):
        df.rename(columns={old_col: new_col}, inplace=True)
        return df
    
    def rename_columns(self, df, columns_dict):
        df.rename(columns=columns_dict, inplace=True)
        return df
    
    def filter_dataframe(self, df, column, value):
        return df[df[column] == value]