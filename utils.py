from configparser import ConfigParser


class Parser:

    def __init__(self, path):
        self.path = path
        self.p = ConfigParser()
        self.p.read(path)

    def get(self, *args):
        return self.p.get(*args)

    def set(self, *args):
        self.p.set(*args)
        with open(self.path, "w") as f:
            self.p.write(f)


cfgParse = Parser(".ddns.ini")

if __name__ == "__main__":
    cfgParse.set("route", "ip", "1233")
    print(cfgParse.get("other", "ip_url"))
