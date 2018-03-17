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
#
#
#
#
#

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
waypoints = []

with open(path, 'r') as f:
    for e, l in enumerate(f):
        if e != 0:
            waypoint = l.split("\t")[0]
            location = l.split("\t")[1]
            cur.execute(cur.mogrify("SELECT newdata_mothlocations.id from public.newdata_mothlocations WHERE newdata_mothlocations.name=%s;"), (location,))
            fetched = cur.fetchone()
            try:
                location_id = fetched[0]
            except:
                print "error reading value"

            station = int(l.split("\t")[2])
            utm33_lon = float(l.split("\t")[3])
            utm33_lat = float(l.split("\t")[4])

            lon = float(l.split("\t")[5])
            lat = float(l.split("\t")[6].strip())
            #geometry = "ST_GeomFromText('Point({} {})', 4326)".format(lon, lat)
            print lat
            # next commented: required for inserting remaining coordinates after error
            #e = 269 + e
            row = (e, waypoint, location_id, location, station, utm33_lon, utm33_lat, lon, lat, lon, lat,)
            print row
            try:
                cur.execute("INSERT INTO public.newdata_mothwaipoints VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, ST_GeomFromText('Point(%s %s)', 4326));", row)
                pg_conn.commit()
            except:
                print "error inserting"
                pg_conn.rollback()

pg_conn.commit()
cur.close()
pg_conn.rollback()