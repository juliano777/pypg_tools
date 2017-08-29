# Imports
import lzma
import os
import re
import requests
import shutil
import sys
import tarfile
import urllib.request

from argparse import ArgumentParser
from bs4 import BeautifulSoup as bs
from distutils.version import LooseVersion

URL = 'https://ftp.postgresql.org/pub/source/'


def get_all_pg_versions():
    'Gets all PostgreSQL versions'

    page = requests.get(URL).text
    soup = bs(page, 'html.parser')    
    pg_versions = []
    anchors = (soup.find_all('a'))
    re_pattern = r'^v((\d)*.*)'

    for i in anchors:
        dir_ = i.extract().get_text()
        if re.search(re_pattern, dir_):
            version_ = re.sub(re_pattern, r'\1', dir_)
            pg_versions.append(version_)
        

    return sorted(pg_versions, key=LooseVersion)


def pg_latest_version(stable_version=True):
    versions = []
    re_pattern = r'(\d)*\.(\d).*'

    if not stable_version:
        re_pattern = r'.*(alpha|beta).*'

    for i in get_all_pg_versions():        
        if re.search(re_pattern, i):  # If pattern matches...
            # ... append item to versions
            versions.append(i)

    return versions[-1]
    


def extract_bz2(bz2_file):
    'Extract bz2 file'

    with tarfile.open(bz2_file, 'r:bz2') as f:
        f.extractall()


def to_tar(dir_name):
    'Binds a directory to a tar file'

    tar_file = '{}.tar'.format(dir_name)
    with tarfile.open(tar_file, 'w') as f:
        f.add(dir_name)


def to_xz(target_file):
    xz_file = '{}.xz'.format(target_file)

    with open(target_file, 'rb') as f:
        data = f.read()

    with lzma.open(xz_file, 'wb', preset=9) as f:
        f.write(data)


def download_file(url, filename):
    xzfile = '{}xz'.format(filename.strip('bz2'))
    if os.path.isfile(xzfile) or os.path.isfile(filename):
        return 0
    urllib.request.urlretrieve(url, filename)
    print('File downloaded!')


def main():
    n_args = len(sys.argv)

    # Strings
    desc_0 = 'Download the source code of PostgreSQL'
    help_d = 'Download the source code'
    help_v = 'Especific version'
    help_o = 'Output'
    help_x = 'Enable XZ compression output (default: bz2)'
    help_S = 'Show alpha or beta version'

    # Argument parser
    parser = ArgumentParser(description=desc_0)

    # Arguments creation
    parser.add_argument('-d', '--download', help=help_d, action='store_true',
                        dest='download')
    parser.add_argument('-o', '--output', type=str, help=help_o,
                        action='store', metavar='output_dir',
                        dest='output_dir')
    parser.add_argument('-v', '--version', type=str, help=help_v,
                        action='store', metavar='version', dest='version')
    parser.add_argument('-x', '--xz-compression', help=help_x,
                        action='store_true', dest='xz_comp')

    parser.add_argument('-S', '--not-stable', help=help_S,
                        action='store_false', dest='not_stable') 

    # Parsed arguments
    args = parser.parse_args()
    download_y = args.download
    output_dir = args.output_dir
    pg_version = args.version
    xz_comp_y = args.xz_comp
    not_stable = args.not_stable

    # ========================================================================

    if output_dir:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    else:
        output_dir = os.getcwd()

    if not os.access(output_dir, os.W_OK):
        raise PermissionError

    # ========================================================================

    
    if not pg_version:        
        pg_version = pg_latest_version(not_stable)

    print(pg_version)

    if download_y:
        base_name_file = 'postgresql-{}'.format(pg_version)  # Base name file
        dw_file = '{}.tar.bz2'.format(base_name_file)  # File to be downloaded
        
        url = ('{}{}'.format(URL, 'v{}/{}')).format(pg_version, dw_file)

        output_file = '{}/{}'.format(output_dir, dw_file)
        download_file(url, output_file)

        if xz_comp_y:
            os.chdir(output_dir)
            extract_bz2(dw_file)
            os.remove(dw_file)
            to_tar(base_name_file)
            tarfile = '{}.tar'.format(base_name_file)
            shutil.rmtree(base_name_file)
            to_xz(tarfile)
            os.remove(tarfile)

    print(pg_version)


if __name__ == '__main__':
    try:
        main()
        sys.exit(0)

    except KeyboardInterrupt:
        print()

    except PermissionError:
        print('Error: Permission denied!')

    except urllib.error.URLError:
        print('Error: There is no version!')

    finally:
        sys.exit(1)
