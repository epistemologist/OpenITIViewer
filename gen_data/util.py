translit_table = {
	'،'   : ',',
# letters
	'ء'  : 'c',
	'ؤ'  : 'u',
	'ئ'  : 'i',
	'ا'  : 'A',
	'إ'  : 'I',
	'أ'  : 'a',
	'آ'  : 'O',
	'ب'  : 'b',
	'ة'  : 'o',
	'ت'  : 't',
	'ث'  : 'v',
	'ج'  : 'j',
	'ح'  : 'H',
	'خ'  : 'x',
	'د'  : 'd',
	'ذ'  : 'V',
	'ر'  : 'r',
	'ز'  : 'z',
	'س'  : 's',
	'ش'  : 'E',
	'ص'  : 'S',
	'ض'  : 'D',
	'ط'  : 'T',
	'ظ'  : 'Z',
	'ع'  : 'C',
	'غ'  : 'g',
	'ف'  : 'f',
	'ق'  : 'q',
	'ك'  : 'k',
	'ل'  : 'l',
	'م'  : 'm',
	'ن'  : 'n',
	'ه'  : 'h',
	'و'  : 'w',
	'ى'  : 'Y',
	'ي'  : 'y',
}

def transliterate_arabic(str_in):
	return str_in.translate(str.maketrans(translit_table))

def untransliterate_arabic(str_in):
	return str_in.translate(str.maketrans({v:k for k,v in translit_table.items()}))
