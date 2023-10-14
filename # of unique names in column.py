import openpyxl

# Set the path to the Excel file
file_path = "/Users/antaeus.coe/Desktop/dbase_slack_alerts/Parent scraped file for dbase alerts.xlsx"

# Load the workbook and select the active sheet
wb = openpyxl.load_workbook(file_path)
sheet = wb.active

# Extract all names from column A
names = [cell.value for cell in sheet['A'] if cell.value]

# Convert to a set to get unique names and count them
unique_names_count = len(set(names))

print(f"There are {unique_names_count} unique names in column A.")

# Close the workbook
wb.close()
