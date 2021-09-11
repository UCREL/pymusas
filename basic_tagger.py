import csv
import logging
from pathlib import Path
from typing import Dict, Tuple

logger = logging.getLogger(__name__)

def load_lexicon(lexicon_path: Path, has_headers: bool = True
                 ) -> Dict[Tuple[str, str], str]:
    '''
    :param lexicon_path: File path to the lexicon data. This data should be in 
                         TSV format with the following data in this column / field 
                         order: 1. lemma, 2. Part Of Speech label / tag, 3. 
                         USAS / Semantic label.
    :param has_headers: This should be set to True if the lexicon file on it's 
                        first line contains a header row e.g. the first line 
                        contain no lexicon data. When this is set to True the 
                        first line of the lexicon file is ignored.
    :returns: A dictionary whereby the key is a tuple of 
              (lemma, Part Of Speech label) and the value is the USAS / Semantic 
              label e.g. `{('Andrew', 'NN'): 'Z0'}`.
    '''
    lemma_pos_usas: Dict[(str, str), str] = {}
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
            lemma, pos_label = row['lemma'], row['pos_label']
            if (lemma, pos_label) in lemma_pos_usas:
                number_duplicate_entires += 1
            lemma_pos_usas[(row['lemma'], row['pos_label'])] = row['usas_label']

    logger.info(f"Loaded {number_tags} semantic tags, from file path: "
                f"{lexicon_path.resolve()}")
    logger.debug(f"Number of duplicate (lemma, POS) entires in lexicon file: {number_duplicate_entires}")
    
    return lemma_pos_usas
            