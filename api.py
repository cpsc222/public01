#!/usr//bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import pwd
import grp
import base64

HOST = "0.0.0.0"
PORT = 3000

USERNAME = "test"
PASSWORD = "abcABC123456"

class API(BaseHTTPRequestHandler):

	def _unauthorized(self):
		self.send_response(401)
		self.send_header("www-authenticate",'basic realm-"restricted"')
		self.end_headers()

	def _authorized(self):
		auth =  self.headers.get("Authorization")
		if not auth or not auth.startswith("Basic "):
			return False

		encoded = auth.split(" ")[1]
		decoded = base64.b64decode(encoded).decode()
		user, pw = decoded.split(":", 1)
		return user == USERNAME and pw == PASSWORD

	def do_POST(self):
		if not self._authorized():
			self._unauthorized()
			return

		if self.path == "/api/users":
			users = {str(u.pw_uid): u.pw_name for u in pwd.getpwall()}
			self._send_json(users)

		elif self.path == "/api/groups":
			groups = {str(g.gr_gid): g.gr_name for g in grp.getgrall()}
			self._send_json(groups)

		else:
			self.send_response(404)
			self.end_headers()

	def _send_json(self, data):
		self.send_response(200)
		self.send_header("content type","application/json")
		self.end_headers()
		self.wfile.write(json.dumps(data).encode())

if __name__ == "__main__":
	server = HTTPServer((HOST, PORT), API)
	print(f"api listening on http://{HOST}:{PORT}")
	server.serve_forever()
