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
("Oranges", "per kg", "£1.99/kg"),
("Ale", "2.5", "n/a")]

print(len(item_info))
    
# Create the DataFrame with column names
item_dict = {}
item_dict["Prices"] = pd.DataFrame(item_info, columns=["Item_name", "Price", "Price per kg"])
item_dict["Prices"]["Item_name_upper"] = item_dict["Prices"]["Item_name"].str.upper()

print(item_dict["Prices"])
# print(item_dict["Prices"]["Item_name"])

item_list = item_dict["Prices"]["Item_name"].to_list()
print(f"\nItem list:\n{item_list}\ntype:{type(item_list)}")

basket_list = []
add_item = "Yes"
while add_item.upper().strip() == "YES":
    selected_item = input("Please enter item name: ")
    add_item = input("Do you want to add another item? (Yes/No) ")
    basket_list.append(selected_item)

print(f"\nThe items in the basket are:\n{basket_list}")

basket_df = pd.DataFrame(basket_list, columns=["Item_name"])
basket_df["Item_name_upper"] = basket_df["Item_name"].str.upper()
# print(basket_df)

basket_with_prices = basket_df.merge(item_dict["Prices"], on='Item_name_upper',how='left')
basket_with_prices = basket_with_prices[["Item_name_y", "Price", "Price per kg"]]
print(basket_with_prices)