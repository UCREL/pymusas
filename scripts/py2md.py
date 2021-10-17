'''
A lot of this code has been copied and inspired from the AllenNLP code base.
Reference:
https://github.com/allenai/allennlp/blob/main/scripts/py2md.py
'''
import argparse
import dataclasses
import logging
from multiprocessing import Pool, cpu_count
import os
from pathlib import Path
import re
import sys
from typing import Dict, List, Optional, TextIO, Tuple

import databind.core.annotations as A
import docspec
from pydoc_markdown import PydocMarkdown
from pydoc_markdown.contrib.loaders.python import PythonLoader
from pydoc_markdown.contrib.processors.crossref import CrossrefProcessor
from pydoc_markdown.contrib.processors.smart import SmartProcessor
from pydoc_markdown.contrib.renderers.docusaurus import CustomizedMarkdownRenderer, MarkdownRenderer
from pydoc_markdown.interfaces import Processor, Renderer, Resolver
from pydoc_markdown.util.docspec import format_function_signature, is_method
import typing_extensions as te


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


CROSS_REF_RE = re.compile("(:(class|func|mod):`~?([a-zA-Z0-9_.]+)`)")
BASE_MODULE = 'pymusas'
API_BASE_URL = '/pymusas/docs/API/'
BASE_SOURCE_LINK = "https://github.com/UCREL/pymusas/blob/main/pymusas/"


