import pandas as pd
import openai

# Initialize OpenAI key
openai.api_key = "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"

# Load data
data = pd.read_excel('/Users/antaeus.coe/Desktop/dbase_slack_alerts/Organized Alertsnil.xlsx')
unique_urls = data['Unique URL'].unique()

# Function to generate a message for an executive based on URL
def generate_message_for_executive(url):
    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt=f"Generate a punchy, professional email body message (under 60 words) for an executive interested in the content at this URL: {url}",
            max_tokens=90  # Roughly 60 words
        )
        return response.choices[0].text.strip()
    except openai.error.OpenAIApiError:
        return "Failed to generate message."

# Lists to hold unique URLs and their messages
url_list = []
messages = []

# For each unique URL, generate message
for url in unique_urls:
    message = generate_message_for_executive(url)
    url_list.append(url)
    messages.append(message)

# Create a DataFrame with URLs and messages
output_data = pd.DataFrame({
    'Unique URL': url_list,
    'Generated Messages': messages
})

# Save to Excel
output_data.to_excel('/Users/antaeus.coe/Desktop/dbase_slack_alerts/Unique_URL_2.xlsx', index=False)



