from bs4 import BeautifulSoup
from requests import get as get_product
from os import remove
from unidecode import unidecode
from json import dumps,load
from os.path import dirname, join
from sqlite3 import connect, Error
from django.utils.text import slugify
# GENERAL INFORMATIONS
# DELL: 36
# HP: 162
# CASPER: 15
# ASUS: 244
# ACER: 82
# MSI: 49
# APPLE : 100
# LENOVO: 330
# HUAWEI: 26
# N11: 242 
# TRENDYOL: 426
# HEPSIBURADA: 302
# VATAN: 65
# 426+302+65+242 = 1035
# TOTAL : 347*2 + 101*3 + 9*4 = 1035

def writecsv(file:str, products:list):
    with open(file, 'a+', encoding = 'utf-8') as f:
        for i in products:f.write(i)
    with open(file, encoding='utf-8') as f_normal:
        with open(file.replace(".csv","_sorted.csv"),"w",encoding="UTF-8") as f_sorted:
            for line in sorted(f_normal.readlines()):f_sorted.write(line+"\n")
    remove(file)

def writejson(file, liste):
    with open(file, 'a+', encoding = 'utf-8') as f:f.write(dumps(liste, indent=2))

def vatan():
    start_url = 'https://www.vatanbilgisayar.com/lenovo-huawei-hp-dell-casper-asus-apple-acer-msi/notebook/'
    pagination=1
    products=[]
    while True:
        if pagination == 21:break
        html = get_product(start_url).content
        soup = BeautifulSoup(html,"html.parser")
        for div in soup.find_all("div",{"class":"product-list product-list--list-page"}):
            name = div.find("div",{"class":"product-list__product-name"}).text.strip().upper()
            link = "https://www.vatanbilgisayar.com"+ str(div.find("a",{"class":"product-list__link"}).get("href"))
            rate = str(int(div.find("span",{"class":"score"}).get("style").strip("width: ").strip("%;"))/20)
            image = div.find("img",{"class":"lazyimg"}).get("data-src")
            price = int((float(div.find("span",{"class":"product-list__price"}).text.strip().replace(" TL","").replace(".","").replace(",","."))))
            products.append(f"{unidecode(name)}, {link}, {price}, {rate}, {image}\n")
        try:
            start_url = f'https://www.vatanbilgisayar.com/lenovo-huawei-hp-dell-casper-asus-apple-acer-msi/notebook/?page={pagination}'
            pagination+=1
        except:break
    writecsv("vatan.csv",products)

def hepsiburada():
    headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 OPR/91.0.4516.36"}
    start_url = 'https://www.hepsiburada.com/asus-lenovo-dell-hp-msi-casper-acer-huawei-apple/laptop-notebook-dizustu-bilgisayarlar-c-98'
    pagination=1
    products=[]
    while True:
        if pagination == 52:break
        html = get_product(start_url,headers=headers).content
        soup = BeautifulSoup(html,"html.parser")
        for li in soup.find_all("li",{"class":"productListContent-zAP0Y5msy8OHn5z7T_K_"}):
            name = li.h3.text.strip().upper()
            link = "https://www.hepsiburada.com"+str(li.a.get("href"))
            rate = li.find("ul",{"data-baseweb":"star-rating"})
            price = li.find("div",{"data-test-id":"price-current-price"})
            if rate is None:rate = "0"
            else:rate = len(rate)
            if price is None:price = "0"
            else:price = int(float(price.text.strip().replace(" TL","").replace(".","").replace(",",".")))
            products.append(f"{unidecode(name)},{link},{price},{rate}\n")
        try:
            start_url = f"https://www.hepsiburada.com/asus-lenovo-dell-hp-msi-casper-acer-huawei-apple/laptop-notebook-dizustu-bilgisayarlar-c-98?sayfa={pagination}"
            pagination+=1
        except:break
    writecsv("hepsi.csv",products)

