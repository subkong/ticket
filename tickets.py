#coding:utf-8

"""
Usage: tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help    显示帮助菜单
    -g           高铁
    -d           动车
    -t           特快
    -k           普快
    -z           直达

Examples:
    tickets 合肥 北京 2016-06-22
    tickets -dz 北京 合肥 2016-06-22
"""

from docopt import docopt
import requests
from stations import stations
from prettytable import PrettyTable
from colorama import init, Fore
import time

#：获取输入参数
def getParams(func):
    args = docopt(__doc__)
    # print args.get('<date>')
    # print args.get('<from>')
    # print args.get('<to>')
    func(args)

#: 格式化20160623时间为2016-06-23
def formateDate(query_date):

    TIMESTAMP = "%Y%m%d%H%M%S"

    query_date = int(query_date) * 100000 + 1
    # print query_date
    time_mills = time.mktime(time.strptime(str(query_date), TIMESTAMP))

    formate_date = time.strftime('%Y-%m-%d %H:%M:%S',  time.localtime(time_mills))

    return formate_date.split()[0]

#: 获取时间参数
def getDate(query_date):
    if not query_date:
        return datetime.date.today()
    else:
        return formateDate(query_date)

#: 获取查询火车类型
def getTrainType(args):
    #: print args
    if not args.get('-d') and not args.get('-g') and not args.get('-k') and not args.get('-t') and not args.get('-z'):
        return {'D':True, 'G':True, 'K':True, 'T':True, 'Z':True}

    type_dict = {'D':False, 'G':False, 'K':False, 'T':False, 'Z':False}

    type_dict['D'] = args.get('-d')
    type_dict['G'] = args.get('-g')
    type_dict['K'] = args.get('-k')
    type_dict['T'] = args.get('-t')
    type_dict['Z'] = args.get('-z')

    return type_dict

@getParams
def getTickets(args):
    if not args:
	print 'get info fail!'
    #: 定义文本输出颜色
    init(autoreset=True)

    headers = '车次 车站 时间 历时 商务 一等 二等 软卧 硬卧 软座 硬座 无座'.split()

    #: 定义表格样式输出
    pt = PrettyTable(headers)
    pt.align['车次'] = '1'
    pt.padding_width = 1
    # pt.pt._set_field_names(headers)

    types = getTrainType(args)
    #: print types

    query_date = getDate(args.get('<date>'))
    query_from = args.get('<from>').decode('utf-8')
    query_to = args.get('<to>').decode('utf-8')

    #: 获取数据
    com_url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate=%s&from_station=%s&to_station=%s' % (query_date, stations.get(query_from), stations.get(query_to))

    #: print com_url

    #关闭请求验证提示
    requests.packages.urllib3.disable_warnings()

    try:
    	results = requests.get(com_url, verify=False)
    except Exception, e:
    	print '12306渣渣不响应!'

    if results and 200 == results.json()['httpstatus']:
	datas = results.json()['data']['datas']
        data_filter = [train_info for train_info in datas if types.get(train_info['station_train_code'][0])]
	for row in data_filter:
	    pt.add_row([Fore.CYAN + row['station_train_code'], Fore.RED + row['start_station_name'] + Fore.CYAN + '>>' + Fore.GREEN + row['end_station_name'], Fore.RED + row['start_time'] + Fore.CYAN + '--' + Fore.GREEN + row['arrive_time'], Fore.CYAN + row['lishi'], row['swz_num'], row['zy_num'], row['ze_num'], row['rw_num'], row['yw_num'], row['yb_num'], row['yz_num'], row['wz_num']])

	print pt
    else:
        print 'get info fail!'

#if __name__ == '__main__':
    #getTickets
