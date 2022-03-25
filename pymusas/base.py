"""
Base classes for custom classes to inherit from.
"""

from abc import ABC, abstractmethod
import importlib
from typing import Iterable, List, cast

import srsly


class Serialise(ABC):
    '''
    An **abstract class** that defines the basic methods, `to_bytes`, and
    `from_bytes` that is required for all :class:`Serialise`s.
    '''
    @abstractmethod
    def to_bytes(self) -> bytes:
        '''
        Serialises the class to a bytestring.

        # Returns

        `bytes`
        '''
        ...  # pragma: no cover

    @staticmethod
    @abstractmethod
    def from_bytes(bytes_data: bytes) -> "Serialise":
        '''
        Loads the class from the given bytestring and returns it.

        # Parameters

        bytes_data : `bytes`
            The bytestring to load.
        
        # Returns

        :class:`Serialise`
        '''
        ...  # pragma: no cover

    @staticmethod
    def serialise_object_to_bytes(serialise_object: "Serialise"
                                  ) -> bytes:
        '''
        Given a serialise object it will serialise it to a bytestring.

        This function in comparison to calling `to_bytes` on the serialise
        object saves meta data about what class it is so that when loading the
        bytes data later on you will know which class saved the data, this
        would not happen if you called `to_bytes` on the custom object.

        # Parameters

        serialise_object : `Serialise`
            The serialise object, of type :class:`Serialise`, to serialise.

        # Returns

        `bytes`
        '''
        class_name = serialise_object.__class__.__name__
        module_name = serialise_object.__module__
        serialised_object = serialise_object.to_bytes()
        serialised_object_and_meta_data \
            = (serialised_object, (class_name, module_name))
        return cast(bytes, srsly.msgpack_dumps(serialised_object_and_meta_data))

    @staticmethod
    def serialise_object_from_bytes(bytes_data: bytes) -> "Serialise":
        '''
        Loads the serialise object from the given bytestring and return it.
        This is the inverse of function of :func:`serialise_object_to_bytes`.

        # Parameters

        bytes_data : `bytes`
            The bytestring to load.

        # Returns

        `Serialise`
        '''
        serialised_custom_object, meta_data = srsly.msgpack_loads(bytes_data)
        class_name, module_name = meta_data
        custom_object_class: Serialise \
            = getattr(importlib.import_module(module_name), class_name)
        return custom_object_class.from_bytes(serialised_custom_object)

    @staticmethod
    def serialise_object_list_to_bytes(serialise_objects: Iterable["Serialise"]
                                       ) -> bytes:
        '''
        Serialises an `Iterable` of serialise objects in the same way as
        :func:`serialise_object_to_bytes`.

        # Parameters

        serialise_objects : `Iterable[Serialise]`
            The serialise objects, of type :class:`Serialise`, to serialise.

        # Returns

        `bytes`
        '''
        serialised_objects: List[bytes] = []
        for serialise_object in serialise_objects:
            serialised_object \
                = Serialise.serialise_object_to_bytes(serialise_object)
            serialised_objects.append(serialised_object)
        return cast(bytes, srsly.msgpack_dumps(serialised_objects))

    @staticmethod
    def serialise_object_list_from_bytes(bytes_data: bytes
                                         ) -> Iterable["Serialise"]:
        '''
        Loads the serialise objects from the given bytestring and return them.
        This is the inverse of function of
        :func:`serialise_object_list_to_bytes`.

        # Parameters

        bytes_data : `bytes`
            The bytestring to load.

        # Returns

        `Iterable[Serialise]`
        '''
        serialised_objects: List[bytes] = srsly.msgpack_loads(bytes_data)
        serialise_objects: List[Serialise] = []
        for serialised_object in serialised_objects:
            serialise_object \
                = Serialise.serialise_object_from_bytes(serialised_object)
            serialise_objects.append(serialise_object)
        return serialise_objects