def trendyol():
    start_url = 'https://www.trendyol.com/sr?wb=102323%2C101606%2C101849%2C103505%2C104964%2C105536%2C101470%2C102324%2C103502%2C107655&wc=103108'
    pagination=1
    products=[]
    while True:
        if pagination == 210:break
        html = get_product(start_url).content
        soup = BeautifulSoup(html,"html.parser")
        for div in soup.find_all("div",{"class":"p-card-chldrn-cntnr card-border"}):
            name = div.find("div",{"class":"prdct-desc-cntnr-ttl-w two-line-text"}).find_all("span")[0].text.strip().upper() + " " + div.find("div",{"class":"prdct-desc-cntnr-ttl-w two-line-text"}).find_all("span")[1].text.strip().upper()
            rate = div.find("div",{"class":"ratings"})
            if rate is None: rate = "0"
            else: rate = len(rate.find_all("div",{"class":"star-w"}))
            price = div.find("div",{"class":"prc-box-dscntd"})
            if price is None: price = "0"
            else: price = int(float(price.text.strip().replace(" TL","").replace(".","").replace(",",".")))
            link = div.find("a")
            if link is None: link = "0"
            else: link = "https://www.trendyol.com"+str(link.get("href"))
            products.append(f"{unidecode(name)},{link},{price},{rate}\n")
        try:
            start_url = f"https://www.trendyol.com/sr?wb=102323%2C101606%2C101849%2C103505%2C104964%2C105536%2C101470%2C102324%2C103502%2C107655&wc=103108&pi={pagination}"
            pagination+=1
        except:break
    writecsv("trendyol.csv",products)

def n11():
    headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 OPR/91.0.4516.36"}
    start_url = 'https://www.n11.com/bilgisayar/dizustu-bilgisayar?m=Lenovo-Asus-HP-Dell-Msi-Monster-Huawei-Acer-Apple-Casper'
    products=[]
    while True:
        html = get_product(start_url,headers=headers).content
        soup = BeautifulSoup(html,"html.parser")
        for li in soup.find_all("li",{"class":"column"}):
            name = li.div.a.h3.text.strip().upper()
            link = "https://www.n11.com/urun" + str(li.div.a.get("href"))
            rate = int(li.find("div",{"class":"ratingCont"}).find_all("span")[0].get("class")[1].strip("r"))/20
            price = int(float(li.find("div",{"class":"priceContainer"}).find("ins").text.strip().replace(" TL","").replace(".","").replace(",",".")))
            products.append(f"{unidecode(name)},{link},{price},{rate}\n")
        try:start_url = soup.find("a", attrs = {"class":"next navigation"})["href"]
        except:break
    writecsv("n11.csv",products)

