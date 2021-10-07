#!/usr/bin/env python
# coding: utf-8

# # 1_Markdown 
# 
# 環境設置，default位置查詢，SparkContext object建立
# 
# 

# In[1]:


#Build object pyspark context as the extrance to launch main
import findspark
findspark.init

get_ipython().system('pip install pyspark')
from pyspark.context import SparkContext,SparkConf
import os
import sys
from pyspark.rdd import RDD

#若沒有下面這段
#會有Exception: Java gateway process exited before sending its port number
#Config
os.environ['JAVA_HOME'] = 'C:\Program Files\Java\jre1.8.0_301'
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable


# In[2]:


sc = SparkContext(conf=SparkConf().setAppName("matrix_machine").setMaster("local"))
sc


# In[3]:


os.getcwd()


# # 2_Markdown
# 
# 1. 將檔案input.txt 讀入，切成分別為M開頭的matrix_one  的list 與N開頭的 matrix_two list
# 
# 2. 依照element後切分成兩份txt檔案再存到本機端，再當作兩個matrix RDD檔案匯入(因為不知道RDD怎麼切)。
# 
# 3. 分別存檔成m1.txt, m2.txt
# 4. 將已經拆分的兩份txt matrix檔案以RDD形式讀入
# 
# 

# In[4]:


#讀入有 '\n' 並依照M, N拆成兩筆list

with open('C:///Users/LeoShr/MDA/Hw1///input.txt','r') as f:
    contents = [x for x in f.readlines()]    
    
#切割text file，分別為M開頭的matrix_one  的list 與N開頭的 matrix_two list
matrix_one =[]
matrix_two = []
for ele in contents:
    if ele[0] == 'M':
        matrix_one.append(ele)
    elif(ele[0] == 'N'):
        matrix_two.append(ele)



#讀入沒有 '\n' #依照M, N拆成兩筆text file

# with open('C:///Users/LeoShr/MDA///matrix_com.txt','r') as f:
#     contents = [x.rstrip("\n") for x in f.readlines()]       
# contents


# In[5]:


#default matrix_one, matrix_two會丟到C:\Users\LeoShr\MDA\，並分別命名為m1.txt,m2.txt 

#分別存檔成m1.txt, m2.txt
def save_the_txt_file(lines):
    path_1 = 'C:///Users/LeoShr/MDA///m1.txt'
    path_2 = 'C:///Users/LeoShr/MDA///m2.txt'
    assert (lines == matrix_one)| (lines == matrix_two),'InputError:only matrix_one/matrix_two are acceptable'
    if lines == matrix_one:
        f = open(path_1, 'w')
        f.writelines(lines)
        f.close()
    elif(lines == matrix_two):
        f = open(path_2, 'w')
        f.writelines(lines)
        f.close()       
        

save_the_txt_file(matrix_one)
save_the_txt_file(matrix_two)


# In[6]:


#將已經拆分的兩份txt matrix檔案以RDD讀入
path_1 = 'file:///C:/Users/LeoShr/MDA///m1.txt'
matrix_1  =sc.textFile(path_1)

path_2 = 'file:///C:/Users/LeoShr/MDA///m2.txt'
matrix_2 = sc.textFile(path_2)

#words =sc.textFile(name = 'file://' + path)
print(f'matrix_1:\n{matrix_1}\nmatrix_2:\n{matrix_2}')


# # 3_Markdown
# 
# 1. 看看兩個切好的RDD檔，前20個檔案看看

# In[7]:


n = 20
print(f'matrix_1前{n}個:\n{matrix_1.take(n)}')
print(f'matrix_2前{n}個:\n{matrix_2.take(n)}')


# # 4_Markdown
# 
# 1.  建立to_matrix_a(x)，分別將matrix a 依照','分割成'matrix 字母','row','col','value'，並回傳['col',('row','val')], 以col 為key
# 2. 建立to_matrix_b(x)，分別將matrix b 依照','分割成'matrix 字母','row','col','value'，並回傳['row',('col','val')], 以row 為key
# 
# 矩陣相乘時，matrix_a.col == matrix_b.row; matrix_a.row = matrix_b.col

# In[8]:


#split string to (column, (row, value))
def to_matrix_a(x):
    m,i, j, v = x.split(',')
    return (j, (i, v))
#split string to (row, (column, value))
def to_matrix_b(x):
    m,j, k, v = x.split(',')
    return (j, (k, v))


