from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import csv
import base64
import spacy
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# Initialize the Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    creds = None
    if creds and not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('/Users/antaeus.coe/Desktop/dbase_slack_alerts/credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    return build('gmail', 'v1', credentials=creds)

nlp = spacy.load("en_core_web_sm")

def add_links_to_noun_phrases(text, url):
    doc = nlp(text)
    hyperlinked = False
    for np in doc.noun_chunks:
        if not hyperlinked:
            text = text.replace(np.text, f"<a href='{url}'>{np.text}</a>")
            hyperlinked = True
    return text

# Testing the add_links_to_noun_phrases function
test_text = "This is a sample description with multiple noun phrases."
test_url = "https://example.com"
result = add_links_to_noun_phrases(test_text, test_url)
print(result)

service = get_gmail_service()

counter = 0
start_sending = False

with open('/Users/antaeus.coe/Desktop/dbase_slack_alerts/finalGMAIL_procurementpeople_dbase.csv', 'r', encoding='utf-8-sig') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    print(csv_reader.fieldnames)
    companies_to_urls = {}

    for row in csv_reader:
        company = row['Company']
        url = row['Url the person visited']

        if company in companies_to_urls:
            companies_to_urls[company].append(url)
        else:
            companies_to_urls[company] = [url]

    csv_file.seek(0)  # Reset the file pointer to the start of the file

    for row in csv_reader:
        email = row['Email']

        company = row['Company']
        if company in companies_to_urls:
            visited_urls = companies_to_urls[company]
            # If the company has multiple URLs and the 'enterprise.fiverr.com' URL exists in the list, we remove it
            if len(visited_urls) > 1 and "enterprise.fiverr.com" in visited_urls:
                visited_urls.remove("enterprise.fiverr.com")
            selected_url = random.choice(visited_urls)
        else:
            # Skip this iteration if company is not in the dictionary
            continue

        # Debug prints to verify URL Description transformation
        print(f"URL Description before linking: {row['Demand Base URL descriptions']}")
        url_description = add_links_to_noun_phrases(row['Demand Base URL descriptions'], selected_url)
        print(f"URL Description after linking: {url_description}")

        if email == "john_konsler@aztecamilling.com":
            start_sending = True

        if email == "zakaria.sallak@novartis.com":
            break

        if start_sending:
            try:
                first_name = row['First Name']
                last_name = row['Last Name']
                title = row['Title']
                company = row['Company']

                visited_urls = companies_to_urls[company]

                # If the company has multiple URLs and the 'enterprise.fiverr.com' URL exists in the list, we remove it
                if len(visited_urls) > 1 and "enterprise.fiverr.com" in visited_urls:
                    visited_urls.remove("enterprise.fiverr.com")

                selected_url = random.choice(visited_urls)

                print(f"Sending email to {email}")

                first_paragraph = f"{url_description}"
                second_paragraph = "My initial conversations are kept to 15 minutes. If you'd like - we can even start with a <a href='https://fiverrent.wistia.com/medias/tpqf6eb18f'>virtual 30 seconds here right now</a> - and you can decide for yourself at the end if you'd like to have the 15min chat live."

                signature_html = '''
                <br><br>
                <table>
                    <tr>
                        <td rowspan="3"><img src="cid:image1" alt="Fiverr Logo" style="width: 50px;"></td>
                        <td>
                            <strong>Antaeus Coe</strong><br>
                            Senior Enterprise Account Executive, Fiverr Enterprise<br>
                            <a href="https://enterprise.fiverr.com">enterprise.fiverr.com</a> | <a href="https://blog.fiverr.com">Visit our blog</a>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <a href="https://www.linkedin.com/company/fiverrenterprise/mycompany/"><img src="cid:image2" alt="LinkedIn Logo" style="width:25px"></a>
                        </td>
                    </tr>
                </table>
                <br><br>
                #.howboutahighfiverr.#
                '''

                email_body = f"Hello {first_name or last_name},<br><br>"
                email_body += f"{url_description}<br><br>"
                email_body += f"{second_paragraph}{signature_html}"

                msg = MIMEMultipart('related')
                msg_alternative = MIMEMultipart('alternative')
                msg.attach(msg_alternative)
                msg_text = MIMEText(email_body, 'html')
                msg_alternative.attach(msg_text)

                with open("/Users/antaeus.coe/Desktop/dbase_slack_alerts/antaeussignature.gif", 'rb') as fp:
                    img = MIMEImage(fp.read())
                    img.add_header('Content-ID', '<image1>')
                    msg.attach(img)

                with open("/Users/antaeus.coe/Desktop/dbase_slack_alerts/linkedinhyperlink.png", 'rb') as fp:
                    img = MIMEImage(fp.read())
                    img.add_header('Content-ID', '<image2>')
                    msg.attach(img)

                # Changed this to only send test emails to your address
                msg['to'] = 'antaeus.coe@stoketalent.com'
                msg['from'] = 'antaeus.coe@stoketalent.com'
                msg['subject'] = "You've been watching us... "

                raw_message = base64.urlsafe_b64encode(msg.as_string().encode("utf-8"))
                raw_message = raw_message.decode("utf-8")

                message = service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
                print(f"Test email sent to {email}.")
                counter += 1
            except Exception as e:
                print(f"Failed to send email to {email}. Reason: {str(e)}")
            except KeyError:
                print(f"Error processing description for {email}. Skipping this email.")
                continue


            

