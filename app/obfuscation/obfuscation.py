import ast
import pathlib

import astor

import yapf.yapflib.yapf_api as yapf_api

from app.obfuscation.intensio import intensio_replace
from app.obfuscation.tree_scanner import TreeScanner
from app.obfuscation.semantic_obfuscator import Obfuscator, ObfuscatedTreeResolver
from app.obfuscation.syntax_obfuscator import ObfuscateBySyntaxGenerator
from app.obfuscation import obfuscation_settings


def obfuscate(source_code):

    vars_renamer = intensio_replace.ObfuscateRenameVars()
    vars_renamed_source_code = vars_renamer.rename_vars(source_code)

    tree = ast.parse(vars_renamed_source_code)

    tree_scanner = TreeScanner()
    tree_scanner.visit(tree)

    obfuscator = Obfuscator(tree_scanner)
    obfuscated_tree = obfuscator.visit(tree)

    tree_resolver = ObfuscatedTreeResolver(tree_scanner, obfuscator.additional_function_defs)
    tree_resolver.resolve()

    obfuscated_source = astor.to_source(obfuscated_tree, source_generator_class=ObfuscateBySyntaxGenerator)

    style_config_path = pathlib.Path(__file__).parent / 'obfuscated_code_style' / '.style.yapf'
    if obfuscation_settings.settings['syntax']['code_style_obfuscation']['is_on']:
        obfuscated_source = yapf_api.FormatCode(obfuscated_source, style_config=str(style_config_path))[0]

    return obfuscated_source
