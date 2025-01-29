#--------------------------------------------#
#                                            #
#          Supermarket Python Code           #
#                                            #
#--------------------------------------------#
#  Stephanie Tuohey 27/02/2025

# Import librarys
import pandas as pd
import math

#-------------------------------------------------#
#    1) Store items available in Supermarket      #
#-------------------------------------------------#

# Store the list of available items to buy at the supermarket as ("Item_name", "Price", "Price per kg")
# Change these lines to change the prices or add items
item_info = [
("Beans", "0.5", "n/a"),
("Coke", "0.7", "n/a"),
("Oranges", "per kg", "1.99"),
("Onions", "per kg", "0.29"),
("Amber Ale", "2.5", "n/a"),
("Pale Ale", "2.5", "n/a"),
("Ginger Ale", "2.5", "n/a"),
("IPA", "2.5", "n/a")]

# print(len(item_info))

# Create the DataFrame with column names
item_dict = {}
item_dict_df = pd.DataFrame(item_info, columns=["Item_name", "Price", "Price per kg"])
item_dict_df["Item_name_upper"] = item_dict_df["Item_name"].str.upper()
item_list = item_dict_df["Item_name"].to_list()
print(f"\nList of available items:\n{item_list}\n")

#---------------------------------------------------------------------------#
#      2) Defining deals - add any deals here under the correct type        #
#---------------------------------------------------------------------------#
# 3 types of deals are defined here
# Note:  make Item_name consistant with the available items

# Bogof-type deals - e.g. 3 for 2, 2 for 1 etc.
deals_type_1 = [
    ("Beans", 2, 1,"Beans 3 for 2") # Beans, 2 for the price of 1
    # ,("Example item", number of items, for ___, "Name of deal")
    ]

# Bulk reduction-type deals - e.g. 2 for £1, 3 for £5 etc.
deals_type_2 = [    
    ("Coke", 2, 1,"Coke 2 for £1") # Coke, 2 for £1
    # ,("Example item", number of items, reduced price (in £),"Name of deal")
    ]

# Grouped item-type deals - e.g. Any 3 ales from the set {...} for £6
item_group = {}
item_group["Ale"] = ["Amber Ale","Pale Ale","Ginger Ale","IPA"] # Add the group of items in deal below
# item_group["group2"] = ["item1","item2","...etc"]

deals_type_3 = [
    ("Ale", 3, 6,"Any 3 ales for £6") # Add deal descriptions below
    # ,("group2", number of items, reduced price (in £),"Name of deal")
    ]

# Make deals into dfs
deal_1_df = pd.DataFrame(deals_type_1, columns=["Item_name", "Number to buy", "Number to price","Name of deal"])
deal_2_df = pd.DataFrame(deals_type_2, columns=["Item_name", "Number to buy", "Deal price","Name of deal"])
deal_3_df = pd.DataFrame(deals_type_3, columns=["Item_name", "Number to buy", "Deal price","Name of deal"])



#--------------------------------------------------------------#
#      3) Input items to basket and store in basket_df         #
#--------------------------------------------------------------#

# Initialise basket_df
basket_df = pd.DataFrame(columns=["Item_name", "Weight (kg)"])
# Initialise add_item
add_item = "Yes"

# Start loop to add multiple items
while add_item.upper().strip() == "YES":

    selected_item = input("Please enter item name: ")
    
    selected_item_info = item_dict_df[item_dict_df["Item_name_upper"] == selected_item.upper()]

    # Reject items that are not available
    if selected_item_info.empty:
        print(f"'{selected_item}' is not a on the list of available items. Please try again.")
        continue

    # Require weight for items priced by the kg
    elif selected_item_info.iloc[0]["Price per kg"] != "n/a":
        kg = input("Please enter item weight (kg): ")
    else:
        kg = 0

    basket_item_info = [(selected_item,kg)]
    basket_item_df = pd.DataFrame(basket_item_info, columns=["Item_name", "Weight (kg)"])
    basket_df = pd.concat((basket_df,basket_item_df), ignore_index = True)

    add_item = input("Do you want to add another item? (Yes/No) ")

# print(f"\nThe items in the basket are:\n{basket_df}")


#--------------------------------------#
#      4) Manipulate basket_df         #
#--------------------------------------#

# Upcase item names to improve matching
basket_df["Item_name_upper"] = basket_df["Item_name"].str.upper()

