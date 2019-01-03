# coding:utf-8
# UNIX密码破解脚本
# hash加密口令文件位置： /etc/shadow
# TODO:升级脚本，增加破解SHA-512 hash的功能（hashlib）

import crypt
import os

current_path = os.path.dirname(os.path.abspath(__file__))
passwords_path = os.path.abspath(os.path.join(current_path, 'passwords.txt'))
dictionary_path = os.path.abspath(os.path.join(current_path, 'dictionary.txt'))

def testPass(cryptPass):
  global dictionary_path
  # 将加密口令的前两个字符视为salt
  salt = cryptPass[0:2]
  dictFile = open(dictionary_path, 'r')
  for word in dictFile.readlines():
    word = word.strip('\n')
    cryptWord = crypt.crypt(word, salt)
    if (cryptWord == cryptPass):
      print('Found Password: ' + word + '\n')
      return
  print('Password Not Found')

def main():
  global passwords_path
  passwordFile = open(passwords_path)
  for line in passwordFile.readlines():
    if ':' in line:
      user = line.split(':')[0]
      cryptPass = line.split(':')[1].strip(' ')
      cryptPass = cryptPass.strip('\n')
      print("Checking Password For: " + user)
      testPass(cryptPass)

if __name__ == "__main__":
  main()