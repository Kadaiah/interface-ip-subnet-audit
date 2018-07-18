from netmiko import ConnectHandler
import getpass
from datetime import datetime
import pprint
import socket
import csv
user_name = input('Please enter username ')
pwd = getpass.getpass('Enter Password: ')
#host_list = raw_input('Please enter hostname/h
show_eigrp_cmd = 'show  ip eigrp neigh'


with open('routerlist.txt') as f:
    content = f.readlines()

content = [x.strip() for x in content]
host_list = content 
for host in host_list:
    print ("Connecting to device %s with cerdentials of %s" %(host,user_name))
    cisco = {'device_type': 'cisco_ios','ip': host ,'username': user_name ,'password': pwd}
    ssh_conn = ConnectHandler(**cisco)
    if ssh_conn.check_enable_mode() == True:
        print ('logged into the device and we are in enable prompt !')
    else:#
        print ('Ops !! something wrong with the password of %s, pls try again !!' %user_name)
    print ("preparing the details for the audit")
	
    show_ip_eigrp = ssh_conn.send_command(show_eigrp_cmd)
    #pprint.pprint(show_ip_eigrp)


# break the long string into a list based on newlines.
    show_ip_lines = show_ip_eigrp.split("\n")

# Initialize a blank list so that we can use .append() on it

    show_ip_list = []


# Iterate over each of the lines in the 'show ip int brief'
    for line in show_ip_lines:

    # Skip the header line
        if 'Address' in line:
            continue

    # Break line into words
        line_split = line.split()

    # Filter out lines that don't have the correct number of fields
        if len(line_split) == 9:

        # map these variables to the fields in the line_split list
            discard1, ip_addr, if_name, discard2, discard3, discard4, discard5, discard6, discard7 = line_split
            show_int_addr=ssh_conn.send_command('show int {} | in Internet'.format(if_name))
            #pprint.pprint(show_int_addr)
			
            int_addr =show_int_addr.split()[3]
           
            print ("****************************")
            print ("Script Completed")

            hostnames=socket.gethostbyaddr(ip_addr)[0]
            show_ip_list.append((host,if_name,int_addr,hostnames,ip_addr))			
    with open('nfa.csv', 'a') as myfile:
        writer = csv.writer(myfile, delimiter=',')
        for line in show_ip_list:
            writer.writerow(line)
