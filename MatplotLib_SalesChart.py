#This is a program that prompts the user to enter total sales thrn plots the data using matlibplot
#Author: Maz Radwan
#Date: Nov 19, 2023

import matplotlib.pyplot as plt


# Define functions and create lists
def enter_sales_data():
    monthly_sales = []
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # Required user inputs
    for month in months:
        while True:
            try:
                
                sales = input(f"Enter total sales for {month} (if not applicable, enter 0): ")

                # Convert the input to a float and check if it's non-negative
                sales_amount = float(sales)
                if sales_amount < 0:
                    raise ValueError("Sales amount cannot be negative.")
                
                # Add the sales amount to the list and break the loop
                monthly_sales.append(sales_amount)
                break
            except ValueError as e:
                print(f"Invalid input: {e}")

    return months, monthly_sales

def plot_sales(months, monthly_sales):
    # Create a bar chart
    plt.bar(months, monthly_sales)


    plt.title("Monthly Sales for the Year")
    plt.xlabel("Months")
    plt.ylabel("Total Sales ($)")

    # Display the plot
    plt.show()


def main():
    months, monthly_sales = enter_sales_data()
    plot_sales(months, monthly_sales)


main()
