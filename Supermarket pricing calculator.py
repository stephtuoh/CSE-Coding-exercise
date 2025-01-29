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

print(len(item_info))

# Create the DataFrame with column names
item_dict = {}
item_dict_df = pd.DataFrame(item_info, columns=["Item_name", "Price", "Price per kg"])
item_dict_df["Item_name_upper"] = item_dict_df["Item_name"].str.upper()
item_list = item_dict_df["Item_name"].to_list()
print(f"\nList of available items:\n{item_list}")
print("")

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
Ales_set = ["Amber Ale","Pale Ale","Ginger Ale","IPA"]
deals_type_3 = [
    (Ales_set, 3, 6,"Any 3 ales for £6")
    # ,(set, number of items, reduced price (in £),"Name of deal")
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

print(f"\nThe items in the basket are:\n{basket_df}")


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

print(f"\nThe items in the basket with prices are:\n{basket_with_prices}")

# Calculate prices for items by kg
basket_with_prices["Full price"] = (
    basket_with_prices["Price"].fillna(0) +
    (basket_with_prices["Price per kg"] * basket_with_prices["Weight (kg)"].fillna(1).astype(float)).fillna(0)
)

# Create count of each item and price per item name
basket_summary = (basket_with_prices.groupby("Item_name", as_index=False)
    .agg(Number_in_basket=("Item_name", "count"), 
         Full_price=("Full price", "sum"),
         Price=("Price", "first"))  # Retains the first price found for each item
    .rename(columns={"Number_in_basket": "Number in basket","Full_price": "Full price"}))

print(f"\nbasket_summary is:\n{basket_summary}")

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
            print("Deals found!")
            # Calculate savings
            no_full_deals = math.floor(row['Number in basket'] / row['Number to buy'])
            deals_remainder = row['Number in basket'] % row['Number to buy']
            Deal_price = (no_full_deals * row["Number to price"] * row["Price"]) + (deals_remainder * row["Price"])
            Savings = Deal_price - row["Full price"]
            print(f"\nSavings are:\n{Savings}")
            return Savings
        else:
            return 0
    

    basket_items_with_deal_1["Savings"] = basket_items_with_deal_1.apply (lambda row: savings_col_calc(row), axis=1)
    recieptsavings_deal1 = basket_items_with_deal_1[["Name of deal","Savings"]]
    print(recieptsavings_deal1)

else:
    print("No Deal 1 items found in basket.")
    recieptsavings_deal1 = pd.DataFrame(columns=["Name of deal","Savings"])




recieptsavings_deal1 = basket_items_with_deal_1[["Name of deal","Savings"]]
print(recieptsavings_deal1)

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
            print("Deals found!")
            # Calculate savings
            no_full_deals = math.floor(row['Number in basket'] / row['Number to buy'])
            deals_remainder = row['Number in basket'] % row['Number to buy']
            Deal_price = (no_full_deals * row["Deal price"]) + (deals_remainder * row["Price"])
            Savings = Deal_price - row["Full price"]
            print(f"\nSavings are:\n{Savings}")
            return Savings
        else:
            return 0

    basket_items_with_deal_2["Savings"] = basket_items_with_deal_2.apply (lambda row: savings_col_calc(row), axis=1)
    recieptsavings_deal2 = basket_items_with_deal_2[["Name of deal","Savings"]]
    print(recieptsavings_deal2)


else:
    print("No Deal 2 items found in basket.")
    recieptsavings_deal1 = pd.DataFrame(columns=["Name of deal","Savings"])



#------------------------------------------#
#           7) Impliment Deal 3s           #
#------------------------------------------#

