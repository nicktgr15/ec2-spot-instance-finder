#!/usr/bin/env python

import boto.ec2
import requests
import pandas as pd
from datetime import datetime
import argparse
from collections import namedtuple

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

DataEntry = namedtuple('DateEntry',
                       'instance_type, cores, memory, memory_per_core, '
                       'price_per_hour, price_per_core, price_per_gb, '
                       'price_per_day, price_per_month')


def get_instances_dict():
    res = requests.get('http://www.ec2instances.info/instances.json')
    json_response = res.json()

    d = {}
    for i in json_response:
        d[i['instance_type']] = {
            'vCPU': i['vCPU'],
            'memory': i['memory']
        }
    return d


def main(sort_by, region, zone, sort_type):
    ec2_conn = boto.ec2.connect_to_region(region)

    d = get_instances_dict()
    result = []

    for p in ec2_conn.get_spot_price_history(product_description='Linux/UNIX',
                                             availability_zone=zone,
                                             start_time=datetime.now().isoformat()):
        instance_price = p.price
        instance_type = p.instance_type
        cores = d[instance_type]['vCPU']
        memory = d[instance_type]['memory']
        memory_per_core = memory / cores
        price_per_core = instance_price / float(cores)
        price_per_gb = instance_price / float(memory)
        price_per_day = instance_price * 24
        price_per_month = price_per_day * 30

        data_entry = DataEntry(instance_type, cores, memory, memory_per_core,
                               p.price, price_per_core, price_per_gb,
                               price_per_day, price_per_month)
        result.append(data_entry)

    df = pd.DataFrame(result, columns=list(DataEntry._fields))

    print df.sort_values(by=sort_by, ascending=sort_type)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Explore ec2 spot instances')
    parser.add_argument('--sort-by', dest='sort_by',
                        choices=list(DataEntry._fields),
                        default='price_per_core',
                        help='Sort spot instances by column')

    parser.add_argument('--asc', dest='sort_type', action='store_const',
                        const=1, default=1)

    parser.add_argument('--desc', dest='sort_type', action='store_const',
                        const=0, default=1)

    parser.add_argument('--region', dest='region',
                        default='eu-west-1',
                        help='AWS region')

    parser.add_argument('--zone', dest='zone',
                        default='eu-west-1c',
                        help='AWS zone')

    args = parser.parse_args()
    main(args.sort_by, args.region, args.zone, args.sort_type)
