# encoding: utf-8
#-*- coding=utf-8 -*-
#coding=utf-8

from bs4 import BeautifulSoup
import urllib2
import urllib
import sys
import os
import re


picList = []
Ranking = []
reload(sys)
sys.setdefaultencoding( "utf-8" )


#用户输入单元
while 1:
	mode = raw_input("Please select mode: (P)ic or (O)oxx\n")
	if mode == "P":
		mode = "pic"
		break
	elif mode == "O":
		mode = "ooxx"
		break

jandan_pic_url = "http://jandan.net/"+mode+"/page-"
startPage = int(raw_input("Please input start page:"))
endPage = int(raw_input("Please input end page:"))



#文档保存单元
for page in range(startPage,endPage):
	targeturl = jandan_pic_url+str(page)
	filename = mode+"_save/"+str(page)+".html"
	fileExist = os.path.exists(filename)
	if (fileExist):
		print "Save exists:"+str(page)
		with open(filename,"r+") as savefile:
			pageData = savefile.read()
			savefile.close()
	else:
		target = urllib2.urlopen(targeturl)
		pageData = target.read()
		try:	
			with open(filename,"w+") as savefile:
				savefile.write("PAGE"+str(page)+"DATA")
				savefile.write(pageData)
				savefile.close()
			print str(page)+" saved."
		except:
			print str(page) + " saving error."
			continue
##吐槽一句，jandan的代码规范做得有点差啊……

	pageData = pageData.replace("</span></small>","</small>") #无故出现的/span会导致bs4出现灵异现象

#数据处理单元
	soup = BeautifulSoup(pageData)
	# picSet = soup.select(".text")
	picSet = soup.select("li[id|=comment] div.row")
	# print picSet
	for pic in picSet:
		# print pic.previous_element
		src = []
		getin = False;
		try:
			content = pic.find("div",class_="text").p.text
			oo = pic.select("[id|=cos_support]")[0].text
			xx = pic.select("[id|=cos_unsupport]")[0].text
		except:
			print "过滤错误"
			print pic
			continue
		



		# print len(pic.select("img"))
		# print pic.select("img")
		# try:
		# 	for i in range(0,len(pic.select("img"))):
		# 		src[i] = pic.select("img")[i]["src"]
		# 		if "gif" in src[i]:
		# 			src[i] = pic.select("img")[i]["org_src"]
		# except:
		# 	print "error."
		# 	continue
		try:
			for i in range(0,len(pic.select("img"))):
				# print i
				src.append(pic.select("img")[i]["src"])
				if "gif" in src[i]:
					src[i] = pic.select("img")[i]["org_src"]
		except:
			print "error."
			print pic
			continue
		score = int(oo) - int(xx)
		is_nsfw = False;
		# print content.lower()
		if ("nsfw" in content.lower()):
			is_nsfw = True
		author = pic.find("div",class_="author").strong.text
		pic = {}
		pic['author'] = author
		pic['score'] = score
		pic['src'] = src
		pic['oo'] = oo
		pic['xx'] = xx
		pic['content'] = content
		pic['page'] = page
		# if (is_nsfw):
		if (int(score) >= 1000 or int(oo) >= 500):
			picList.append(pic)
	print page,"Done."

print "筛选到图片"+str(len(picList))+"张，正在排序，请等待"

while(len(picList)):
	maxid = 0
	maxScore = 0
	for pics in picList:
		# print pics['score']
		if (pics['score'] > maxScore):
			maxid = picList.index(pics)
			maxScore = pics['score']
	Ranking.append(picList[maxid])
	picList.remove(picList[maxid])

documentHead = """
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html" charset="utf-8" />
	<title>jandan 无聊图排行</title>
	<style>
		#header {
			width:100%;
			height:300px;
			text-align:center;
			background-color:rgb(0,178,255);
			color:rgb(255,242,0);
		}
		h1 {
		    margin: 0 50px 50px 50px;
		}

		#title {
		    line-height: 200px;
		}

		body {
		    margin: 0;
		}
		.pic {
		    text-align: center;
		    margin-top: 20px;
		}

		span.oo,span.xx {
		    margin: 10px;
		}

		hr {
		    border-style: solid;
		    color: rgb(255, 203, 0);
		}

		a {
		    color: rgb(255, 174, 0);
		}
	</style>
</head>
<body>
<div id='header'>
	<div id="title"><h1>煎蛋无聊图排行</h1></div>
	<div id="h_text"><small>此网页由<a href='http://weibo.com/aurorad'>Yinz</a>制作生成</small></div>
</div>
"""


documentEnd = """
<!-- 多说评论框 start -->
	<div class="ds-thread" data-thread-key="yinzwuliaotu" data-title="煎蛋无聊图排行" data-url="meiyouurlyineishibendide.com"></div>
<!-- 多说评论框 end -->
<!-- 多说公共JS代码 start (一个网页只需插入一次) -->
<script type="text/javascript">
var duoshuoQuery = {short_name:"yinzwuliaotu"};
	(function() {
		var ds = document.createElement('script');
		ds.type = 'text/javascript';ds.async = true;
		ds.src = (document.location.protocol == 'https:' ? 'https:' : 'http:') + '//static.duoshuo.com/embed.js';
		ds.charset = 'UTF-8';
		(document.getElementsByTagName('head')[0] 
		 || document.getElementsByTagName('body')[0]).appendChild(ds);
	})();
	</script>
<!-- 多说公共JS代码 end -->
<img style="display:none" src="http://547300.cicp.net/statistics/jandan_ranker/">

</body>
</html>
"""
document = documentHead

print "总计上榜：",len(Ranking)
listNum = int(raw_input("请输入输出数量：\n"))
picPerPage = int(raw_input("请输入每页图片数量（推荐20）：\n"))
resultfilename = str(raw_input("请输入输出文件名称（无后缀名）："))

num = 0		#控制循环数量
pageNum = 1
for pic in Ranking:
	# for picIndex in picPerPage:
	if(num==int(listNum)):
		break
	document += "<div class='pic'>"
	for picx in pic['src']:
		document += "<a href='"+picx+"'><img src='"+picx+"'></a><br />"
	document += "<p><strong>发布者："+pic['author']+"</strong></p><br />"
	document += "<p>"+str(pic['content'])+"</p>"
	document += "<span class='oo'>oo:	"+str(pic['oo'])+"</span><span class='xx'>xx:	"+str(pic['xx'])+"</span>"
	document += "<a href='"+jandan_pic_url+str(pic['page'])+"'><p>第"+str(pic['page'])+"页</p></a>"
	document += "<hr /></div>"
	num+=1
	if num % picPerPage == 0:
		document += documentEnd
		with open(resultfilename+str(pageNum)+".html","w+") as resultfile:
			resultfile.write(document)
		document = documentHead
		pageNum += 1	
if listNum % picPerPage:
	document += documentEnd
	with open(resultfilename+str(pageNum)+".html","w+") as resultfile:
		resultfile.write(document)
