from Apriori_Function import *
transactions = [
    ["bread", "milk"],
    ["bread", "diaper", "beer", "eggs"],
    ["milk", "diaper", "beer", "cola"],
    ["bread", "milk", "diaper", "beer"],
    ["bread", "milk", "diaper", "cola"],
    ["milk", "bread"],
    ["bread", "butter"],
    ["milk", "butter"],
    ["bread", "milk", "butter"],
    ["diaper", "beer"]
]

supp_thresh = 0.2
run_apriori(transactions, supp_thresh)