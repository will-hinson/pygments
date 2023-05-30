"""
    pygments.lexers.verifpal
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for Verifpal languages.

    :copyright: Copyright 2006-2023 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re

from pygments.lexer import RegexLexer, include, words, bygroups, default
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Punctuation, Whitespace

__all__ = ['VerifpalLexer']


class VerifpalLexer(RegexLexer):
    """
    For Verifpal code.

    .. versionadded:: 2.16.0
    """

    name = 'Verifpal'
    aliases = ['verifpal']
    filenames = ['*.vp']
    mimetypes = ['text/x-verifpal']
    url = 'https://verifpal.com'

    tokens = {
        'root': [
            (r'//.*$', Comment.Single),
            (r'(principal)( +)(\w+)( *)(\[)(.*)$', bygroups(Name.Builtin, Whitespace, String, Whitespace, Punctuation, Whitespace)),
            (r'(attacker)( *)(\[)( *)(passive|active)( *)(\])( *)$', bygroups(Name.Builtin, Whitespace, Punctuation, Whitespace, String, Whitespace, Punctuation, Whitespace)),
            (r'(knows)( +)(private|public)( +)', bygroups(Name.Builtin, Whitespace, Keyword.Constant, Whitespace), 'shared'),
            (r'(queries)( +)(\[)', bygroups(Name.Builtin, Whitespace, Punctuation), 'queries'),
            (r'(\w+)( +)(->|→)( *)(\w+)( *)(\:)', bygroups(String, Whitespace, Punctuation, Whitespace, String, Whitespace, Punctuation), 'shared'),
            (words(('generates', 'leaks'), suffix=r'\b'), Name.Builtin, 'shared'),
            (words(( 'phase', 'precondition',), suffix=r'\b'), Name.Builtin),
            (r'[\[\(\)\]\?:=→^,]', Punctuation),
            (r'->', Punctuation),
            (words(('password',), suffix=r'\b'), Keyword.Constant),
            (words(('AEAD_DEC', 'AEAD_ENC', 'ASSERT', 'BLIND', 'CONCAT',
                    'DEC', 'ENC', 'G', 'HASH', 'HKDF', 'MAC', 'PKE_DEC',
                    'PKE_ENC', 'PW_HASH', 'RINGSIGN', 'RINGSIGNVERIF',
                    'SHAMIR_JOIN', 'SHAMIR_SPLIT', 'SIGN', 'SIGNVERIF',
                    'SPLIT', 'UNBLIND', '_', 'nil'), suffix=r'\b'),
             Name.Function),
            (r'\s+', Whitespace),
            (r'\w+', Name.Variable),
        ],
        'shared': [
            (r'[\^\[\],]', Punctuation),
            (r' +', Whitespace),
            (r'\w+', Name.Variable),
            default('#pop')
        ],
        'queries': [
            (r'\s+', Name.Variable),
            (words(('confidentiality?', 'authentication?', 'freshness?',
                    'unlinkability?', 'equivalence?'), suffix='( )'),
             bygroups(Keyword.Pseudo, Whitespace), 'shared'),
            default('#pop')
        ]
    }