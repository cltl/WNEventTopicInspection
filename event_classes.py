from nltk.corpus import wordnet as wn

class LexExpr:
    def __init__(self, lexical_expression):
        self.lexical_expression = lexical_expression
        self.event_meanings = set()
    
    @property
    def wn_ambiguity(self):
        return len(wn.synsets(self.lexical_expression))
                
    @property
    def event_ambiguity(self):
        return len(self.event_meanings)
    
    @property
    def event_instance_ids(self):
        return {ev_meaning_obj.ev_meaning_id
                for ev_meaning_obj in self.event_meanings}
    
    @property
    def event_instance_defs(self):
        results = []
        for event_meaning in self.event_meanings:
            local = ';'.join([synset.definition()
                              for synset in event_meaning.wn_synsets])
            results.append(local)
        return ' AND '.join(results)
        
class EventMeaning:
    def __init__(self, ev_meaning_id, wn_meanings, domain):
        self.ev_meaning_id = ev_meaning_id
        self.wn_meanings = wn_meanings
        self.lexical_expressions = self.get_lexical_expressions()
        self.domain = domain
    
    @property
    def wn_synsets(self):
        return {wn.synset(wn_meaning) 
                for wn_meaning in self.wn_meanings}
    
    @property
    def ili_defs(self):
        ilis = set()
        for synset in self.wn_synsets:
            pos = synset.pos()
            if pos == 's':
                pos = 'a'
            offset = str(synset.offset()).zfill(8)
            ili = 'ili-30-%s-%s' % (offset, pos)
            ilis.add(ili)
        return ilis
            

    def get_lexical_expressions(self):
        return {lemma_name 
                for synset in self.wn_synsets
                for lemma_name in synset.lemma_names()}
    
    @property
    def variance(self):
        return len(self.lexical_expressions)