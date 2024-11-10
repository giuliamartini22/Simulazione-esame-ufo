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
                            and year (s.`datetime`)  = %s
                            order by s.shape asc"""
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
    def getAllWeightedEdges(anno, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s1.state as stato1, s2.state as stato2, count(*) as peso
                        from sighting s1, sighting s2, neighbor n
                        where ((s1.state = n.state1 and s2.state = n.state2)
                        or (s1.state = n.state2 and s2.state = n.state1))
                        and n.state1 < n.state2 
                        and s1.shape = %s
                        and s2.shape = %s
                        and year(s1.`datetime`) = %s
                        and year(s2.`datetime`) = %s
                        group by s1.state, s2.state"""
            cursor.execute(query, (shape, shape, anno, anno,))

            for row in cursor:
                result.append((row["stato1"], row["stato2"], row["peso"]))
            cursor.close()
            cnx.close()
            return result