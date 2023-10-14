import twarc
import pandas as pd

# Set up twarc
t = twarc.Twarc2(bearer_token="AAAAAAAAAAAAAAAAAAAAAA8GqQEAAAAAMiwwED%2B93Ij2InPC1ocNGqqT8zI%3DtTryCvEyvm82Eyp7zbC37QMAQIFKGkJ7R5dBM0tY3H7sCKBsV3")

# Define the search query
query = "freelancer OR freelance marketplace OR IR35 compliance OR contractor payments OR worker classification OR enterprise independent contractors OR freelancer marketplace OR independent contractor OR contingent workforce OR non-W2 worker OR contingent worker OR vendor management OR compliance management OR requisition management OR procurement platforms OR freelancer management OR MSP OR sourcing freelancers OR direct sourcing OR indirect sourcing OR staffing vendors OR EORs OR vendor selection technology OR consolidated invoice  OR legal and tax compliance"

# Fetch tweets
tweets = list(t.search_recent(query, tweet_fields="text,created_at", max_results=100))

# Process and store tweets
tweet_data = [[tweet['id'], tweet['text'], tweet['created_at']] for tweet in tweets]

# Convert to DataFrame and save to Excel
df = pd.DataFrame(tweet_data, columns=['Tweet_ID', 'Text', 'Date'])
df.to_excel("/Users/antaeus.coe/Desktop/dbase_slack_alerts/non2_tweets_output_twarc_simplified.xlsx", index=False)

