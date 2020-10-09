from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import Global_var
from Insert_On_Datbase import insert_in_Local,create_filename
import sys, os
import ctypes
import string
import requests
import urllib.request
import urllib.parse
import re
import html
import wx
app = wx.App()
def ChromeDriver():

    browser = webdriver.Chrome(executable_path=str(f"F:\\chromedriver.exe"))
    browser.maximize_window()
    browser.get("""https://chrome.google.com/webstore/detail/browsec-vpn-free-and-unli/omghfjlpggmjjaagoclmmobgdodcjboh?hl=en" ping="/url?sa=t&amp;source=web&amp;rct=j&amp;url=https://chrome.google.com/webstore/detail/browsec-vpn-free-and-unli/omghfjlpggmjjaagoclmmobgdodcjboh%3Fhl%3Den&amp;ved=2ahUKEwivq8rjlcHmAhVtxzgGHZ-JBMgQFjAAegQIAhAB""")
    for Add_Extension in browser.find_elements_by_xpath('/html/body/div[4]/div[2]/div/div/div[2]/div[2]/div'):
        Add_Extension.click()
        break
    wx.MessageBox(' -_-  Add Extension and Select Proxy Between 25 SEC -_- ', 'Info', wx.OK | wx.ICON_WARNING)
    time.sleep(25)  # WAIT UNTIL CHANGE THE MANUAL VPN SETTING
    browser.get("https://nrc.oil.gov.iq/")
    wx.MessageBox(' -_-  Fill captch First If There -_- ', 'Info', wx.OK | wx.ICON_INFORMATION)
    time.sleep(2)
    browser.get("https://nrc.oil.gov.iq/index.php?name=monaksa")
    time.sleep(2)
    for Search_button in browser.find_elements_by_xpath('/html/body/div[1]/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td[2]/table[2]/tbody/tr/td/table/tbody/tr/td/center/input'):
        Search_button.click()
        break
    td = 2
    tender_href_list = []
    for release_date in browser.find_elements_by_xpath('/html/body/div[1]/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td[2]/table[2]/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr/td[5]/center'):
        release_date = release_date.get_attribute('innerText').strip()
        datetime_object = datetime.strptime(release_date, '%Y-%m-%d')
        publish_date = datetime_object.strftime("%Y-%m-%d")
        datetime_object_pub = datetime.strptime(publish_date, '%Y-%m-%d')
        User_Selected_date = datetime.strptime(str(Global_var.From_Date), '%Y-%m-%d')
        timedelta_obj = datetime_object_pub - User_Selected_date
        day = timedelta_obj.days
        if day >= 0:
            for tender_href in browser.find_elements_by_xpath(f'/html/body/div[1]/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td[2]/table[2]/tbody/tr/td/table/tbody/tr/td/table[2]/tbody/tr[{str(td)}]/td[8]/div/a'):
                tender_href = tender_href.get_attribute('href').strip()
                tender_href_list.append(tender_href)
                td += 1
                break
        else:
            Scrap_data(browser, tender_href_list)


