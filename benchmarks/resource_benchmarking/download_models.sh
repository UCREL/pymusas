spacy_models=(
    "en_core_web_sm"
    "zh_core_web_sm"
    "da_core_news_sm"
    "nl_core_news_sm"
    "fr_core_news_sm"
    "it_core_news_sm"
    "pt_core_news_sm"
    "es_core_news_sm"
    "fi_core_news_sm"
)

echo "Install the small spaCy models for all languages"
for spacy_model in "${spacy_models[@]}"; do
    uv pip install https://github.com/explosion/spacy-models/releases/download/${spacy_model}-3.8.0/${spacy_model}-3.8.0-py3-none-any.whl
done
echo "Finished installing the small spaCy models for all languages"

echo ""


pymusas_rule_based_models=(
    "en_dual_none_contextual_none"
    "cmn_dual_upos2usas_contextual_none"
    "da_dual_none_contextual_none"
    "nl_single_upos2usas_contextual_none"
    "fr_single_upos2usas_contextual_none"
    "it_dual_upos2usas_contextual_none"
    "pt_dual_upos2usas_contextual_none"
    "es_dual_upos2usas_contextual_none"
    "fi_single_upos2usas_contextual_none"
)
echo "Installing the rule based PyMUSAS models for all languages"
for pymusas_model in "${pymusas_rule_based_models[@]}"; do
    uv pip install https://github.com/UCREL/pymusas-models/releases/download/${pymusas_model}-0.4.0/${pymusas_model}-0.4.0-py3-none-any.whl
done
echo "Finished installing the rule based PyMUSAS models for all languages"

pymusas_neural_models=(
    "en_none_none_none_englishsmallbem"
    "en_none_none_none_englishbasebem"
    "xx_none_none_none_multilingualsmallbem"
    "xx_none_none_none_multilingualbasebem"
)
echo "Installing the neural PyMUSAS models for all languages"
for pymusas_model in "${pymusas_neural_models[@]}"; do
    uv pip install https://github.com/UCREL/pymusas-models/releases/download/${pymusas_model}-0.4.0/${pymusas_model}-0.4.0-py3-none-any.whl
done
echo "Finished installing the neural PyMUSAS models for all languages"
