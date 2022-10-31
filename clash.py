from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO
import wget
import os


# class MyDumper(yaml.Dumper):
#     def increase_indent(self, flow=False, indentless=False):
#         return super(MyDumper, self).increase_indent(flow, False)
class MyYAML(YAML):
    def dump(self, data, stream=None, **kw):
        inefficient = False
        if stream is None:
            inefficient = True
            stream = StringIO()
        YAML.dump(self, data, stream, **kw)
        if inefficient:
            return stream.getvalue()


yaml = MyYAML()
yaml.indent(mapping=2, sequence=4, offset=2)


def readfile(filepath):
    with open(filepath, encoding="utf-8", mode="r") as f:
        content = f.read()
    x = yaml.load(content)
    return x


def savefile(rules, filename, path):
    domain = {"payload": rules[0]}
    ipcidr = {"payload": rules[1]}
    if domain["payload"]:
        with open(f"{path}/{filename}.yaml", encoding="utf-8", mode="w") as f:
            content_domain = yaml.dump(domain)
            content_domain = content_domain.replace("\"\'", "\'")
            content_domain = content_domain.replace("\'\"", "\'")
            f.write(content_domain)
    if ipcidr["payload"]:
        with open(f"{path}/{filename}IP.yaml", encoding="utf-8", mode="w") as f:
            content_ip = yaml.dump(ipcidr)
            content_ip = content_ip.replace("\"\'", "\'")
            content_ip = content_ip.replace("\'\"", "\'")
            f.write(content_ip)


def downloadfile(filepath):
    with open(filepath, encoding="utf-8", mode="r") as f:
        content = f.readlines()
    for line in content:
        wget.download(line, "ClassicRules/")
    print("Download Complete!")


def main():
    downloadfile("ClashList.list")
    classic_path = "ClassicRules"
    new_path = "Clash"
    rule_list = os.listdir(classic_path)
    for rule in rule_list:
        filename = rule.split(".")[0]
        rule_dict = readfile(f"{classic_path}/{rule}")
        payload = rule_dict["payload"]
        domain_list = []
        ip_list = []
        for line in payload:
            rule = line.split(",")
            if rule[0] == "DOMAIN-SUFFIX" or rule[0] == "DOMAIN":
                domain_list.append(f"'+.{rule[1]}'")
            elif rule[0] == "IP-CIDR":
                ip_list.append(f"'{rule[1]}'")
        savefile([domain_list, ip_list], filename, new_path)


if __name__ == "__main__":
    main()
    print("Transformation Complete!")
