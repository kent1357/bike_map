import folium
import urllib.request as req
import json
import requests
from bs4 import BeautifulSoup
import tkinter as tk
import os

# 匯入資料
with req.urlopen("https://datacenter.taichung.gov.tw/swagger/OpenData/9af00e84-473a-4f3d-99be-b875d8e86256") as res:
    page_data = json.load(res)    # 以 JSON 格式，讀取「網站伺服器的回應
# print(page_data)   

# print(page_data['retVal'][0]['lat'])  #查看第一筆資料站點的緯度

# len(page_data['retVal'])   #查看資料共幾筆
# In[]
# 地址地名轉經緯度
# https://richard98hess444.medium.com/python%E7%88%AC%E8%9F%B2-google-maps-%E5%9C%B0%E6%A8%99%E8%88%87%E5%9C%B0%E5%9D%80%E8%BD%89%E7%B6%93%E7%B7%AF%E5%BA%A6-b63eea8d8ca7
num_data=[]
def get_add():
    num_data.clear()
    address=address_entry.get()

    URL="https://www.google.com/maps/place?q="+address

    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.prettify()


    initial_pos = text.find(";window.APP_INITIALIZATION_STATE")
#尋找;window.APP_INITIALIZATION_STATE所在位置

    data = text[initial_pos+36:initial_pos+85] #將其後的參數進行存取    

    line = tuple(data.split(',')) 
    num1 = float(line[2])
    num2 = float(line[1])
    
    num_data.append(num1)
    num_data.append(num2)
    make_map()

# In[]
# 定義地圖初始位置
def thu():
    num_data.clear()
    num_data.append(24.1805919)
    num_data.append(120.5982932)
    make_map()

def fengyuan():
    num_data.clear()
    num_data.append(24.2541919)
    num_data.append(120.7212929)
    make_map()
def fss():
    num_data.clear()
    num_data.append(24.1504541)
    num_data.append(120.6843595)
    make_map()
def mitsukoshi():
    num_data.clear()
    num_data.append(24.1653475)
    num_data.append(120.6425868) 
    make_map()
def tai_train():
    num_data.clear()
    num_data.append(24.1367988)
    num_data.append(120.6866958)
    make_map()
def fcu():
    num_data.clear()
    num_data.append(24.1786547)
    num_data.append(120.6467411)
    make_map()
def thsrc():
    num_data.clear()
    num_data.append(24.1122514)
    num_data.append(120.6155867)
    make_map()
def nmns():
    num_data.clear()
    num_data.append(24.1565094)
    num_data.append(120.666452)
    make_map()

# In[]
# 繪製地圖、打上各站點icon
def make_map():
    fmap = folium.Map(location=[num_data[0],num_data[1]], zoom_start=16) 
    fmap.add_child(folium.Marker(location=[num_data[0],num_data[1]],
                                 color='#ffffff', 
                                 popup='您的所在地', 
                                 ))
    for i in range(len(page_data['retVal'])):
        x=''
        if page_data['retVal'][i]['act']!=1:
            x="gray"
        elif int(page_data['retVal'][i]['sbi'])==0 or int(page_data['retVal'][i]    ['bemp'])==0:
            x='red'
        else:
            x='green'
        
        m = folium.Marker(location=[page_data['retVal'][i]['lat'],page_data['retVal'][i]    ['lng']],
                   popup=page_data['retVal'][i]['sna']+'剩餘車輛數'+page_data['retVal'][i]   ['sbi']+'剩餘車位數'+page_data['retVal'][i]['bemp'],
                   icon=folium.Icon(color=x))

        fmap.add_child(child=m)

    fmap.save('map.html')

    os.system('C:/Users/user/Desktop/OneDrive_1_2021-6-26/練習/map.html')
    # 開啟產出的html檔，這邊用的是我個人電腦上的路徑，請自行修改


# In[]
# 圖像化界面，定義各按鈕功能
win=tk.Tk()

win.title('u-bike車位查詢')

header_label1 = tk.Label(win, text='選擇查詢地點或輸入地址、地名')
header_label1.pack()

label2 = tk.Label(win, text="資料更新時間:"+page_data['updated_at'],bg="yellow", padx=20, pady=10)
label2.pack()

button1=tk.Button(win,text='東海大學',command=thu,width=20)
button1.pack()

button2=tk.Button(win,text='豐原火車站',command=fengyuan,width=20)
button2.pack()

button3=tk.Button(win,text='一中街',command=fss,width=20)
button3.pack()

button4=tk.Button(win,text='新光三越',command=mitsukoshi,width=20)
button4.pack()

button5=tk.Button(win,text='台中火車站',command=tai_train,width=20)
button5.pack()

button6=tk.Button(win,text='逢甲大學',command=fcu,width=20)
button6.pack()

button7=tk.Button(win,text='高鐵台中站',command=thsrc,width=20)
button7.pack()

button8=tk.Button(win,text='科學博物館',command=nmns,width=20)
button8.pack()

address_frame = tk.Frame(win)
address_frame.pack(side=tk.TOP)
address_label = tk.Label(address_frame, text='請輸入地址或地名')
address_label.pack(side=tk.LEFT)
address_entry = tk.Entry(address_frame)
address_entry.pack(side=tk.LEFT)

map_btn = tk.Button(win, text='產生地圖', command=get_add)
map_btn.pack()

win.mainloop()
