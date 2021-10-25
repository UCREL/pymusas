from pathlib import Path

welsh_gold_path = Path('.', 'original_gold_standard_data.txt').resolve()
just_text_path = Path('.', 'txt_gold_standard_data.txt').resolve()

with just_text_path.open('w') as write_fp:
    with welsh_gold_path.open('r') as read_fp:
        for line in read_fp:
            all_tokens = [token_data.split('|')[0] for token_data in line.split()]
            write_fp.write(' '.join(all_tokens))
            write_fp.write('\n')