def generalParser(file1,file2):  
    screens=["15.6INC","14INC","13INC","13.3INC","13.4INC","13.5INC","13.6INC","14.2INC","14.5INC","15INC","16.1INC","16INC","17.3INC","13.9INC","17INC"]
    ram=["4GB","8GB","12GB","16GB","20GB","24GB","32GB","36GB","40GB","48GB","64GB"]
    systems=["W10","W11","W10P","W11P","FREEDOS","LINUX","UBUNTU","MACOS"]
    storage=["128GB","256GB","512GB","1TB","2TB"]
    gen=["I3","I5","I7","I9","R3","R5","R7","R9","M1","M2"]
    processors=["0","11800H","10710U","10850H","10885H","4300U","4500U","11400H","12700H","5500U","12900HK","12900H","1195G7","12500H","1155G7","1135G7","1035G1","10210U","1065G7","1165G7","5800H","5600H","5300U","1005G1","1115G4","3250U","3150U","10200H","5700U","4700U","10300H","6800H","11370H","11300H","11390H","1160G7","3500U","4600H","10870H","10110U","1255U","1035G1U","1155G4","11600H","5900HX","6900HX","9300H","5800U","5600U","4800H","11260H","10750H","12450H","1245U","1145G7","12600H","5005U","1235U","1250U","10500H","12650H","3700U","5825U","12800H","3450U","6100U","7100U","5625U","1035G4","11320H","6600H","8565U","3200U","1265U","7020U","4650U","6900HS","11850H","7020U","12900HX","11980HK","1185G7","6800HS","5800HS","3020E","3050E","11135G7","10510U","12800HX","10510U","5900HS","8265U","11900H","11950H","1130G7","9750HF","10810U","1235G","12950HX","12850HX"]
    brands=["DELL","LENOVO","ASUS","MSI","ACER","HP","APPLE","HUAWEI","HP","CASPER"]
    products=[]            
    with open(file1, encoding='utf-8') as file:
        for line in file:
            name = str(line.strip().split(',')[0]).replace('" DOS','" FREE DOS').replace('" ',"INC ").replace(" GB ","GB ").replace(" TB " ,"TB ").replace("DIZUSTU BILGISAYAR","").replace("DIZSUTU BILGISAYAR","").replace("FREE DOS","FREEDOS").replace("WQXGA","").replace("FHD","").replace("WQHD","").replace("QHD","").replace("WUXGA","").replace("TOUCH","").replace("RYZEN ","R").replace(" HD+","").replace(" HD","").replace("UHD","").replace("CPU "," ").replace("AMD ","").replace(" CORE","").replace("12.NESIL","").replace("11.NESIL","").replace("10.NESIL","").replace("9.NESIL","").replace("8.NESIL","").replace("7.NESIL","").replace("6.NESIL","").replace("5.NESIL","").replace("4.NESIL","").replace("3.NESIL","").replace("2.NESIL","").replace("1.NESIL","").replace("TASINABILIR ","").replace("BILGISAYAR ","").replace(" GUMUS","").replace(" GECE YARISI","").replace(" UZAY GRISI","").replace(" ALTIN","").replace(" YILDIZ ISIGI","").replace(" RETINA","")
            name = name.split(" ")
            name[:] = [x for x in name if x]
            link = str(line.strip().split(',')[1])
            price = str(line.strip().split(',')[2])
            rate = str(line.strip().split(',')[3])
            if len(line.strip().split(','))>4:
                image_link = str(line.strip().split(',')[4])
                products.append([name,price,rate,link,image_link])
            else:
                products.append([name,price,rate,link])
    liste=[]
    modelling=[]
    count=0
    for i in range(len(products)):
        for j in range(len(products[i][0])):
            if products[i][0][j] in screens:
                sc = products[i][0][j]
            elif products[i][0][j] in ram:
                rm = products[i][0][j]
            elif products[i][0][j] in systems:
                ss = products[i][0][j]
            elif products[i][0][j] in storage:
                sr = products[i][0][j]
            elif products[i][0][j] in gen:
                pt = products[i][0][j]
            elif products[i][0][j] in brands:
                br = products[i][0][j]
            elif products[i][0][j] in processors:
                pg = products[i][0][j]
            else:
                modelling.append(products[i][0][j])
        count+=1
        if(count>i and len(products[i])>4):
            liste.append({"br":br,"md":' '.join(modelling),"sc":sc,"rm":rm,"ss":ss,"sr":sr,"pt":pt,"pg":pg,"pr":products[i][1],"rt":products[i][2],"ln":products[i][3],"im":products[i][4]})
            modelling=[]        
        else:
            liste.append({"br":br,"md":' '.join(modelling),"sc":sc,"rm":rm,"ss":ss,"sr":sr,"pt":pt,"pg":pg,"pr":products[i][1],"rt":products[i][2],"ln":products[i][3]})
            modelling=[]

    writejson(file2, liste)

def generalEditer():
    allmodel=[]
    files=["vatan_parsed.json","n11_parsed.json","trendyol_parsed.json","hepsi_parsed.json"]
    for file in files:
        with open(file) as read_file:
            data = load(read_file)
            for i in data:
                site = file.replace("_parsed.json","").upper()
                allmodel.append(f"{i['br']} {i['rm']} {i['sr']} {i['pt']} {i['pg']} {i['ss']} {i['sc']}, {i['rt']}, {i['pr']}, {i['md']}, {i['ln']}, {site}\n")

    writecsv("allmodel.csv",allmodel)
    names=[]
    models=[]
    sites=[]
    with open("allmodel_sorted.csv", encoding='utf-8') as f_normal:
        for line in f_normal:
            name = str(line.strip().split(', ')[0])
            rate = str(line.strip().split(', ')[1])
            price = str(line.strip().split(', ')[2])
            model = str(line.strip().split(', ')[3])
            link = str(line.strip().split(', ')[4])
            site = str(line.strip().split(', ')[5])
            names.append(name)
            models.append(model)
            sites.append(f"{link} {price} {rate}")
            
    def unique(list1):
        ornames = []
        for i in range(len(list1)):
            if list1[i] not in ornames:
                ornames.append(list1[i])
        total=[]
        for i in range(len(ornames)):
            if list1.count(ornames[i])>=3:
                total.append(f"{list1.count(ornames[i])}, {ornames[i]}\n")
        writecsv("allmodel_unique.csv",total)
    unique(names)
    totalization = []
    with open("allmodel_unique_sorted.csv", encoding='utf-8') as f_normal:
        for line in f_normal:
            search = str(line.strip().split(', ')[1])
            with open("allmodel_sorted.csv", encoding='utf-8') as f_normal:
                for line in f_normal:
                    name = str(line.strip().split(', ')[0])
                    rate = str(line.strip().split(', ')[1])
                    price = str(line.strip().split(', ')[2])
                    model = str(line.strip().split(', ')[3])
                    link = str(line.strip().split(', ')[4])
                    site = str(line.strip().split(', ')[5])
                    if search in name:
                        totalization.append(f"{name}, {rate}, {price}, {model}, {link}, {site}\n")
    writecsv("total.csv",totalization)

