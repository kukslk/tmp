from pyzabbix import ZabbixAPI

zapi = ZabbixAPI('http://localhost/zabbix/')
zapi.session.verify = False
try:
	zapi.login("Admin", "zabbix")
except:
	print('Fuck yourself')
	
def get_hosts(zapi):
	for host in zapi.host.get():
		interfaces=zapi.hostinterface.get(hostids=host['hostid'])
		for interface in interfaces:
			print(host['hostid'],host['name'],interface['dns'],f'{interface["ip"]}:{interface["port"]}',sep=' ___ ')
get_hosts(zapi)
hosts=zapi.host.get()
id=zapi.script.create(name='asdasdasd',command='uname -a;ip a;',type=0,scope=2)
print(id['scriptids'][0])
print(hosts[0]['hostid'])
try:
	print(zapi.script.execute(scriptid=id['scriptids'][0]))
except Exception as e:
	print(e)
#zapi.script.delete(id['scriptids'][0])
