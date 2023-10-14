import openai

# Initialize OpenAI API
openai.api_key = "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"  # Replace with your actual API key

urls = ["https://enterprise-fiverr-com.translate.goog/independent-contractors-taxes/form-1042-s/",
"https://enterprise.fiverr.com/",
"https://enterprise.fiverr.com/#popmake-5233",
"https://enterprise.fiverr.com/ads.txt",
"https://enterprise.fiverr.com/agencies/",
"https://enterprise.fiverr.com/agencies/agencies-thank-you/",
"https://enterprise.fiverr.com/blog/",
"https://enterprise.fiverr.com/blog/7-things-you-need-to-know-about-outsourcing/",
"https://enterprise.fiverr.com/blog/73-of-freelancers-will-turn-to-freelancing-in-2023/",
"https://enterprise.fiverr.com/blog/building-out-a-talent-pool-of-freelancers/",
"https://enterprise.fiverr.com/blog/category/compliance/"]

def get_message_for_url(url, max_retries=3):
    retries = 0
    while retries < max_retries:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt = f"We noticed you recently visited a page related to '{url.split('/')[-2]}'. Given this specific topic and considering Fiverr Enterprise's focus on providing solutions for large enterprises, craft a concise and engaging message tailored for our customers about the specific value or offering this URL likely presents.",
            max_tokens=100
        )
        
        message = response.choices[0].text.strip()
        if message:
            break
        else:
            retries += 1
    
    # Append the fixed part of the message
    message += "\n\nMy initial conversations are kept to 15 minutes. If you're interested, we can [start with a virtual 30 seconds here right now](https://fiverrent.wistia.com/medias/tpqf6eb18f) and then decide if a 15-min chat would be beneficial.\n\n\n\n.#howboutahighfiverr#."
    
    return message

# File where the results will be saved
with open("output_messages.txt", "w") as file:
    for url in urls:
        message = get_message_for_url(url)
        file.write(message + "\n\n\n\n")





