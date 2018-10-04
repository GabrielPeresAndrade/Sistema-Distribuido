from multiprocessing import Process;
import time;
import os;
import socket;
import threading;
import struct;

def comeco():
    p = Process(target=main, args=());
    p.start();
    p1 = Process(target=main, args=());
    p1.start();
    main();

def main():
    time.sleep(2);
    fila=[(9999,-1,-1),(9999,-1,-1),(9999,-1,-1),(9999,-1,-1),(9999,-1,-1),(9999,-1,-1),(9999,-1,-1),(9999,-1,-1),(9999,-1,-1),(9999,-1,-1),(9999,-1,-1)]
    ordena(fila)
    print('O MEU PID :{}\n'.format(os.getpid()));
    #OUVIR
    t_ouvir = threading.Thread(target=ouvir,args=(fila,2));
    t_ouvir.start();
    time.sleep(2);
    #FALAR
    falar(fila)

def falar(fila):

    HOST1 = '225.0.0.250'
    PORT = 8888
    global clock
    print('{} # Mandando mensagem :\n'.format(os.getpid()))


    addrinfo = socket.getaddrinfo('225.0.0.250', None)[0]
    sf = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    ttl = struct.pack('b', 1)
    sf.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL,ttl)
    

    c=('clock = %d PID =%d'% (clock,os.getpid()))
    a =(clock,os.getpid(),0)
    clock = clock +1;
    sf.sendto(c.encode(),(HOST1,PORT))
    fila[0]=a
    ordena(fila)
    
    time.sleep(2);


def ouvir(fila,t):

    HOST = ''
    PORT = 8888
    global clock
    contador=0

    addrinfo = socket.getaddrinfo('225.0.0.250', None)[0]
    sl = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sl.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sl.bind((HOST, PORT));
    group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
    mreq = group_bin + struct.pack('=I', socket.INADDR_ANY)
    sl.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while 1:
        data, addr = sl.recvfrom(1024); 
        print ("recebi a mesnagem:", data.decode())
        if (data.decode()[0]!='a'): #diferente de ACK
            if (int(data.decode()[8])>=clock):
                clock=int(data.decode()[8])+1
            print ('Conectado com %s PID: %d\n' % (addr,os.getpid())); 
            c = ('ack %d'% int((data[15:].decode())))
            sl.sendto(c.encode(),('225.0.0.250',PORT))
        else:
            flag=0
            i=0
            while(flag==0):
                a=fila[i]
                b=data.decode()[4:]
                if(int(a[1])>0):
                    if (int(a[1])==int(b)):
                        flag=1
                        if(a[2]<2):
                        	tupla_nova=(a[0],a[1],a[2]+1)
                        	fila[i]=tupla_nova
                        	ordena(fila)
                        else:
                        	if(i==0):
                        		print("3 acks recebidos! Mensagem enviada para a camada de cima")
                        		fila[i]=(9999,-1,-1)
                        		ordena(fila)
                        	else:
                        		tupla_nova=(a[0],a[1],a[2]+1)
                        		fila[i]=tupla_nova
                        		ordena(fila)
                    else:
                        i=i+1
                else:
                    tupla_nova=(clock,b,1)
                    fila[i]=tupla_nova
                    flag=1
            i=0
            while(fila[i][0]!=9999):
                b = data.decode()[4:]
                a=fila[i]
                if ((int(a[1])==int(b))and(a[2]==3)and(i==0)):
                    print("3 acks recebidos! Mensagem enviada para a camada de cima")
                    fila[i]=(9999,-1,-1)
                    ordena(fila)
                i=i+1



    sl.close()
def ordena(fila):
	fila.sort(key=lambda x: x[0])

clock = 0;

if __name__ == "__main__":
    main()

