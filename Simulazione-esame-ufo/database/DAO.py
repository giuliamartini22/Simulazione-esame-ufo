from database.DB_connect import DBConnect
from model.state import State


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllYears():

        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct year (`datetime`) as anno
                        from sighting s
                        order by anno desc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["anno"])
            cursor.close()
            cnx.close()
            return result

    @staticmethod
    def getAllShapes(anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct s.shape
                        from sighting s
                        where s.shape <> ""
                        and year (s.`datetime`)  = %s"""
            cursor.execute(query, (anno,))

            for row in cursor:
                result.append(row["shape"])
            cursor.close()
            cnx.close()
            return result

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllEdges():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select n.state1 as id1, n.state2 as id2
                    from neighbor n """

        cursor.execute(query)

        for row in cursor:
            result.append((row["id1"], row["id2"]))

        cursor.close()
        conn.close()
        return result
#dao che restituisce solo 1 valore
    @staticmethod
    def getPesoArchi(shape, anno, id1, id2):
        conn = DBConnect.get_connection()

        result = 0

        cursor = conn.cursor(dictionary=True)
        query = """select count(*) as peso
                from sighting s, state s1, state s2
                where (s.state = s1.id or s.state = s2.id)
                and s.shape = %s
                and year(s.`datetime`) = %s
                and s1.id = %s
                and s2.id = %s"""

        cursor.execute(query, (shape, anno, id1, id2,))

        result = cursor.fetchone()[0]

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllWeightedEdges(shape, anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select n.state1 as id1, n.state2 as id2, count(*) as peso
                    from neighbor n, sighting s
                    WHERE s.shape = %s
                    and year(s.`datetime`) = %s
                    and (s.state = n.state1 or s.state = n.state2)
                    and n.state1 < n.state2 
                    group by n.state1, n.state2 """

        cursor.execute(query, (shape, anno))

        for row in cursor:
            result.append((row["id1"], row["id2"], row["peso"]))

        cursor.close()
        conn.close()
        return result
