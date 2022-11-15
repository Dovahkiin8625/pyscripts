from taosrest import connect, TaosRestConnection, TaosRestCursor

def get_taos_data_size():
    conn: TaosRestConnection = connect(url="http://10.64.6.57:6041",
                                    user="root",
                                    password="taosdata",
                                    timeout=30)
    cursor: TaosRestCursor = conn.cursor()

    cursor.execute("SHOW xkjt.stables")
    data: list = cursor.fetchall()
    count_all: int = 0
    for stable in data:
        cursor.execute("select count(*) from xkjt."+stable[0])
        count = cursor.fetchall()
        line_count: int = 0 if not count or not count[0] else count[0][0]
        count_all += line_count
    print("taos_data,tag=test data_size="+str(count_all))

if __name__ == "__main__":
    get_taos_data_size()