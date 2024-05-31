import sys
import getopt
import matplotlib.pyplot as plt
import crawl
import tcp_recv
import tcp_send

vars = sys.argv
options = "hmo:"
long_options = ["Help", "My_file", "Output = "]

def handler(args):
    try:
        keys, values = getopt.getopt(args, options, long_options)
        for key, value in keys:
            if key in ("-h", "--Help"):
                print("Displaying Help")
            elif key in ("-m", "--My_file"):
                print("Display file name: ", args[0])
            elif key in ("-o", "--Output"):
                print("Enable special output mode (%s)", value)
            else: pass
    except getopt.error as err: print(str(err))   
    while True:
        try:
            cmd = input('Enter process command> ').strip()
            match cmd:
                case 'tcp-send':
                    info = input('Enter the IP & Port to be connected> ').split(' ')
                    params = list(filter(None, info))
                    if len(params) == 2: tcp_send.tcp_send_msg(params[0], int(params[1]))
                    else: tcp_send.tcp_send_msg()
                case 'mega-news':
                    info = input('Please enter the required type, date and page> ').split()
                    params = list(filter(None, info))
                    if len(params) == 3: crawl.mega_news(params[0], params[1], params[2])
                case 'udn-news':
                    category_num = input('What classification do you need ?> ')
                    crawl.udn_news(category_num)
                case 'exit':
                    print('Ok bye-bye') 
                    break
        except Exception as ex: print(ex.args)

handler(vars[1:])