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
S -> NP VP | NP VP CP | NP VP Conj VP
NP -> N | Det N | Det Adj NP | NP PP | PP NP | CP | Adj NP
VP -> V | VP NP | VP PP | PP VP | Adv VP | VP Adv | Conj VP | V VP
PP -> P | P NP
CP -> Conj S | Conj NP
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
    # List lowercased words
    words = nltk.word_tokenize(sentence.lower())

    for w in words.copy():
        # Remove words without at leat one alphabetic character and .'s
        if w.islower() is False:
            words.remove(w)

    #print(words)
    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    NP = []
    # Filter all NP subtrees
    for s in tree.subtrees(filter=lambda t: t.label() == 'NP'):
        #print("s", s, str(list(s)).count("Tree('N', "))
        # If > 1 'N'/noun or > 0 V/P
        if str(list(s)).count("Tree('N', ") > 1 or \
            str(list(s)).count("Tree('V', ") > 0 or \
            str(list(s)).count("Tree('P', ") > 0:
                # Keep looping
                continue

        # Only one NP
        if s not in NP:
            # Add noun phrase chunk
            NP.append(s)
        
        for i in NP:
            # Is a NP subtree
            if s in i.subtrees(filter=lambda t: t.label() == 'NP') and s != i:
                NP.remove(s)

    #print("NP", NP)
    return NP


if __name__ == "__main__":
    main()
