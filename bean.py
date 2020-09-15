import json


class Fragment:
    local_ip = None
    local_port = None
    dest_ip = None
    dest_port = None
    filename = None

    def to_json(self):
        return json.dumps({
            "local_ip": self.local_ip,
            "local_port": self.local_port,
            "dest_ip": self.dest_ip,
            "dest_port": self.dest_port,
            "filename": self.filename
        })

    def from_json(self, fragment):
        json_loads = json.loads(fragment)
        self.local_ip = json_loads["local_ip"]
        self.local_port = json_loads["local_port"]
        self.dest_ip = json_loads["dest_ip"]
        self.dest_port = json_loads["dest_port"]
        self.filename = json_loads["filename"]
