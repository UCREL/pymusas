'''
A lot of this code has been copied and inspired from the AllenNLP code base.
Reference:
https://github.com/allenai/allennlp/blob/main/scripts/py2md.py
'''
import argparse
import logging
from multiprocessing import Pool, cpu_count
import os
from pathlib import Path
import re
import sys
from typing import Dict, List, Optional, Tuple

import docspec
from pydoc_markdown import PydocMarkdown
from pydoc_markdown.contrib.loaders.python import PythonLoader
from pydoc_markdown.contrib.processors.crossref import CrossrefProcessor
from pydoc_markdown.contrib.processors.filter import FilterProcessor
from pydoc_markdown.contrib.processors.smart import SmartProcessor
from pydoc_markdown.contrib.renderers.docusaurus import CustomizedMarkdownRenderer, DocusaurusRenderer
from pydoc_markdown.interfaces import Resolver


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


CROSS_REF_RE = re.compile("(:(class|func|mod):`~?([a-zA-Z0-9_.]+)`)")
BASE_MODULE = 'pymusas'
API_BASE_URL = '/pymusas/docs/API/'


class DocstringError(Exception):
    pass


class CustomCrossrefProcess(CrossrefProcessor):

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


def py2md(module: str, out: Optional[str] = None) -> bool:
    """
    Returns `True` if module successfully processed, otherwise `False`.
    """
    logger.debug(f"Processing {module}")
    custom_markdown_renderer = CustomizedMarkdownRenderer(filename=out,
                                                          add_method_class_prefix=False,
                                                          add_member_class_prefix=False,
                                                          data_code_block=True,
                                                          signature_with_def=True,
                                                          use_fixed_header_levels=True,
                                                          render_module_header=False,
                                                          descriptive_class_title=False,)
    pydocmd = PydocMarkdown(
        loaders=[PythonLoader(modules=[module])],
        processors=[FilterProcessor(skip_empty_modules=True), SmartProcessor(), CustomCrossrefProcess()],
        renderer=DocusaurusRenderer(
            custom_markdown_renderer,
            docs_base_path='docs/docs',
            relative_output_path='API',
            relative_sidebar_path='sidebar.json',
            sidebar_top_level_label='Reference',
        ),
    )
    if out:
        out_path = Path(out)
        os.makedirs(out_path.parent, exist_ok=True)

    a = pydocmd.load_modules()
    try:
        pydocmd.process(a)
    except DocstringError as err:
        logger.exception(f"Failed to process {module}.\n{err}")
        return False
    pydocmd.render(a)
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
