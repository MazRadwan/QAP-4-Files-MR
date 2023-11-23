#This is a program that generates a receipt for a customer of One Stop Insurance , it takes 
# in the customer's information and calculates the premium and total cost of the insurance

#Author : Maz Radwan
# Date: Nov 18, 2023
#QAP 4

import datetime

# Default value constants
NEXT_POLICY_NUMBER = 1943 # Next policy number will display as 1944
BASIC_PREMIUM = 869.00
DISCOUNT_ADDITIONAL_CAR = 0.25
EXTRA_LIABILITY_COST = 130.00
GLASS_COVERAGE_COST = 86.00
LOANER_CAR_COST = 58.00
HST_RATE = 0.15
PROCESSING_FEE = 39.99

# Valid provinces and payment methods
VALID_PROVINCES = ["ON", "QC", "NS", "NB", "MB", "BC", "PE", "SK", "AB", "NL"]
VALID_PAYMENT_METHODS = ["Full", "Monthly", "Down Pay"]

# Functions to validate province and payment method
def validate_province(province):
    return province.upper() in VALID_PROVINCES

def validate_payment_method(method):
    return method.title() in VALID_PAYMENT_METHODS

def calculate_premium(num_cars, extra_liability, glass_coverage, loaner_car):
    total_premium = BASIC_PREMIUM
    if num_cars > 1:
        total_premium += (num_cars - 1) * BASIC_PREMIUM * (1 - DISCOUNT_ADDITIONAL_CAR)
    if extra_liability == 'Y':
        total_premium += EXTRA_LIABILITY_COST * num_cars
    if glass_coverage == 'Y':
        total_premium += GLASS_COVERAGE_COST * num_cars
    if loaner_car == 'Y':
        total_premium += LOANER_CAR_COST * num_cars
    return total_premium

def calculate_total_cost(premium, down_payment=0):
    hst = premium * HST_RATE
    total_cost = premium + hst
    if down_payment > 0:
        total_cost -= down_payment
    return total_cost, hst

def calculate_monthly_payments(total_cost, down_payment):
    adjusted_cost = total_cost + PROCESSING_FEE
    if down_payment > 0:
        adjusted_cost -= down_payment
    return adjusted_cost / 8


# Functions to format values
def format_amount(amount):
    formatted_amount = f"${amount:,.2f}"
    return formatted_amount

def format_right_aligned(value):
    formatted_value = f"{value:>9s}"
    return formatted_value


#Function to generate receipt
def generate_receipt(customer_info, premium, hst, total_cost, monthly_payment=None, down_payment=0, payment_method=""):
    receipt = f"                   \n\n\n"
    receipt += f"                                                         Date: {datetime.datetime.now().strftime('%B %d, %Y')}\n"
    receipt += f"                                                         Invoice #: {NEXT_POLICY_NUMBER}\n\n"
    receipt += f"Customer:\n\n{customer_info['first_name'].title()} {customer_info['last_name'].title()}\n"
    receipt += f"{customer_info['address'].title()}\n{customer_info['city'].title()}, {customer_info['province'].upper()}, {customer_info['postal_code']}\n"
    receipt += f"{customer_info['phone']}\n"
    receipt += '-' * 80 + '\n'
    receipt += "                            Insurance Policy Receipt\n"
    receipt += '-' * 80 + '\n'
    receipt += f"Number of Vehicles: {customer_info['num_cars']}\n"
    receipt += f"Optional Extra Liability: {'Yes' if customer_info['extra_liability'] == 'Y' else 'No'}\n"
    receipt += f"Optional Glass Coverage: {'Yes' if customer_info['glass_coverage'] == 'Y' else 'No'}\n"
    receipt += f"Optional Loaner Coverage: {'Yes' if customer_info['loaner_car'] == 'Y' else 'No'}\n\n"
    receipt += f"                                                   Basic Premium:      {format_right_aligned(format_amount(BASIC_PREMIUM))}\n"
    if customer_info['num_cars'] > 1:
        additional_cars_cost = (customer_info['num_cars'] - 1) * BASIC_PREMIUM * (1 - DISCOUNT_ADDITIONAL_CAR)
        receipt += f"                                                   Additional Car(s):  {format_right_aligned(format_amount(additional_cars_cost))}\n"
    if customer_info['extra_liability'] == 'Y':
        receipt += f"                                                   Extra Liability:    {format_right_aligned(format_amount(EXTRA_LIABILITY_COST * customer_info['num_cars']))}\n"
    if customer_info['glass_coverage'] == 'Y':
        receipt += f"                                                   Glass Coverage:     {format_right_aligned(format_amount(GLASS_COVERAGE_COST * customer_info['num_cars']))}\n"
    if customer_info['loaner_car'] == 'Y':
        receipt += f"                                                   Loaner Coverage:    {format_right_aligned(format_amount(LOANER_CAR_COST * customer_info['num_cars']))}\n"
    receipt += f"                                                   HST:                {format_right_aligned(format_amount(hst))}\n"
    receipt += f"                                                   -----------------------------\n"
    receipt += f"                                                   Total Amount:       {format_right_aligned(format_amount(total_cost))}\n\n"
    if monthly_payment:
        if down_payment > 0 and payment_method == "Down Pay":
            receipt += f"Payment Option: Monthly with down payment\n\n"
        else:
            receipt += f"Payment Option: Monthly\n\n"
        receipt += f"Processing Fee:   {format_amount(PROCESSING_FEE)}\n"
        if down_payment > 0:
            receipt += f"Down Payment:    {format_amount(down_payment)}\n"
        receipt += f"Monthly Payment: {format_amount(monthly_payment)}\n\n"
    else:
        receipt += "Payment Option: Full\n\n"
    receipt += "Claim History\n"
    receipt += '-' * 80 + '\n'

    # Adding headers for Claim #, Claim Date, and Amount
    
    claim_num_width = 10
    claim_date_width = 20
    amount_width = 15

    receipt += f"{'Claim #':<{claim_num_width}} {'Claim Date':<{claim_date_width}} {'Amount':>{amount_width}}\n"
    receipt += '-' * 80 + '\n'
    for i, claim in enumerate(customer_info['claims'], 1):
        receipt += f"{i}.{'':<{claim_num_width - 2}} {claim['date']:<{claim_date_width}} {format_amount(claim['amount']):>{amount_width}}\n"
    receipt += '-' * 80 + '\n'
    receipt += "Thank You for using One Stop Insurance\n"

    return receipt
   
