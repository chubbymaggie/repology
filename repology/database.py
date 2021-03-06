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

import psycopg2


class Database:
    def __init__(self, dsn, querymgr, readonly=True, autocommit=False, application_name=None):
        self.db = psycopg2.connect(dsn, application_name=application_name)
        self.db.set_session(readonly=readonly, autocommit=autocommit)
        querymgr.inject_queries(self, self.db)

    def commit(self):
        self.db.commit()

    # XXX: move these away from here
    linkcheck_status_timeout = -1
    linkcheck_status_too_many_redirects = -2
    linkcheck_status_unknown_error = -3
    linkcheck_status_cannot_connect = -4
    linkcheck_status_invalid_url = -5
    linkcheck_status_dns_error = -6
