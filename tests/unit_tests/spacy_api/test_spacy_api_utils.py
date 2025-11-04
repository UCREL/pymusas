import pytest
from spacy.language import Language
from spacy.tokens import Doc, Token

from pymusas.spacy_api.utils import set_custom_token_extension, update_factory_attributes


@pytest.fixture
def create_test_component() -> str:
    component_name = "info_component"

    @Language.component(component_name)
    def my_component(doc: Doc) -> Doc:
        print(f"After tokenization, this doc has {len(doc)} tokens.")
        print("The part-of-speech tags are:", [token.pos_ for token in doc])
        if len(doc) < 10:
            print("This is a pretty short document.")
        return doc

    return component_name


def test_set_custom_token_extension() -> None:
    assert not Token.has_extension('tags')
    set_custom_token_extension('tags')
    assert Token.has_extension('tags')

    with pytest.warns(UserWarning):
        set_custom_token_extension('tags')


@pytest.mark.parametrize("meta_information_to_update",
                         ["assigns", "requires", "error"])
def test_update_factory_attributes(meta_information_to_update: str,
                                   create_test_component: str) -> None:
    
    if meta_information_to_update == 'error':
        with pytest.raises(ValueError):
            update_factory_attributes(meta_information_to_update,
                                      create_test_component,
                                      'token._.tag', 'token._.pos')
    else:
        factory_meta_data = Language.get_factory_meta(create_test_component)
        assert not getattr(factory_meta_data, meta_information_to_update)
        setattr(factory_meta_data, meta_information_to_update, ['token._.pos'])

        update_factory_attributes(meta_information_to_update,
                                  create_test_component,
                                  'token._.tag', 'token._.pos')
        assert getattr(factory_meta_data,
                       meta_information_to_update) == ['token._.tag']
