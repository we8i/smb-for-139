#! /usr/bin/env python
#-*- coding: utf-8 -*-
import tempfile,time,optparse
from smb.SMBConnection import SMBConnection
from nmb.NetBIOS import NetBIOS
def ip2hostname(ip):
    nb = NetBIOS(broadcast=True, listen_port=0)
    try:
        hostname = nb.queryIPForName(str(ip), port=137, timeout=10)
        hostname=hostname[0]
    except:
        print 'hostname get fail please use -n'
        exit(0)
    return str(hostname)
def run(username,password,ip,hostname='',Pathurl='',filename='',outfile=''):
    try:
        print Pathurl
        if '\\\\' in Pathurl:
            sharename = str(Pathurl.split('\\\\')[0])
            #print sharename
            path = str(Pathurl.split('\\\\')[1])
            #print path
        else:
            sharename = ''
            path = ''
        if hostname=='':
            hostname = ip2hostname(ip)
        if '\\' in username:
            domain = username.split('\\')[0]
            username = username.split('\\')[1]
        else:
            domain=''
        conn = SMBConnection(username,password,'',hostname,domain)
        try:
            conn.connect(ip, 139)
        except Exception ,e:
            print e
            return
        result = ''
        if sharename == '':
            if conn.auth_result:
                print 'Login Success to %s!' %hostname 
                shares = conn.listShares()
                for share in shares:
                    result = result + share.name + '\r\n'
            else:
                print 'Login Fail to %s!' %hostname 
        elif filename == '':
            if conn.auth_result:
                try:
                    files = conn.listPath(sharename,path)
                    result = result + 'share dir:' + sharename + '/'+ path + '\r\n'
                    for f in files:
                        type =('<DIR>' if f.isDirectory else '<File>')
                        result = result+str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(f.create_time) )) +'    '+str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(f.last_write_time ) ))+'    '+type+' '+str(f.file_size) +'  '+f.filename + '\r\n'
                except Exception ,e:
                    print e
            else:
                print 'Login Fail to %s!' % hostname 
        else:
            if conn.auth_result:
                tempfp = tempfile.TemporaryFile()
                conn.retrieveFile(str(sharename), str(path) + '\\' + str(filename), tempfp)
                tempfp.seek(0)
                result = tempfp.read()
                if outfile != '':
                    output = open(outfile, 'wb')
                    output.write(result)
                    output.close
                    result =  'Write to %s successs! on %s' % (outfile,hostname)
            tempfp.close()
        print result
    except Exception ,e:
        print e
if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-i", "--ip", dest="ip", help="Target IP")
    parser.add_option("-u", "--username", dest="username", help="Target username")
    parser.add_option("-p", "--password", dest="password", help="Target password")
    parser.add_option("-f", "--file", dest="file",help="Show Target file (e.g \"smb.py -u admin -p admin -b c$\\\\temp\\ -f 1.txt\")",default='')
    parser.add_option("-o", "--outfile", dest="outfile",help="Download Target file (e.g \"smb.py -u admin -p admin -b c$\\\\temp\\ -f 1.txt -o c:\\1.txt \")",default='')
    parser.add_option("-b", "--path", dest="path",help="Show Target paths (e.g \"smb.py -u admin -p admin -b c$\")",default='')
    parser.add_option("-n", "--hostname", dest="hostname",help="Target hostname (e.g \"smb.py -u admin -p admin -b c$ -f 1.txt -n apple-pc\")",default='')
    options, _ = parser.parse_args()
    if (options.ip and options.username and options.password):
        run(options.username,options.password,options.ip,options.hostname,options.path,options.file,options.outfile)
    else:
        parser.print_help()