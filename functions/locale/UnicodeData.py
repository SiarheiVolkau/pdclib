#!/usr/bin/python
# -*- coding: <encoding name> -*-
# Unicode Data Converter
#
# This file is part of the Public Domain C Library (PDCLib).
# Permission is granted to use, modify, and / or redistribute at will.
"""
Converts the character information provdied by Unicode in the UnicodeData.txt
file from the Unicode character database into a table for use by PDCLib.

Usage: Download the UnicodeData.txt file to the same directory as this script 
and then run it. Both Python 2 and 3 are supported.

Download the data from
    ftp://ftp.unicode.org/Public/UNIDATA/UnicodeData.txt
"""
import os

# MUST BE KEPT SYNCHRONIZED WITH _PDCLIB_locale.h
BIT_ALPHA =   1
BIT_BLANK =   2
BIT_CNTRL =   4
BIT_GRAPH =   8
BIT_PUNCT =  16
BIT_SPACE =  32
BIT_LOWER =  64
BIT_UPPER = 128
BIT_DIGIT = 256

# Category to bitfield mapping
categories = {
    'Lu': BIT_ALPHA | BIT_GRAPH | BIT_UPPER,    # Uppercase
    'Ll': BIT_ALPHA | BIT_GRAPH | BIT_LOWER,    # Lowercase
    'Lt': BIT_ALPHA | BIT_GRAPH | BIT_UPPER,    # Title case. Upper?
    'Lm': BIT_ALPHA | BIT_GRAPH,                # Modifier. Case?
    'Lo': BIT_ALPHA | BIT_GRAPH,                # "Other" letter (e.g. Ideograph)
    'Nd': BIT_DIGIT | BIT_GRAPH,                # Decimal digit
    'Nl': BIT_GRAPH,                            # Letter-like numeric character
    'No': BIT_GRAPH,                            # Other numeric
    'Pc': BIT_PUNCT | BIT_GRAPH,                # Connecting punctuation
    'Pd': BIT_PUNCT | BIT_GRAPH,                # Dash punctuation
    'Ps': BIT_PUNCT | BIT_GRAPH,                # Opening punctuation
    'Pe': BIT_PUNCT | BIT_GRAPH,                # Closing punctuation
    'Pi': BIT_PUNCT | BIT_GRAPH,                # Opening quote
    'Pf': BIT_PUNCT | BIT_GRAPH,                # Closing quote
    'Po': BIT_PUNCT | BIT_GRAPH,                # Other punctuation
    'Sm': BIT_GRAPH,                            # Mathematical symbol
    'Sc': BIT_GRAPH,                            # Currency symbol
    'Sk': BIT_GRAPH,                            # Non-letterlike modifier symbol
    'So': BIT_GRAPH,                            # Other symbol
    'Zs': BIT_SPACE | BIT_GRAPH | BIT_BLANK,    # Non-zero-width space character
    'Zl': BIT_SPACE | BIT_GRAPH,                # Line separator
    'Zp': BIT_SPACE | BIT_GRAPH,                # Paragraph separator
    'Cc': BIT_CNTRL,                            # C0/C1 control codes
}

in_file  = open('UnicodeData.txt', 'r')
out_file = open('_PDCLIB_unicodedata.c', 'w')
try:
    out_file.write("""
/* Unicode Character Information ** AUTOMATICALLY GENERATED FILE **
 *
 * This file is part of the PDCLib public domain C Library, but is automatically
 * generated from the Unicode character data information file found at
 *   ftp://ftp.unicode.org/Public/UNIDATA/UnicodeData.txt
 * 
 * As a result, the licensing that applies to that file also applies to this 
 * file. The licensing which applies to the Unicode character data can be found 
 * in Exhibit 1 of the Unicode Terms of Use, found at
 *   http://www.unicode.org/copyright.html#Exhibit1
 */
 #include <_PDCLIB_locale.h>

 _PDCLIB_wctype_t _PDCLIB_wctype[] = {
//   { value,\tflags,\tlower,\tupper\t}, // name
 """)
    for line in in_file:
        (num_hex, name, category, combining_class, bidi_class, decomposition,
         numeric_type, numeric_digit, numeric_value, mirrored, u1name, iso_com, 
         upper_case_hex, lower_case_hex, title_case_hex) = line.split(";")

        num       = int(num_hex, 16)
        upper_case = int(upper_case_hex, 16) if len(upper_case_hex) else num
        lower_case = int(lower_case_hex, 16) if len(lower_case_hex) else num
        bits = categories.get(category, 0)

        if upper_case == 0 and lower_case == 0 and bits == 0:
            continue

        out_file.write("    { 0x%X,\t0x%X,\t0x%X,\t0x%X }, // %s\n" % (
            num, bits, lower_case, upper_case, name))
    out_file.write('};\n\n')
    out_file.write('size_t _PDCLIB_wctype_size = sizeof(_PDCLIB_wctype) / sizeof(_PDCLIB_wctype[0]);\n\n')
except:
    in_file.close()
    out_file.close()
    os.remove('_PDCLIB_unicodedata.c')
    raise
else:
    in_file.close()
    out_file.close()
