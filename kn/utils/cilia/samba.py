import subprocess
import datetime

import cStringIO as StringIO

def samba_setpass(cilia, user, password):
	ph = subprocess.Popen(['smbpasswd', '-as', user],
	                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
	                stderr=subprocess.STDOUT, close_fds=True)
	(output, bogus) = ph.communicate("%s\n" % password)
	return output

def set_samba_map(cilia, _map):
	io = StringIO.StringIO()
	io.write("# Automatically generated by Cilia.set_samba_map()\n\n")
	for g in _map['groups']:
		gname = ('kn-%s'%g)[:32]
		io.write("[%s]\n" %g )
		io.write("  comment = %s\n" % g)
		io.write("  path = /groups/%s\n" % g)
		io.write("  valid users = +%s\n" % gname)
		io.write("\n")
	group_config = io.getvalue()
	with open("/etc/samba/groups.conf", "w") as gc:
		gc.write(group_config)
	with open("/etc/samba/base.conf") as bc:
		base = bc.read()
	with open("/etc/samba/smb.conf", "w") as fc:
		fc.write(base)
		fc.write("\n")
		fc.write(group_config)
	# NOTE We could SIGHUP samba but it picks up new configurations
	# each minute anyway