settings = {
    'syntax': {
        'num_obfuscation': {
            'is_on': True,
            
            'int': True,
            'float': True,
            'complex': True,
        },

        'code_style_obfuscation': {
            'is_on': False
        }
    },

    'semantic': {
        'num_obfuscation': {
            'is_on': True,

            'int_obfuscations': True,
            'int_call_repr': True,
            
            'float_call_repr': True,
            'complex_call_repr': True,
        },

        'str_obfuscation': {
            'is_on': True,
            
            'str_obfuscations': True,
            'str_call_repr': True,
        },

        'useless_expressions': {
            'is_on': True,

            'global': 1,
            'functions': 1
        },

        'vars_renames': {
            'is_on': True,

            'min_len': 5,
            'max_len': 7
        }
    }
}
