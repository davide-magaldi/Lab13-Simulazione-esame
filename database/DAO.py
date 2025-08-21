from database.DB_connect import DBConnect
from model.drivers import Driver


class DAO():
    @staticmethod
    def getYears():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = '''select year from seasons s'''
        cursor.execute(query)

        for row in cursor:
            result.append(row['year'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodes(year):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = '''select d.driverId, forename, surname from(select driverId from results r 
                    join races r2 
                    on r.raceId = r2.raceId 
                    where r2.`year` = %s and `position` is not null
                    group by driverId) tab
                    join drivers d 
                    on d.driverId = tab.driverId'''
        cursor.execute(query, (year,))

        for row in cursor:
            result.append(Driver(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(year):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor()
        query = '''select d1, d2, count(*) as weight
                    from ((select r.raceId  , r.`position`as pos1, r.driverId as d1
                    from results r 
                    join races r2 
                    on r.raceId = r2.raceId 
                    where r2.`year` = %s and `position` is not null) tab1
                    join (select r.raceId , r.`position` as pos2, r.driverId as d2
                    from results r 
                    join races r2 
                    on r.raceId = r2.raceId 
                    where r2.`year` = %s and `position` > 1) tab2
                    on tab1.raceId = tab2.raceId)
                    where tab1.pos1 < tab2.pos2
                    group by d1, d2'''
        cursor.execute(query, (year, year))

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result