def Scrap_data(browser, Tender_href):

    a = True
    while a == True:
        try:
            for href in Tender_href:
                browser.get(href)
                time.sleep(2)
                SegFeild = []
                for data in range(45):
                    SegFeild.append('')

                get_htmlSource = ""
                for outerHTML in browser.find_elements_by_xpath('/html/body/div/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td[2]/center/table'):
                    get_htmlSource = outerHTML.get_attribute('outerHTML')
                    get_htmlSource = get_htmlSource.replace('href="upload/', 'href="https://nrc.oil.gov.iq/upload/')
                    break
                # Purchaser
                SegFeild[12] = 'NORTH REFINERIES COMPANY (NRC)'
                SegFeild[2] = "Baiji, Iraq<br>\n Phone: +974 7725 7608"
                SegFeild[8] = 'http://www.nrc.oil.gov.iq/'
                Name_of_Directorate = ''
                for Name_of_Directorate in browser.find_elements_by_xpath('/html/body/div/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td[2]/center/table/tbody/tr[2]/td[2]'):
                    Name_of_Directorate = Name_of_Directorate.get_attribute('innerText').replace('&nbsp;', '').strip()
                    break

                # Title
                for Tender_Subject in browser.find_elements_by_xpath('/html/body/div/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td[2]/center/table/tbody/tr[3]/td[2]'):
                    Tender_Subject = Tender_Subject.get_attribute('innerText').replace('&nbsp;', '').strip()
                    Tender_Subject = string.capwords(str(Tender_Subject)).strip()
                    SegFeild[19] = Tender_Subject
                    break

                # Email
                for Email in browser.find_elements_by_xpath('/html/body/div/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td[2]/center/table/tbody/tr[4]/td[2]/div'):
                    Email = Email.get_attribute('innerText').replace('&nbsp;', '').replace('&nbsp;', '').strip().replace(' ','')
                    SegFeild[1] = Email.strip()
                    break

                # tender NO
                for Bid_number in browser.find_elements_by_xpath('/html/body/div/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td[2]/center/table/tbody/tr[5]/td[2]'):
                    Bid_number = Bid_number.get_attribute('innerText').replace('&nbsp;', '').strip()
                    SegFeild[13] = Bid_number.strip()
                    break

                # Release Date
                Release_Date = ""
                for Release_Date in browser.find_elements_by_xpath('/html/body/div/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td[2]/center/table/tbody/tr[6]/td[2]'):
                    Release_Date = Release_Date.get_attribute('innerText').replace('&nbsp;', '').strip()
                    break

                # Extention Date
                Extention_Date = ""
                for Extention_Date in browser.find_elements_by_xpath('/html/body/div/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td[2]/center/table/tbody/tr[8]/td[2]'):
                    Extention_Date = Extention_Date.get_attribute('innerText').replace('&nbsp;', '').strip()
                    if Extention_Date == "لايوجد تمديد":
                        Extention_Date = ""
                    break

                # Close Date
                try:
                    for Close_Date in browser.find_elements_by_xpath('/html/body/div/center/table/tbody/tr[7]/td/table[1]/tbody/tr/td[2]/center/table/tbody/tr[7]/td[2]'):
                        Close_Date = Close_Date.get_attribute('innerText').strip()
                        datetime_object = datetime.strptime(Close_Date, "%Y-%m-%d")
                        mydate = datetime_object.strftime("%Y-%m-%d")
                        SegFeild[24] = mydate
                except:
                    SegFeild[24] = ""

                SegFeild[18] = "موضوع المناقصة: " + str(SegFeild[19]) + "<br>\n""اسم المديرية: " + str(Name_of_Directorate) + "<br>\n""تاريخ الاصدار: " + str(Release_Date) + "<br>\n""تاريخ تمديد المناقصة: " + str(Extention_Date) + "<br>\n""تاريخ الاغلاق: " + str(SegFeild[24])

                SegFeild[7] = "IQ"

                # notice type
                SegFeild[14] = "2"

                SegFeild[22] = "0"

                SegFeild[26] = "0.0"

                SegFeild[27] = "0"  # Financier

                SegFeild[28] = str(href)

                # Source Name
                SegFeild[31] = 'nrc.oil.gov.iq'

                SegFeild[20] = ""
                SegFeild[21] = "" 
                SegFeild[42] = SegFeild[7]
                SegFeild[43] = "" 

                for SegIndex in range(len(SegFeild)):
                    print(SegIndex, end=' ')
                    print(SegFeild[SegIndex])
                    SegFeild[SegIndex] = html.unescape(str(SegFeild[SegIndex]))
                    SegFeild[SegIndex] = str(SegFeild[SegIndex]).replace("'", "''")
                a = False
                check_date(get_htmlSource, SegFeild)
                print(" Total: " + str(len(Tender_href)) + " Duplicate: " + str(
            Global_var.duplicate) + " Expired: " + str(Global_var.expired) + " Inserted: " + str(
            Global_var.inserted) + " Skipped: " + str(
            Global_var.skipped) + " Deadline Not given: " + str(
            Global_var.deadline_Not_given) + " QC Tenders: " + str(Global_var.QC_Tender),"\n")
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("Error ON : ", sys._getframe().f_code.co_name + "--> " + str(e), "\n", exc_type, "\n", fname, "\n", exc_tb.tb_lineno)
            a = True
        ctypes.windll.user32.MessageBoxW(0, "Total: " + str(len(Tender_href)) + "\n""Duplicate: " + str(
            Global_var.duplicate) + "\n""Expired: " + str(Global_var.expired) + "\n""Inserted: " + str(
            Global_var.inserted) + "\n""Skipped: " + str(
            Global_var.skipped) + "\n""Deadline Not given: " + str(
            Global_var.deadline_Not_given) + "\n""QC Tenders: " + str(Global_var.QC_Tender) + "",
                                         "nrc.oil.gov.iq", 1)
        Global_var.Process_End()
        browser.quit()
        sys.exit()


def check_date(get_htmlSource, SegFeild):
    tender_date = str(SegFeild[24])
    nowdate = datetime.now()
    date2 = nowdate.strftime("%Y-%m-%d")
    try:
        if tender_date != '':
            deadline = time.strptime(tender_date , "%Y-%m-%d")
            currentdate = time.strptime(date2 , "%Y-%m-%d")
            if deadline > currentdate:
                insert_in_Local(get_htmlSource, SegFeild)
            else:
                print("Tender Expired")
                Global_var.expired += 1
        else:
            print("Deadline was not given")
            Global_var.deadline_Not_given += 1
    except Exception as e:
        exc_type , exc_obj , exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("Error ON : " , sys._getframe().f_code.co_name + "--> " + str(e) , "\n" , exc_type , "\n" , fname , "\n" , exc_tb.tb_lineno)


ChromeDriver()