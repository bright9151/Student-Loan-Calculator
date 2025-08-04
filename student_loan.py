import numpy as np # for numerical operations
import pandas as pd # for data manipulation and analysis
import matplotlib.pyplot as plt # for data visualization
import streamlit as st # for building web applications


class StudentLoanCalculator: # this is used to create a student loan calculator class
    def __init__(self, loan_amount, annual_rate, years): # constructor to initialize the loan amount, annual interest rate, and loan term in years
        self.loan_amount = loan_amount # principal amount of the loan
        self.annual_rate = annual_rate / 100 # convert percentage to decimal
        self.years = years # term of the loan in years
        self.monthly_rate = self.annual_rate / 12 # monthly interest rate
        self.months = years * 12 # total number of months for the loan
        
    def calculate_monthly_payment(self): # method to calculate the monthly payment
        r = self.monthly_rate # monthly interest rate
        n = self.months # total number of payments
        p = self.loan_amount
        
        if r == 0: # if the interest rate is zero
            return p / n # return the principal divided by the number of payments
        
        M = p * (r * (1 + r) ** n) / ((1 + r) ** n - 1) # formula for monthly payment
        return M # return the monthly payment amount
    
    def build_amortization_schedule(self): # method to build the amortization schedule
        balance = self.loan_amount # initial balance is the loan amount
        monthly_payment = self.calculate_monthly_payment() # calculate the monthly payment
        r = self.monthly_rate # monthly interest rate
        
        schedule = [] # list to hold the amortization schedule
        
        for month in range(1, self.months + 1): # iterate over each month
            interest = balance * r # calculate interest for the month
            principal = monthly_payment - interest # calculate principal for the month
            balance -= principal # reduce the balance by the principal paid
            balance = max(balance, 0) # ensure the balance is non-negative
            
            schedule.append({ # append the month data to the schedule
                "Month": month, # month number
                "Payment": round(monthly_payment, 2), # monthly payment amount
                "Interest": round(interest, 2), # interest paid for the month
                "Principal": round(principal, 2), # principal paid for the month
                "Balance": round(balance, 2) # remaining balance after payment
            })
        
        return pd.DataFrame(schedule) # return the amortization schedule as a pandas DataFrame

# Streamlit User Interface
st.set_page_config(page_title="Student Loan Calculator", layout = "centered") # set the title and layout of the User Interface
st.title("Student Loan Calculator") # add a title to the User

# Sidebar Inputs
st.sidebar.header("Loan Details") # add a header to the sidebar
loan_amount = st.sidebar.number_input("Loan Amount ($)", value=1000000, step=50000) # input box for loan amount
interest_rate = st.sidebar.slider("Annual Interest Rate (%)", 0.0, 25.0, 10.0, step=0.5) # slider for annual
loan_term = st.sidebar.slider("Loan Term (Years)", 1, 30, 50) # slider for loan terms

# Run Calculator
calculator = StudentLoanCalculator(loan_amount, interest_rate, loan_term) # create an instance of the StudentLoanCalculator class
monthly_payment = calculator.calculate_monthly_payment() # calculate the monthly payment
schedule_df = calculator.build_amortization_schedule() # build the amortization schedule

# Summary
st.header("Loan Summary") # add a header to the User
st.write(f"**Monthly Payment:** ${monthly_payment:.2f}") # display the monthly payment
st.write(f"**Total Repayment:** ${monthly_payment * calculator.months:,.2f}") # display the total repayment
st.write(f"**Total Interest Paid:** ${(monthly_payment * calculator.months) - loan_amount:,.2f}") # display the total interest paid

# Line Chart
st.subheader("Loan Balance Over Time") # add a subheader to the User
fig, ax = plt.subplots(figsize=(10, 5)) # create a figure and axis for the line chart
ax.plot(schedule_df["Month"], schedule_df["Balance"], color ='blue', linewidth = 2) # plot the balance over time
ax.set_xlabel("Month") # set the x-axis label
ax.set_ylabel("Balance ($)") # set the y-axis label
ax.set_title("Remaining Loan Balance") # set the title
ax.grid(True) # add a grid
st.pyplot(fig) # display the line chart

# Show Table
st.subheader("Amortization Schedule (First 12 Months)") # add a subheader to the User
st.dataframe(schedule_df.head(12)) # display the first 12 rows of the amortization schedule

# Optional Download
csv = schedule_df.to_csv(index=False).encode('utf-8') # convert the DataFrame to a CSV file
st.download_button("Download Full Schedule as CSV", data=csv, file_name="loan_schedule.csv", mime="text/csv") # Create the file Download Button
