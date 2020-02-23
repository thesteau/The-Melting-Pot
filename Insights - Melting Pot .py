"""
The Insights Melting Pot by Steven Au.
This script ultimately replaces the excel file that was initially used to convert insights to a usable file also created by Steven Au.

Dataset metlter to automate data transformation
"""
import pandas as pd

# Global Var- for tracking purposes
the_encode = 'utf_8_sig'

def file_import():
    """This is a proprietary function. We are importing the raw download from Insights.
    HOWEVER, if the service is to change, this file reader function will read the entire file and SKIP the first row.
    If yopu need to skip any more rows or not skip a row, simply change the number in the argument.
    
    Note: We are trying to get to header row. THe first row originally did not have a header row.
    
    Returns:
        df: The read excel dataframe, first sheet only!
        the_file_name: THe file path with the extension name.
    """
    the_file_name = input("xls or xlsx Filepath with name (You can drag and drop, remove the quote marks please!):\n> ")
    while 1:
        try:
            df = pd.read_excel(the_file_name,skiprows=1,encoding=the_encode)
        except:
            print("You've probably didn't delete the quotes or this is not an excel file.")
            print("You can delete the quotes by editing the file name")
            continue
        return df, the_file_name

def value_capture(dataframe, reg_calltype):
    """This function primarily captures the header column names

    Parameters:
        dataframe: The dataframe that we are using
        reg_calltype: Has to be entered to the function as 'Units[)]' OR 'Revenue[)]' as a variable
    
    Returns:
        value_capturing: Returns the filtered dataframe columns according to either Units or Revenue
    """
    value_capturing = dataframe.filter(regex=reg_calltype)
    return value_capturing

def melting_pot(the_dataframe, values_ID, var_calltype):
    """Meltss the corresponding dataframes to the values that are usable
    This function is proprietary to get the corresponding column values that we need.
    Note that it is well known that these values may change, even to the point of renamed or eliminated.
    Since you are reading the source code, you can just modify the id_vars to reflect the appropriate columns.

    Parameters:
        the_dataframe: The raw pandas dataframe used.
        values_ID: These are all from the value_capture function for its respective columns (We're only using the names)
        var_calltype: needs to be specfied to either: Units OR Revenue

    Returns:
        melted: The dataframe melted per the original. Retains conditionally based on the parameters.
    
    Note: 
        var_name "Partners" is basically the Partner names of the evaluating column values.
        That is, we have thrown all the column names together from the initial file.
        And then we have renamed the columns we have captured as Partners.
    """
    melted = the_dataframe.melt(id_vars= ["eISBN13","Series","Volume","Currency"],
                                var_name = "Partners",
                                value_vars = values_ID,
                                value_name = var_calltype
                                )
    return melted

def melting_process(melty, malty):
    """One time use melter using the two dataframes

    Parameters:
        melty: Uses dataframe A to create the initial dataframe for concatenation
        malty: Uses dataframe B to create the secondary dataframe to be concatenated

    Procedure:
        Concats the two dataframes and then drops the duplicated column names.
        With this new dataframe, drops all Revenue values that have a 0 (Keep all that do not equal 0)
        Finally, replace all Partner values that have a "Units" in the name.

    Returns:
        The new pandas dataframe.    
    """
    fin_melted = pd.concat([melty, malty],axis=1)
    fin_melted = fin_melted.loc[:,~fin_melted.columns.duplicated()]
    fin_melted = fin_melted[fin_melted.Revenue != 0]
    fin_melted['Partners'] = fin_melted['Partners'].str.replace(' [(]Units[)]','')
    return fin_melted

def exporting_porcess(fin_melted, the_filename):
    """Exporting Process - the final step.
    
    Parameters:
        fin_melted: The final melted and concatenated dataframe.
        the_filename: From the original input, we are going to create the file name accordingly.
    
    Variables:
        file_extension_name: This is an intermediary variable with the filename string split into a list.
        path_name: This is the raw path. We're using file_extension_name variable to get the file name with extension.
                    With this extension (The last value in the list), we are going to remove it to get the raw path.
    
    Final Procedure:
        Use the melted dataframe, convert this to a CSV.
            This uses the path_name we've extracted. Append the converted.csv and remove the index number column created by Pandas.
    """
    file_extension_name = the_filename.split(".")
    path_name = the_filename.strip(file_extension_name[-1])
    print("The file path and name is as followed:\n"+path_name+"-converted.csv")
    fin_melted.to_csv(path_name+"-converted.csv",index=None,encoding=the_encode)

def main():
    """Main program
    Process:
        1. File Import
        2. Two Dataframes created from the import: Unit and Revenue
        3. Melt each dataframe accordingly
        4. Main processing melting pot procedure
        5. Export the file in CSV format (Due to the limitations of Excel)
    """
    ### Step 1
    insights_file, the_filename = file_import()
    print("Step 1 completed.")

    ### Step 2
    units_type = 'Units[)]'
    revenue_type = 'Revenue[)]'
    units = value_capture(insights_file,units_type)
    revenue = value_capture(insights_file,revenue_type)
    print("Step 2 completed.")

    ### Step 3
    val_name_u = "Units"
    val_name_r = "Revenue"
    melty = melting_pot(insights_file, units, val_name_u)
    malty = melting_pot(insights_file, revenue, val_name_r)
    print("Step 3 completed.")

    ### Step 4
    fatal_frame = melting_process(melty, malty)
    print("Step 4 completed.")

    ### Step 5
    exporting_porcess(fatal_frame, the_filename)

print("Insights Data conversion")
main()
input("Fully Completed. Press any key to end.")
