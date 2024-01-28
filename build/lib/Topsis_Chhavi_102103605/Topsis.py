import sys
import pandas as pd
import os

class tp(object):
    def symbol_to_int(impact_symbol):
        # Map the impact symbols to integer values
        if impact_symbol == '+':
            return 1
        elif impact_symbol == '-':
            return -1
        else:
            raise ValueError(f"Invalid impact symbol: {impact_symbol}")
        
    def topsis(data,weights,impact):
        #Step 1
        #removing first column that's usually the name of modes/criteria
        df=data.drop(data.columns[0],axis=1)
        
        #Step2
        #check for any categorical columns
        categorical_columns = df.select_dtypes(include=['object']).columns
        
        # if yes, Convert categorical columns to numeric using cat.codes
        df[categorical_columns] = df[categorical_columns].apply(lambda col: col.astype('category').cat.codes)
        
        #Step 3
        #Calculate root of square of sum for each column
        rss=[]
        for j in range(0,df.shape[1]):
            l=[]
            for i in range(0,df.shape[0]):
                l.append(df.iloc[i,j]**2)
            rss.append((sum(l))**0.5)
        
        #Step 4
        #Calculate normalized performance values
        for i in range(0,df.shape[1]):
            for j in range(0,df.shape[0]):
                df.iloc[j,i]=df.iloc[j,i]/rss[i]
        
        #Step 5
        #Calculate weighted normalised decision matrix
        for i in range(0,df.shape[1]):
            for j in range(0,df.shape[0]):
                df.iloc[j,i]=df.iloc[j,i]/weights[i]
        
        #Step 6
        #Extract ideal best and ideal worst for each column according to impact
        ideal_best=[]
        ideal_worst=[]
        for i in range(0,df.shape[1]):
                if impact[i] == 1:
                    ideal_best.append(max(df.iloc[:,i]))
                    ideal_worst.append(min(df.iloc[:,i]))
                elif impact[i] == -1:
                    ideal_best.append(min(df.iloc[:,i]))
                    ideal_worst.append(max(df.iloc[:,i]))
        
        #Step 7
        #Calculate euclidean distance for both ideal best and ideal worst value
        Sp=[]
        Sn=[]
        for i in range(0,df.shape[0]):
            l1=[]
            l2=[]
            for j in range(0,df.shape[1]):
                l1.append((df.iloc[i,j]-ideal_best[j])**2)
                l2.append((df.iloc[i,j]-ideal_worst[j])**2)
            Sp.append(sum(l1)**0.5)
            Sn.append(sum(l2)**0.5)
        
        #Step 8
        #Calculate performance score
        p=[]
        for i in range(0,len(Sp)):
            p.append(Sn[i]/(Sn[i]+Sp[i]))
        
        #Step 9
        #Create DataFrame
        df_new=pd.DataFrame(data)
        df_new['Performance Score']=p
        
        #Step 10
        #Calculate Rank based on performance score and add it to the dataframe
        df_new['Rank'] = df_new['Performance Score'].rank(ascending=False)
        
        return df_new

    def convert_to_csv(input_file):
        try:
            # Check if the input file has an XLSX extension
            if input_file.lower().endswith('.xlsx'):
                # Read the Excel file into a Pandas DataFrame
                data = pd.read_excel(input_file)

                # Create a new CSV file based on the input file name
                output_file = os.path.splitext(input_file)[0] + '.csv'

                # Write the DataFrame to the new CSV file
                data.to_csv(output_file, index=False)

                print(f"Conversion successful: {input_file} -> {output_file}")
                return output_file
            elif input_file.lower().endswith('.csv'):
                print(f"File is already in CSV format: {input_file}")
                return input_file
            else:
                print(f"Error: Unsupported file format for {input_file}")

        except Exception as e:
            print(f"Error during conversion: {e}")
            sys.exit(1)

#cmd Implementation

if __name__ == "__main__":
    # Check if enough command-line arguments are provided
    if len(sys.argv) < 5:
        print("Usage: python 102103605.py <file_path> <weights> <impacts>")
        sys.exit(1)

    # Read file path, weights, and impacts from command-line arguments
    input_file_path = sys.argv[1]
    file_path=tp.convert_to_csv(input_file_path)
    weights = list(map(float, sys.argv[2].split(',')))
    impacts = sys.argv[3].split(',')
    impacts_int = [tp.symbol_to_int(symbol) for symbol in impacts]
    output_file_path = sys.argv[4]

    try:
        # Load dataset from file (CSV or XLSX)
        if file_path.endswith('.csv'):
            data = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            data = pd.read_excel(file_path)
        else:
            print(f"Error: Unsupported file format for {file_path}")
            sys.exit(1)


        # Check if weights and impacts have the same length as the number of columns in the matrix
        if len(weights) != data.shape[1]-1 or len(impacts_int) != data.shape[1]-1:
            print(f"Error: Number of weights and impacts must match the number of columns in {file_path}")
            sys.exit(1)

        # Perform TOPSIS analysis
        result_dataframe = tp.topsis(data, weights, impacts_int)

        # Save the result DataFrame to a CSV file
        result_dataframe.to_csv(output_file_path, index=False)

        print(f"TOPSIS result saved to {output_file_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        sys.exit(1)
