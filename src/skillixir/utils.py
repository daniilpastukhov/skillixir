__all__ = ['remove_hyphens', 'dehyphenate']


def remove_hyphens(text: str) -> str:
	"""

	This fails for:
	* Natural dashes: well-known, self-replication, use-cases, non-semantic,
	                  Post-processing, Window-wise, viewpoint-dependent
	* Trailing math operands: 2 - 4
	* Names: Lopez-Ferreras, VGG-19, CIFAR-100
	"""
	lines = [line.rstrip() for line in text.split('\n')]

	# Find dashes
	line_numbers = []
	for line_no, line in enumerate(lines[:-1]):
		if line.endswith('-'):
			line_numbers.append(line_no)

	# Replace
	for line_no in line_numbers:
		lines = dehyphenate(lines, line_no)

	return '\n'.join(lines)


def dehyphenate(lines: list[str], line_no: int) -> list[str]:
	next_line = lines[line_no + 1]
	word_suffix = next_line.split(' ')[0]

	lines[line_no] = lines[line_no][:-1] + word_suffix
	lines[line_no + 1] = lines[line_no + 1][len(word_suffix) :]
	return lines
