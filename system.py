from subprocess import Popen, PIPE 
import re 

#获取主机名,也可以使用 uname -n 命令获取 
def hostname(): 
	hostname = Popen(["hostname"], stdout=PIPE) 
	hostname = hostname.stdout.read() 
	return hostname 

#获取操作系统版本 
def osversion(): 
	with open("/etc/redhat-release") as f: 
		osversion = f.read() 
	return osversion 

#获取操作系统内核版本 
def oscoreversion(): 
	oscoreversion = Popen(["uname", "-r"], stdout=PIPE) 
	oscoreversion = oscoreversion.stdout.read() 
	return oscoreversion 

#获取CPU相关信息,如果存在多种不同CPU，那么CPU型号统计的为最后一种型号,这种情况少见 
def cpuinfo(): 
	corenumber = [] 
	with open("/proc/cpuinfo") as cpuinfo: 
		for i in cpuinfo: 
			if i.startswith("processor"): 
				corenumber.append(i) 
			if i.startswith("model name"): 
				cpumode = i.split(":")[1] 
	return corenumber, cpumode #调用此函数需要用两个变量来接收参数 

#获取内存相关信息 
def meminfo(): 
	with open("/proc/meminfo") as meminfo: 
		for i in meminfo: 
			if i.startswith("MemTotal"): 
				totalmem = i.split(":")[1] 
	return totalmem 

#获取服务器硬件相关信息 
def biosinfo(): 
	biosinfo = Popen(["dmidecode", "-t", "system"], stdout=PIPE) 
	biosinfo = biosinfo.stdout.readlines() 

for i in biosinfo: 
	if "Manufacturer" in i: 
		manufacturer = i.split(":")[1] 
	if "Serial Number" in i: 
		serialnumber = i.split(":")[1] 
	return manufacturer, serialnumber #调用此函数需要使用两个变量接收参数 

#获取网卡信息,包括网卡名，IP地址，MAC地址 
def ipaddrinfo(): 

	#定义存储格式，以网卡名为key，mac地址和ip地址为一个列表，这个列表又为这网卡名的value 
	def add(dic, key, value): 
		dic.setdefault(key, [ ]).append(value) 

		ipinfo = Popen(["ip", "addr"], stdout=PIPE) 
		ipinfo = ipinfo.stdout.readlines() 

		dict1 = {} 
		for i in ipinfo: 
			if re.search(r"^\d", i): 
				devname = i.split(": ")[1] 
				continue
			if re.findall("ether", i): 
				devmac = i.split()[1] 
				add(dict1, devname, devmac) 
				continue
			if re.findall("global", i): 
				devip = i.split()[1] 
				add(dict1, devname, devip) 
				continue
		return dict1 

if __name__ == "__main__": 
	hostname = hostname() 
	osversion = osversion() 
	oscoreversion = oscoreversion() 
	totalmem = meminfo() 
	cpunumber, cpumode = cpuinfo() 
	manufacturer, serialnumber = biosinfo() 
	ipinfo = ipaddrinfo() 
	print("%s:\t\t %s" %("主机名", hostname)), 
	print("%s:\t %s" %("系统版本", osversion)), 
	print("%s:\t %s" %("系统内核版本", oscoreversion)), 
	print("%s:\t %s" %("总内存", totalmem)), 
	print("%s:\t%s" %("CPU生厂商", cpumode)), 
	print("%s:\t %s" %("CPU总核心数", len(cpunumber))) 
	print("%s:\t%s" %("服务器生厂商", manufacturer)), 
	print("%s:\t%s" %("服务器序列号", serialnumber)), 
	for x in ipinfo: 
		y = ipinfo.get(x) 
		ip = y[1] 
		mac = y[0] 
		print("%s%s:\t %s\t%s" %("网卡", x, ip, mac))