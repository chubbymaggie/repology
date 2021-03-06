# Copyright (C) 2016-2018 Dmitry Marakasov <amdmi3@amdmi3.ru>
#
# This file is part of repology
#
# repology is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# repology is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with repology.  If not, see <http://www.gnu.org/licenses/>.

import os

from repology.parsers import Parser
#from repology.parsers.maintainers import extract_maintainers
from repology.parsers.versions import VersionStripper


class ArchDBParser(Parser):
    def iter_parse(self, path, factory, transformer):
        normalize_version = VersionStripper().strip_right_greedy('-').strip_left(':').strip_right_greedy('+')

        for package in os.listdir(path):
            desc_path = os.path.join(path, package, 'desc')
            if not os.path.isfile(desc_path):
                continue

            with open(desc_path, encoding='utf-8') as file:
                pkg = factory.begin(package)

                comment = None

                tag = None
                for line in file:
                    line = line.strip()

                    if line == '':
                        tag = None
                    elif tag == 'NAME':
                        pkg.set_name(line)
                    elif tag == 'VERSION':
                        pkg.set_version(line, normalize_version)
                    elif tag == 'DESC':
                        if comment is None:
                            comment = ''
                        if comment != '':
                            comment += '\n'
                        comment += line
                    elif tag == 'URL':
                        pkg.add_homepages(line)
                    elif tag == 'LICENSE':
                        pkg.add_licenses(line)
                    #elif tag == 'PACKAGER':
                    #    pkg.add_maintainers(extract_maintainers(line))
                    elif tag == 'BASE':
                        pkg.set_extra_field('base', line)
                        pkg.set_basename(line)
                    elif line.startswith('%') and line.endswith('%'):
                        tag = line[1:-1]

                pkg.set_summary(comment)

                yield pkg
