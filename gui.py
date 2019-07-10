
from tkinter import *
import tkinter
from phone import Phone
import pygeoip
import re
from PIL import Image
import os
from tkinter import messagebox


def phone_type(args):
    pass

class App(object):
    
    def __init__(self):
        self.gi = Phone('phone.dat')
        self.gi2 = pygeoip.GeoIP('GeoLiteCity.dat')
        self.root = tkinter.Tk()
        self.menubar = Menu(self.root)
        filemenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='图片编辑', menu=filemenu)
        self.root['menu'] = self.menubar
        filemenu.add_command(label="压缩图片", command=lambda:self.compressImage('pic','mini_pic'))
        filemenu.add_command(label="帮助", command=self.help)
        filemenu.add_command(label="关于", command=self.about)
        filemenu.add_command(label="退出", command=self.root.quit)
        self.root.title("ip地址和号码归属地查询、批量压缩图片小工具")
        self.Label=tkinter.Label(self.root, text="请输入IP地址或者电话号码:",width=50)
        self.text_input = tkinter.Entry(self.root,width=30 )
        self.display_info = tkinter.Listbox(self.root, width=50)
        self.result_button = tkinter.Button(self.root,background='blue',command = self.find_position, text ="查询")
    def about(self):
        messagebox.showinfo('关于', '作者：darwin \n verion 1.0 \n 感谢您的使用！ \n fengxiaoyu.info@gmail.com ')
    def help(self):
        messagebox.showinfo('帮助','在当前目录下建名为‘pic’文件夹,\n将需要压缩的图片放入点击压缩,\n压缩后的图片会在当前目录下,\n一个名为‘pic_mini’的文件夹中。')
    def compressImage(self,srcPath,dstPath):
        for filename in os.listdir(srcPath):
            if not os.path.exists(dstPath):
                os.makedirs(dstPath)
            srcFile=os.path.join(srcPath,filename)
            dstFile=os.path.join(dstPath,filename)
            if os.path.isfile(srcFile):
                sImg=Image.open(srcFile)
                w,h=sImg.size
                dImg=sImg.resize((w//3,h//3),Image.ANTIALIAS)  
                dImg.save(dstFile) 
            if os.path.isdir(srcFile):
                compressImage(self,srcFile,dstFile)
    def gui_arrang(self):
        self.Label.pack()
        self.text_input.pack()
        self.display_info.pack()
        self.result_button.pack()
    def find_position(self):
        self.text_addr = self.text_input.get() 
        if re.match(r"^1[35678]\d{9}$", self.text_addr):
            aim = self.gi.find(self.text_addr)
            try:
                phones = aim["phone"]
                phone_type= aim["phone_type"]
                province = aim["province"]
                city = aim["city"]
                zip_code = aim["zip_code"]
                area_code = aim["area_code"]
            except:
                pass           
            the_info = ["号段:"+str(phones),"公司:"+str(phone_type),"省份:"+str(province),"城市:"+str(city), "邮编:"+str(zip_code),"座机:"+str(area_code), "需要查询的号段:"+str(self.text_addr)]
            for item in range(10):
                self.display_info.insert(0,"")
            for item in the_info:
                self.display_info.insert(0,item)
            return the_info
        elif re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", self.text_addr):
            aim= self.gi2.record_by_addr(self.text_addr)
            try:
                city = aim["city"]
                region_code= aim["region_code"]
                country_name = aim["country_name"]
                longitude = aim["longitude"]
                latitude = aim["latitude"]
            except:
                pass
            the_info = ["城市:"+str(city),"编号:"+str(region_code),"国家:"+str(country_name),"纬度:"+str(longitude), "经度:"+str(latitude), "需要查询的IP:"+str(self.text_addr)]
            for item in range(10):
                self.display_info.insert(0,"")
            for item in the_info:
                self.display_info.insert(0,item)
            return the_info
        else:
        	
            the_info="请输入正确的ip、手机号码地址！"
            self.display_info.insert(0,the_info)
            return the_info
    
       

def main():

    FL = App()
    FL.gui_arrang()
    tkinter.mainloop()
    pass


if __name__ == "__main__":
    main()
    
