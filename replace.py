import urllib.request
import re

def save_image(url,path):
    url=url[4:-1]
    urllib.request.urlretrieve(url,filename=path.split('(')[1][1:-1])

to_fix="_posts/2022-4-26-AWS-ECR-ECS.md"
with open(to_fix,"r") as f:
    data=f.read()

folder=re.findall("image: /images/(.*)/info.png",data)[0]


for i in re.findall(pattern="!\[\]\(.*\)",string=data):
    name=i.split("/")[-1][:-1]
    file=f"![](/images/{folder}/{name})"
    save_image(i,file)
    data=data.replace(i,file)

with open(to_fix,"w") as f:
    f.write(data)
