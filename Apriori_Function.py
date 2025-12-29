from itertools import combinations, chain

def generate_cand_itemset(all_freq_itemset, freq_one_itemset):
    cand_itemset = set()
    # Get the most recent itemsets
    for itemset in all_freq_itemset[len(all_freq_itemset) - 1]:
        # Add all possible distinct frequent one-itemsets to the most recent nth-itemset
        for item in freq_one_itemset:
            (item, ) = item
            # Not in used to check if item is in itemset or not
            if item not in itemset:
                # Convert frozenset to normal set to add item and then convert back to frozenset to add to set list
                upd_itemset = set(itemset)
                upd_itemset.add(item)
                cand_itemset.add(frozenset(upd_itemset))

    return cand_itemset

def subset_freq_check(cand_itemset, all_freq_itemset):
    updated_cand_itemset = set()
    counter = 0
    # For each itemset, check if all its n-1 subsets are part of the frequent itemset collection and if all are,
    # append to the new nth itemset frequent collection to be added into the overall frequent itemset collection
    for itemset in cand_itemset:
        for item in itemset:
            # Convert to set to allow removal of one item and then convert back to frozenset for check in
            upd_itemset = set(itemset)
            upd_itemset.discard(item)
            upd_itemset = frozenset(upd_itemset)
            if upd_itemset not in all_freq_itemset[-1]:
                counter += 1
                break
        if counter == 0:
            updated_cand_itemset.add(itemset)
        counter = 0

    return updated_cand_itemset

def freq_check(trans_data, updated_cand_itemset, support_dict, supp_thresh):
    new_freq_itemset = set()
    for itemset in updated_cand_itemset:
        count = 0
        for transaction in trans_data:
            # Convert each transaction to a set for easier comparison of whether itemset is in transacation or not
            set_transaction = set(transaction)
            if set(itemset).issubset(set_transaction):
                count += 1
        support_prob = count / len(trans_data)

        # Add itemset to dictionary and new frequent itemset if it is supported enough
        if support_prob >= supp_thresh:
            support_dict[itemset] = support_prob
            new_freq_itemset.add(itemset)

    return new_freq_itemset, support_dict

def metric_calc(all_freq_itemset, support_dict):
    confidence_dict, lift_dict = {}, {}
    for item_list in all_freq_itemset[1:]:
        for item_set in item_list:
            item_set = set(item_set)
            item_subset = list(chain.from_iterable(combinations(item_set, s) for s in range(1, len(item_set))))
            for subset in item_subset:
                antecedent = frozenset(subset)
                consequent = item_set - antecedent
                item_key = (antecedent, frozenset(consequent))
                if item_key not in confidence_dict:
                    confidence_dict[item_key] = support_dict[antecedent.union(consequent)] / support_dict[antecedent]
                    lift_dict[item_key] = confidence_dict[item_key] / support_dict[frozenset(consequent)]
                else:
                    continue

    return confidence_dict, lift_dict


def run_apriori(trans_data, supp_thresh):
    count = 0
    support_dict = {}
    confidence_dict = {}
    list_dict = {}
    freq_one_itemset = set()
    all_freq_itemset = []
    relevant_rules = {}

    # Get all distinct items in the customer transaction data using a set
    set_list = set()
    for i in range(len(trans_data)):
        for item in trans_data[i]:
            set_list.add(item)

    # Generate the initial single item frequent list (all frequent one itemsets)
    for item in set_list:
        frozen_item = frozenset({item})
        for i in range(len(trans_data)):
            if item in trans_data[i]:
                count += 1
        support_prob = count / len(trans_data)

        if support_prob >= supp_thresh:
            # Add item + support value to dictionary for later use
            support_dict[frozen_item] = support_prob
            freq_one_itemset.add(frozen_item)
        count = 0

    all_freq_itemset.append(freq_one_itemset)

    # Generate all candidate n+1 itemsets and check if they're frequent itemsets until no more is unable to be generated
    while True:
        cand_itemset = generate_cand_itemset(all_freq_itemset, freq_one_itemset)
        updated_cand_itemset = subset_freq_check(cand_itemset, all_freq_itemset)
        new_freq_itemset, support_dict = freq_check(trans_data, updated_cand_itemset, support_dict, supp_thresh)
        # Stop when no new n+1 itemset has been added
        if new_freq_itemset == set():
            break
        else:
            all_freq_itemset.append(new_freq_itemset)

    # After generating all frequent itemset, calculate confidence and lift using 2+ frequent itemsets
    confidence_dict, list_dict = metric_calc(all_freq_itemset, support_dict)
    for item_set in confidence_dict.keys():
        if (confidence_dict[item_set] >= 0.6) and (list_dict[item_set] >= 1.2):
            relevant_rules[item_set[0]] = item_set[1]


    for keys in relevant_rules.keys():
        print(f"{set(keys)} -> {set(relevant_rules[keys])}")