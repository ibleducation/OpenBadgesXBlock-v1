#
#
import sys, os
from pymongo import Connection

## -----------------------------
## FUNCTIONS -------------------
## -----------------------------

# Convert unicode2utf8 dicts
def convertUnicode2Utf8Dict(data):
	import collections
	if isinstance(data, basestring):
		return str(data)
	elif isinstance(data, collections.Mapping):
		return dict(map(convertUnicode2Utf8Dict, data.iteritems()))
	elif isinstance(data, collections.Iterable):
		return type(data)(map(convertUnicode2Utf8Dict, data))
	else:
		return data

#
# Mongo DB Connect
#
xmoduledb = "edxapp"
connection = Connection()
db = connection[xmoduledb]
mongo_modulestore = db['modulestore']

# course -> id.category : course
	# section -> id.category : chapter
		# subsection -> _id.category : sequential
			# problem -> _id.category : vertical

#
# Get Chapters : sections
#
def getCourseChapters(dict_course):
	res_list = []
	if len(dict_course)>0:
		for i, v in enumerate(dict_course):
			_id			= v.get('_id')
			definition	= v.get('definition')
			metadata	= v.get('metadata')
			if v.get('_id')['category'] == 'course':
				chapters = definition['children']
				if len(chapters)>0:
					for k in chapters:
						sequentials  = getCourseSequentials(dict_course,k.split('/')[::-1][0])
						res_list.append( {'category': 'chapter', 'module_id' : k, 'name' : k.split('/')[::-1][0], 'chapters': sequentials } )
	return res_list

#
# Get Sequentials : subsections
#
def getCourseSequentials(dict_course,cname):
	res_list = []
	if len(dict_course)>0:
		for i, v in enumerate(dict_course):
			if v.get('_id')['name']==cname and v.get('_id')['category']=='chapter':
				childs = v.get('definition')['children']
				if len(childs)>0:
					for k in childs:
						verticals = getCourseVerticals(dict_course,k.split('/')[::-1][0])
						res_list.append( {'category': 'sequential', 'module_id' : k, 'name' : k.split('/')[::-1][0], 'verticals': verticals } )
	return res_list

#
# Get Verticals : for group problems in subsection
#
def getCourseVerticals(dict_course,cname):
	res_list = []
	if len(dict_course)>0:
		for i, v in enumerate(dict_course):
			if v.get('_id')['name']==cname and v.get('_id')['category']=='sequential':
				childs = v.get('definition')['children']
				items  = []
				if len(childs)>0:
					for k in childs:
						items			= getCourseItems(dict_course,k.split('/')[::-1][0])
						total_score     = getCourseVerticalsScore(dict_course,cname)
						res_list.append( {'category': 'vertical', 'module_id' : k, 'name' : k.split('/')[::-1][0], 'items': items , 'total_score': total_score} )
	return res_list

#
# Get Items : last level 
# filter: problems and iblopenbadges
#
def getCourseItems(dict_course,cname):
	res_list = []
	badge_id = 0
	item_score = 0
	total_score = 0
	if len(dict_course)>0:
		for i, v in enumerate(dict_course):
			if v.get('_id')['name']==cname and v.get('_id')['category']=='vertical':
				childs = v.get('definition')['children']
				if len(childs)>0:
					for k in childs:
						item_name = k.split('/')[::-1][0]
						for item,val in enumerate(dict_course):
							if val.get('_id')['name']==item_name and (val.get('_id')['category']=='problem' or val.get('_id')['category']=='iblopenbadges'):
								category   = val.get('_id')['category']
								revision   = val.get('_id')['revision']
								metadata   = val.get('metadata')
								definition = val.get('definition')
								if category =='iblopenbadges' and revision!='draft':
									if 'bg_id' in definition['data']:
										badge_id  = val.get('definition')['data']['bg_id']
									else:
										badge_id  = 0
									res_list.append( {'category': category, 'module_id' : k, 'name' : item_name,'badge_id': badge_id, 'item_score': item_score } )
								else:
									if category =='problem' and revision!='draft':
										item_score=0 #init
										if 'weight' in metadata:
											item_score= metadata['weight']
										if item_score==0: item_score=1
										res_list.append( {'category': category, 'module_id' : k, 'name' : item_name,'badge_id': badge_id, 'item_score': item_score } )
	return res_list

