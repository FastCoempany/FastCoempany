import openai

# Your OpenAI API key
openai.api_key = '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'

urls = ["https://enterprise-fiverr-com.translate.goog/independent-contractors-taxes/form-1042-s/",
"https://enterprise.fiverr.com/ads.txt",
"https://enterprise.fiverr.com/agencies/agencies-thank-you/",
"https://enterprise.fiverr.com/blog/category/compliance/",
"https://enterprise.fiverr.com/blog/changing-scope-of-talent-management/",
"https://enterprise.fiverr.com/blog/employee-misclassification-penalties/#",
"https://enterprise.fiverr.com/blog/external-workforce-management/",
"https://enterprise.fiverr.com/blog/full-time-equivalent/",
"https://enterprise.fiverr.com/blog/skill-gaps-examples/",
"https://enterprise.fiverr.com/blog/thinking-about-staff-augmentation/",
"https://enterprise.fiverr.com/blog/what-is-global-compliance/",
"https://enterprise.fiverr.com/california-assembly-bill-5-ab5/",
"https://enterprise.fiverr.com/california-assembly-bill-5-ab5/ab5-exemptions/",
"https://enterprise.fiverr.com/case-studies/how-scale-ai-upped-the-tempo-by-simplifying-the-process-of-onboarding-freelancers/",
"https://enterprise.fiverr.com/case-studies/how-slt-consulting-saves-20-hours-a-month-and-went-from-5-tools-to-1-to-manage-freelancers/",
"https://enterprise.fiverr.com/compliance-management/",
"https://enterprise.fiverr.com/global-payroll-guide/",
"https://enterprise.fiverr.com/how-to-pay-independent-contractors/aml-check/",
"https://enterprise.fiverr.com/hr/",
"https://enterprise.fiverr.com/independent-contractor-agreement/",
"https://enterprise.fiverr.com/independent-contractor-agreement/consulting-agreement/",
"https://enterprise.fiverr.com/independent-contractors-taxes/1099-k-requirements/",
"https://enterprise.fiverr.com/independent-contractors-taxes/1099-nec-vs-1099-misc/",
"https://enterprise.fiverr.com/independent-contractors-taxes/form-1042-s/",
"https://enterprise.fiverr.com/legal/",
"https://enterprise.fiverr.com/lp/vubiquity/",
"https://enterprise.fiverr.com/my-talent-portal/",
"https://enterprise.fiverr.com/thank-you-contact-us/",
"https://enterprise.fiverr.com/webinars/get-your-projects-moving-faster-with-our-hiring-service/",
"https://enterprise.fiverr.com/workforce-management/",
"https://meetings.hubspot.com/antaeus-coe/demo-meeting-with-antaeus-",
"http://enterprise.fiverr.com/blog/pay-freelancers-overseas/",]

def generate_description_and_opinion(url):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Given the URL: {url}, please provide a brief description and opinion about its content.",
        max_tokens=100
    )

    return response.choices[0].text.strip()

# File where the results will be saved
with open("output_descriptions.txt", "w") as file:
    for url in urls:
        result = generate_description_and_opinion(url)
        file.write(f"URL: {url}\n{result}\n\n")

print(f"Descriptions saved to output_descriptions.txt")






