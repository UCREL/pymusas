import json
import xml.etree.ElementTree as ET
from pathlib import Path

def read_gold_data(gold_data_path: Path,
                   basic_to_core_pos_mapper: dict[str, str]
                   ) -> list[list[str]]:
    '''
    :returns: A list whereby the outer list represents each sentence/line data. 
              The inner list represents each token's data. The dictionary is 
              made up of the following keys: 1. `token`, 2. `basic_pos`, 
              3. `core_pos`, and 4. `usas_tag`. Whereby the `core_pos` is 
              mapped from the `basic_pos` using the `basic_to_core_pos_mapper`.
    '''
    all_sentence_data: list[list[dict[str, str]]] = []

    with gold_data_path.open('r') as gold_data:
        for line in gold_data:
            sentence_data: list[dict[str, str]] = []
            for token_data in line.split():
                token, basic_pos, usas_tag = token_data.split('|')
                core_pos = basic_to_core_pos_mapper[basic_pos]
                sentence_data.append({'token': token, 'basic_pos': basic_pos, 
                                      'core_pos': core_pos, 'usas_tag': usas_tag})
            all_sentence_data.append(sentence_data)
    return all_sentence_data


def read_cytag_data(cytag_data_path: Path
                    ) -> list[list[dict[str, str]]]:
    '''
    :returns: A list whereby the outer list represents each sentence/line data. 
              The inner list represents each token's data. The dictionary is 
              made up of the following keys: 1. `lemma`, 2. `enhanced_pos`, 
              3. `token`.
    '''
    all_sentence_data: list[list[dict[str, str]]] = []
    tree = ET.parse(str(cytag_data_path))
    root = tree.getroot()
    rich_pos_error_mapper = {'pron.demd': 'Rha', 'pron.demg': 'Rha', 
                             'pron.demb': 'Rha', 'unk': 'Gw'}
    for sentence in root.iter('sentence'):
        sentence_data: list[dict[str,str]] = []
        for token in sentence.iter('token'):
            token_data = {}
            # have to split on `|` as some tokens can have more than one potential 
            # lemma we take the first lemma and associated rich pos tag.
            token_data['lemma'] = token.get('lemma').split('|')[0].strip(' ')
            enhanced_pos = token.get('rich_pos').split('|')[0].strip(' ')
            if enhanced_pos in rich_pos_error_mapper:
                enhanced_pos = rich_pos_error_mapper[enhanced_pos]
            token_data['enhanced_pos'] = enhanced_pos
            token_data['token'] = token.text
            sentence_data.append(token_data)
        all_sentence_data.append(sentence_data)
    return all_sentence_data

def collapse_sentences_to_tokens(sentence_data: list[list[dict[str, str]]]
                                 ) -> list[dict[str, str]]:
    '''
    :returns: converts a list of a list of token data into a list of token data.
              This therefore removes the sentence structure that the outer list 
              provided.
    '''
    token_data: list[dict[str, str]] = []
    for sentence in sentence_data:
        for token in sentence:
            token_data.append(token)
    return token_data
            

cytag_data_path = Path('.', 'cytag_output.xml').resolve()
cytag_data = read_cytag_data(cytag_data_path)

basic_to_core_pos_mapper_path = Path('.', 'basic_cy_tags_to_core_tags.json').resolve()
basic_to_core_pos_mapper = {}
with basic_to_core_pos_mapper_path.open('r') as basic_to_core_data:
    basic_to_core_pos_mapper = json.load(basic_to_core_data)

gold_data_path = Path('.', 'original_gold_standard_data.txt').resolve()
gold_data = read_gold_data(gold_data_path, basic_to_core_pos_mapper)

# Check that the gold token data aligns with the predicted.
gold_token_data = collapse_sentences_to_tokens(gold_data)
cytag_token_data = collapse_sentences_to_tokens(cytag_data)
assert len(gold_token_data) == len(cytag_token_data)
for gold_token, cytag_token in zip(gold_token_data, cytag_token_data):
    assert gold_token['token'] == cytag_token['token']

enhanced_gold_path = Path('.', 'enhanced_gold_standard_data.txt').resolve()
with enhanced_gold_path.open('w') as enhanced_fp:
    token_count = 0
    for sentence in gold_data:
        enhanced_token_data: list[str] = []
        for token in sentence:
            gold_token_data = token
            pred_token_data = cytag_token_data[token_count]
            token_string = (f'{gold_token_data["token"]}|{pred_token_data["lemma"]}|'
                            f'{token["core_pos"]}|{token["basic_pos"]}'
                            f'|{pred_token_data["enhanced_pos"]}'
                            f'|{gold_token_data["usas_tag"]}')
            enhanced_token_data.append(token_string)
            token_count += 1
        enhanced_fp.write(' '.join(enhanced_token_data))
        enhanced_fp.write('\n')