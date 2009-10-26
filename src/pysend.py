#!/usr/bin/python
import sys
import socket


def main(argv):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect(( '127.0.0.1', 123456) )
  input = sys.stdin.read()
  print input.strip()
  s.send(input)
  ret = s.recv(1024)
  if len(ret.strip()) > 1:
    print ret
  s.close()

if "__main__" == __name__:
  main(sys.argv)
