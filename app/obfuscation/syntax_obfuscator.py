# Copyright (c) 2012, Patrick Maupin
# Copyright (c) 2013, Berker Peksag
# Copyright (c) 2008, Armin Ronacher
# All rights reserved.

# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import math

import astor

from app.obfuscation.obfuscation_types import *
from app.obfuscation import obfuscation_settings


class ObfuscateBySyntaxGenerator(astor.SourceGenerator):

    def __init__(self, *args, **kwargs):

        super(ObfuscateBySyntaxGenerator, self).__init__(*args, **kwargs)

        self.settings = obfuscation_settings.settings['syntax']

    def _handle_numeric_constant(self, value):
        if not self.settings['num_obfuscation']['is_on']:
            return super(ObfuscateBySyntaxGenerator, self)._handle_numeric_constant(value)

        def obfuscate_num(num):

            def obfuscate_int(num):

                if not self.settings['num_obfuscation']['int']:
                    return repr(num)

                obfuscate_num_type = IntNumReprObfuscateType.get_random_value()

                if obfuscate_num_type == IntNumReprObfuscateType.BIN:
                    return bin(num)
                elif obfuscate_num_type == IntNumReprObfuscateType.OCT:
                    return oct(num)
                elif obfuscate_num_type == IntNumReprObfuscateType.HEX:
                    return hex(num)
                else:
                    return repr(num)

            def obfuscate_float(num):

                if not self.settings['num_obfuscation']['float']:
                    return repr(num)

                # we can't obfuscate float numbers syntaxly
                return repr(num)

            if isinstance(num, int):
                return obfuscate_int(num)
            elif isinstance(num, float):
                return obfuscate_float(num)
            else:
                return RuntimeError('unexpected number type for syntax obfuscation')

        def part(p, imaginary, with_obfuscation=True):

            # Represent infinity as 1e1000 and NaN as 1e1000-1e1000.
            s = 'j' if imaginary else ''

            try:
                if math.isinf(p):
                    if p < 0:
                        return '-1e1000' + s
                    return '1e1000' + s
                if math.isnan(p):
                    return '(1e1000%s-1e1000%s)' % ( s, s )
            except OverflowError:
                # math.isinf will raise this when given an integer
                # that's too large to convert to a float.
                pass

            if not imaginary:
                return obfuscate_num(p) if with_obfuscation else repr(p)
            else:
                return repr(p) + s

        x = value

        if isinstance(x, complex):
            with_complex_obfuscation = self.settings['num_obfuscation']['complex']

            real = part(x.real, False, with_complex_obfuscation)
            imag = part(x.imag, True, with_complex_obfuscation)

            if x.imag == 0:
                s = '(%s+0j)' % real
            else:
                # x has nonzero real and imaginary parts.
                s = '(%s%s%s)' % ( real, [ '+', ''][imag.startswith('-')], imag )
        else:
            s = part(x, False)

        self.write(s)
