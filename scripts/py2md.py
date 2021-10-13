'''
A lot of this code has been copied and inspired from the AllenNLP code base.
Reference:
https://github.com/allenai/allennlp/blob/main/scripts/py2md.py
'''
import argparse
import os
import logging
from typing import Optional, Tuple, List, Dict
from pathlib import Path
from multiprocessing import Pool, cpu_count
import sys
import re

import docspec
from pydoc_markdown import PydocMarkdown
from pydoc_markdown.contrib.loaders.python import PythonLoader
from pydoc_markdown.contrib.renderers.docusaurus import DocusaurusRenderer, CustomizedMarkdownRenderer
from pydoc_markdown.contrib.processors.filter import FilterProcessor
from pydoc_markdown.contrib.processors.smart import SmartProcessor
from pydoc_markdown.contrib.processors.crossref import CrossrefProcessor
from pydoc_markdown.interfaces import Resolver

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class DocstringError(Exception):
    pass


class CustomResolver(Resolver):

    def resolve_ref(self, scope: docspec.ApiObject, ref: str) -> Optional[str]:
        print(f'scope: {scope.docstring}')
        print(f'ref: {ref}')
        return None


class CustomCrossrefProcess(CrossrefProcessor):

    def process(self, modules: List[docspec.Module],
                resolver: Optional[Resolver]) -> None:
        resolver = CustomResolver()
        super().process(modules, resolver)

    def _preprocess_refs(self, node: docspec.ApiObject, resolver: Resolver,
                         reverse: docspec.ReverseMap,
                         unresolved: Dict[str, List[str]]) -> None:
    
        if not node.docstring:
            return None

        def handler(match: re.Match) -> str:
            ref = match.group('ref')
            parens = match.group('parens') or ''
            trailing = (match.group('trailing') or '').lstrip('#')
            # Remove the dot from the ref if its trailing (it is probably just
            # the end of the sentence).
            has_trailing_dot = False
            if trailing and trailing.endswith('.'):
                trailing = trailing[:-1]
                has_trailing_dot = True
            elif not parens and ref.endswith('.'):
                ref = ref[:-1]
                has_trailing_dot = True
            href = resolver.resolve_ref(node, ref)
            if href:
                result = '[`{}`]({})'.format(ref + parens + trailing, href)
            else:
                uid = '.'.join(x.name for x in reverse.path(node))
                unresolved.setdefault(uid, []).append(ref)
                result = '`{}`'.format(ref + parens + trailing)
            # Add back the dot.
            if has_trailing_dot:
                result += '.'
            return result
        print(type(node.docstring))
        #docspec.Docstring(content="hello")
        #node.docstring = Docstring(re.sub(r'\B#(?P<ref>[\w\d\._]+)(?P<parens>\(\))?(?P<trailing>#[\w\d\._]+)?', handler, node.docstring))

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
