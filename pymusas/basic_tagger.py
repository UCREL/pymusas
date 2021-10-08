import csv
import logging
from pathlib import Path
from typing import List, Tuple, Dict

logger = logging.getLogger(__name__)


def load_lexicon(lexicon_path: Path, has_headers: bool = True,
                 include_pos: bool = True
                 ) -> Dict[str, List[str]]:
    '''
    :param lexicon_path: File path to the lexicon data. This data should be in
                         TSV format with the following data in this column / field
                         order: 1. lemma, 2. Part Of Speech (POS) label / tag,
                         3. USAS / Semantic label.
    :param has_headers: This should be set to True if the lexicon file on it's
                        first line contains a header row e.g. the first line
                        contain no lexicon data. When this is set to True the
                        first line of the lexicon file is ignored.
    param include_pos: Whether or not the returned dictionary uses POS
                       within it's key.
    :returns: A dictionary whereby the key is a tuple of
              (lemma, Part Of Speech label), the lexeme, and the value is a list of
              USAS / Semantic labels e.g. `{('Andrew', 'NN'): ['Z0', 'Z1']}`. The
              list of USAS labels represents all the likely USAS labels that the
              tuple could be, whereby the first label in the list (`Z0`) is the
              most likely USAS label, for more details on the USAS tagset see
              the USAS tagset documentation.
    '''
    lemma_pos_usas: Dict[str, List[str]] = {}
    number_tags = 0
    number_duplicate_entires = 0
    with lexicon_path.open('r') as lexicon_data:
        headers = ['lemma', 'pos_label', 'usas_label']
        usas_reader = csv.DictReader(lexicon_data, delimiter='\t', fieldnames=headers)
        
        # Skips the header row
        if has_headers:
            next(usas_reader)

        for row in usas_reader:
            number_tags += 1

            lemma = row['lemma']
            lemma_pos = f"{lemma}|{row['pos_label']}"

            if not include_pos:
                lemma_pos = lemma
            
            if lemma_pos in lemma_pos_usas:
                number_duplicate_entires += 1
            lemma_pos_usas[lemma_pos] = row['usas_label'].split()

    logger.info(f"Loaded {number_tags - number_duplicate_entires} semantic tags"
                f", from file path: {lexicon_path.resolve()}")
    if include_pos:
        logger.warning("Number of duplicate (lemma, POS) entires in"
                       f" lexicon file: {number_duplicate_entires}")
    else:
        logger.warning("Number of duplicate lemma entries, this is to be "
                       "expected as you are not using POS information, in "
                       f"lexicon file: {number_duplicate_entires}")
    
    return lemma_pos_usas


def tag_token(text: str, lemma: str, pos: str,
              lexicon_lookup: Dict[str, List[str]],
              lemma_lexicon_lookup: Dict[str, List[str]]) -> List[str]:
    if pos == 'punc':
        return ["PUNCT"]

    text_pos = f"{text}|{pos}"
    if text_pos in lexicon_lookup:
        return lexicon_lookup[text_pos]

    lemma_pos = f"{lemma}|{pos}"
    if lemma_pos in lexicon_lookup:
        return lexicon_lookup[lemma_pos]

    text_lower = text.lower()
    text_pos_lower = f"{text_lower}|{pos}"
    if text_pos_lower in lexicon_lookup:
        return lexicon_lookup[text_pos_lower]

    lemma_lower = lemma.lower()
    lemma_pos_lower = f"{lemma_lower}|{pos}"
    if lemma_pos_lower in lexicon_lookup:
        return lexicon_lookup[lemma_pos_lower]

    if pos == 'num':
        return ['N1']

    if text in lemma_lexicon_lookup:
        return lemma_lexicon_lookup[text]

    if lemma in lemma_lexicon_lookup:
        return lemma_lexicon_lookup[lemma]

    if text_lower in lemma_lexicon_lookup:
        return lemma_lexicon_lookup[text_lower]

    if lemma_lower in lemma_lexicon_lookup:
        return lemma_lexicon_lookup[lemma_lower]

    return ['Z99']


class RuleBasedTagger():

    def __init__(self, lexicon_path: Path, has_headers: bool) -> None:
        self.lexicon_lookup = load_lexicon(lexicon_path, has_headers)
        self.lexicon_lemma_lookup = load_lexicon(lexicon_path, has_headers,
                                                 include_pos=False)

    def tag_data(self, tokens: List[Tuple[str, str, str]]) -> List[List[str]]:
        '''
        :param tokens: Each tuple represents a token. The tuple must contain the
                       following lingustic information per token: 1. token text,
                       2. lemma, 3. Part Of Speech.
        '''
        sem_tags: List[List[str]] = []
        for token in tokens:
            token_text = token[0]
            lemma = token[1]
            pos = token[2]

            token_sem_tags = tag_token(token_text, lemma, pos,
                                       self.lexicon_lookup,
                                       self.lexicon_lemma_lookup)
            sem_tags.append(token_sem_tags)
        return sem_tags
