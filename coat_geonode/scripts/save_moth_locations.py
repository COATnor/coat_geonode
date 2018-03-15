# -*- coding: utf-8 -*-
######################################################################
# Copyright (C) 2018 NINA
######################################################################
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################
# This script reads the coordinates.txt file provided by Jane listing
# moth waypoints with coordinates and related locations. It extracts
# locations names and saves them in the mothlocations table.
######################################################################

import psycopg2

pg_host=r'localhost'
pg_user=r'geonode'
pg_pwd='geonode'
pg_db=r'geonode'
pg_port=r'5432'

try:
    pg_conn = psycopg2.connect("host={} dbname={} user={} password= {} port={}".format(pg_host, pg_db, pg_user, pg_pwd, pg_port))
    print "Successfull connection to postgres"
except:
    print "Connection error"

cur = pg_conn.cursor()

path = "Coordinates.txt"
locations = []

with open(path, 'r') as f:
    for e, l in enumerate(f):
        location = l.split("\t")[1]
        if e != 0:
            if location not in locations:
                locations.append(location)

for e, l in enumerate(locations):
    e = e+1
    row = (e, l)
    try:
        cur.execute("INSERT INTO public.newdata_mothlocations VALUES (%s, %s)", row)
    except:
        print "error inserting values"

pg_conn.commit()
cur.close()
pg_conn.rollback()