class AllenNlpRenderer(MarkdownRenderer):
    '''
    This is a custom version of the
    [AllenNLPRenderer](https://github.com/allenai/allennlp/blob/main/scripts/py2md.py#L317),
    vast majority of this code has come from the original AllenNLPRenderer.
    '''
    
    @staticmethod
    def dotted_name(obj: docspec.ApiObject) -> str:
        return '.'.join(x.name for x in obj.path)

    def _is_method(self, obj: docspec.ApiObject) -> bool:
        return is_method(obj, self._resolver.reverse_map) # type: ignore  # noqa

    def _get_parent(self, obj: docspec.ApiObject) -> Optional[docspec.ApiObject]:
        '''
        This never gets called. As `signature_class_prefix` is False.
        '''
        return self._resolver.reverse_map.get_parent(obj) # type: ignore  # noqa

    def format_arglist_list(self, args: List[docspec.Argument],
                            render_type_hints: bool = True) -> List[str]:
        """
        Formats a Python argument list.
        """
        result = []

        for arg in args:
            parts = []
            if arg.type == docspec.Argument.Type.KEYWORD_ONLY and '*' not in result:
                result.append('*')
            parts = [arg.name]
            if arg.datatype and render_type_hints:
                parts.append(': ' + arg.datatype)
            if arg.default_value:
                if arg.datatype:
                    parts.append(' ')
                parts.append('=')
            if arg.default_value:
                if arg.datatype:
                    parts.append(' ')
                parts.append(arg.default_value)
            if arg.type == docspec.Argument.Type.POSITIONAL_REMAINDER:
                parts.insert(0, '*')
            elif arg.type == docspec.Argument.Type.KEYWORD_REMAINDER:
                parts.insert(0, '**')
            result.append(''.join(parts))
        return result

    def _format_function_signature(self, func: docspec.Function,
                                   override_name: Optional[str] = None,
                                   add_method_bar: bool = True,
                                   include_parent_class: bool = True,
                                   ) -> str:
        '''
        This formats both functions and methods.
        '''
        parts = []
        if func.decorations:
            for dec in func.decorations:
                dec_args = dec.args if dec.args is not None else ""
                parts.append(f"@{dec.name}{dec_args}\n")
        if self.signature_python_help_style and not self._is_method(func):
            parts.append('{} = '.format(self.dotted_name(func)))
        parts += [x + ' ' for x in func.modifiers or []]
        if self.signature_with_def:
            parts.append("def ")
        if self.signature_class_prefix and self._is_method(func):
            parent = self._get_parent(func)
            assert parent, func
            parts.append(parent.name + '.')
        parts.append((override_name or func.name))
        func_signature = format_function_signature(func, self._is_method(func))
        if (len(parts[-1]) + len(func_signature) > 60):
            func_args_strings = self.format_arglist_list(func.args)
            signature_args = ",\n    ".join(
                filter(lambda s: s.strip() not in ("", ","), func_args_strings)
            )
            parts.append("(\n    " + signature_args + "\n)")
            if func.return_type:
                parts.append(f' -> {func.return_type}')
        else:
            parts.append(func_signature)
        result = "".join(parts)
        if add_method_bar and self._is_method(func):
            result = "\n".join(" | " + line for line in result.split("\n"))
            if include_parent_class:
                parent_class: docspec.Class = func.parent # type: ignore  # noqa
                bases = ''
                if parent_class.bases is not None:
                    bases = ", ".join(map(str, parent_class.bases))
                if parent_class.metaclass is not None:
                    bases += ", metaclass=" + str(parent_class.metaclass)
                if bases:
                    class_signature = f"class {parent_class.name}({bases})"
                else:
                    class_signature = f"class {parent_class.name}"
                result = f"{class_signature}:\n | ...\n{result}"
        return result
    
    def _format_data_signature(self, data: docspec.Data) -> str:
        '''
        Format for anything that is not a function, module, or class e.g.
        Global variables.
        '''
        expr = str(data.value)
        if len(expr) > self.data_expression_maxlength:
            expr = expr[: self.data_expression_maxlength] + " ..."
        
        if data.datatype is not None:
            signature = f"{data.name}: {data.datatype} = {expr}"
        else:
            signature = f"{data.name} = {expr}"

        if data.parent and isinstance(data.parent, docspec.Class):
            bases = ''
            if data.parent.bases is not None:
                bases = ", ".join(map(str, data.parent.bases))
            if data.parent.metaclass:
                bases += ", metaclass=" + str(data.parent.metaclass)
            if bases:
                class_signature = f"class {data.parent.name}({bases})"
            else:
                class_signature = f"class {data.parent.name}"
            return f"{class_signature}:\n | ...\n | {signature}"
        else:
            return signature

    def _format_classdef_signature(self, cls: docspec.Class) -> str:
        code = ""
        if cls.decorations is not None:
            for dec in cls.decorations:
                dec_args = dec.args if dec.args is not None else ""
                code += f"@{dec.name}{dec_args}\n"
        bases = ''
        if cls.bases is not None:
            bases = ", ".join(map(str, cls.bases))
        if cls.metaclass:
            bases += ", metaclass=" + str(cls.metaclass)
        if bases:
            code += f"class {cls.name}({bases})"
        else:
            code += f"class {cls.name}"
        if self.signature_python_help_style:
            code = self.dotted_name(cls) + ' = ' + code

        if self.classdef_render_init_signature_if_needed:
            for member in cls.members:
                if member.name == '__init__':
                    assert isinstance(member, docspec.Function)
                    code = self._format_function_signature(member, add_method_bar=True)
                    break
        return code

    def _render_module_breadcrumbs(self, fp: TextIO, mod: docspec.Module) -> None:
        submods = mod.name.split(".")
        breadcrumbs = []
        for i, submod_name in enumerate(submods):
            if i == 0:
                title = f"<i>{submod_name}</i>"
            elif i == len(submods) - 1:
                title = f"<strong>.{submod_name}</strong>"
            else:
                title = f"<i>.{submod_name}</i>"
            breadcrumbs.append(title)
        "/".join(submods[1:])
        source_link = BASE_SOURCE_LINK + "/".join(submods[1:]) + ".py"
        fp.write(
            '<div className="source-div">\n'
            ' <p>' + "".join(breadcrumbs) + "</p>\n"
            f' <p><a className="sourcelink" href="{source_link}">[SOURCE]</a></p>\n'
            "</div>\n"
            '<div></div>\n\n---\n\n'
        )

    def _render_object(self, fp: TextIO, level: int, obj: docspec.ApiObject) -> None:
        '''
        # Parameters

        level : `int`
            The header level to assign to the object. e.g. if it is Module then
            the level will be 1 and if it was a function it would be 4.
        '''
        if obj.name == '__init__':
            return None
        if not isinstance(obj, docspec.Module) or self.render_module_header:
            self._render_header(fp, level, obj)
        if isinstance(obj, docspec.Module):
            self._render_module_breadcrumbs(fp, obj)
        self._render_signature_block(fp, obj)
        if obj.docstring:
            lines = obj.docstring.split("\n")
            if self.docstrings_as_blockquote:
                lines = ["> " + x for x in lines]
            fp.write("\n".join(lines))
            fp.write("\n\n")


