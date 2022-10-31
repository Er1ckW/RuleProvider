import wget
import os


def savefile(rules, filename, path):
    domain = rules[0]
    ipcidr = rules[1]
    if domain:
        with open(f"{path}/{filename}.list", encoding="utf-8", mode="w") as f:
            f.writelines(domain)
    if ipcidr:
        with open(f"{path}/{filename}IP.list", encoding="utf-8", mode="w") as f:
            f.writelines(ipcidr)


def downloadfile(filepath):
    with open(filepath, encoding="utf-8", mode="r") as f:
        content = f.readlines()
    for line in content:
        wget.download(line, "ClassicRules/")
    print("Download Complete!")


def main():
    downloadfile("SurgeList.list")
    classic_path = "ClassicRules"
    new_path = "Surge"
    rule_list = os.listdir(classic_path)
    for rule in rule_list:
        filename = rule.split(".")[0]
        filepath = f"{classic_path}/{rule}"
        with open(filepath, encoding="utf-8", mode="r") as f:
            content_list = f.readlines()
        domain_list = []
        ip_list = []
        for content in content_list:
            rule = content.split(",")
            if rule[0] == 'DOMAIN-SUFFIX' or rule[0] == 'DOMAIN':
                domain_list.append(f".{rule[1]}")
            elif rule[0] == "IP-CIDR":
                ip_list.append(",".join(rule))

        savefile([domain_list, ip_list], filename, new_path)


if __name__ == "__main__":
    main()
    print("Transformation Complete!")
