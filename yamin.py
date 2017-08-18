#
# Yaminator
# 한글 야민정음 변환 모듈
# Author: Ilhwan Hwang (https://github.com/IlhwanHwang/)
# Date: 17.08.19
#

consonent_first = ord(u'ㄱ')
consonent_last = ord(u'ㅎ')
vowel_first = ord(u'ㅏ')
vowel_last = ord(u'ㅣ')
syllable_first = ord(u'가')
syllable_last = ord(u'힣')

list_initial = ['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
list_medial = ['ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ','ㅗ','ㅘ','ㅙ','ㅚ','ㅛ','ㅜ','ㅝ','ㅞ','ㅟ','ㅠ','ㅡ','ㅢ','ㅣ']
list_final = ['','ㄱ','ㄲ','ㄳ','ㄴ','ㄵ','ㄶ','ㄷ','ㄹ','ㄺ','ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ','ㅁ','ㅂ','ㅄ','ㅅ','ㅆ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']

#
# Helper functions to analyze korean syllables
#

# Seperate a korean syllable into phonemes
# @Parameter
#	unicode string	syllable (or phoneme)
# @Return
#	unicode string 	initial (consonent)
#	unicode string 	medial (vowel)
#	unicode string 	final (consonent)
def sep(syl):
	uind = ord(syl)

	if uind >= consonent_first and uind <= consonent_last:
		return syl, '', ''

	elif uind >= vowel_first and uind <= vowel_last:
		return '', syl, ''

	elif uind >= syllable_first and uind <= syllable_last:
		ind = ord(syl) - syllable_first
		ind_final = ind % len(list_final)
		ind_medial = (ind // len(list_final)) % len(list_medial)
		ind_initial = (ind // len(list_final)) // len(list_medial)

		return list_initial[ind_initial], list_medial[ind_medial], list_final[ind_final]

	else: 	# Not a korean syllable
		return '', '', ''


# Build a korean syllable out of phonemes
# @Parameter
#	unicode string 	initial (consonent)
#	unicode string 	medial (vowel)
#	unicode string 	final (consonent)
# @Return
#	unicode string	syllable (or phoneme)
def build(initial, medial, final):
	if medial == '' and final == '':
		return initial

	elif initial == '' and final == '':
		return medial

	elif initial == '' and medial == '':
		return final

	else:
		try:
			ind = list_initial.index(initial)
			ind *= len(list_medial)
			ind += list_medial.index(medial)
			ind *= len(list_final)
			ind += list_final.index(final)
			return chr(ind + syllable_first)
		except ValueError:
			return ''


# Check whether it is a korean syllable (or phoneme) or not
# @Parameter
#	unicode string	syllable
# @Return
#	bool
def is_korean_syllable(syl):
	uind = ord(syl)

	consonent = (uind >= consonent_first and uind <= consonent_last)
	vowel = (uind >= vowel_first and uind <= vowel_last)
	syllable = (uind >= syllable_first and uind <= syllable_last)

	return consonent or vowel or syllable

#
# Yaminator classes
#

# Class for naive syllable transform
class NaiveTransform:

	def __init__(self, initial, medial, final, syl1, syl2):
		self.initial = initial
		self.medial = medial
		self.final = final
		self.syl1 = syl1
		self.syl2 = syl2

	# Transform syllable
	# @Return
	#	unicode string	resulted syllable
	#	bool			transformed
	def transform(self, syl):
		# Do transform back and forth
		ressyl, check = self.__transform(syl, self.syl1, self.syl2)
		if check:
			return ressyl, True
		else:
			ressyl, check = self.__transform(syl, self.syl2, self.syl1)
			return ressyl, check
	
	# Transform syllable from sylfrom to sylto
	# @Return
	#	unicode string	resulted syllable
	#	bool			transformed
	def __transform(self, sylsub, sylfrom, sylto):
		i, m, f = sep(sylsub)
		fi, fm, ff = sep(sylfrom)
		ti, tm, tf = sep(sylto)


		i_check = (i == fi or not self.initial)
		m_check = (m == fm or not self.medial)
		f_check = (f == ff or not self.final)

		if not (i_check and m_check and f_check):
			return sylsub, False
		else:
			if self.initial:
				i = ti
			if self.medial:
				m = tm
			if self.final:
				f = tf
			return build(i, m, f), True


import codecs
import os

class Yaminator:

	def __init__(self, dbpath):

		self.trans = []

		f = codecs.open(os.path.join(dbpath, 'dic_naive.txt'), 'r', 'utf-8')

		for line in f.read().splitlines():
			row = line.split()
			initial = row[0] == '1'
			medial = row[1] == '1'
			final = row[2] == '1'
			syl1 = row[3]
			syl2 = row[4]
			self.trans.append(NaiveTransform(initial, medial, final, syl1, syl2))

		f.close()

	# Transform string
	# @Parameter
	#	String 	subject string
	# @Return
	#	String	resulted string
	def transform(self, string):
		result = ''
		for syl in string:
			if is_korean_syllable(syl):
				done = False
				for trans in self.trans:
					ressyl, check = trans.transform(syl)
					if check:
						result += ressyl
						done = True
						break
				if not done:
					result += syl
			else:
				result += syl
		return result


if __name__ == "__main__":
	yamin = Yaminator('db')
	while True:
		string = input('>> ')
		print('<< {}'.format(yamin.transform(string)))