def finalparser():
    finallist=[]
    c1,c2,c3,c4=0,0,0,0
    givenid=1
    imagelink=""
    linkpro=[]
    with open(join(dirname(__file__), "links.csv"), encoding='utf-8') as fx:
        for i in fx:
            linkpro.append((str(i.strip().split(',')[0]),str(i.strip().split(',')[1])))

    with open(join(dirname(__file__), "total.csv"), encoding='utf-8') as f_normal:
        for line in f_normal:
            if line=="\n":
                if c1==0:
                    Hlink,Hprice,Hrate ="None","None","None"
                if c2==0:
                    Tlink,Tprice,Trate ="None","None","None"
                if c3==0:
                    Nlink,Nprice,Nrate ="None","None","None"
                if c4==0:
                    Vlink,Vprice,Vrate ="None","None","None"
                for i in linkpro:
                    if i[0] == str(givenid):
                        imagelink=i[1]
                finallist.append({"_id":givenid,"slug":slugging,"brand":brand,"model":model,"ram":ram,"storage":storage,"processor":processor,"system":system,"screen":screen,"hepsirate":Hrate,"trendyolrate":Trate,"n11rate":Nrate,"vatanrate":Vrate,"hepsiprice":Hprice,"trendyolprice":Tprice,"n11price":Nprice,"vatanprice":Vprice ,"hepsilink":Hlink,"trendyollink":Tlink,"n11link":Nlink,"vatanlink":Vlink,"imagelink":imagelink})
                c1,c2,c3,c4=0,0,0,0
                givenid+=1     
            else:
                brand = str(line.strip().split(', ')[0]).split(' ')[0]
                model = str(line.strip().split(', ')[3])
                ram = str(line.strip().split(', ')[0]).split(' ')[1]
                storage = str(line.strip().split(', ')[0]).split(' ')[2]
                processor= str(line.strip().split(', ')[0]).split(' ')[3] + " " + str(line.strip().split(', ')[0]).split(' ')[4]
                system = str(line.strip().split(', ')[0]).split(' ')[5]
                screen= str(line.strip().split(', ')[0]).split(' ')[6] 
                link = str(line.strip().split(', ')[4])
                slugging=slugify(brand+" "+model+" "+processor+" "+ram+" "+storage+" "+system+" "+screen)
                screens=["13INC","13.3INC","13.4INC","13.5INC","13.6INC","13.9INC","14INC","14.2INC","14.5INC","15INC","15.6INC","16.1INC","16INC","17.3INC","17INC"]
                rams=["4GB","8GB","12GB","16GB","20GB","24GB","32GB","36GB","40GB","48GB","64GB"]
                systems=["W10","W10P","W11","W11P","FREEDOS","LINUX","UBUNTU","MACOS"]
                storages=["128GB","256GB","512GB","1TB","2TB"]
                processors=['I3 1005G1', 'I3 10110U', 'I3 1115G4', 'I3 7020U', 'I5 10210U', 'I5 10300H', 'I5 1035G1', 'I5 1035G1U', 'I5 10500H', 'I5 11135G7', 'I5 11260H', 'I5 11300H', 'I5 1135G7', 'I5 11400H', 'I5 1155G7', 'I5 1235U', 'I5 12450H', 'I5 9300H', 'I7 1065G7', 'I7 10870H', 'I7 11370H', 'I7 11390H', 'I7 11600H', 'I7 1160G7', 'I7 1165G7', 'I7 11800H', 'I7 11850H', 'I7 1195G7', 'I7 1255U', 'I7 12700H', 'I7 12800HX', 'I7 8565U', 'I9 11950H', 'I9 12900H', 'I9 12900HK', 'I9 12900HX', 'M1 0', 'M2 0', 'R3 3200U', 'R3 3250U', 'R3 5300U', 'R5 3500U', 'R5 4600H', 'R5 5500U', 'R5 5600H', 'R5 5625U', 'R7 3700U', 'R7 4700U', 'R7 4800H', 'R7 5700U', 'R7 5800H', 'R7 5800HS', 'R7 5825U', 'R7 6800H', 'R7 6800HS', 'R9 5900HX', 'R9 6900HX']
                ram = rams.index(ram)+1
                storage= storages.index(storage)+1
                processor = processors.index(processor)+1
                system = systems.index(system)+1
                screen = screens.index(screen)+1
                if link.startswith("https://www.hepsiburada.com"):
                    Hlink = link
                    Hprice,Hrate = str(line.strip().split(', ')[2]),str(line.strip().split(', ')[1])
                    c1+=1
                if link.startswith("https://www.trendyol.com"):
                    Tlink = link
                    Tprice,Trate = str(line.strip().split(', ')[2]),str(line.strip().split(', ')[1])
                    c2+=1
                if link.startswith("https://www.n11.com"):
                    Nlink = link
                    Nprice,Nrate = str(line.strip().split(', ')[2]),str(line.strip().split(', ')[1])
                    c3+=1
                if link.startswith("https://www.vatanbilgisayar.com"):
                    Vlink = link
                    Vprice,Vrate = str(line.strip().split(', ')[2]),str(line.strip().split(', ')[1])
                    c4+=1
    
    writejson("total.json",finallist)

