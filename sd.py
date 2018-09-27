from multiprocessing import Process;
import random;
import time;
import os;
import socket;
import threading;
import struct;
import asyncio;

def comeco():
    p = Process(target=main, args=());
    p.start();
    p1 = Process(target=main, args=());
    p1.start();
    main();

def main():
    time.sleep(2);
    print('O MEU PID :{}\n'.format(os.getpid()));
    #OUVIR
    t_ouvir = threading.Thread(target=ouvir,args=());
    t_ouvir.start();
    time.sleep(2);
    #FALAR
    falar()
        #teste
    while(fila.empty()!= True):
        print ('',fila.get_nowait())
    time.sleep(4);

def falar():

    HOST1 = '225.0.0.250'
    PORT = 8888
    global clock
    global fila
    print('{} # vou comecar a falar\n'.format(os.getpid()))


    addrinfo = socket.getaddrinfo('225.0.0.250', None)[0]
    sf = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    ttl = struct.pack('b', 1)
    sf.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL,ttl)
    

    c=('clock = %d PID =%d'% (clock,os.getpid()))
    a =(clock,os.getpid())
    clock = clock +1;
    sf.sendto(c.encode(),(HOST1,PORT))
    fila.put_nowait(a)


    c=('clock = %d PID =%d'% (clock,os.getpid()))
    a =(clock,os.getpid())
    clock = clock +1;
    sf.sendto(c.encode(),(HOST1,PORT))    
    print('{} # parei de falar\n'.format(os.getpid()));
    fila.put_nowait(a)

    time.sleep(2);


def ouvir():

    HOST = ''
    PORT = 8888
    global clock
    print('{} # vou comecar a ouvir\n'.format(os.getpid()));

    addrinfo = socket.getaddrinfo('225.0.0.250', None)[0]
    sl = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sl.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sl.bind((HOST, PORT));
    group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
    mreq = group_bin + struct.pack('=I', socket.INADDR_ANY)
    sl.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while 1:
        print('{} # ouvindo\n'.format(os.getpid()));
        data, addr = sl.recvfrom(1024); 
        print ("received message:", data.decode())
        if (data.decode()[0]!='a'): #diferente de ACK
            if (int(data.decode()[8])>=clock):
                clock=int(data.decode()[8])+1
            print ('Connected with %s PID: %d\n' % (addr,os.getpid())); 
            c='ack'
            sl.sendto(c.encode(),('225.0.0.250',PORT))
        #else:
            #guardar de quem foi o ack para contar
            #quando chegar a 3 acks do mesmo x , "tirar da fila"
    sl.close()

clock = 0;
fila = asyncio.PriorityQueue()
if __name__ == "__main__":
    comeco()
