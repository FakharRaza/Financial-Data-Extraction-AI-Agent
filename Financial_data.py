import os
import json
from groq import Groq
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


def extract_financial_info(article):
    prompt = get_prompt_financial() + article
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    content = response.choices[0].message.content.replace("```json", "").replace("```", "")
    print(type(content))
    try:
        data = json.loads(content)

        return pd.DataFrame(data.items(), columns=["Measures", "Values"])
    except Exception as e:
        print(f"Error parsing JSON: {e}") # Yeh bataega ke JSON kyun nahi load hua
        return None
    
    data = pd.DataFrame({
        "Measures": ["Company Name", "Stock Symbol", "Revenue", "Net Income", "EPS"],
        "Values": ["", "", "", "", ""]
    })
    return data
 
def get_prompt_financial():
    return '''
    You are a financial data extraction assistant. Extract the following information from the provided news article:
    - Company Name
    - Stock Symbol
    - Revenue
    - Net Income
    - EPS

    Format your response STRICTLY as a valid JSON object. 
    If a value is missing, use "N/A". 
    Do not include any conversational text, explanations, or markdown code blocks (like ```json).
    
    Example format:
    {
      "Company Name": "Apple",
      "Stock Symbol": "AAPL",
      "Revenue": "$111.18 billion",
      "Net Income": "N/A",
      "EPS": "$2.01"
    }

    Article:
    '''

text = '''Apple
issued a better-than-expected revenue forecast for the current period after beating on sales and earnings in the fiscal second quarter. The stock rose about 3% in extended trading.

Sales for iPhones missed estimates for the second time in three quarters, the only significant number that came up short of expectations in Thursday’s report.

Here’s how the company did compared to analyst estimates, according to LSEG consensus.

EPS: $2.01 vs. $1.95
Revenue: $111.18 billion vs. $109.66 billion
Wall Street is also looking at these key areas: 

iPhone revenue: $56.99 billion vs $57.21 billion expected
Mac revenue: $8.4 billion vs. $8.02 billion expected
iPad revenue: $6.91 billion vs. $6.66 billion expected
Wearables, Home and Accessories revenue: $7.9 billion vs. $7.7 billion expected
Services revenue: $30.98 billion vs. $30.39 billion expected
Gross margin: 49.3% vs. 48.4% expected
Revenue climbed 17% from $95.4 billion a year earlier, Apple said. It was the first time the company faced Wall Street since the announcement last week that Tim Cook will be stepping down as CEO after 15 years on the job.

Apple said on the earnings call that revenue in the June quarter will increase between 14% and 17% from a year earlier. Analysts were expecting growth of 9.5% to $103 billion, according to LSEG.

The company’s board authorized an additional $100 billion in stock repurchases and declared a cash dividend of 27 cents per share, up 4%.

Sales of iPhones rose 22% in the quarter from a year earlier. Like other consumer electronics companies and device makers, Apple faces supply chain constraints, largely due to the global memory shortage that’s being driven by soaring artificial intelligence demand. Meta
 and Microsoft
 said Wednesday that higher memory prices contributed to their increased capital expenditures forecasts for the year.

'''
extract_financial_info(text)