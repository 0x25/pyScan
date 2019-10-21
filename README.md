# pyScan
multi thread nmap scan parallel  

>scan.py -h  
>usage: scan.py [-h] [-t THREAD] -f FILE [-c CMD]  
>  
> Parallel scan with nmap. Default value : thread [4] nmap cmd [-n -Pn
-sT -A]                                                                                                                                   
>  
>optional arguments:  
>  -h, --help            show this help message and exit  
>  -t THREAD, --thread THREAD  
>                        Number of concurent thread  
>  -f FILE, --file FILE  File with one IP/CIDR line by line  
>  -c CMD, --cmd CMD     Set nmap parameter (don't add -v or xml,nmap output).  
>                        Use quote !  
>  -s, --shuffle         shuffle IP values  


# install
>git clone https://github.com/0x25/pyScan.git  
>cd pyScan  
>chmod +x pyscan.py  
>./pyscan.py -h  

# to do
progress bar