# Merge on the item prices
basket_with_prices = basket_df.merge(item_dict_df, on='Item_name_upper',how='left', suffixes=('_basket', '_prices'))
# Drop some cols
basket_with_prices = basket_with_prices[["Item_name_prices", "Price", "Price per kg","Weight (kg)"]]
# Sort by Item Name
basket_with_prices = basket_with_prices.sort_values(by=['Item_name_prices']).rename(columns={"Item_name_prices":"Item_name"})

# Convert cols to numeric
basket_with_prices["Price"] = pd.to_numeric(basket_with_prices["Price"], errors="coerce")
basket_with_prices["Price per kg"] = pd.to_numeric(basket_with_prices["Price per kg"], errors="coerce")

# print(f"\nThe items in the basket with prices are:\n{basket_with_prices}")

# Calculate prices for items by kg
basket_with_prices["Calc price"] = (
    basket_with_prices["Price"].fillna(0) +
    (basket_with_prices["Price per kg"] * basket_with_prices["Weight (kg)"].fillna(1).astype(float)).fillna(0))
    
basket_with_prices = basket_with_prices.drop(columns=['Price'])

# Create count of each item and price per item name
basket_summary = (basket_with_prices.groupby("Item_name", as_index=False)
    .agg(Number_in_basket=("Item_name", "count"), 
         Total_item_price=("Calc price", "sum"),
         Price=("Calc price", "first"))  # Retains the first price found for each item
    .rename(columns={"Number_in_basket": "Number in basket","Total_item_price": "Total item price"}))

# print(f"\nbasket_summary is:\n{basket_summary}")

#------------------------------------------#
#           5) Impliment Deal 1s           #
#------------------------------------------#

# Check to see if any basket items are in deal 1
basket_items_with_deal_1 = deal_1_df.merge(basket_summary, on='Item_name', how = 'inner')

# If any items in basket match deal 1 items, start loop
if not basket_items_with_deal_1.empty:

    def savings_col_calc (row):
        
        # Check theres enough of this item to qualify for the deal
        if row['Number in basket'] >= row['Number to buy']:
            # print("Deals found!")
            # Calculate savings
            no_full_deals = math.floor(row['Number in basket'] / row['Number to buy'])
            deals_remainder = row['Number in basket'] % row['Number to buy']
            Deal_price_full = (no_full_deals * row["Number to price"] * row["Price"]) + (deals_remainder * row["Price"])
            Savings = Deal_price_full - row["Total item price"]
            # print(f"\nSavings are:\n{Savings}")
            return Savings
        else:
            return 0
    

    basket_items_with_deal_1["Savings"] = basket_items_with_deal_1.apply (lambda row: savings_col_calc(row), axis=1)
    receiptsavings_deal1 = basket_items_with_deal_1[["Name of deal","Savings"]]
    # print(receiptsavings_deal1)

else:
    # print("No Deal 1 items found in basket.")
    receiptsavings_deal1 = pd.DataFrame(columns=["Name of deal","Savings"])



#------------------------------------------#
#           6) Impliment Deal 2s           #
#------------------------------------------#

# Check to see if any basket items are in deal 2
basket_items_with_deal_2 = deal_2_df.merge(basket_summary, on='Item_name', how = 'inner')

# If any items in basket match deal 1 items, start loop
if not basket_items_with_deal_2.empty:

    def savings_col_calc (row):
        
        # Check theres enough of this item to qualify for the deal
        if row['Number in basket'] >= row['Number to buy']:
            # print("Deals found!")
            # Calculate savings
            no_full_deals = math.floor(row['Number in basket'] / row['Number to buy'])
            deals_remainder = row['Number in basket'] % row['Number to buy']
            Deal_price_full = (no_full_deals * row["Deal price"]) + (deals_remainder * row["Price"])
            Savings = Deal_price_full - row["Total item price"]
            # print(f"\nSavings are:\n{Savings}")
            return Savings
        else:
            return 0

    basket_items_with_deal_2["Savings"] = basket_items_with_deal_2.apply (lambda row: savings_col_calc(row), axis=1)
    receiptsavings_deal2 = basket_items_with_deal_2[["Name of deal","Savings"]]
    # print(receiptsavings_deal2)

else:
    # print("No Deal 2 items found in basket.")
    receiptsavings_deal2 = pd.DataFrame(columns=["Name of deal","Savings"])


#------------------------------------------#
#           7) Impliment Deal 3s           #
#------------------------------------------#

# print(len(deal_3_df))

#  Make col deals_type_3["Item_name"] into list
type_3_list = list(deal_3_df["Item_name"])
# print(type_3_list)