@dataclasses.dataclass
class CustomDocusaurusRenderer(Renderer):
    """
    This is a simpler version of the original
    [DocusaurusRenderer.](https://github.com/NiklasRosenstein/pydoc-markdown/
    blob/develop/src/pydoc_markdown/contrib/renderers/docusaurus.py#L40)
    """

    #: The #MarkdownRenderer configuration.
    markdown: te.Annotated[MarkdownRenderer, A.typeinfo(deserialize_as=CustomizedMarkdownRenderer)] = \
        dataclasses.field(default_factory=CustomizedMarkdownRenderer)

    #: The path where the docusaurus docs content is. Defaults "docs" folder.
    docs_base_path: str = 'docs'

    #: The output path inside the docs_base_path folder, used to output the
    #: module reference.
    relative_output_path: str = 'reference'

    def render(self, modules: List[docspec.Module]) -> None:
        output_path = Path(self.docs_base_path) / self.relative_output_path
        for module in modules:
            filepath = output_path

            module_parts = module.name.split(".")
            if module.location is not None:
                if module.location.filename is not None:
                    if module.location.filename.endswith("__init__.py"):
                        module_parts.append("__init__")

            for module_part in module_parts[1:-1]:

                # descend to the file
                filepath = filepath / module_part

            # create intermediary missing directories and get the full path
            filepath.mkdir(parents=True, exist_ok=True)
            filepath = filepath / f"{module_parts[-1]}.md"

            with filepath.open('w') as fp:
                logger.info(f"Render file {filepath}")
                self.markdown.render_to_stream([module], fp)


class DocstringError(Exception):
    pass


class CustomCrossrefProcess(CrossrefProcessor):
    '''
    Combination of the [cross ref processor](https://github.com/
    NiklasRosenstein/pydoc-markdown/blob/6535ad5a06252c87dc7f03e8e900689d
    84712c04/src/pydoc_markdown/contrib/processors/crossref.py) and the
    [AllenNLP version](https://github.com/allenai/allennlp/blob/main/scripts/py2md.py#L174)
    '''

    def process(self, modules: List[docspec.Module],
                resolver: Optional[Resolver]) -> None:
        if len(modules) > 0:
            reverse = docspec.ReverseMap(modules)
            unresolved: Dict[str, List[str]] = {}
            resolver = None
            docspec.visit(modules, lambda x: self._preprocess_refs(x, resolver, reverse, unresolved)) # type: ignore  # noqa

    def _preprocess_refs(self, node: docspec.ApiObject, resolver: Resolver,
                         reverse: docspec.ReverseMap,
                         unresolved: Dict[str, List[str]]) -> None:
    
        if not node.docstring:
            return None

        doc_string = str(node.docstring)
        for match, ty, name in CROSS_REF_RE.findall(doc_string):
            if name.startswith(f"{BASE_MODULE}."):
                path = name.split(".")
                if ty == "mod":
                    href = API_BASE_URL + "/".join(path[1:])
                else:
                    href = API_BASE_URL + "/".join(path[1:-1]) + "/#" + path[-1].lower()
                cross_ref = f"[`{path[-1]}`]({href})"
            elif "." not in name:
                cross_ref = f"[`{name}`](#{name.lower()})"
            else:
                cross_ref = f"`{name}`"
            doc_string = doc_string.replace(match, cross_ref)

        node.docstring = docspec.Docstring(content=doc_string, location=None)


