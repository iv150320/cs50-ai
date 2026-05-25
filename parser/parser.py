import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP VP Conj S

NP -> N | Det N | Det Adj N | Det Adj Adj N | Det Adj Adj Adj N | NP PP | Det N PP | Det Adj N PP

PP -> P NP | P Det Adj N | P Det Adj Adj N | P Det Adj Adj Adj N

VP -> V | V NP | V PP | V Adv | Adv VP | VP Adv | VP Conj VP
"""


grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Tokenize and lowercase
    tokens = nltk.word_tokenize(sentence)
    
    # Filter words that contain at least one alphabetic character and lowercase
    words = [word.lower() for word in tokens if any(c.isalpha() for c in word)]
    
    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = []
    
    # Iterate through subtrees
    for subtree in tree.subtrees():
        # Check if this is an NP
        if subtree.label() == "NP":
            # Check if it contains any other NP as a descendant subtree
            has_np_child = any(
                sub.label() == "NP"
                for sub in subtree.subtrees()
                if sub is not subtree
            )
            if not has_np_child:
                chunks.append(subtree)
    
    return chunks


if __name__ == "__main__":
    main()
