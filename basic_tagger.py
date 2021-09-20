import csv
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def load_lexicon(lexicon_path: Path, has_headers: bool = True, 
                 include_pos: bool = True
                 ) -> dict[str, list[str]]:
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
    lemma_pos_usas: dict[str, str] = {}
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
            lemma_pos = f"{lemma}_{row['pos_label']}"

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

class RuleBasedTagger():

    def __init__(self, lexicon_path: Path, has_headers: bool) -> None:
        self.lexicon_lookup = load_lexicon(lexicon_path, has_headers)
        self.lexicon_lemma_lookup = load_lexicon(lexicon_path, has_headers, 
                                                 include_pos=False)

    def tag_data(self, tokens: list[tuple[str, str, str]]) -> list[list[str]]:
        '''
        :param tokens: Each tuple represents a token. The tuple must contain the 
                       following lingustic information per token: 1. token text,
                       2. lemma, 3. Part Of Speech.
        '''
        sem_tags: list[list[str]] = []
        for token in tokens:
            token_text = token[0]
            lemma = token[1]
            pos = token[2]

            if pos == 'punc':
                sem_tags.append(["PUNCT"])
                continue

            token_pos = f"{token_text}_{pos}"
            if token_pos in self.lexicon_lookup:
                sem_tags.append(self.lexicon_lookup[token_pos])
                continue

            lemma_pos = f"{lemma}_{pos}"
            if lemma_pos in self.lexicon_lookup:
                sem_tags.append(self.lexicon_lookup[lemma_pos])
                continue

            token_lower = token_text.lower()
            token_pos_lower = f"{token_lower}_{pos}"
            if token_pos_lower in self.lexicon_lookup:
                sem_tags.append(self.lexicon_lookup[token_pos_lower])
                continue

            lemma_lower = lemma.lower()
            lemma_pos_lower = f"{lemma_lower}_{pos}"
            if lemma_pos_lower in self.lexicon_lookup:
                sem_tags.append(self.lexicon_lookup[lemma_pos_lower])
                continue

            if pos == 'num':
                sem_tags.append(['N1'])
                continue

            if token_text in self.lexicon_lemma_lookup:
                sem_tags.append(self.lexicon_lemma_lookup[token_text])
                continue

            if lemma in self.lexicon_lemma_lookup:
                sem_tags.append(self.lexicon_lemma_lookup[lemma])
                continue

            if token_lower in self.lexicon_lemma_lookup:
                sem_tags.append(self.lexicon_lemma_lookup[token_lower])
                continue

            if lemma_lower in self.lexicon_lemma_lookup:
                sem_tags.append(self.lexicon_lemma_lookup[lemma_lower])
                continue

            sem_tags.append(['Z99'])
        return sem_tags
            