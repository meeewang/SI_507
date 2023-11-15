#
# Name: Meng Wang
#

from Proj2_tree import printTree

#
# The following two trees are useful for testing.
#
smallTree = \
    ("Is it bigger than a breadbox?",
        ("an elephant", None, None),
        ("a mouse", None, None))
mediumTree = \
    ("Is it bigger than a breadbox?",
        ("Is it gray?",
            ("an elephant", None, None),
            ("a tiger", None, None)),
        ("a mouse", None, None))

original_tree = []
new_tree = []


def main():
    '''Main function to play 20 questions with the user

    Parameters
    ----------
   None

    Returns
    -------
    Tuple of tuples

    '''
    print("Welcome to 20 Questions!")
    next_game = play(smallTree)
    answer = yes("Would you like to play again?")
    while answer == True:
        new_tree.clear()
        next_game = play(next_game)
        answer = yes("Would you like to play again?")
    else:
        save_tree = yes('Would you like to save this tree for later?')
        if save_tree == True:
            file_name = input('Please input a file name')
            treefile = open(file_name, 'w')
            saveTree(next_game, treefile)
            treefile.close()
            print("Thank you! The file has been saved.")
            exit
        else:
            exit

def isleaf(tree):
    '''Return whether a tree is a leaf or not

    Parameters
    ----------
    tree: tuple

    Returns
    -------
    Boolean
    True or False

    '''
    if type(tree[0]) == str and tree[1] == None and tree[2] == None:
        return True
    else:
        return False

def yes(prompt):
    '''return whether the user has responded yes or no to a question
    Parameters
    ----------
    prompt: question to ask the user in the form of a string

    Returns
    -------
    Boolean
    True or False

    '''
    response = input(prompt)
    yes_words = ['yes', 'y', 'yup', 'sure']
    if response in yes_words:
        return True
    else:
        return False

def deep_in(tup, elem):
    '''Recursively checks if an element is within the nested tuple

    Parameters
    ----------
    tup: tuple, the tuple to be search
    elem: string, the element you are looking for

    Returns
    -------
    Boolean
    True or False

    '''
    for v in tup:
        if v == elem:
          return True
        if isinstance(v, tuple) and deep_in(v, elem):
           return True
    return False

def playLeaf(tree):
    '''Goes through the leaf and gets user input based on whether the computer correctly guessed the answer or not
    Parameters
    ----------
    tree: tuple
    tree to be used in the 20 questions game

    Returns
    -------
    tree
    OR
    tuple:
    new tuple with question and answer

    '''
    if yes(f"Is it {tree[0]}?") == True:
        return tree
    else:
        response = input("What was it?")
        new_q = input(f"What's something that distinguishes between {response} and {tree[0]}")
        new_answer = yes(f"What's the answer for {response}?")
        tup = (response, None, None)
        n = (new_tree[0])
        if deep_in(n, tree):
            if new_answer == True:
                new_tup = (new_q, tup, tree)
                return new_tup
            else:
                new_tup = (new_q, tree, tup)
                return new_tup


def simplePlay(tree):
    '''Plays the game with the user using the specified tree

    Parameters
    ----------
    tree: tuple
    tree to be used in the 20 questions game

    Returns
    -------
    None

    '''
    if isleaf(tree) == True:
        playLeaf(tree)
    else:
        question = tree[0]
        if yes(question) == True:
            simplePlay(tree[1])
        else:
            simplePlay(tree[2])


def play(tree):
    '''Plays the game with the user using the specified tree and updates the tree based on user input

    Parameters
    ----------
    tree: tuple
    tree to be used in the 20 questions game

    Returns
    -------
    tuple:
    new tree based on the user's input

    '''
    original_tree.append(tree)
    new_tree.append(tree)
    if isleaf(tree) == True:
        new_node = playLeaf(tree)
        return new_node
    else:
        question = tree[0]
        if yes(question) == True:
            x = play(tree[1])
            return (question, x, tree[2])
        else:
            x = play(tree[2])
            return (question, tree[1], x)

def saveTree(tree, treeFile):
    '''Saves the tree to a txt file

    Parameters
    ----------
    tree: tuple containing the tuples of the tree
    treeFile: string, name of the file

    Returns
    -------
    txt file of the users saved tree

    '''
    if isleaf(tree) == True:
        print("Leaf", file= treeFile)
        print(tree[0], file= treeFile)
    else:
        print("Internal Node", file= treeFile)
        print(tree[0], file= treeFile)
        saveTree(tree[1], treeFile)
        saveTree(tree[2],treeFile)

# The following two-line "magic sequence" must be the last thing in
# your file.  After you write the main() function, this line it will
# cause the program to automatically play 20 Questions when you run
# it.
#
if __name__ == '__main__':
    main()
