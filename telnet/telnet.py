# coding: utf-8
# this file is a part of VK4XMPP Transport.
# Parts of code from telnetsrvlib.

import SocketServer
import threading
import time
import sys
from telnetsrv.threaded import TelnetHandler, command


try: 
	execfile("telnetcfg.txt")
except Exception:
	Print("#! Telnet config doesn't exists or it's wrong!")

class TelnetHandler(TelnetHandler):

	WELCOME = "You have connected to the vk4xmpp debug server."
	PROMPT = "vk4xmpp> "
	authNeedUser = True
	authNeedPass = True
	
	def authCallback(self, username, password):
		"""Called to validate the username/password."""
		if self.client_address[0] not in ALLOW_FROM:
			raise

		if username != TELNET_USERNAME or password != TELNET_PASSWORD:
			raise

	def session_start(self):
		"""Called after the user successfully logs in."""
		self.writeline("This server is running on %s." % TELNET_IP)
		self.writeline("Hello %s!" % self.username)
	
	def session_end(self):
		"""Called after the user logs off."""
		pass

	def writeerror(self, text):
		"""Called to write any error information (like a mistyped command).
		Add a splash of color using ANSI to render the error text in red.
		see http://en.wikipedia.org/wiki/ANSI_escape_code"""
		self.writeline("\x1b[91m%s\x1b[0m" % text )

	@command("eval")
	def command_eval(self, params):
		"""[params]
		Execute python's eval"""
		params = str.join(" ", params)
		try:
			result = unicode(eval(params))
		except:
			result = returnExc()
		self.writeline(result)

	@command("exec")
	def command_exec(self, params):
		"""[params]
		Execute python's exec in globals.
		Note: you can use only one line in code. So better use execfile("filename", globals()) or contact transport in jabber."""
		params = str.join(" ", params)
		try: 
			exec(unicode(params + "\n"), globals())
			result = "Done."
		except Exception: 
			result = returnExc()
		self.writeline(result)

	@command("stop")
	def command_stop(self, nothing):
		"""
		Stopping transport
		"""
		os.kill(os.getpid(), 15)

	@command("list")
	def command_userlist(self, count):
		"""[count]
		Shows the count list splitted by \\n"""
		if not count:
			count = -1
		else:
			count = count[0]
		count = int(count)
		with Database(DatabaseFile) as db:
			db("select jid from users")
			while count != 0:
				jid = db.fetchone()
				if jid:
					jid = jid[0]
				else:
					break
				self.writeline(jid)
				count -= 1

	@command("globmsg")
	def command_globmsg(self, msg):
		"""[msg]
		Will send message to each transport user"""
		count = 0
		with Database(DatabaseFile) as db:
			db("select jid from users")
			jids = db.fetchall()
			msg = str.join("", msg)
			for jid in jids:
				count += 1
				msgSend(Component, jid[0], msg, TransportID, timestamp = 1) ## TODO: Maybe use server-like messages instead
		self.writeline("Your message was successfully sent to %d users." % count)

	@command("delete")
	def command_deleteuser(self, users):
		"""[user]
		Deletes users splitted by space from database"""
		with Database(DatabaseFile) as db:
			for user in users:
				db("delete from users where jid=?", (user,))
				self.writeline("deleting %s from database..." % user)

	@command("flushlog")
	def command_flushlog(self, nothing):
		"""
		Flushing log file
		"""
		with open(logFile, "w") as file:
			file.flush()

	@command("config")
	def command_config(self, nothing):
		"""
		Reloads transport's config
		"""
		try:
			execfile(Config, globals())
		except Exception:
			self.writeline(returnExc())


class TelnetServer(SocketServer.TCPServer):
	allow_reuse_address = True
	

def init_server():
	Print("Starting telnet server at port %d.  (Ctrl-C to stop)" % (TELNET_PORT) )
	global server
	server = TelnetServer((TELNET_IP, TELNET_PORT), TelnetHandler)
	server.serve_forever()


def shutdown():
	try:
		server.server_close()
	except Exception:
		Print("#! Couldn't stop telnet server.")

Handlers["evt01"].append(init_server)
Handlers["evt02"].append(shutdown)