# # 5_Markdown
# 
# 1. 實際執行map，將matrix_1 rdd依照 to_matrix_a 的function 做map，並assigned as entrance_a
# 2. 實際執行map，matrix_2 rdd依照 to_matrix_b 的function 做map，並assigned as entrance_b
# 
# 3. 觀察一下 entrance_a.collect()  <- 形式(column, (row, value))
# 4.  觀察一下 entrance_b.collect() <- 形式(row, (column, value))
# 
# 
# 5. multiply_mat是最後用來map的function，用途在於使用join好的RDD依照function進行取值，回傳((row,col),(value))的format  

# In[9]:


# entrance_a = matrix_1.flatMap(to_matrix_a)
# entrance_b = matrix_2.flatMap(to_matrix_b)
entrance_a = matrix_1.map(to_matrix_a)

entrance_b = matrix_2.map(to_matrix_b)


# In[10]:


# entrance_a.collect()
# #(column, (row, value))
# entrance_b.collect()
# #(row, (column, value))


# In[11]:


#邏輯 a.col == b.row; a.row == b.col

def multiply_mat(x):
    i, v = x[1][0]
    #print(f'x[1][0]::x:{x}\ni:{i},v:{v}\n\n')
    k, w = x[1][1]
    #print(f'x[1][1]::x:{x}\nk:{k},w:{w}\n\n')

    return ((i, k), (int(v) * int(w)))


# # Final_Markdown
# 
# 1. 將rdd entrance_a 與 entrance_b 以a之key join成同一張RDD後，拿該RDD丟到function- multiply_mat中，取得((i, k), 相乘的值)
# 2. operator.add 會輸入x, y, return (x+y), 該x與y 來自.map(multiply_mat)之後的結果 
# 3. reduceByKey(operator.add)  則在將RDD依照key相加(operator.add)(Basically, we've acheve the goal here already)
# 4. 最後依據function format 回傳 (r,c,v) 避免輸出的位置亂跳
# 5. 使用collect得到rdd

# In[12]:


#依照 sql join 設計的
import operator
from pyspark.mllib.linalg.distributed import CoordinateMatrix, MatrixEntry
from pyspark.sql import SparkSession


#將rdd entrance_a 與 entrance_b 以a之key join成同一張RDD後，拿該RDD丟到function- multiply_mat中，取得((i, k), 相乘的值)
#operator.add 會輸入x, y, return (x+y), 該x與y 來自.map(multiply_mat)之後的結果 
#reduceByKey(operator.add)  則在將RDD依照key相加(operator.add)(Basically, we've acheve the goal here already)
#最後依據function format 回傳 (r,c,v) 避免輸出的位置亂跳

product_entries = entrance_a     .join(entrance_b)     .map(multiply_mat)     .reduceByKey(operator.add)     .map(lambda x:  (x[0][0], x[0][1], x[1]))


# In[13]:


output = product_entries.collect()
output


# In[14]:


len(product_entries.collect()) #250000


# # Save the output as a text file
# - 用with遇到城市會自動close問題   solution: 換行手動寫入txt檔
# - 遇到turple 內int無法iterate問題，因此採用concate(+) solution: 連接轉成str的值，

# In[15]:


fp = open('output.txt', 'w')
for element in output:
    jj = element[0]+','+element[1]+','+str(element[2])
    #print(jj)
    fp.write(jj+'\n')
        
fp.close()              


# In[17]:


#get the unique value in the row
# def get_unique_numbers(numbers):

#     list_of_unique_numbers = []

#     unique_numbers = set(numbers)

#     for number in unique_numbers:
#         list_of_unique_numbers.append(number)

#     return list_of_unique_numbers

#b 的row數 

# def getrow(list_ab):
#     a_list = entrance_a.collect()
#     b_list = entrance_b.collect()
#     rowcount = []
#     for element in range(len(list_ab)):
#         rowcount.append(list_ab[element][0])
#     return get_unique_numbers(rowcount)    
        
# row_count = len(getrow(b_list))
# print(f' #matrix-b: row數量:{row_count}') 

# # b的總長
# entrance_b.count()

# ## b rdd的shape
# b_shape = (len(getrow(b_list)),int(entrance_b.count()/len(getrow(b_list))))
# b_shape


# In[18]:


# #求取a rdd shape
# entrance_a.count()

# a_shape =  (int(entrance_a.count()/len(getrow(a_list))),len(getrow(a_list)))
# a_shape

