from r2env.package import Package
from r2env.repl import main
import r2env.ipdb


def load_packages(cfg):
	from r2env.db import Radare2
	pkgs = []
	pkgs.append(Radare2(cfg))
	return pkgs

cfg = {
	"srcdir": "", # depends on the pkg
	"linkdir": "/usr",
	"envdir": 123,
	"prefix": "",
}

class R2Env:
	def __init__(self):
		self.db = load_packages(cfg)
	def du(self):
		return "0KB"
	def version(self):
		return "0.1.0"
	def available_packages(self):
		return self.db
	def installed_packages(self):
		return ipdb.list()
