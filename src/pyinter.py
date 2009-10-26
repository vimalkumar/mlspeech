#!/usr/bin/python
import sys
import socket


def main(argv):
  s = socket.socket()
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
  s.bind(( '', 123456) )
  s.listen(10)
  global_context = {}
  local_context = {}
  while 1:
    conn, addr = s.accept()
    print ' connected by ' , addr
    chunk = 'something';
    while len(chunk) > 1:
      chunk = conn.recv(1024);
      print chunk
      try:
        exec(chunk, global_context, local_context)
        conn.send("\n")
      except Exception , e:
        conn.send(str(e) + "\n")


if "__main__" == __name__:
  main(sys.argv)
