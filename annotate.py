from nltk.corpus import wordnet as wn

def search_for_event_meanings(lemmas):
    """
    show information about all possible meanings
    
    :param iterable lemmas: one or more lemmas
    """
    for lemma in lemmas:
        print()
        print(lemma)
        print()
        for synset in wn.synsets(lemma):
            print()
            for hypernym in synset.hypernyms():
                print
                print('HYPERNYM', hypernym, hypernym.definition())
            print
            print(synset, synset.definition())
            print(synset.examples())