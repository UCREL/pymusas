import csv
from pathlib import Path

import typer
from typing_extensions import Annotated
import spacy
import xlsxwriter

def main(spacy_model_name: str,
         text_to_tag_file_path: Annotated[Path,
                                          typer.Argument(exists=True, file_okay=True, dir_okay=False, readable=True)],
         tagged_text_output_file_path: Annotated[Path,
                                          typer.Argument(dir_okay=False)],
         excel_format: bool = False) -> None:
    # We exclude the following components as we do not need them. 
    nlp = spacy.load(spacy_model_name, exclude=['parser', 'ner'])
    # Load the Chinese PyMUSAS rule-based tagger in a separate spaCy pipeline
    chinese_tagger_pipeline = spacy.load('cmn_dual_upos2usas_contextual')
    # Adds the Chinese PyMUSAS rule-based tagger to the main spaCy pipeline
    nlp.add_pipe('pymusas_rule_based_tagger', source=chinese_tagger_pipeline)

    with text_to_tag_file_path.open('r', encoding='utf-8') as text_fp:
        fieldnames = ['Token', 'POS', 'Predicted-USAS', 'Corrected-USAS', 'Errors', 'Notes']
        if not excel_format:
            with tagged_text_output_file_path.open('w', encoding='utf-8', newline='') as csv_fp:
                tsv_writer = csv.DictWriter(csv_fp, fieldnames=fieldnames, dialect='excel-tab', delimiter='\t')
                tsv_writer.writeheader()
                for line in text_fp:
                    line = line.strip()
                    if not line:
                        continue
                    output_doc = nlp(line)
                    for token in output_doc:
                        token_text = token.text
                        pos_tag = token.pos_
                        usas_tags = token._.pymusas_tags
                        formatted_usas_tags = '; '.join(usas_tags).strip(" ")
                        tsv_writer.writerow({
                            'Token': token_text,
                            'POS': pos_tag,
                            'Predicted-USAS': formatted_usas_tags
                        })
        else:
            with xlsxwriter.Workbook(str(tagged_text_output_file_path.resolve())) as excel_workbook:
                worksheet = excel_workbook.add_worksheet()
                bold = excel_workbook.add_format({'bold': 1})

                for field_index, field_name in enumerate(fieldnames):
                    worksheet.write(0, field_index, field_name, bold)
                    worksheet.set_column(field_index, field_index, len(field_name) + 2)
                row = 1
                for line in text_fp:
                    line = line.strip()
                    if not line:
                        continue
                    output_doc = nlp(line)
                    for token in output_doc:
                        token_text = token.text
                        pos_tag = token.pos_
                        usas_tags = token._.pymusas_tags
                        formatted_usas_tags = '; '.join(usas_tags).strip(" ")
                        worksheet.write_string(row, 0, token_text)
                        worksheet.write_string(row, 1, pos_tag)
                        worksheet.write_string(row, 2, formatted_usas_tags)
                        worksheet.write_blank(row, 3, None)
                        worksheet.write_blank(row, 4, None)
                        row += 1

            
if __name__ == "__main__":
    typer.run(main)