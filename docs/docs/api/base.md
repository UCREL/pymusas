<div className="source-div">
 <p><i>pymusas</i><strong>.base</strong></p>
 <p><a className="sourcelink" href="https://github.com/UCREL/pymusas/blob/main/pymusas/base.py">[SOURCE]</a></p>
</div>
<div></div>

---

Base classes for custom classes to inherit from.

<a id="pymusas.base.Serialise"></a>

## Serialise

```python
class Serialise(ABC)
```

An **abstract class** that defines the basic methods, `to_bytes`, and
`from_bytes` that is required for all [`Serialise`](#serialise)s.

<a id="pymusas.base.Serialise.to_bytes"></a>

### to\_bytes

```python
class Serialise(ABC):
 | ...
 | @abstractmethod
 | def to_bytes() -> bytes
```

Serialises the class to a bytestring.

<h4 id="to_bytes.returns">Returns<a className="headerlink" href="#to_bytes.returns" title="Permanent link">&para;</a></h4>


- `bytes` <br/>

<a id="pymusas.base.Serialise.from_bytes"></a>

### from\_bytes

```python
class Serialise(ABC):
 | ...
 | @staticmethod
 | @abstractmethod
 | def from_bytes(bytes_data: bytes) -> "Serialise"
```

Loads the class from the given bytestring and returns it.

<h4 id="from_bytes.parameters">Parameters<a className="headerlink" href="#from_bytes.parameters" title="Permanent link">&para;</a></h4>


- __bytes\_data__ : `bytes` <br/>
    The bytestring to load.

<h4 id="from_bytes.returns">Returns<a className="headerlink" href="#from_bytes.returns" title="Permanent link">&para;</a></h4>


- [`Serialise`](#serialise) <br/>

<a id="pymusas.base.Serialise.serialise_object_to_bytes"></a>

### serialise\_object\_to\_bytes

```python
class Serialise(ABC):
 | ...
 | @staticmethod
 | def serialise_object_to_bytes(
 |     serialise_object: "Serialise"
 | ) -> bytes
```

Given a serialise object it will serialise it to a bytestring.

This function in comparison to calling `to_bytes` on the serialise
object saves meta data about what class it is so that when loading the
bytes data later on you will know which class saved the data, this
would not happen if you called `to_bytes` on the custom object.

<h4 id="serialise_object_to_bytes.parameters">Parameters<a className="headerlink" href="#serialise_object_to_bytes.parameters" title="Permanent link">&para;</a></h4>


- __serialise\_object__ : `Serialise` <br/>
    The serialise object, of type [`Serialise`](#serialise), to serialise.

<h4 id="serialise_object_to_bytes.returns">Returns<a className="headerlink" href="#serialise_object_to_bytes.returns" title="Permanent link">&para;</a></h4>


- `bytes` <br/>

<a id="pymusas.base.Serialise.serialise_object_from_bytes"></a>

### serialise\_object\_from\_bytes

```python
class Serialise(ABC):
 | ...
 | @staticmethod
 | def serialise_object_from_bytes(
 |     bytes_data: bytes
 | ) -> "Serialise"
```

Loads the serialise object from the given bytestring and return it.
This is the inverse of function of [`serialise_object_to_bytes`](#serialise_object_to_bytes).

<h4 id="serialise_object_from_bytes.parameters">Parameters<a className="headerlink" href="#serialise_object_from_bytes.parameters" title="Permanent link">&para;</a></h4>


- __bytes\_data__ : `bytes` <br/>
    The bytestring to load.

<h4 id="serialise_object_from_bytes.returns">Returns<a className="headerlink" href="#serialise_object_from_bytes.returns" title="Permanent link">&para;</a></h4>


- `Serialise` <br/>

<a id="pymusas.base.Serialise.serialise_object_list_to_bytes"></a>

### serialise\_object\_list\_to\_bytes

```python
class Serialise(ABC):
 | ...
 | @staticmethod
 | def serialise_object_list_to_bytes(
 |     serialise_objects: Iterable["Serialise"]
 | ) -> bytes
```

Serialises an `Iterable` of serialise objects in the same way as
[`serialise_object_to_bytes`](#serialise_object_to_bytes).

<h4 id="serialise_object_list_to_bytes.parameters">Parameters<a className="headerlink" href="#serialise_object_list_to_bytes.parameters" title="Permanent link">&para;</a></h4>


- __serialise\_objects__ : `Iterable[Serialise]` <br/>
    The serialise objects, of type [`Serialise`](#serialise), to serialise.

<h4 id="serialise_object_list_to_bytes.returns">Returns<a className="headerlink" href="#serialise_object_list_to_bytes.returns" title="Permanent link">&para;</a></h4>


- `bytes` <br/>

<a id="pymusas.base.Serialise.serialise_object_list_from_bytes"></a>

### serialise\_object\_list\_from\_bytes

```python
class Serialise(ABC):
 | ...
 | @staticmethod
 | def serialise_object_list_from_bytes(
 |     bytes_data: bytes
 | ) -> Iterable["Serialise"]
```

Loads the serialise objects from the given bytestring and return them.
This is the inverse of function of
[`serialise_object_list_to_bytes`](#serialise_object_list_to_bytes).

<h4 id="serialise_object_list_from_bytes.parameters">Parameters<a className="headerlink" href="#serialise_object_list_from_bytes.parameters" title="Permanent link">&para;</a></h4>


- __bytes\_data__ : `bytes` <br/>
    The bytestring to load.

<h4 id="serialise_object_list_from_bytes.returns">Returns<a className="headerlink" href="#serialise_object_list_from_bytes.returns" title="Permanent link">&para;</a></h4>


- `Iterable[Serialise]` <br/>

