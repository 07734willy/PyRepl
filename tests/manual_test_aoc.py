from subprocess import Popen, run
from pyrepl import run_code
import pyrepl.parser

import re
import os

AOC_URLS_RAW = """
* [0xVector/AdventOfCode2020](https://github.com/0xVector/AdventOfCode2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--26-brightgreen)
* [Akumatic/Advent-of-Code](https://github.com/Akumatic/Advent-of-Code) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--19-brightgreen)
* [IanFindlay/advent-of-code](https://github.com/IanFindlay/advent-of-code) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2021--01--27-brightgreen)
* [IsaacG/Advent-of-Code](https://github.com/IsaacG/Advent-of-Code) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2021--02--13-brightgreen)
* [James-Ansley/adventofcode](https://github.com/James-Ansley/adventofcode) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2021--01--09-brightgreen)
* [JoseTomasTocino/AdventOfCode2020](https://github.com/JoseTomasTocino/AdventOfCode2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--25-brightgreen)
* [Kurocon/AdventOfCode2020](https://github.com/Kurocon/AdventOfCode2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--25-brightgreen)
* [Levivig/AdventOfCode2020](https://github.com/Levivig/AdventOfCode2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--07-brightgreen)
* [Manas02/Advent-of-code](https://github.com/Manas02/Advent-of-code) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--15-brightgreen)
* [Robin-Bakker/advent-of-code](https://github.com/Robin-Bakker/advent-of-code) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--08-brightgreen)
* [TheLocehiliosan/advent-of-code](https://github.com/TheLocehiliosan/advent-of-code) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--25-brightgreen)
* [VasileiosGeladaris/AdventOfCode2020](https://github.com/VasileiosGeladaris/AdventOfCode2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--10-brightgreen)
* [agubelu/Advent-of-Code-2020](https://github.com/agubelu/Advent-of-Code-2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2021--01--03-brightgreen)
* [alstn2468/Advent_of_Code_2020](https://github.com/alstn2468/Advent_of_Code_2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2021--01--02-brightgreen)
* [aribchowdhury/AdventOfCode2020](https://github.com/aribchowdhury/AdventOfCode2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--25-brightgreen)
* [asiron/aoc](https://github.com/asiron/aoc) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--13-brightgreen)
* [aufbakanleitung/advent-of-code-2020](https://github.com/aufbakanleitung/advent-of-code-2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2021--01--08-brightgreen)
* [aureliensimon/avent-of-code-2020](https://github.com/aureliensimon/avent-of-code-2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--15-brightgreen)
* [brianbarbieri](https://github.com/brianbarbieri/adventofcode2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2021--03--15-brightgreen)
* [bsoyka/aoc](https://github.com/bsoyka/aoc) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2021--04--15-brightgreen)
* [campierce/advent-of-code](https://github.com/campierce/advent-of-code) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--30-brightgreen)
* [candemircan/adventofcode](https://github.com/candemircan/adventofcode) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2021--05--01-brightgreen)
* [codemicro/adventOfCode](https://github.com/codemicro/adventOfCode) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--25-brightgreen)
* [d1618033/aoc](https://github.com/d1618033/aoc) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--25-brightgreen)
* [dalealleshouse/advent_of_code](https://github.com/dalealleshouse/advent_of_code) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--19-brightgreen)
* [danwigrizer/Advent-of-Code](https://github.com/danwigrizer/Advent-of-Code) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--15-brightgreen)
* [darkarp/AdventSolutions](https://github.com/darkarp/AdventSolutions) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--10-brightgreen)
* [david-ds/adventofcode-2020](https://github.com/david-ds/adventofcode-2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2021--01--08-brightgreen)
* [dsardelic/AdventOfCode2020](https://github.com/dsardelic/AdventOfCode2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--26-brightgreen)
* [eliseomartelli/Advent-of-Code-2020](https://github.com/eliseomartelli/Advent-of-Code-2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--04-brightgreen)
* [elvinyhlee/advent-of-code-2020-python](https://github.com/elvinyhlee/advent-of-code-2020-python) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2021--03--21-brightgreen)
* [ephemient/aoc2020](https://github.com/ephemient/aoc2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2021--05--19-brightgreen)
* [facufrau/Advent-of-code-2020](https://github.com/facufrau/Advent-of-code-2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2021--01--05-brightgreen)
* [gamma032steam/Advent-of-code-2020](https://github.com/gamma032steam/Advent-of-code-2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--19-brightgreen)
* [gbusch/AdventOfCode/](https://github.com/gbusch/AdventOfCode/) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--09-brightgreen)
* [gui1612/advent_2020](https://github.com/gui1612/Advent-of-code-2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--02-orange)
* [harbenml/advent-of-code-2020](https://github.com/harbenml/advent-of-code-2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2021--01--22-brightgreen)
* [hmludwig/aoc2020](https://github.com/hmludwig/aoc2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2021--03--28-brightgreen)
* [howtodowtle/advent_of_code](https://github.com/howtodowtle/advent_of_code) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2021--01--05-brightgreen)
* [iphysresearch/advent-of-code-2020](https://github.com/iphysresearch/advent-of-code-2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2021--01--03-brightgreen)
* [irobin591/advent-of-code](https://github.com/irobin591/advent-of-code) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--25-brightgreen)
* [jayascript/adventofcode2020](https://github.com/jayascript/adventofcode2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--10-brightgreen)
* [jesperdramsch/advent-of-code](https://github.com/jesperdramsch/advent-of-code) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--25-brightgreen)
* [jkershaw2000/aoc-2020](https://github.com/jkershaw2000/aoc-2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2021--01--06-brightgreen)
* [john-sandall/advent-of-code](https://github.com/john-sandall/advent-of-code) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--01-brightgreen)
* [jon-edward/advent-of-code-2020](https://github.com/jon-edward/advent-of-code-2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--04-brightgreen)
* [jordyjwilliams/advent_of_code](https://github.com/jordyjwilliams/advent_of_code) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--15-brightgreen)
* [kamaravichow/advent-of-code-2020-python](https://github.com/kamaravichow/advent-of-code-2020-python) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--06-brightgreen)
* [ktmeaton/advent-of-code-2020](https://github.com/ktmeaton/advent-of-code-2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--22-brightgreen)
* [lukestorry/advent-of-code-2020](https://github.com/lukestorry/advent-of-code-2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--22-brightgreen)
* [matus-pikuliak/advent_2020](https://github.com/matus-pikuliak/advent_2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--25-brightgreen)
* [mebeim/aoc](https://github.com/mebeim/aoc) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2021--05--17-brightgreen)
* [nagybalint/advent-of-code-2020](https://github.com/nagybalint/advent-of-code-2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--20-brightgreen)
* [npanuhin/Advent-of-Code](https://github.com/npanuhin/Advent-of-Code) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2021--05--23-brightgreen)
* [pauldraper/advent-of-code-2020](https://github.com/pauldraper/advent-of-code-2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--23-brightgreen)
* [peter-roland-toth/AoC-2020-Python](https://github.com/peter-roland-toth/AoC-2020-Python) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--25-brightgreen)
* [phoebegoh/aoc2020](https://github.com/phoebegoh/aoc2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--11-brightgreen)
* [r0f1/adventofcode2020](https://github.com/r0f1/adventofcode2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--28-brightgreen)
* [rkc007/advent-of-code-2020](https://github.com/rkc007/advent-of-code-2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--16-brightgreen)
* [rosscon/rosscon_advent_of_code](https://github.com/rosscon/rosscon_advent_of_code) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2021--02--19-brightgreen)
* [rubennoriegamier/advent_of_code_2020](https://github.com/rubennoriegamier/advent_of_code_2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2021--01--16-brightgreen)
* [sammyrulez/adventofcode](https://github.com/sammyrulez/adventofcode) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--08-brightgreen)
* [scorphus/advent-of-code-2020](https://github.com/scorphus/advent-of-code-2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2021--02--12-brightgreen)
* [sebadel/adventofcode2020](https://github.com/sebadel/adventofcode2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2021--02--19-brightgreen)
* [sejaldua/advent-of-code-2020](https://github.com/sejaldua/advent-of-code-2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--11-brightgreen)
* [silverben10/aoc](https://github.com/silverben10/aoc) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--22-brightgreen)
* [smetanin-av/advent_of_code](https://github.com/smetanin-av/advent_of_code) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--28-brightgreen)
* [tboschi/advent-of-code-2020](https://github.com/tboschi/advent-of-code-2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--21-brightgreen)
* [terezaif/adventofcode](https://github.com/terezaif/adventofcode) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--25-brightgreen)
* [terror/aoc](https://github.com/terror/aoc) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--13-brightgreen)
* [thosquey/aoc2020](https://github.com/thosquey/aoc2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--21-brightgreen)
* [tombombadilv/advent-of-code-2020](https://github.com/tombombadilv/advent-of-code-2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--19-brightgreen)
* [wysockipiotr/aoc](https://github.com/wysockipiotr/aoc) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--18-brightgreen)
* [yeurch/advent-of-code](https://github.com/yeurch/advent-of-code) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--27-brightgreen)
* [yspreen/adventofcode](https://github.com/yspreen/adventofcode) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2021--05--02-brightgreen)
* [yufengg/adventofcode](https://github.com/yufengg/adventofcode) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--21-brightgreen)
* [zed-b/advent-of-code](https://github.com/zed-b/advent-of-code) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--22-brightgreen)
* [aboutroots/AoC2020](https://github.com/aboutroots/AoC2020) ![Last Commit on GitHub](https://img.shields.io/badge/last%20commit-2020--12--31-brightgreen)
"""