def databaseWrite():
    datam=[]
    with open(join(dirname(__file__), "total.json")) as file:
        file_data = load(file)
        count=0
        for i in file_data:
            if i["trendyollink"]!="None" and count<=100:
                # datam.append((i["_id"],i["brand"],i["model"]))
                count+=1
            # slug = slugify(i["brand"]+" "+i["model"]+" "+str(i["ram"])+"GB "+str(i["storage"])+"GB "+str(i["processor"])+" "+str(i["system"])+" "+str(i["screen"]))
                datam.append((i["_id"],i["slug"],i["processor"],i["ram"],i["storage"],i["system"],i["screen"],i["_id"],i["imagelink"],float(i['trendyolrate']),float(i['trendyolprice'])))
            
            # if i["hepsilink"]!="None":
            #     datam.append((i['hepsilink'],float(i['hepsirate']),float(i['hepsiprice']),i['_id'],'hepsiburada'))
            # if i["trendyollink"]!="None":
            #     datam.append((i['trendyollink'],float(i['trendyolrate']),float(i['trendyolprice']),i['_id'],'trendyol'))
            # if i["n11link"]!="None":
            #     datam.append((i['n11link'],float(i['n11rate']),float(i['n11price']),i['_id'],'n11'))
            # if i["vatanlink"]!="None":
            #     datam.append((i['vatanlink'],float(i['vatanrate']),float(i['vatanprice']),i['_id'],'vatanbilgisayar'))
            
    try:
        sqliteConnection = connect('db.sqlite3')
        cursor = sqliteConnection.cursor()
        print("Bağlantı başarılı")

        # selection = """INSERT INTO shop_brand
        #                 (_id, name, model) 
        #                 VALUES (?, ?, ?);"""
        
        # selection = """INSERT INTO scrap_product
        #                 (_id, slug, processor_id, ram_id, storage_id, system_id, screen_id, name_id, sitelink, rate, price)
        #                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
                        
        # selection = """INSERT INTO scrap_sitesinformation
        #                 (link, rate, price, whichproduct_id,sitename) 
        #                 VALUES (?, ?, ?, ?, ?);"""
        # q=[(i+1,processors[i]) for i in range(len(processors))]
        # selection = """INSERT INTO shop_processor
        #                 (_id, type)
        #                 VALUES (?, ?);"""
        selection = """INSERT INTO shop_product
                        (_id, slug, processor_id, ram_id, storage_id, system_id, screen_id, name_id, image, rate, price)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        cursor.executemany(selection, datam)
        sqliteConnection.commit()
        cursor.close()

    except Error as error:
        print("Hatanın Nedeni", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("Başarıyla tamamlandı")

def getpicture():
    datam=[]
    with open(join(dirname(__file__), "total.json"), encoding='utf-8') as f_normal:
        file_data = load(f_normal)
        for i in file_data:
            if i["trendyollink"]!="None" and i["hepsilink"]!="None" and i["n11link"]!="None" and i["vatanlink"]!="None":
                datam.append((i['_id'],i['trendyollink']))
            if i["trendyollink"]!="None" and i["hepsilink"]=="None":
                datam.append((i['_id'],i['trendyollink']))
            elif i["trendyollink"]=="None" and i["hepsilink"]!="None":
                datam.append((i['_id'],i['hepsilink']))
            elif i["trendyollink"]!="None" and i["n11link"]=="None":
                datam.append((i['_id'],i['trendyollink']))
            elif i["trendyollink"]=="None" and i["n11link"]!="None":
                datam.append((i['_id'],i['n11link']))
            elif i["trendyollink"]!="None" and i["vatanlink"]=="None":
                datam.append((i['_id'],i['trendyollink']))
            elif i["trendyollink"]=="None" and i["vatanlink"]!="None":
                datam.append((i['_id'],i['vatanlink']))
            elif i["hepsilink"]=="None" and i["n11link"]!="None":
                datam.append((i['_id'],i['hepsilink']))
            elif i["hepsilink"]!="None" and i["n11link"]=="None":
                datam.append((i['_id'],i['n11link']))
            elif i["hepsilink"]!="None" and i["vatanlink"]=="None":
                datam.append((i['_id'],i['trendyollink']))
            elif i["hepsilink"]=="None" and i["vatanlink"]!="None":
                datam.append((i['_id'],i['vatanlink']))
            elif i["vatanlink"]!="None" and i["n11link"]=="None":
                datam.append((i['_id'],i['vatanlink']))
            elif i["vatanlink"]=="None" and i["n11link"]!="None":
                datam.append((i['_id'],i['n11link']))
    products=[]
    for i in datam:
        headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 OPR/91.0.4516.36"}
        html = get_product(i[1],headers=headers).content
        soup = BeautifulSoup(html,"html.parser")
        if(i[1].startswith("https://www.hepsiburada")):
            images = soup.find_all("img",{"id":"image-0"})
            print(len(images),end="")
            for q in images:
                products.append((i[0],q.get("src")))
        if(i[1].startswith("https://www.trendyol")):
            images = soup.find_all("img",{'class':'detail-section-img'})
            print(len(images),end="")
            for q in images:
                if i.get("src").startswith("https://cdn.dsmcdn.com/ty"):
                    image=i.get("src")
                    products.append((i[0],image))
    writecsv("links.csv",products)

def myown1():
    start_url = 'http://127.0.0.1:8000'
    pagination=1
    products=[]
    while True:
        if pagination == 20:break
        html = get_product(start_url).content
        soup = BeautifulSoup(html,"html.parser")
        for div in soup.find_all("a",{"class":"col-sm-3 mb-3"}):
            name = div.find_all("p",{"class":"card-title fs-6 info"})[0].text.strip()+" "+div.find_all("p",{"class":"card-title fs-6 info"})[1].text.strip()
            link = 'http://127.0.0.1:8000'+div.get("href")
            image = div.find("img",{"class":"card-img-top img-fluid img-thumbnail"}).get("src")
            products.append(f"{unidecode(name)}, {link} , {image}\n")
        try:
            start_url = f'http://127.0.0.1:8000/?page={pagination}'
            pagination+=1
        except:break
    # writecsv("vatan.csv",products)
    for i in products:
        print(i)

def myown2():
    start_url = 'http://127.0.0.1:8000/shop'
    pagination=1
    products=[]
    while True:
        if pagination == 5:break
        html = get_product(start_url).content
        soup = BeautifulSoup(html,"html.parser")
        for div in soup.find_all("a",{"class":"col-sm-3 mb-3"}):
            name = div.find_all("p",{"class":"card-title fs-6 info"})[0].text.strip()+" "+div.find_all("p",{"class":"card-title fs-6 info"})[1].text.strip()
            link = 'http://127.0.0.1:8000'+div.get("href")
            image = div.find("img",{"class":"card-img-top img-fluid img-thumbnail"}).get("src")
            price = div.find("li",{"class":"list-group-item ms-auto itemsing2"}).text.strip()
            products.append(f"{unidecode(name)}, {link} , {image}, {price}\n")
        try:
            start_url = f'http://127.0.0.1:8000/shop?page={pagination}'
            pagination+=1
        except:break
    print(len(products))
    for i in products:
        print(i)

# vatan()
# n11()
# hepsiburada()
# trendyol() 
# generalParser("hepsi_sorted.csv", "hepsi_parsed.json")
# generalParser("n11_sorted.csv", "n11_parsed.json")
# generalParser("vatan_sorted.csv", "vatan_parsed.json")
# generalParser("trendyol_sorted.csv", "trendyol_parsed.json")
# generalEditer()
# finalparser()
# databaseWrite()
# getpicture()
# myown1()
# myown2()