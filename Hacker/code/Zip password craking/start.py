# coding:utf-8
# zip口令破解脚本
# -f 待破解zip文件
# -d 口令字典文件

import optparse
import zipfile
import sys
import os
from threading import Thread

# 解析标志和参数
parser = optparse.OptionParser("usage prog " + "-f <zipfile> -d <dictionary>")
parser.add_option('-f', dest='zname', type='string', help='specify zip file')
parser.add_option('-d', dest='dname', type='string', help='specify zip file')
(options, args) = parser.parse_args()
if (options.zname == None) | (options.dname == None):
  print(parser.usage)
  exit(0)
else:
  zname = options.zname
  dname = options.dname
  # 检测文件是否存在
  if not os.path.isfile(zname):
    print('filename: ' + zname + ' does not exist')
    exit(0)
  if not os.path.isfile(dname):
    print('filename: ' + dname + ' does not exist')
    exit(0)
current_path = os.path.dirname(os.path.abspath(__file__))
zip_path = os.path.abspath(os.path.join(current_path, zname))
dictionary_path = os.path.abspath(os.path.join(current_path, dname))

def extractFile(zFile, password):
  try:
    zFile.extractall(pwd=password)
    print('Found Password = ' + password + '\n')
  except Exception:
    pass

def main():
  global zip_path, dictionary_path
  zFile = zipfile.ZipFile(zip_path)
  passFile = open(dictionary_path)
  for line in passFile.readlines():
    password = line.strip('\n')
    t = Thread(target=extractFile, args=(zFile, password))
    t.start()

if __name__ == '__main__':
  main()