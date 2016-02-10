import requests
from bs4 import BeautifulSoup

over = []
text = []
new = []

Team_id = 1 

def comment():

		url = 'http://www.espncricinfo.com/australia-v-india-2015-16/engine/match/895815.html?innings='
		url+=str(Team_id)
		url+=';view=commentary'
		source_code = requests.get(url)   # source code of page
		plain_text = source_code.text
		soup = BeautifulSoup(plain_text)
		soup.encode('UTF-8')
		for link in soup.findAll('div' , {'class' : 'commentary-text'} ):      # a = find all links of the titles 
			#href = link.get('href')     # pulling links of this class
			title = link.contents[1].encode('UTF-8')         # here string is for <href = "something"...> Titlesndjsnd </href>   then it is Titlesndjsnd 
			text.append(str(title))
			#print(title)
			#overs.append(title)
		#	print(href , "\t")
		#	print( get_single_item_data(href) )   # who posted in that page forums 
		
		for link in soup.findAll('div' , {'class' : 'commentary-overs'} ):      # a = find all links of the titles 
			#href = link.get('href')     # pulling links of this class
			title1 = link.string         # here string is for <href = "something"...> Titlesndjsnd </href>   then it is Titlesndjsnd 
			over.append(str(title1))
		

		clean_up_list(text)
		#print("\n")



def clean_up_list(word_list):
	i=0;
	for word in word_list:
		
		word = word.replace(r"b'<p>", r"")
		word = word.replace(r'b"<p>', r"")
		word = word.replace(r'\n', r" ")
		word = word.replace(r'\t', r" ")
		word = word.replace(r'</p>"', r" ")
		word = word.replace(r"</p>'", r" ")
		word = word.replace(r"</b>", r" ")
		word = word.replace(r'span class="commsImportant">',r" ")
		word = word.replace(r'</span>' , r" ")
		word = word.replace(r'<strong>',r" ")
		word = word.replace(r'</strong>',r" ")
		word = word.replace('\\', r" ")

		if word.startswith("<b>") :
			continue
		word = word.replace(r'<',r'')
		new.append(word)

		#print(over[i] , word)
		i+=1

# call
def Separate(content):
	bowler = ""
	Batsman = ""
	Run = 0
	Wicket = ""
	status = ""
	Runstatus = False
	Outstatus = False
	total = 0
	wide = False
	no_ball = False
	for comment1 in content:
		comment = comment1.split()
		#print(comment)
		#print(comment[0] , "    "  ,comment[1] )
		if comment[1] =="to" :
			bowler = comment[0]
			x = comment[2]
			if x[-1]==",":
				Batsman = x[:-1]
				status = comment[3]
				if comment[4] =="wide," :
					wide = True
				else:
					wide= False
				
				if comment[3] =="(no" :
					no_ball = True
					status = comment[5]
				else: 
					no_ball= False

				if comment[4] =="leg" :
					leg = True
				else: 
					leg = False



			else:
				Batsman = comment[2]+ " " +comment[3][:-1]
				status = comment[4]
				if comment[5] =="wide," :
					wide = True
				else: 
					wide = False
				
				if comment[4] =="(no" :
					no_ball = True
					status = comment[6]
				else: 
					no_ball= False

				if comment[5] =="leg" :
					leg = True
				else: 
					leg = False


		else :
			bowler = comment[0]+comment[1]
			x = comment[3]
			if x[-1]==",":
				Batsman = x[:-1]
				status = comment[4]
				if comment[5] =="wide," :
					wide = True
				else:
					wide = False

				if comment[4] =="(no" :
					no_ball = True
					status = comment[6]
				else: 
					no_ball= False

				if comment[5] =="leg" :
					leg = True
				else: 
					leg = False

			else:
				Batsman = comment[3]+ " " +comment[4][:-1]
				status = comment[5]
				if comment[6] =="wide," :
					wide = True
				else:
					wide = False

				if comment[5] =="(no" :
					no_ball = True
					status = comment[7]
				else: 
					no_ball= False

				if comment[6] =="leg" :
					leg = True
				else: 
					leg = False


		if status=="no":
				run = 0
				Runstatus = True
		elif status=="1":
				run = 1
				Runstatus = True
		elif status =="2":
				run = 2
				Runstatus = True
		elif status =="3":
				run = 3
				Runstatus = True
		elif status =="FOUR":
				run = 4
				Runstatus = True
		elif status =="SIX":
				run = 6
				Runstatus = True
		elif status =="OUT":
				Outstatus = True
				Runstatus = False

		if Runstatus:
			total+=run
		else:
			run=0
		if no_ball:
			total+=1

		#print(bowler , "       " , Batsman  , "     " , run , "   " , Runstatus   , "wide=" , wide  , "no ball =" , no_ball , "leg=" , leg)
		#print(total)

		out = False
		if Outstatus:
			out=True



		s = "INSERT into commentary(bowler , batsman , run, out_status , wide , no_ball , leg , TEAM_ID) values ( \'"
		s+= bowler
		s+="\' , \'"
		s+= Batsman
		s+="\' , "
		s+=str(run)
		s+=" , \'"
		s+=str(out) 
		s+="\' , \'"
		s+=str(wide) 
		s+="\' ,\' "
		s+=str(no_ball) 
		s+="\' , \'"
		s+=str(leg)
		s+="\' ,"
s		s+=str(Team_id)
		s+=");" 

		print(s)





def Insert(over , content ):
	for i in range(len(over)):
		s = "INSERT INTO commentary(overs , comment) values( "
		s+=over[i]
		s+=' , " '
		s+=content[i]
		s+=' "  ); '	
		
		#print(s,"\n")
			#cur.execute("SELECT * FROM YOUR_TABLE_NAME")

comment()
Insert(over,new)
Separate(new)
