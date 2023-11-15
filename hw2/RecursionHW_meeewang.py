"""
############################## Homework Recursion ##############################

% Student Name: Meng Wang

% Student Unique Name: meeewang

% Lab Section 00X: 103

% I worked with the following classmates: None

%%% Please fill in the first 4 lines of this file with the appropriate information before submitting on Canvas.
"""

# Submit a file named RecursionHW_uniqid.py
# This file should have at least the following functions.
# change()
# giveChange()

# IMPORT 
from math import inf

# FUNCTIONS
def change(amount, coins):
    """return the smallest number of coins that makes up the given amount of money.
    
    check all possibilities of differnt combination of coins that makes up the given amount 
    return the number of coins that is smallest
    otherwise return inf

    Args:
        amount (int): the amount of change to be made.
        coin (list): a list of coin values.

    Returns:
        minlayer+1 (int): non-negative integer indicating the minimum number of coins required to make up the given amount
        inf: when change can't be made for that amount
    """
    if amount < 0:
        return inf
    if amount == 0:
        return 0
    minlayer = inf
    for i in range(len(coins)):
        res = change(amount - coins[i], coins)
        minlayer = min(res, minlayer)
    return minlayer + 1

def isTotal(l, target):

    """return the result about whether the sum of coin values selected is equal to the given amount of money.
    
    Args:
        l (list): the list of selected coin values.
        target (int): the amount of change to be made.

    Returns:
        bool:  true if the sum of coin values equals the amount of change to be made, false otherwise.

    """
    t = 0
    for i in range(len(l)):
        t += l[i]
    return t == target

def giveChangeHelper(total, remainingAmount, coins, coinsUsed):

    """return the list of coin values that can make up the given amount of money.
    
    Args:
        total (int): the amount of change to be made.
        remainingAmount (int): the difference bwtween the given amount of money and the sum of current coin values.
        coins (list): the list of coin values.
        coinsUsed (list): the list of selected coin values.

    Returns:
        finalCoinList (list):  the list of coin values that can make up the given amount money.
        []: when change can't be made for that amount

    """
    
    if remainingAmount == 0:
        return coinsUsed
    elif remainingAmount < 0:
        return []

    minLen = inf
    finalCoinList = list(coinsUsed)

    for i in range(len(coins)):
        newCoinsUsed = list(coinsUsed)
        newCoinsUsed.append(coins[i])

        res = giveChangeHelper(total, remainingAmount - coins[i], coins, newCoinsUsed)

        if len(res) != 0 and isTotal(res, total) and len(res) < minLen:
            minLen = len(res)
            finalCoinList = list(res)

    return finalCoinList           


def giveChange(total, coins):

    """return the smallest number of coins that makes up the given amount of money and the list of coin values that can make up that amount of money.
    
    Args:
        total (int): the amount of change to be made.
        coins (list): the list of coin values.


    Returns:
        [len(res), res]:  the smallest number of coins that makes up the given amount of money and the list of coin values that can make up that amount of money.   
        [inf, []]: when change can't be made for that amount

    """
    res = giveChangeHelper(total, total, coins, [])

    if not isTotal(res, total):
        return [inf, []]

    return [len(res), res]
 
