# coding:utf-8
# NMAP端口扫描器
# NMAP即Network Mapper，用于列举网络主机清单、管理服务更新进程、监控主机、服务执行状况等
# 可用于检测目标主机是否在线、端口开放情况、侦测执行的服务类型以及版本资讯，用于评估网络系统安全
# 其它端口扫描类型
# TCP SYN SCAN --- 也称为半开放扫描，这种类型的扫描发送一个SYN包，启动一个TCP会话，并等待响应的数据包。如果收到的是一个reset包，表明端口是关闭的，而如果收到的是一个SYN/ACK包，则表示相应的端口是打开的
# TCP NULL SCAN --- NULL扫描把TCP头中的所有标志位都设为NULL。如果收到的是一个RST包，则表示相应的端口是关闭的
# TCP FIN SCAN --- TCP FIN 扫描发送一个表示拆除一个活动的TCP连接的FIN包，让对方关闭连接。如果收到了一个RST包，则表示相应的端口是关闭的
# TCP XMAS SCAN --- TCP XMAS 扫描发送PSH、FIN、URG和TCP标志位被设为1的数据包。如果收到了一个RST包，则表示相应的端口是关闭的

import optparse
import nmap

def nmapScan(tgtHost, tgtPort):
  nmScan = nmap.PortScanner()
  try:
    nmScan.scan(tgtHost, tgtPort)
    # 端口状态：Open（开放）、Closed（关闭）、Filtered（过滤）、Unfiltered（未过滤）、Open|Filtered（开放或过滤）、Closed|Filtered（关闭或过滤）
    state = nmScan[tgtHost]['tcp'][int(tgtPort)]['state']
    print(tgtHost + ' tcp/' + tgtPort + ' ' + state)
  except:
    print('scan error')

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
  for tgtPort in tgtPorts:
    nmapScan(tgtHost, tgtPort)

if __name__ == '__main__':
  main()