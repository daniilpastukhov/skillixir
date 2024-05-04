from pathlib import Path
import os
from pdf2image import convert_from_path, convert_from_bytes
import pytesseract

from keybert import KeyBERT

from skillixir.utils import remove_hyphens


class KeywordsProcessor:
	def __init__(self) -> None:
		self.keybert = KeyBERT('BAAI/bge-m3')

	def pdf2text(self, file_path: str) -> str:
		# doc = convert_from_path(file_path, fmt='png')
		doc = convert_from_bytes(file_path, fmt='png')
		result = ''
		for page_number, page_data in enumerate(doc):
			txt = pytesseract.image_to_string(page_data)
			result += remove_hyphens(txt)
		return result

	def extract_keywords(self, text: str) -> list:
		return self.keybert.extract_keywords(
			text, top_n=30, nr_candidates=50, keyphrase_ngram_range=(1, 2), use_maxsum=False, use_mmr=True
		)

	def process_resume(self, file_path: str | Path, position: str, location: str) -> list:
		text = self.pdf2text(file_path)
		resume_keywords = self.extract_keywords(text)
		position_keywords = self.extract_keywords(position)
		return self.match_keywords(resume_keywords, position_keywords)

	@staticmethod
	def match_keywords(resume_keywords: list, position_keywords: list) -> list:
		return [keyword for keyword in resume_keywords if keyword in position_keywords]
