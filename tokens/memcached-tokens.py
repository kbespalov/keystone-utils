import json
import pickle

import memcached_stats
import argparse
import sys
import yaml

CONF = None


def get_config(cfg_file='./c.yaml'):
    global CONF
    if not CONF:
        with open(cfg_file) as f:
            CONF = yaml.load(f)
    return CONF


def args_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config-file', default='./c.yaml', dest='cfg_file')
    return parser.parse_args(sys.argv[1:])


def main():
    parsed = args_parse()
    configs = get_config(parsed.cfg_file)
    stats = memcached_stats.MemcachedStats(**configs['memcache'])
    for k in stats.keys():
        result = stats.command('get %s' % k).split('\r\n')[1:-1]
        if len(result) != 2:
            continue
        key, value = result
        if 'expires_at' in value:
            try:
                token = json.loads(value)
            except:
                token = pickle.loads(value)
            token_info = token[0]['token']
            print k, token_info['user']['name'], token_info['expires_at']


if __name__ == '__main__':
    main()
