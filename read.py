import pandas as pd
# df = pd.read_csv("D://Python//items.csv", sep="|", names=['id', 'name', 'date', '', 'image_url'])
df = pd.read_csv("D://Python//foo.csv", sep="|",usecols=[0,1,2,4,24], names=['id', 'name', 'date', 'link', 'image_url'])
# df.columns = ['id', 'name', 'date', '','link','','','','','','','','','','','','','','','','','','','', 'image_url']
# print(type(df.loc[:,'id':'date'].to_json))
def index():
  return df
