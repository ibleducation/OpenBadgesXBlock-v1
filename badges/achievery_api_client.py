#
#
import sys, os,requests,json,achievery_api_client 
#
# Additional system modules
#
sys.path.append("/usr/lib/python2.7/dist-packages/")

#
# Class to create objBadge
#
class BadgesAchievery:

        def __init__(self, id):
                self.id = id
                self.apply = None
                #self.categories = [{'category':None}]
                self.categories = []
                self.course_id  = None
                self.criteria   = None
                self.description= None
                #self.evidences  = [{'description':None,'id':None,'private':None,'required':None,'type':None}]
                self.evidences  = []
                self.image              = None
                #self.links             = [{'description':None,'id':None,'name':None,'url':None}]
                self.links              = []
                self.name               = None
                self.status             = None
                #self.tags              = [{'text':None}]
                self.tags               = []
                self.version    = None
#
# Process getToken
#
def process_get_access_token(pname,purl,pusr,ppwd):
	access_token = get_auth_credentials(pname,purl,pusr,ppwd)
	return access_token

#
# Get credentials
#
def get_auth_credentials(pname,purl,pusr,ppwd):
	import requests, json

	if pname == 'achievery':
		pdata = {'grant_type':'client_credentials'}
	else:
		pdata = ''

	# eval results
	result = ''
	if pdata is not '': 
		res  = requests.post(purl, data=pdata, auth=(pusr,ppwd) )
		#return r.content
		data = json.loads(res.content)

		try:
			for key,value in data.items():
				if key is not "code":
					if key == 'access_token':
						result = value
		except:
			result = ''
	
	return result



def get_badges_list(pname,purl,token):
        global request, json

        if pname == 'achievery':
                headers_provider = {'Authorization' : 'Bearer '+token+'' }
                res  = requests.get(purl, headers=headers_provider )
                #print res.content
                data = json.loads(res.content)
		try:
			for key,value in data.items():
				if key is "code":
					return ''
			return res.content
		except:
			return ''
        else :
                return ''


def create_obj_badges_lists(jsondata):
        import json
        import CommonFunc

        #remove non asccii 128 compat python2.x
	jsonResponse	= json.loads(jsondata.decode("ascii","ignore"))
        jsonData        = jsonResponse["data"]
        jsonData        = CommonFunc.convertUnicode2Utf8Dict(jsonData)

        obj_BadgesList = []

        for item in jsonData:
                b = BadgesAchievery(item['id'])
                b.id            = item['id']
                #b.apply         = item['apply']
                b.name          = item['name']
                b.criteria      = item['criteria']
                b.description= item['description']
                b.image         = item['image']
                b.course_id     = item['course_id']
                b.status        = item['status']
                b.version       = item['version']
                if "evidences" in item:
                        b.evidences = item["evidences"]
                else:
                        b.evidences = []
                if "categories" in item:
                        b.categories = item["categories"]
                else:
                        b.categories = []
                if "tags" in item:
                        b.tags = item["tags"]
                else:
                        b.categories = []
                if "links" in item:
                        b.links = item["links"]
                else:
                        b.links = []

                #adding to object
                obj_BadgesList.append(b)

        return obj_BadgesList

def get_badge_by_id(selid,sourceList):
        for obj in sourceList:
                if str(obj.id) == str(selid):
                        #CommonFunc.debug_object_data(obj)
                        return obj
        return '0'


#
# Build Form Evidences
#
def build_evidences(data_evidences):
	result = ''
	if data_evidences:
		#list of dict
		for evidence in data_evidences:
			#get needed values
			id 		= evidence.get("id", 0)
			private 	= evidence.get("private", 'None')
			description	= evidence.get("description", 'None')
			type 		= evidence.get("type", 'None')
			required	= evidence.get("required", 'N')
			
			#allowed evidences
			if id>0 and private is None and (type =='url' or type == 'video' or type =='text' ) :
				#controls
				if description is None:
					description = 'Description'

				if required  == 'Y':
					required = 'required'

	  			#contruct results
	  			result +='<tr>'
	  			result +='<td>%s</td>' % (description)
	  			result +='<tr><tr><td>'
	  			
	  			if type == "text":
	  				result +='<textarea name="evidence|%s" id="evidence|%s" style="width:820px;resize:vertical;height:200px; overflow:auto" %s></textarea>' % (id,id,required)
	  			else:
	  				result +='<input type="text" name="evidence|%s" id="evidence|%s" value="" %s  style="width:820px;"><br><span style="font-size:small;font-style:italic;">Note: just online http addresess (URL) are allowed</span>' % (id,id,required)
	  			result +='</td>'
	  			result +='</tr><tr><td>&#160;</td></tr>'

	return result


