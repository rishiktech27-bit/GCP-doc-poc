import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
import json
import fitz, re


pdf_path = "C:\\Users\\Rishik\\Downloads\\Application form re.pdf"

# def upload_file(file_path):
#     up




def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    given_list= []

    for page_num in doc:
        page = doc[page_num]
        text += page.get_text()
        given_list.append(text)
    given_account = text.split('/n')
    return text, given_list, given_account   # "text", "blocks", "words", "json" also available
        
def loan_underwriting(credit_score, loan_amount, months, dti, annual_income):
    """
    Business rule-based loan underwriting.
    
    Parameters:
        credit_score (int)   : Applicant's credit score
        loan_amount (float)  : Requested loan amount
        months (int)         : Loan term in months
        dti (float)          : Debt-to-Income ratio (in %)
        annual_income (float): Applicant's annual income
        
    Returns:
        dict : decision + reason
    """
    
    # Rule 1: Credit score threshold
    if credit_score < 600:
        return {"decision": "Reject", "reason": "Credit score too low"}
    
    # Rule 2: Maximum DTI allowed
    if dti > 40:   # e.g., >40% debt-to-income ratio
        return {"decision": "Reject", "reason": "High debt-to-income ratio"}
    
    # Rule 3: Loan-to-income ratio
    if loan_amount > annual_income * 5:   # cannot borrow more than 5x income
        return {"decision": "Reject", "reason": "Loan amount too high relative to income"}
    
    # Rule 4: Maximum loan term
    if months > 360:   # 30 years
        return {"decision": "Reject", "reason": "Loan term too long"}
    
    # Rule 5: Minimum income requirement
    if annual_income < 20000:
        return {"decision": "Reject", "reason": "Income too low"}
    
    # If all rules pass → Approve
    return {"decision": "Approve", "reason": "Meets underwriting criteria"}

def iter_over_the_list(given_account):
    for item in given_account:
        if "Credit Score (Approximate):"in item:
            print("yes", item)
            givenitem = item.split("__")
            new_list =[it for it in givenitem if it != ""]
            creditamount = int(new_list[1])
        if "Loan Amount:" in item:
            givenitem = item.split("__")
            new_list =[it for it in givenitem if it != ""]
            loanamount = int(new_list[1])
        if "Annual Income:" in item:
            givenitem = item.split("__")
            new_list =[it for it in givenitem if it != ""]
            annualincome = int(new_list[1])
        if "Total Monthly Debt Payments:" in item:
            givenitem = item.split("__")
            new_list =[it for it in givenitem if it != ""]
            dtiamount = int(new_list[1])
            monthly_income = int(amount)/12
            totalmonthlydebt = int(dtiamount)
            dti = (totalmonthlydebt/monthly_income)*100
        if "(✔) 36" in item or "(✔) 60" in item or "(✔) 12" in item or "(✔) 24" in item or "(✔) 48" in item :
            givenitem = item.split(" ")
            new_list =[it for it in givenitem if it != ""]
            month = int(new_list[1])
    return creditamount, loanamount, month, amount, dti

def underwriting_decision():
    try:
        application, data_extracted, given_account =  extract_text("C:\\Users\\Rishik\\Downloads\\Application form re.pdf")
        creditamount, loanamount, month, amount, dti = iter_over_the_list(data_extracted)
        decision = loan_underwriting(creditamount, loanamount, month, dti, amount)
        return decision
    except Exception as err:
        import traceback
        traceback.print_exc()
        print(err)







# def get_weather(city: str) -> dict:
#     """Retrieves the current weather report for a specified city.

#     Args:
#         city (str): The name of the city for which to retrieve the weather report.

#     Returns:
#         dict: status and result or error msg.
#     """
#     if city.lower() == "new york":
#         return {
#             "status": "success",
#             "report": (
#                 "The weather in New York is sunny with a temperature of 25 degrees"
#                 " Celsius (77 degrees Fahrenheit)."
#             ),
#         }
#     else:
#         return {
#             "status": "error",
#             "error_message": f"Weather information for '{city}' is not available.",
#         }





# def get_current_time(city: str) -> dict:
#     """Returns the current time in a specified city.

#     Args:
#         city (str): The name of the city for which to retrieve the current time.

#     Returns:
#         dict: status and result or error msg.
#     """

#     if city.lower() == "new york":
#         tz_identifier = "America/New_York"
#     else:
#         return {
#             "status": "error",
#             "error_message": (
#                 f"Sorry, I don't have timezone information for {city}."
#             ),
#         }

#     tz = ZoneInfo(tz_identifier)
#     now = datetime.datetime.now(tz)
#     report = (
#         f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
#     )
#     return {"status": "success", "report": report}


root_agent = Agent(
    name="loan_underwriting_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to answer questions about the loan approved or not."
    ),
    instruction=(
        "call the underwriting decision tool return the response"
    ),
    tools=[underwriting_decision],
)

