# coding:utf-8
# 端口扫描器
# 加入多线程扫描和信号量加锁来控制线程的屏幕输出

import optparse
import socket
import threading

# 创建一个信号量，同一时间线程数量上限为1
screenLock = threading.Semaphore(value=1)

# 尝试建立与目标主机和端口的连接，给信号量加锁来控制线程的运行
def connScan(tgtHost, tgtPort):
  try:
    connSkt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connSkt.connect((tgtHost, tgtPort))
    connSkt.send('ViolentPython\r\n')
    results = connSkt.recv(100)
    # 信号量加锁
    screenLock.acquire()
    print('%d/tcp open'%tgtPort)
    print('results: ' + str(results))
  except:
    screenLock.acquire()
    print('%d/tcp closed'%tgtPort)
  finally:
    # 信号量释放锁
    screenLock.release()
    connSkt.close()

def portScan(tgtHost, tgtPorts):
  try:
    # 获取主机名映射的ip地址
    tgtIP = socket.gethostbyname(tgtHost)
  except:
    print('Cannot resolve "%s": Unknown host'%tgtHost)
    return
  try:
    tgtName = socket.gethostbyaddr(tgtIP)
    print('Scan Results for: ' + tgtName[0])
  except:
    print('Scan Results for: ' + tgtIP)
  socket.setdefaulttimeout(1)
  # 扫描端口
  for tgtPort in tgtPorts:
    t = threading.Thread(target=connScan, args=(tgtHost, int(tgtPort)))
    t.start()

def main():
  parser = optparse.OptionParser('usage prog -H <target host> -p <target port>')
  parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
  parser.add_option('-p', dest='tgtPort', type='string', help='specify target port')
  (options, args) = parser.parse_args()
  tgtHost = options.tgtHost
  tgtPorts = str(options.tgtPort).split(',')
  if (tgtHost == None) | (tgtPorts[0] == None):
    print('you must specify a target host and port[s].')
    exit(0)
  portScan(tgtHost, tgtPorts)

if __name__ == '__main__':
  main()