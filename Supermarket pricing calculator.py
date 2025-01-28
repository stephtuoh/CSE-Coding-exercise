#--------------------------------------------#
#          Supermarket Python Code           #
#--------------------------------------------#
#  Stephanie Tuohey 27/02/2025


# Import librarys
import pandas as pd
from tkinter import *

# Store the list of available items to buy at the supermarket as ("Item_name", "Price", "Price per kg")
# Change these lines to change the prices or add items
item_info = [
("Beans", "0.5", "n/a"),
("Coke", "0.7", "n/a"),
("Oranges", "per kg", "1.99"),
("Onions", "per kg", "0.29"),
("Ale", "2.5", "n/a")]

print(len(item_info))
    
# Create the DataFrame with column names
item_dict = {}
item_dict["Prices"] = pd.DataFrame(item_info, columns=["Item_name", "Price", "Price per kg"])
item_dict["Prices"]["Item_name_upper"] = item_dict["Prices"]["Item_name"].str.upper()
item_list = item_dict["Prices"]["Item_name"].to_list()

# Deals

# Bogof-type deals - e.g. 3 for 2, 2 for 1 etc.
deals_type_1 = [
    ("Beans", "2", "1")
    # ,("Example item", "number of items", "1")
    ]

# Bulk reduction-type deals - e.g. 2 for £1, 3 for £5 etc.
deals_type_2 = [    
    ("Coke", "2", "1")
    # ,("Example item", "number of items", "reduced price (in £)")
    ]

# Grouped item-type deals - e.g. Any 3 ales from the set {...} for £6
deals_type_3 = [(
    )]

print(f"\nList of available items:\n{item_list}")
print("")

basket_df = pd.DataFrame(columns=["Item_name", "Weight (kg)"])
add_item = "Yes"
while add_item.upper().strip() == "YES":

    selected_item = input("Please enter item name: ")
    
    selected_item_info = item_dict["Prices"][item_dict["Prices"]["Item_name_upper"] == selected_item.upper()]

    if selected_item_info.empty:
        print(f"'{selected_item}' is not a on the list of available items. Please try again.")
        continue

    elif selected_item_info.iloc[0]["Price per kg"] != "n/a":
        kg = input("Please enter item weight (kg): ")
    else:
        kg = "n/a"



    basket_item_info = [(selected_item,kg)]
    basket_item_df = pd.DataFrame(basket_item_info, columns=["Item_name", "Weight (kg)"])
    basket_df = pd.concat((basket_df,basket_item_df), ignore_index = True)
    # basket_list.append(selected_item)



    add_item = input("Do you want to add another item? (Yes/No) ")

# print(f"\nThe items in the basket are:\n{basket_df}")

# basket_df = pd.DataFrame(basket_list, columns=["Item_name"])
basket_df["Item_name_upper"] = basket_df["Item_name"].str.upper()
# print(basket_df)

basket_with_prices = basket_df.merge(item_dict["Prices"], on='Item_name_upper',how='left', suffixes=('_basket', '_prices'))
basket_with_prices = basket_with_prices[["Item_name_prices", "Price", "Price per kg","Weight (kg)"]]
basket_with_prices = basket_with_prices.sort_values(by=['Item_name_prices']).rename(columns={"Item_name_prices":"Item_name"})

# print(basket_with_prices)
print(f"\nThe items in the basket with prices are:\n{basket_with_prices}")

summary = basket_with_prices.groupby(["Item_name"], as_index=False)['Item_name'].agg(['count'])
print(summary)