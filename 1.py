import  urllib2,datetime,glob 
import pandas as pd

def garbage_collection(file_contents):
   print "Зашли в чистку"
   index = file_contents.find("<pre>",0)
   file_contents = file_contents[index+5:]
   index = file_contents.find("</pre>",0)
   file_contents = file_contents[:index]
   index = file_contents.find("provinceID")
   file_contents = file_contents[:(index-3)] + file_contents[(index+10):]
   file_contents = file_contents.replace('  ', ' ')
   file_contents = file_contents.replace(' ', ',')
   file_contents = file_contents.replace(',,', ',')  
   return file_contents

def download(region_index):
   print "Зашли в скрипт"
   url="https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_provinceData.php?country=UKR&provinceID="+str(region_index)+"&year1=1981&year2=2018&type=Mean"
   vhi_url = urllib2.urlopen(url)
   now = datetime.datetime.now()
   date='';
   for part_of_date in [now.year , now.month, now.day, now.hour, now.minute, now.second]:
      if len(str(part_of_date))<2:
         date+="_0"+str(part_of_date)
      else:
         date+="_"+str(part_of_date)
   print "Дописали дату"
   csv_file_name="vhi_id_" + str(get_id(region_index))+date+".csv"
   out = open(csv_file_name,'wb')
   
   file_contents = vhi_url.read()
   print "Открыли для чистки"
   file_contents = garbage_collection(file_contents)

   out.write(file_contents)
   print "Почистили"
   out.close()
   print ("VHI is downloaded..."+str(region_index)) 

def csv_into_frame(path,region_index):
   temp = path + "/vhi_id_" + str(get_id(region_index))+ "*.csv"
   temp = temp.replace('//','/')
   files = glob.glob(temp)
   for file_name in files:
      file_name = file_name.replace('//','/')
      #print file_name
      df = pd.read_csv(file_name,header=0,names=['year','week','SMN','SMT','VCI','TCI','VHI'],delimiter=',')
      return df

def get_id(region_index):
   id_dict = {1:22 , 2:24 , 3:23 , 4:25 , 5:3 ,6:4 ,7:8 ,8:19 ,9:20 ,10:21 , 11:9
   ,12:9 ,13:10 ,14:11 ,15:12 ,16:13 ,17:14 ,18:15 ,19:16 ,20:25 ,21:17 ,22:18 ,
   23:6 ,24:1 ,25:2 ,26:6 ,27:5 }
   return id_dict[region_index]
   

key = 0
path = r"C:\Users\НАТАЛИ\Desktop\1"
if key:
   for region_index in range(1,28):
      download(region_index)
      #print csv_into_frame(path,region_index)
else:
   for region_index in range(1,2):
      print csv_into_frame(path,region_index)

def choice_1(year,region_index):
   df = csv_into_frame(path,region_index)
   table = df.loc[(df['year']==year)]
   print table['VHI']
   print "Максимальное за год"
   print table['VHI'].nlargest(1)
   print "Минимальное за год"
   print table['VHI'].nsmallest(1)

def choise_2(region_index):
   table = csv_into_frame(path,region_index)
   print "Екстремальное"
   print table.loc[(table['VHI'] < 15)]
   print "Не екстремальное"
   print table.loc[(table['VHI'] > 15) & (table['VHI'] < 35)]

choice_1(2005,2)
choise_2(2)
   



   