def get_badge_form(self,f_bg_id,f_claim_name,f_claim_mail,f_form_text,obj_sel_badge):

	#construct evidences
	import achievery_api_client
	if obj_sel_badge.id > 0:
		#get html evidences for substitutions
		if obj_sel_badge.evidences:
			f_claim_evidences = achievery_api_client.build_evidences(obj_sel_badge.evidences)
		else:
			f_claim_evidences = ''

        #split student_name
        f_claim_full_name    = f_claim_name.split(' ')
        f_claim_s_first_name = f_claim_full_name[0]
        if len(f_claim_full_name) > 1:
                f_claim_s_last_name  = f_claim_full_name[1:len(f_claim_full_name)]
                f_claim_s_last_name  = f_claim_s_last_name[0] 
        else:
                f_claim_s_last_name = '.'

	form = "<table cellpadding=4 cellspacing=4 style='border:solid 1px #333;'><tr><td><img src='%s' style='max-width:300px;'></td><td valign=top><div style='padding-top:14px;'><b>%s</b></div><br>%s</td></tr></table><br>" % (obj_sel_badge.image,obj_sel_badge.name,obj_sel_badge.description)

	form += "<form action='student_claim_save' name='badge_claimer' id='badge_claimer' method='post'>"
	form += '<input type="hidden" name="id" value="%s" requried>' % (obj_sel_badge.id)
	form += '<input type="hidden" name="bname" value="%s">' % (obj_sel_badge.name)
	form += '<input type="hidden" name="bimage" value="%s">' % (obj_sel_badge.image)
	form += '<input type="hidden" name="bcourse" value="%s">' % (obj_sel_badge.course_id)	
	form += '<input type="hidden" name="first_name" value="%s">' % (f_claim_s_first_name)
	form += '<input type="hidden" name="last_name" value="%s">' % (f_claim_s_last_name)
	form += '<input type="hidden" name="email" value="%s">' % (f_claim_mail)
	form += '<input type="hidden" name="allow_dupe" value="false">'

	form += "<table>"
	form += "<tr><td><span style='color:#d9d9d9;'>%s</span></td></tr>" % (f_form_text)
	form += "<tr><td>&#160;</td></tr>"
	form += "%s" % (f_claim_evidences)
	form += "<tr><td>&#160;</td></tr>"
	form += "<tr><td><input type='submit' name='claim-button' value='CLAIM YOUR BADGE'></td></tr>"
	form += "</table>"

	form += "</form>"

	return form 

#
# Get data from Badge Form
#
def set_form_data_to_award(pname,app_form_data):
	import urllib,CommonFunc
	#define vars
	params 		= {}
	evidences 	= ''	

	# get form values : single function
	form  = app_form_data

	#proceed
	if pname == 'achievery':
		i =0
		for k,v in form.iteritems():
			#decode chars for evidences
			field = k.replace('%7C','|')
			field = field.split('|')
			if field[0] != 'evidence':
				if v != 'None':
					params[k] = v
			else:
				if i > 0:
					evidences+= "&"
				if v!='':
					#decode chars
					v = v.replace('%3A',':')
					v = v.replace('%2F','/')
					#evidences += ('evidence[%s][id]=%s&evidence[%s][value]=%s') % (i,field[1],i,urllib.quote(v)) 
					evidences += ('evidence[%s][id]=%s&evidence[%s][value]=%s') % (i,field[1],i,v) 
					i +=1 
	
		#check dict created
		if params:
			data = CommonFunc.convert_dict2querystring(params)
			if (data is not '' and evidences is not ''):
				data = ("%s&%s") % (data,evidences)
		else:
			data = ''
	else:
	 	data =''

	return data

#
# Set Award Single Badge
#
def set_award_single_badge(pname,purl,token,award_data):

	# Form data must be provided already urlencoded. Not for achievery
	# if you need urlencode import urllib
	#postfields = urllib.urlencode(award_data)	
	postfields = str(award_data)
	result = ''
	if award_data is not '':
		
		#send data
		# using pycurl. Bug 7.19.3
		if pname == 'achievery':
			import pycurl
			from StringIO import StringIO
			#send curl data
			c = pycurl.Curl()
			c.setopt(c.URL, purl)
			c.setopt(pycurl.HTTPHEADER, ['Accept: application/json','Authorization: Bearer %s' % str(token)]) 
			c.setopt(pycurl.SSL_VERIFYPEER, 0)
			c.setopt(pycurl.SSL_VERIFYHOST, 0)
			#c.setopt(c.VERBOSE, True)
			c.setopt(c.POSTFIELDS, postfields)
			#c.setopt(c.POST, 1)
			buffer = StringIO()
			#version pycurl >= 7.19.3
			#c.setopt(c.WRITEDATA, buffer)
			c.setopt(c.WRITEFUNCTION, buffer.write)
			c.perform()
			c.close()
			result = buffer.getvalue()
	return result

#
# Parse Award Result
#
def get_award_result(pname,data2parse):
	result = 'error'
	if pname == 'achievery':
		if data2parse != '':
			for key,val in data2parse.iteritems():
				if key == "data":
					for k,v in val.iteritems():
						if k == "award_id":
								result = v
		
	return result

#
# Print Award Results
#
def get_award_result_formatted(pname,resultdata,congratulations):
        result =''
        if pname == 'achievery':
                if resultdata != 'error':
                        result  ='<div style="color:green;">'
                        result +="<h1 style='color:green;'>%s</h1>" % (congratulations)
                        result +='<div><a href="%s" target="_blank">%s</a></div>' % (resultdata,resultdata)
                        result +='</div>'
                else:
                        result  ='<div style="color:red;">'
                        result +='<div><h1 style="color:red">Error: The award could not be created</h1></div>'
                        result +='</div>'

        return result