#
# Get Verticals Score : total subsections
#
def getCourseVerticalsScore(dict_course,cname):
	res_list = []
	total_score = 0
	if len(dict_course)>0:
		for i, v in enumerate(dict_course):
			if v.get('_id')['name']==cname and v.get('_id')['category']=='sequential':
				childs = v.get('definition')['children']
				items  = []
				if len(childs)>0:
					for k in childs:
						items			= getCourseItems(dict_course,k.split('/')[::-1][0])
						for item in items:
							item_score = item['item_score']
							total_score += int(item_score)
	return total_score

## -----------------------------
## ENGINE ----------------------
## -----------------------------

def getDictCompleteCourseData(conn,course_id):
	course = setParseCourseId(course_id)
	dict_course = []
	if course!='':
		corg   = course[0]
		ccourse= course[1]
		cname  = course[2]
		res_query = conn.find({'_id.org': ''+corg+'', '_id.course': ''+ccourse+'', '_id.category': { "$in": [ 'course','chapter', 'sequential', 'vertical', 'problem', 'iblopenbadges' ] } }, {'definition.children':1, 'definition.data.bg_id':1, 'metadata.weight':1})
		if res_query:
			for item in res_query:
				dict_course.append(convertUnicode2Utf8Dict(item) )
	return dict_course

def getCompleteListProblems(conn,course_id):
	result_dict = []
	dict_course = getDictCompleteCourseData(conn,course_id)
	if len(dict_course)>0:
		res_complete = getCourseChapters(dict_course)
		for k1 in res_complete:
			chapters = k1['chapters']
			for k2 in chapters:
				chapter_module_id	 = k2['module_id']
				verticals = k2['verticals']
				for k3 in verticals:
					vertical_module_id = k3['module_id']
					vertical_total_score = k3['total_score']
					items = k3['items']
					for k4 in items:
						data_list = {'chapter_module_id':chapter_module_id, 'vertical_module_id':vertical_module_id,
									'item_module_id':k4['module_id'],'item_category':k4['category'], 
									'item_badge_id': k4['badge_id'], 'item_score':k4['item_score'], 'chapter_max_score':vertical_total_score
									}
						result_dict.append(data_list)
	return result_dict
#
# Parse course_id
#
def setParseCourseId(course_id):
	if course_id !='' and course_id !='None':
		course  = course_id.split('/')
		corg= course[0]
		ccourse = course[1]
		cname   = course[2]
		if corg!='' and ccourse!='' and cname!='':
			return course
		else:
			return ''

#
# Get Problems from guiven badge_id
#
def getListProblemsFromBadgeId(conn,badge_id,course_id):
	chapter_module_id =''
	problems_list     =[]
	if course_id!='' and course_id!='None' and badge_id!='' and badge_id!='None':
		dict_course = getCompleteListProblems(conn,course_id)
		if len(dict_course)>0:
			for k in dict_course:
				if k['item_badge_id'] == badge_id:
					chapter_module_id = k['chapter_module_id']
		if chapter_module_id !='':
			for p in dict_course:
				if p['chapter_module_id'] == chapter_module_id:
					#print ('%s : %s') % (p['item_module_id'],p['item_score'])
					problems_list.append({ 'problem_id':p['item_module_id'], 'problem_score':p['item_score'] } )
	return problems_list

#
# Get Score from guiven badge_id
#
def getScoreFromBadgeId(conn,badge_id,course_id):
	score = '0'
	problems_list=[]
	if course_id!='' and course_id!='None' and badge_id!='' and badge_id!='None':
		dict_course = getCompleteListProblems(conn,course_id)
		if len(dict_course)>0:
			for k in dict_course:
				if k['item_badge_id'] == badge_id:
					score = k['chapter_max_score']
	return score

# -----------------------------------------------
# To remove when finish : Tests
# -----------------------------------------------
"""
# Mongo DB Connect
from pymongo import Connection
xmoduledb = "edxapp"
connection = Connection()
db_mongo = connection[xmoduledb]
mongo_modulestore = db_mongo['modulestore']

bg_id='2008'
course_id='IBL/1/2015_2'

#badge_list_problems = getListProblemsFromBadgeId(mongo_modulestore,bg_id,course_id)
#print badge_list_problems

#badge_problems_score =getScoreFromBadgeId(mongo_modulestore,bg_id,course_id)
#print badge_problems_score
"""
