import pandas as pd
import 爬取数据 as pa
datas = []
for name, auther, kinds, statues in zip(pa.names, pa.authors, pa.kinds, pa.statuses):
    datas.append([name, auther, kinds, statues])
df = pd.DataFrame(datas, columns=['书名','作者','类型','状态'])
print(df)