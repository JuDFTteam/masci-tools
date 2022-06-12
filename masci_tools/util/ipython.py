"""
Import this module to activate useful ipython extensions
"""
from __future__ import annotations

from lxml import etree
from pygments import highlight
from pygments.lexers import XmlLexer  #pylint: disable=no-name-in-module
from pygments.formatters import HtmlFormatter  #pylint: disable=no-name-in-module

from masci_tools.util.typing import XMLLike
from typing import Any
import difflib
from IPython.display import HTML  #pylint: disable=import-error


def display_xml(data: XMLLike) -> str:
    """
    Display the given lxml XML tree as formatted HTML

    :param data: data to show

    :returns: HTML string for presentation in Jupyter notebooks
    """

    xmlstring = etree.tostring(data, encoding='unicode', pretty_print=True)
    return highlight(xmlstring, XmlLexer(), HtmlFormatter(noclasses=True, nobackground=False))


def xml_diff(old: XMLLike, new: XMLLike, indent: bool = True) -> HTML:
    """
    Create a diff of two lxml trees with HTML with syntax highlighting

    :param old: original XML tree
    :param new: modified XML tree
    :param indent: bool, if True etree.indent is called on the trees before diff
    """

    STYLES = {
        'control': 'font-weight: bold',
        'delete': 'background-color: hsla(0, 100%, 74%, 0.5); color: #000000;',
        'delete-detail': 'background-color: hsla(0, 100%, 74%, 0.5); color: #000000;',
        'insert': 'background-color: hsla(102, 100%, 74%, 0.5); color: #000000;',
        'insert-detail': 'background-color: hsla(102, 100%, 74%, 0.5); color: #000000;',
    }

    if indent:
        etree.indent(old)
        etree.indent(new)

    old_lines = etree.tostring(old, encoding='unicode', pretty_print=True).split('\n')
    new_lines = etree.tostring(new, encoding='unicode', pretty_print=True).split('\n')

    lines = list(difflib.unified_diff(old_lines, new_lines))

    for index, line in enumerate(lines):
        if line.startswith('@@'):
            first_block = index
            break

    lines = lines[first_block:]
    lines.reverse()

    diff_blocks: list[str] = []
    current_block: list[str] = []

    def highlight_xml(xmlstring):
        return highlight(xmlstring, XmlLexer(), HtmlFormatter(noclasses=True, nowrap=True)).rstrip('\n')

    def _line_diff(a, b):

        a, b = highlight_xml(a), highlight_xml(b)
        aline = []
        bline = []
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b).get_opcodes():
            if tag == 'equal':
                aline.append(a[i1:i2])
                bline.append(b[j1:j2])
                continue
            aline.append(f'<span style="{STYLES["delete-detail"]}">{a[i1:i2]}</span>')
            bline.append(f'<span style="{STYLES["insert-detail"]}">{b[j1:j2]}</span>')
        return ''.join(aline), ''.join(bline)

    while lines:
        line = lines.pop()
        if line.startswith('@@') or not lines:
            line = line.strip('\n@- ').replace(',', ' (')
            original, _, changed = line.partition('+')
            control_lines = [f'Original: line {original} lines)', f'Changed line {changed} lines)']

            if len(current_block) == 0:
                current_block = [f'<span style="{STYLES["control"]}"> {line}</span>' for line in control_lines]
            else:
                current_block.append('<span></span>')
                diff_blocks.append('\n'.join(current_block))
                current_block = [f'<span style="{STYLES["control"]}"> {line}</span>' for line in control_lines]
        elif line.startswith('-'):
            if lines:
                _next: list[str] = []
                while lines and len(_next) < 2:
                    _next.append(lines.pop())
                if _next[0].startswith('+') and (len(_next) == 1 or _next[1][0] not in ('+', '-')):
                    aline, bline = _line_diff(line[1:], _next.pop(0)[1:])
                    current_block.append(f'<span style="{STYLES["delete"]}"> {aline}</span>')
                    current_block.append(f'<span style="{STYLES["insert"]}"> {bline}</span>')
                    if _next:
                        lines.append(_next.pop())
                    continue
                lines.extend(reversed(_next))
            current_block.append(f'<span style="{STYLES["delete"]}"> {highlight_xml(line[1:])}</span>')
        elif line.startswith('+'):
            current_block.append(f'<span style="{STYLES["insert"]}"> {highlight_xml(line[1:])}</span>')
        elif len(current_block) > 0:
            current_block.append(highlight_xml(line))

    diff = '\n'.join(diff_blocks)

    formatter = HtmlFormatter()

    return HTML(f"""<div class="{formatter.cssclass}" style="background: {formatter.style.background_color}">
<pre style="line-height: 125%;">
{diff}
</pre></div>
""")


def register_formatters(ipython: Any) -> None:
    """
    Register formatter of lxml trees in HTML form
    """
    html_formatter = ipython.display_formatter.formatters['text/html']
    html_formatter.for_type(etree._Element, display_xml)
    html_formatter.for_type(etree._ElementTree, display_xml)
