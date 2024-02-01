from symspellpy import SymSpell

sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)

sym_spell.load_dictionary(
    corpus='./frequency_dictionary_en_82_765.txt',
    term_index=0,
    count_index=1)
sym_spell.load_bigram_dictionary(
    corpus='./frequency_bigramdictionary_en_243_342.txt',
    term_index=0,
    count_index=2)


def make_correction(line):
    suggestions = sym_spell.lookup_compound(
        line,
        max_edit_distance=2,
        ignore_non_words=True,
        ignore_term_with_digits=True)

    return suggestions[0].term
