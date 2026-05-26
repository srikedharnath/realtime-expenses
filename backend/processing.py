import pandas as pd
import numpy as np

def process(files):
    # Empty list to append processed datasets 
    all_files=[]

    for file in files:
        # Reading File
        if file.filename.endswith(".xlsx"):
            df=pd.read_excel(file.file)
        else:
            df=pd.read_csv(file.file)
        
        # Dropping duplicates
        df=df.drop_duplicates()

        # Filling missing values
        for col in df.select_dtypes(include=np.number).columns:
            df[col].fillna(df[col].mean(), inplace=True)

        # Date conversion
        df['Date']=pd.to_datetime(df['Date'],format="%d-%m-%Y")

        # Handling Outliers
        cols=df.select_dtypes(exclude=['datetime','object']).columns
        for col in cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1-1.5*IQR
            upper = Q3+1.5*IQR
            df[col]=np.where(
                df[col]<lower,lower,df[col]
            )
            df[col]=np.where(
                df[col]>upper,upper,df[col]
            )
            
        # Feature Engineering
        df['day']=df['Date'].dt.day
        df['Month']=df['Date'].dt.month
        df['Year']=df['Date'].dt.year
        df.drop(columns='Date',inplace=True)
        
        df['Expense_Per_Student'] = (df['Total_Expenses']/df['Student_Count'])

        df['Utility_Expenses'] = (df['Electricity_Bill']+df['Water_Bill']+
                                        df['Internet_Charges'])
        
        df['Admission_Expenses'] = np.where(df['Month'].isin([5,6,7]),1,0)

        all_files.append(df)
    
    # Merging Datasets
    final_df=pd.concat(all_files,ignore_index=True)

    return final_df
