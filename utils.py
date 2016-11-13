import pandas 
from tabulate import tabulate
import event_classes

def load_it(domain2lex_expr2ev_meanings):
    """
    load all manual annotations into class instances
    
    :param dict domain2lex_expr2ev_meanings: mapping from
    'domain' -> lexical expression -> event meaning
    
    :rtype: tuple
    :return: (lex_expr_objs, ev_meaning_objs)
    
    """
    lex_expr_objs = {}
    ev_meaning_objs = {}

    for domain, info in domain2lex_expr2ev_meanings.items():
        for lex_exprs, wn_meanings in info.items():
            for lex_expr in lex_exprs:

                ev_meaning_id = frozenset(wn_meanings)
                if ev_meaning_id not in ev_meaning_objs:
                    ev_meaning_obj = event_classes.EventMeaning(ev_meaning_id, 
                                                                wn_meanings, 
                                                                domain)
                    ev_meaning_objs[ev_meaning_id] = ev_meaning_obj
                ev_meaning_obj = ev_meaning_objs[ev_meaning_id]

                if lex_expr not in lex_expr_objs:
                    lex_expr_obj = event_classes.LexExpr(lex_expr)
                    lex_expr_objs[lex_expr] = lex_expr_obj
                lex_expr_obj = lex_expr_objs[lex_expr]
                lex_expr_obj.event_meanings.add(ev_meaning_obj)
    
    return lex_expr_objs, ev_meaning_objs

            
def show_me(main_dict, keys, headers, meta=set()):
    """
    this function shows in a html table
    for the keys of the main dict the headers (attributes)
    
    :param dict main_dict: either lex_expr_objs or ev_meaning_objs
    (see notebook 'Domain2lexical expression2event meanings.ipynb'
    :pararm iterable keys: keys from the main_dict to inspect
    :param list headers: the attribute you want to inspect from the keys
    :param set meta: keys for which you want to show:
    1. number of items
    2. average of values
    
    :rtype: IPython.core.display.HTML
    :return: the results in a html table
    """ 
    rows = []
    for key in keys:
        if key not in main_dict:
            row = [key] + ['NA' for _ in range(len(headers)-1)]
            rows.append(row)
            continue
            
        the_object = main_dict[key]
        row = [getattr(the_object, header) for header in headers]
        rows.append(row)
    
    df = pandas.DataFrame(rows, columns=headers)
    
    if meta:
        print('number of rows: %s' % len(df))
        for key in meta:
            minimum = min(df[key])
            maximum = max(df[key])
            average = sum(df[key]) / len(df)
            print('%s: min(%s), avg(%s), max(%s)' % (key, 
                                                     minimum, 
                                                     round(average, 2),
                                                     maximum))
    
    table = tabulate(df, headers='keys', tablefmt='html')
    return table