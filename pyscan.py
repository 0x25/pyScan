#!/usr/bin/env python

"""Multi thread nmap scan in parallel"""

__author__      = "0x25"
__copyright__   = "GNU General Public Licence"

import shlex, subprocess, time, sys, os, argparse
from multiprocessing import Process, Queue
from random import shuffle
import signal

# configuration
nmapPath="/usr/bin/nmap"
xlstprocPath="/usr/bin/xsltproc"
path="scan"

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    exit(0)

signal.signal(signal.SIGINT, keyboardInterruptHandler)

# child process
def scan(procId,jobs,data):
    try:
        while True:
            jobData = jobs.get_nowait()
            ip = jobData['ip'].strip()

            print "[%s] start scan : %s"%(procId,ip)

            fname =  "%s/%s.log"%(path,ip)
            cmd = "%s %s -v -oA %s/%s %s"%(nmapPath,data,path,ip,ip)

            args = shlex.split(cmd)
            p = subprocess.Popen(args,stdout=open(fname, 'w'))

            while p.poll() is None:
                print "[%s]  process scan : %s"%(procId,ip)
                time.sleep(5)

            if xsltprocExist is True:
                cmd = "%s scan/%s.xml -o %s/%s.html"%(xlstprocPath,ip,path,ip)
                args = shlex.split(cmd)
                p = subprocess.Popen(args,stdout=open(fname, 'w'))

                while p.poll() is None:
                    print "[%s] create html for %s"%(procId,ip)
                    time.sleep(2)

    except:
        pass # when job empty
        #print "Unexpected error:", sys.exc_info()[0]
        #raise
#def
xsltprocExist = True

def main():
    global xsltprocExist

    if not os.path.exists(nmapPath):
        print "Nmap not found\nPlease install it to continue !"
        exit(2)

    if not os.path.exists(xlstprocPath):
        print "xsltproc not found. No HTML output will be done !"
        xsltprocExist = False

    if len(sys.argv) <= 1:
        print "Use -h to see help"
        exit(2)

    defaultNmapCmd = '-n -Pn -sS -A -sC -sV --open --script-args http.useragent="Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.5) Gecko/20041202 Firefox/1.0"'
    defaultThread = 4
    defaultMode = ''
    modes = {"F":"-F", "A":"-p-"}

    description ="\033[1;31m Parallel scan with nmap. Default value : thread [%s] nmap cmd [%s] \033[0m"%(defaultThread,defaultNmapCmd)
    epilog="\033[0;35m If you like this tool you can send me some monero \o/ { 4Ahnr36hZQsJ3P6jowXvs7cLkSVbkq2KyfQBVURYVftcj9tDoA592wT1jskroZEk2QDEZFPYMLqVvJWZHecFwQ9nL15SzRG } \033[0m"

    # parse args
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument('-t','--thread', type=int, default=defaultThread, help='Number of concurent thread')
    parser.add_argument('-f','--file',required=True, help='File with one IP or IP/CIDR line by line')
    parser.add_argument('-c','--cmd',default=defaultNmapCmd, help='Set nmap parameter (don\'t add -v or xml,nmap output). Use quote !')
    parser.add_argument('-m','--mode',default=defaultMode, help='faste F or all A default is Normal(1000)')
    parser.add_argument('-s','--shuffle', action='store_true', help='shuffle IP values')
    args = parser.parse_args()

    filename = args.file
    nbProcess = args.thread
    cmd = args.cmd
    blend = args.shuffle

    if args.mode in modes:
        cmd = "%s %s"%(modes[args.mode],cmd)

    # start code
    jobs = Queue()
    pool=[]

    # process
    for procId in range(nbProcess):
        print "start process [%s/%s]"%(procId,nbProcess)
        pool.append(Process(target=scan, args=(procId,jobs,cmd)))

    # read file
    with open(filename) as f:
        ips = f.read().splitlines()

    # shuffle data if ask
    if blend:
        shuffle(ips)

    # jobs
    for ip in ips:
        jobs.put({'ip': ip})

    print "load %s jobs in queue"%(jobs.qsize())

    # start process
    for proc in pool:
        proc.start()

    for proc in pool:
        proc.join()

# main
if __name__ == '__main__':
    main()
