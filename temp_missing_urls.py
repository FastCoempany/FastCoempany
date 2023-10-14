import pandas as pd

# File path
file_path = "/Users/antaeus.coe/Desktop/dbase_slack_alerts/organized again alerts.xlsx"

# Load the Excel file into a DataFrame
df = pd.read_excel(file_path, engine='openpyxl')

# Check if the required columns exist
if 'Web pages read' in df.columns and 'Company' in df.columns and 'Url Unique' in df.columns:
    # Create an empty list to hold the result for 'companies and their URLs' column
    result = []

    # Iterate through each row
    for unique_url in df['Url Unique']:
        # Find all rows in df where the 'Web pages read' is equal to the unique_url
        matched_rows = df[df['Web pages read'] == unique_url]
        # Get the 'Company' values for these rows and join them with commas
        companies = ", ".join(matched_rows['Company'].unique())
        result.append(companies)

    # Assign the result list to the 'companies and their URLs' column
    df['companies and their URLs'] = result

    # Save the DataFrame back to the Excel file
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer:
        df.to_excel(writer, sheet_name='combined description', index=False)

    print("Process complete. The 'companies and their URLs' column has been updated.")
else:
    print("The loaded sheet doesn't have the required columns. Please double-check the file and the sheet names.")
