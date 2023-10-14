import pandas as pd

# Define the filepath
file_path = "/Users/antaeus.coe/Desktop/dbase_slack_alerts/messagesfinal1019pm.xlsx"

# Load the Excel file
df = pd.read_excel(file_path, engine='openpyxl')

# Check if necessary columns exist in the DataFrame
if "Url for description" in df.columns and "descriptions" in df.columns:
    
    # Function to construct the message
    def construct_message(row):
        description = row['descriptions']
        
        # Check if description is string and not NaN
        if not isinstance(description, str):
            print(f"Found non-string value in 'descriptions' column: {description}")
            return ""
        
        message_part1 = ' '.join(description.split()[:80])  # Take the first 80 tokens
        
        message = message_part1 + " My initial conversations are kept to 15 minutes. If you'd like - we can even [start with a virtual 30 seconds here right now](https://fiverrent.wistia.com/medias/tpqf6eb18f) - and you can decide for yourself at the end if you'd like to have the 15min chat live."
        return message

    # Apply the function to each row
    df['Message'] = df.apply(construct_message, axis=1)

    # Save the output
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer:
        output_df = df[['Url for description', 'Message']]
        output_df.to_excel(writer, sheet_name="output messages", index=False)

else:
    print("The loaded sheet doesn't have the required columns. Please double-check the file and the sheet names.")