# Loop through all deals in type_3_list
for deal in type_3_list:

    # find number of items in basket that are in this deal
    basket_items_with_deal_3 = basket_with_prices[basket_with_prices['Item_name'].isin(item_group[deal])]

    #  Sort by Price
    basket_items_with_deal_3 = basket_items_with_deal_3.sort_values(by=['Calc price']) # Will sort ASCENDING
    # print(f"\nbasket_items_with_deal_3(sorted by price):\n{basket_items_with_deal_3}")

    # Count how many deal items are in the basket
    total_deal_items_in_basket = len(basket_items_with_deal_3)

    # Get deal_to_buy from "Number to buy" col in deal_3_df where Item_name is deal
    deal_to_buy = deal_3_df[deal_3_df["Item_name"] == deal].iloc[0]["Number to buy"]

    # Get deal_to_buy from ""Name of deal"" col in deal_3_df where Item_name is deal
    name_of_deal = deal_3_df[deal_3_df["Item_name"] == deal].iloc[0]["Name of deal"]

    # Get price_per_deal from "Deal price" col in deal_3_df where Item_name is deal
    price_per_deal = deal_3_df[deal_3_df["Item_name"] == deal].iloc[0]["Deal price"]

    if total_deal_items_in_basket >= deal_to_buy: 

        # print("Deals found!")
        # Calculate savings
        no_full_deals = math.floor(total_deal_items_in_basket / deal_to_buy)
        deals_remainder = total_deal_items_in_basket % deal_to_buy

        # If not enough items to qualify for deal, remaining items must have their regular price
        remainder_items_df = basket_items_with_deal_3.head(deals_remainder)
        remaining_items_cost = remainder_items_df['Calc price'].sum()

        Deal_price_full = (no_full_deals * price_per_deal) + remaining_items_cost

        # Calculate the savings 
        price_without_deals = basket_items_with_deal_3['Calc price'].sum()
        Savings = Deal_price_full - price_without_deals


        # print(f"\nThere is a deal on {deal}. Savings are:\n{Savings}")

        # Make receipt
        data = {"Name of deal": [name_of_deal], "Savings": [Savings]}
        receiptsavings_deal3 = pd.DataFrame(data)
        # print(receiptsavings_deal3)

    else:
        # print(f"\n{total_deal_items_in_basket} Deal 3 item(s) found in basket. Not enough for deal.")
        receiptsavings_deal3 = pd.DataFrame(columns=["Name of deal","Savings"])


#--------------------------------------#
#           8) Make receipt            #
#--------------------------------------#

# Create top part of the receipt
top_receipt = basket_with_prices[["Item_name","Calc price"]].rename(columns={"Item_name":"col1","Calc price":"col2"})
top_sum = top_receipt['col2'].sum()

# Create subtotal line
subtotal = pd.DataFrame({"col1": ["Sub-total"], "col2": [top_sum]})

# Create savings line
savings_title = pd.DataFrame({"col1": ["Savings"], "col2": [""]})

# Create savings part of the receipt
savings_receipt = pd.concat((receiptsavings_deal3,receiptsavings_deal2,receiptsavings_deal1), ignore_index = True).rename(columns={"Name of deal":"col1","Savings":"col2"})
tot_savings = savings_receipt['col2'].sum()

# Calculate grand total and add to receipt
grand_tot = top_sum + tot_savings
total_row = pd.DataFrame({"col1": ["Total to Pay"], "col2": [grand_tot]})

# Put it all together!
if tot_savings != 0:
    full_receipt = pd.concat((top_receipt,subtotal,savings_title,savings_receipt,total_row), ignore_index = True)
else:
    full_receipt = pd.concat((top_receipt,subtotal,savings_receipt,total_row), ignore_index = True)

# Format and print final receipt
print("\nFinal Receipt:\n")
for index, row in full_receipt.iterrows():
    # Replace NaN with empty string
    col2_value = row["col2"]
    if isinstance(col2_value, (int, float)):  # If it's a number
        col2_value = f"£{col2_value:,.2f}"  # Format to 2 decimal places with GBP sign
    else:
        col2_value = ""  # For NaN or non-numeric values, make it an empty string
    
    # Bold formatting for "Sub-total" and "Total to Pay"
    if row["col1"] in ["Sub-total", "Total to Pay"]:
        print(f"\033[1m{row['col1']:20} {col2_value}\033[0m")  # Bold
    else:
        print(f"{row['col1']:20} {col2_value}")  # Normal print

print("")