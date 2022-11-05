import easygui
import socket

def createfile():
    template_start = '{"CurrentRegionIdx":3,"Regions":[{"$type":"DnsRegionInfo, Assembly-CSharp","Fqdn":"na.mm.among.us","DefaultIp":"50.116.1.42","Port":22023,"Name":"North America","TranslateName":289,"UseDtls":true},{"$type":"DnsRegionInfo, Assembly-CSharp","Fqdn":"eu.mm.among.us","DefaultIp":"172.105.251.170","Port":22023,"Name":"Europe","TranslateName":290,"UseDtls":true},{"$type":"DnsRegionInfo, Assembly-CSharp","Fqdn":"as.mm.among.us","DefaultIp":"139.162.111.196","Port":22023,"Name":"Asia","TranslateName":291,"UseDtls":true}'
    template_end = ']}'

    template = '{"$type":"DnsRegionInfo, Assembly-CSharp","Fqdn":"~hostname~","DefaultIp":"~ip~","Port":~port~,"Name":"~name~","TranslateName":1003,"UseDtls":false}'

    hostname = easygui.enterbox("hostname of server")
    template = template.replace("~hostname~", hostname)

    ip = socket.gethostbyname(hostname)
    template = template.replace("~ip~", ip)

    while True:
        try:
            port = int(easygui.enterbox("server port"))
            break
        except:
            # not int
            easygui.msgbox("... i don't think that was a number...")

    template = template.replace("~port~", str(port))

    name = easygui.enterbox("how to server should appear in game (the name it will go by similar to the asia server being 'asia' and the North America server being 'North America'")
    template = template.replace("~name~", name)

    with open("./regionInfo.json", 'w') as f:
        f.write(template_start+","+template+template_end)

    with open("./regionInfo.json", 'r') as f:
        print(repr(f.readlines()))
    return "./regionInfo.json"