@dataclasses.dataclass
class CustomFilterProcessor(Processor):
    '''
    Custom version of the [standard filter](https://github.com/NiklasRosenstein/
    pydoc-markdown/blob/6535ad5a06252c87dc7f03e8e900689d84712c04/src/
    pydoc_markdown/contrib/processors/filter.py)
    '''

    expression: Optional[str] = None

    #: Keep only API objects that have docstrings. Default: `true`
    documented_only: bool = True

    #: Exclude API objects that appear to be private members (i.e. their name begins with
    #: and underscore but does not end with one). Default: `true`
    exclude_private: bool = True

    #: Exclude special members (e.g.` __path__`, `__annotations__`, `__name__` and `__all__`).
    #: Default: `true`
    exclude_special: bool = True

    #: Do not filter #docspec.Module objects. Default: `true`
    do_not_filter_modules: bool = True

    #: Skip modules with no content. Default: `false`.
    skip_empty_modules: bool = False

    SPECIAL_MEMBERS = ('__path__', '__annotations__', '__name__', '__all__')
    INCLUDED_MEMBERS = ('__init__')

    def process(self, modules: List[docspec.Module], resolver: Optional[Resolver]) -> None:
        def m(obj: docspec.ApiObject) -> bool:
            return self._match(obj)
        docspec.filter_visit(modules, m, order='post') # type: ignore  # noqa

    def _match(self, obj: docspec.ApiObject) -> bool:
        members = getattr(obj, 'members', [])

        def _check() -> bool:
            if obj.name in self.INCLUDED_MEMBERS:
                return True
            if members:
                return True
            if self.skip_empty_modules and isinstance(obj, docspec.Module) and not members:
                return False
            if self.do_not_filter_modules and isinstance(obj, docspec.Module):
                return True
            if self.documented_only and not obj.docstring:
                return False
            if self.exclude_private and obj.name.startswith('_') and not obj.name.endswith('_'):
                return False
            if self.exclude_special and obj.name in self.SPECIAL_MEMBERS:
                return False
            return True

        if self.expression:
            scope = {'name': obj.name, 'obj': obj, 'default': _check}
            return bool(eval(self.expression, scope))  # pylint: disable=eval-used
        return _check()


def py2md(module: str, out: Optional[str] = None) -> bool:
    """
    Returns `True` if module successfully processed, otherwise `False`.
    """
    logger.debug(f"Processing {module}")
    header_level = {'Module': 1, 'Class': 2, 'Method': 3, 'Function': 3, 'Data': 4}
    custom_markdown_renderer = AllenNlpRenderer(filename=out,
                                                signature_with_vertical_bar=True,
                                                header_level_by_type=header_level,
                                                add_method_class_prefix=False,
                                                add_member_class_prefix=False,
                                                data_code_block=True,
                                                signature_with_def=True,
                                                use_fixed_header_levels=True,
                                                render_module_header=False,
                                                descriptive_class_title=False,)
    filter_instance = CustomFilterProcessor(skip_empty_modules=True, documented_only=True)
    pydocmd_processors = [filter_instance, SmartProcessor(), CustomCrossrefProcess()]
    pydocmd_renderer = CustomDocusaurusRenderer(custom_markdown_renderer,
                                                docs_base_path='docs/docs',
                                                relative_output_path='api',)
    pydocmd = PydocMarkdown(loaders=[PythonLoader(modules=[module])],
                            processors=pydocmd_processors,
                            renderer=pydocmd_renderer,)
    if out:
        out_path = Path(out)
        os.makedirs(out_path.parent, exist_ok=True)

    modules = pydocmd.load_modules()
    try:
        pydocmd.process(modules)
    except DocstringError as err:
        logger.exception(f"Failed to process {module}.\n{err}")
        return False
    pydocmd.render(modules)
    return True


def _py2md_wrapper(x: Tuple[str, str]) -> bool:
    """
    Used to wrap py2md since we can't pickle a lambda (needed for multiprocessing).
    """
    return py2md(x[0], x[1])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("modules", nargs="+", type=str, help="""The Python modules to parse.""")
    parser.add_argument(
        "-o",
        "--out",
        nargs="+",
        type=str,
        help="""Output files.
                If given, must have the same number of items as 'modules'.
                If not given, stdout is used.""",
    )
    return parser.parse_args()


def main() -> None:
    opts = parse_args()
    outputs = opts.out if opts.out else [None] * len(opts.modules)
    if len(outputs) != len(opts.modules):
        raise ValueError("Number inputs and outputs should be the same.")
    n_threads = cpu_count()
    errors: int = 0
    if len(opts.modules) > n_threads and opts.out:
        # If writing to files, can process in parallel.
        chunk_size = max([1, int(len(outputs) / n_threads)])
        logger.info(f"Using {n_threads} threads")
        with Pool(n_threads) as p:
            for result in p.imap(_py2md_wrapper, zip(opts.modules, outputs), chunk_size):
                if not result:
                    errors += 1
    else:
        # If writing to stdout, need to process sequentially. Otherwise the output
        # could get intertwined.
        for module, out in zip(opts.modules, outputs):
            result = py2md(module, out)
            if not result:
                errors += 1
    logger.info(f"Processed {len(opts.modules)} modules")
    if errors:
        logger.error(f"Found {errors} errors")
        sys.exit(1)


if __name__ == "__main__":
    main()
