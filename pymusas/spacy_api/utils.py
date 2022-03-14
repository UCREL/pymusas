'''
Helper functions for anything [spaCy](https://spacy.io/) related in the code
base.
'''

import copy
import warnings

from spacy.language import Language
from spacy.pipe_analysis import validate_attrs
from spacy.tokens import Token


def set_custom_token_extension(extension_name: str) -> None:
    '''
    Defines a custom attribute of the spaCy Token which becomes avaliable
    via `Token._.{extension_name}`. The difference between this and using the
    spaCy [Token.set_extension method](https://spacy.io/api/token#set_extension)
    is this method will check if the extension exists already and if so will force it
    through and output a log message that it has had to force this through.

    # Parameters

    extension_name : `str`
        Name of the custom attribute that will become avaliable through
        `Token._.{extension_name}`.
    '''
    if Token.has_extension(extension_name):
        old_extension = Token.get_extension(extension_name)
        Token.set_extension(extension_name, default=None, force=True)
        message = (f'Overwritten the spaCy Token extension `{extension_name}`'
                   ' which currently has the following (default, method, getter, setter):'
                   f'`{old_extension}`. And replacing it with the following:'
                   f'`{Token.get_extension(extension_name)}`'
                   '. This would only become a problem if the the two Tuples'
                   ' of four are different, if they are the same there is'
                   ' no problem.')
        warnings.warn(message)
    else:
        Token.set_extension(extension_name, default=None)


def update_factory_attributes(factory_name: str, new_attribute_name: str,
                              old_attribute_name: str) -> None:
    '''
    Updates the [spaCy Language required attributes meta information](https://spacy.io/api/language#factorymeta)
    for the given component, find through it's factory name,
    by replacing the `old_attribute_name` with the `new_attribute_name`.

    # Parameters

    factory_name : `str`
        The name of the component factory, e.g. `pymusas_rule_based_tagger`
    new_attribute_name : `str`
        The name of the new `{new_attribute_name}` attribute that is
        required for this component. An example, `token.pos`
    old_attribute_name : `str`
        The name of the `{old_attribute_name}` that is to be replaced with
        the `new_attribute_name`. An example, `token.tag`
    '''
    factory_meta = Language.get_factory_meta(factory_name)
    required_attributes = copy.deepcopy(factory_meta.requires)
    updated_attributes = [attribute for attribute in required_attributes
                          if attribute != old_attribute_name]
    updated_attributes.append(f'{new_attribute_name}')
    
    factory_meta.requires = validate_attrs(updated_attributes)
