from multiprocessing import Process;
from random import randint;
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
    fila = asyncio.PriorityQueue()
    time.sleep(2);
    print('O MEU PID :{}\n'.format(os.getpid()));
    #OUVIR
    t_ouvir = threading.Thread(target=ouvir,args=(fila,2));
    t_ouvir.start();
    time.sleep(2);
    #FALAR
    #flag=0
    #while(int(flag)==0):
    falar(fila)
    #    flag=input()
        #teste
#    while(fila.empty()!= True):
#        print ('',fila.get_nowait())
#        time.sleep(4);

def falar(fila):

    HOST1 = '225.0.0.250'
    PORT = 8888
    global clock
    #global fila
    print('{} # Mandando mensagem :\n'.format(os.getpid()))


    addrinfo = socket.getaddrinfo('225.0.0.250', None)[0]
    sf = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    ttl = struct.pack('b', 1)
    sf.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL,ttl)
    

    c=('clock = %d PID =%d'% (clock,os.getpid()))
    a =(clock,os.getpid(),0)
    clock = clock +1;
    sf.sendto(c.encode(),(HOST1,PORT))
    fila.put_nowait(a)

    time.sleep(2);

  #  c=('clock = %d PID =%d'% (clock,os.getpid()))
   # a =(clock,os.getpid(),0)
   # clock = clock +1;
   # sf.sendto(c.encode(),(HOST1,PORT))    
    #print('{} # parei de falar\n'.format(os.getpid()));
#    fila.put_nowait(a)

 #   time.sleep(2);


def ouvir(fila,t):

    HOST = ''
    PORT = 8888
    global clock
    contador=0
    #global fila
    #print('{} # vou comecar a ouvir\n'.format(os.getpid()));

    addrinfo = socket.getaddrinfo('225.0.0.250', None)[0]
    sl = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sl.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sl.bind((HOST, PORT));
    group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
    mreq = group_bin + struct.pack('=I', socket.INADDR_ANY)
    sl.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while 1:
        #print('{} # ouvindo\n'.format(os.getpid()));
        data, addr = sl.recvfrom(1024); 
        print ("received message:", data.decode())
        if (data.decode()[0]!='a'): #diferente de ACK
            if (int(data.decode()[8])>=clock):
                clock=int(data.decode()[8])+1
            print ('Connected with %s PID: %d\n' % (addr,os.getpid())); 
            c = ('ack %d'% int((data[15:].decode())))
            sl.sendto(c.encode(),('225.0.0.250',PORT))
        else:
                #teoria do que deveria acontecer
                if(contador<2):
                    contador=contador+1;
                else:
                    print("3 acks recebidos! Mensagem enviada para a camada de cima")
                    contador=0

            #guardar de quem foi o ack para contar
            #quando chegar a 3 acks do mesmo x , "tirar da fila"
         #   flag=0
        #    while(flag==0):
       #         if(fila.empty()==True):
      #              time.sleep(randint(5,10));
     #           else:
    #                a = fila.get_nowait()
        #            print(a)
   #                 b=data.decode()[4:]
        #            print(b)
                    #time.sleep(randint(2,35));
  #                  if (int(a[1])==int(b)):
        #                #print('entrou*************')
 #                       flag=1
 #                       if(a[2]<2):
        #                    print(a[2])
        #                    print(type(a[2]))
        #                   # a[2]=a[2]+1
#                            tupla_nova=(a[0],a[1],a[2]+1)
#                            fila.put_nowait(tupla_nova)
#                        else:
#                            print("3 acks recebidos! Mensagem enviada para a camada de cima")
#                    else:
#                        fila.put_nowait(a)


    sl.close()

clock = 0;

if __name__ == "__main__":
    comeco()
