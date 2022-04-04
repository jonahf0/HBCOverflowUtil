These scripts are supposed to help with creating new strings when disassembling Hermes bytecode
using hbctool, which can be found at:

    https://github.com/bongtrop/hbctool

The tool currently does not support overflow of entries, so these scripts fill that role temporarily.

"add_entry_to_end.py" adds a new string to the end of "stringStorage" in "metadata.json" and changes
header and table entry information for a given string ID (which can be found in "string.json").This 
causes the bytecode to go to a different string instead of going to the original one. 
"overflow_entry.py" just overrides the information at the appropriate offset for a given ID regardless
of string length. If the string is shorter than the original length, then it pads it; otherwise, it just
overflows and overwrites other entries (which could be dangerous!).