#function to validate yes or no input
def validate_yes_no_input(prompt):
    value = input(prompt).strip().upper() 
    while value not in ['Y', 'N']:
        print("Invalid input! Please enter 'Y' for Yes or 'N' for No.")
        value = input(prompt).strip().upper()
    return value

#main function
def main():
    global NEXT_POLICY_NUMBER
    while True:
        NEXT_POLICY_NUMBER += 1    # Increment policy number

        # Gather customer information
        first_name = input("\nEnter the customer's first name: ")
        last_name = input("Enter the customer's last name: ")
        address = input("Enter customer's address: ")
        city = input("Enter customer's city: ")
        province = input("Enter customer's province (e.g., ON, QC, etc.): ")
        while not validate_province(province):
            print("Invalid province. Please enter a valid province.")
            province = input("Enter the province (e.g., ON, QC, etc.): ")
        postal_code = input("Enter customer's postal code: ")
        phone = input("Enter customer's phone number (999-999-9999): ")
        num_cars = int(input("Enter the number of cars being insured: "))

        # Validate Yes/No input for extra liability, glass coverage, and loaner car
        extra_liability = validate_yes_no_input("Extra liability coverage (Y/N): ")
        glass_coverage = validate_yes_no_input("Glass coverage (Y/N): ")
        loaner_car = validate_yes_no_input("Loaner car option (Y/N): ")

        payment_method = input("Payment method (Full, Monthly, Down Pay): ").title()
        while not validate_payment_method(payment_method):
            print("Invalid payment method. Please enter a valid method.")
            payment_method = input("Payment method (Full, Monthly, Down Pay): ").title()
        down_payment = 0
        if payment_method == "Down Pay":
            down_payment = float(input("Enter the amount of the down payment: "))

        # Handle claims input
        claims = []
        print("Enter previous claims (press Enter to finish):")
        while True:
            claim_date = input("  Enter the date of the claim (YYYY-MM-DD) or press Enter to finish: ")
            if not claim_date:
                break
            while True:
                claim_amount = input("  Enter the amount of the claim: ")
                if claim_amount.strip() and claim_amount.replace('.', '', 1).isdigit():
                    claim_amount = float(claim_amount)
                    break
                else:
                    print("Invalid claim amount. Please enter a number.")
            claims.append({'date': claim_date, 'amount': claim_amount})

        # Calculate costs
        premium = calculate_premium(num_cars, extra_liability, glass_coverage, loaner_car)
        total_cost, hst = calculate_total_cost(premium, down_payment)
        monthly_payment = None
        if payment_method != "Full":
            monthly_payment = calculate_monthly_payments(total_cost, down_payment)

        # Generate and display receipt
        customer_info = {
            'first_name': first_name,
            'last_name': last_name,
            'address': address,
            'city': city,
            'province': province,
            'postal_code': postal_code,
            'phone': phone,
            'num_cars': num_cars,
            'extra_liability': extra_liability,
            'glass_coverage': glass_coverage,
            'loaner_car': loaner_car,
            'claims': claims
        }
        receipt = generate_receipt(customer_info, premium, hst, total_cost, monthly_payment, down_payment, payment_method)
        print("\n\n                          --- One Stop Insurance ---")
        print(receipt)

        # Ask if the user wants to enter another customer
        another_customer = validate_yes_no_input("Would you like to enter another customer? (Y/N): ")
        if another_customer != 'Y':
            break

if __name__ == "__main__":
    main()