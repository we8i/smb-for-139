# smb-for-139
勒索病毒都把445搞蹦了。。
没事还有个139



Usage: smb_share.py [options]

Options:
  -h, --help            show this help message and exit
  -i IP, --ip=IP        Target IP
  -u USERNAME, --username=USERNAME
                        Target username
  -p PASSWORD, --password=PASSWORD
                        Target password
  -f FILE, --file=FILE  Show Target file (e.g "smb.py -u admin -p admin -b
                        c$\\temp\ -f 1.txt")
  -o OUTFILE, --outfile=OUTFILE
                        Download Target file (e.g "smb.py -u admin -p admin -b
                        c$\\temp\ -f 1.txt -o c:\1.txt ")
  -b PATH, --path=PATH  Show Target paths (e.g "smb.py -u admin -p admin -b
                        c$")
  -n HOSTNAME, --hostname=HOSTNAME
                        Target hostname (e.g "smb.py -u admin -p admin -b c$
                        -f 1.txt -n apple-pc")

