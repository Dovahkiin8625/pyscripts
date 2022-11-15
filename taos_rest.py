from taosrest import connect, TaosRestConnection, TaosRestCursor
import sys, getopt

def get_taos_data_size(url:str,user:str,password:str,timeout:int):
    conn: TaosRestConnection = connect(url=url,user=user,password=password,timeout=timeout)
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

def main(argv):
    url = "http://localhost:6041"
    user = "root"
    password = "taosdata"
    timeout = 30

    try:
        opts, args = getopt.getopt(argv,"hH:u:p:d:t:",["help","url=","user=","password=","timeout="])
    except getopt.GetoptError:
        show_help()
        sys.exit(2)
    if not opts:
        show_help()
    for opt, arg in opts:
        if opt == '-h' or opt=='--help':
            show_help() 
            sys.exit()
        elif opt == '-H' or opt == '--url':
            url = arg
        elif opt == '-u' or opt == '--user':
            user = arg
        elif opt == '-p' or opt == '--password':
            password = arg
        elif opt == '-t' or opt == '--timeout':
            timeout = arg
        else:
            show_help()
            sys.exit()
    get_taos_data_size(url,user,password,timeout)


def show_help():
    print("Usage: python taos_rest.py [options]")
    print("-h, --help show this help")
    print("-H, --url urls of TDengine")
    print("-u, --user user of TDengine,default:root")
    print("-p, --password password of TDengine,default:taosdata")
    print("-t, --timeout timeout of TDengine")


if __name__ == "__main__":
    # print(sys.argv)
    main(sys.argv[1:])