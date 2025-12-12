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
    Defines a custom attribute of the spaCy Token which becomes available
    via `Token._.{extension_name}`. The difference between this and using the
    spaCy [Token.set_extension method](https://spacy.io/api/token#set_extension)
    is this method will check if the extension exists already and if so will force it
    through and output an UserWarning message that it has had to force this through.

    # Parameters

    extension_name : `str`
        Name of the custom attribute that will become available through
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


def remove_custom_token_extension(extension_name: str) -> None:
    """
    Removes a custom attribute of the spaCy Token if it exists already. This
    custom attribute would be accessed via `Token._.{extension_name}`.

    # Parameters

    extension_name : `str`
        Name of the custom attribute to remove from the spaCy Token if it
        exists already.

    # Returns

    `None`
    """
    if Token.has_extension(extension_name):
        Token.remove_extension(extension_name)


def update_factory_attributes(meta_information_to_update: str,
                              factory_name: str,
                              new_attribute_name: str,
                              old_attribute_name: str) -> None:
    '''
    Updates the
    [spaCy Language meta information](https://spacy.io/api/language#factorymeta)
    for either `assigns` or `requires` for the given component, find through
    it's factory name, by replacing the `old_attribute_name` with the
    `new_attribute_name`.

    # Parameters

    meta_information_to_update : `str`
        Either `assigns` or `requires`, raises a ValueError if it is any other
        value.
    factory_name : `str`
        The name of the component factory, e.g. `pymusas_rule_based_tagger`
    new_attribute_name : `str`
        The name of the new attribute that is required for this component.
        An example, `token.pos`.
    old_attribute_name : `str`
        The name of the old attribute that is to be replaced with
        the `new_attribute_name`. An example, `token.tag`.
    '''
    value_error = ('`meta_information_to_update` has to be either `assigns` '
                   f'or `requires` and not {meta_information_to_update}')
    if meta_information_to_update not in set(['assigns', 'requires']):
        raise ValueError(value_error)

    factory_meta = Language.get_factory_meta(factory_name)
    required_attributes = copy.deepcopy(getattr(factory_meta,
                                                meta_information_to_update))
    updated_attributes = [attribute for attribute in required_attributes
                          if attribute != old_attribute_name]
    updated_attributes.append(f'{new_attribute_name}')
    
    setattr(factory_meta, meta_information_to_update,
            validate_attrs(updated_attributes))