AOC_URLS = re.findall(r"https://github.com/[^)]*", AOC_URLS_RAW)


def get_author(url):
	match = re.match(r"https://github.com/([^/]+)/.*", url)
	return match.group(1)

def run_script(filepath):
	
	directory = os.path.dirname(filepath)
	os.chdir(directory)

	with open(filepath, "r") as f:
		code = f.read()

	timeout = 0.1
	offset = 0

	try:
		pyrepl.parser.USE_OLD_SEGMENTATION = False
		result1 = run_code(code, timeout, offset)
		pyrepl.parser.USE_OLD_SEGMENTATION = True
		result2 = run_code(code, timeout, offset)

		if result1 != result2:
			print(f'differing: {filepath}')
		else:
			print('equal')
	except:
		print('could not run')


def main():
	script_dir = os.path.abspath(os.path.dirname(__file__))
	base_dir = os.path.join(script_dir, "aoc")
	os.makedirs(base_dir, exist_ok=True)

	for url in AOC_URLS[:3]:
		dirname = get_author(url)
		aoc_dir = os.path.join(base_dir, dirname)
		os.makedirs(aoc_dir, exist_ok=True)

		run(["git", "clone", url, aoc_dir])

		for root, dirs, files in os.walk(aoc_dir):
			for filename in files:
				if not filename.endswith(".py"):
					continue

				filepath = os.path.join(root, filename)
				run_script(filepath)


if __name__ == "__main__":
	main()
