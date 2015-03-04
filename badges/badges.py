"""TO-DO: Write a description of what this XBlock is."""


import pkg_resources
import datetime

# from xblock.fields import Integer, Scope, String, Any, Boolean, Dict
from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment
from xmodule.fields import RelativeTime

import badgeproviders
import achievery_api_client
import edxappCourseData

class Badges(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    display_name = String(display_name="Display Name", default="Claim Badge", scope=Scope.settings, help="Name of the component in the edxplatform")

    # TO-DO: delete count, and define your own fields.

    form_text = String(display_name="text_desc", default=" ", scope=Scope.content, help="Badge text description")	
    congratulations_text = String(display_name="congratulations_desc", default=" ", scope=Scope.content, help="Congratulations text description")	
    enough_text = String(display_name="enough_desc", default=" ", scope=Scope.content, help="Not-enough-score text description")	
    bg_id = String(display_name="id", default="2008", scope=Scope.content, help="Id of the Badge")	
    bg_provider = String(display_name="provider", default="0", scope=Scope.content, help="Id of the badge provider")	
    n_course_id = String(display_name="CourseId", default="0", scope=Scope.user_state, help="Id of teh current course")	
    n_user_id = String(display_name="UserId", default="0", scope=Scope.user_state, help="Id of the current user")	
    user_score = String(display_name="UserScore", default="0", scope=Scope.user_state, help="Current section user score")	
    required_score = String(display_name="RequiredScore", default="50", scope=Scope.content, help="Requireds core")	
    debug_mode = String(display_name="debug", default="0", scope=Scope.content, help="Enable debug mode")	
	
    #provider data
    claim_prov_info = badgeproviders.BADGEPROVIDERS[0]
    claim_prov_name = claim_prov_info.get('alias')
    
    #now not hardcoed
    #claim_prov_usr = claim_prov_info.get('puser')
    #claim_prov_pwd = claim_prov_info.get('ppwd')
    claim_prov_usr = String(display_name="ProviderUSER", default="ibldemo-8CaZHKGQr", scope=Scope.content, help="Badge provider user")
    claim_prov_pwd = String(display_name="ProviderPass", default="4c46d8a1-70b4-43d9-87da-cdf06b049bea", scope=Scope.content, help="Badge provider pass")

    claim_prov_url_token = claim_prov_info.get('url_auth')
    claim_prov_url_list_all = claim_prov_info.get('url_list_all')
    claim_prov_url_claim = claim_prov_info.get('url_claim')
    claim_prov_url_earn = claim_prov_info.get('url_earn')
    claim_prov_acces_token = 'None'

    #user data	
    claim_name = String(display_name="ClaimUserName", default="Jhon", scope=Scope.user_state, help="")	
    claim_mail = String(display_name="ClaimUserMail", default="sils@iblstudios.com", scope=Scope.user_state, help="")	

    claim_db_user_data = 'None'
    claim_db_user_id = 'None'
    claim_db_user_course = 'None'
    claim_db_user_name = 'None'
    claim_db_user_email = 'None'
    claim_db_user_score = '0'

    #control errors
    claim_badge_errors = ''

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")


    # TO-DO: change this view to display your data your own way.
    def student_view(self, context):
	"""
	Get token provider
	"""
	self.n_user_id = self.get_student_id()
	self.claim_db_user_data = self.DB_get_user_data() 
	self.claim_db_user_id = self.claim_db_user_data[0] 
	self.claim_db_user_course = self.claim_db_user_data[1] 
	self.claim_db_user_name = self.claim_db_user_data[2] 
	self.claim_db_user_email = self.claim_db_user_data[3] 
	self.claim_db_user_score = self.claim_db_user_data[4] 
        self.claim_db_problems_lists = self.claim_db_user_data[5]
	self.claim_db_problems_total_score = self.claim_db_user_data[6]
	self.claim_db_problems_partial_score = self.claim_db_user_data[7]
	self.claim_db_problems_percent_score = self.claim_db_user_data[8]
	self.claim_db_badge_problems_score = self.claim_db_user_data[9]

	#need to be calc
	self.user_score = self.claim_db_user_data[4] 
	
	"""
	Test mongodb connection
	Test course data tree
	"""	
	# Mongo DB Connect
	from pymongo import Connection
	xmoduledb = "edxapp"
	connection = Connection()
	db = connection[xmoduledb]
	mongo_modulestore = db['modulestore']
	self.claim_db_course_id	= ''
	if self.claim_db_user_course!='None':
		self.claim_db_course_id	= self.claim_db_user_course
	self.course_data_tree = ''
	""" Test """
	
	claim_name = self.claim_db_user_name
	claim_mail = self.claim_db_user_email
	
	self.claim_badge_errors = self.claim_badge_errors

	#nunpa debug lvl 2
        if self.claim_badge_errors == "":
		self.claim_prov_access_token = achievery_api_client.process_get_access_token(self.claim_prov_name,self.claim_prov_url_token,self.claim_prov_usr,self.claim_prov_pwd)
		if self.claim_prov_access_token !="":
			badges_list_data = achievery_api_client.get_badges_list(self.claim_prov_name,self.claim_prov_url_list_all,self.claim_prov_access_token)
			if badges_list_data !="":
				obj_list_of_badges = achievery_api_client.create_obj_badges_lists(badges_list_data)
				obj_sel_badge = achievery_api_client.get_badge_by_id(self.bg_id,obj_list_of_badges)
				if obj_sel_badge == '0':
					self.claim_badge_errors = 'Could not retrieve the information associated with the Badge ID selected. Please, verify the ID.'
				else:
					if self.debug_mode == "1":
						set_allow_dupe = "1"
					else:
						set_allow_dupe = "0"
					self.claim_badge_form = achievery_api_client.get_badge_form(self,self.bg_id,self.claim_db_user_name,self.claim_db_user_email,self.form_text,obj_sel_badge,set_allow_dupe)
			else:
				self.claim_badge_errors = 'Could not retrieve the information associated with your account. Please, verify your credentials.'
		else:
			self.claim_badge_errors = 'Could not connect to provider. Please, verify your credentials.'

	#init result : deprecated
	self.claim_data = ""

        """
        The primary view of the IBLBadges, shown to students
        when viewing courses.
        """
	if self.claim_badge_errors == "":
		if self.debug_mode == "1":
			html = self.resource_string("static/html/iblbadges_debug.html")

		else:
			if int(self.user_score) < int(self.required_score):
				html = self.resource_string("static/html/iblbadges_noscore.html")
			else:
				html = self.resource_string("static/html/iblbadges.html")


		frag = Fragment(html.format(self=self))
		frag.add_css(self.resource_string("static/css/iblbadges.css"))
		frag.add_javascript(self.resource_string("static/js/src/iblbadges.js"))
		frag.initialize_js('IBLBadges')
	else:
		html = self.resource_string("static/html/iblbadges_errors.html")
		frag = Fragment(html.format(self=self))
		frag.add_css(self.resource_string("static/css/iblbadges.css"))
		#frag.add_javascript(self.resource_string("static/js/src/iblbadges.js"))
		#frag.initialize_js('IBLBadges')
        return frag

    def get_student_id(self):

        if hasattr(self, "xmodule_runtime"):

            s_id = self.xmodule_runtime.anonymous_student_id  # pylint:disable=E1101

        else:

            if self.scope_ids.user_id is None:

                s_id = "None"

            else:

                s_id = unicode(self.scope_ids.user_id)

	return s_id

    def DB_get_user_data(self):

        import appmysqldb, CommonFunc

	user_id = "None"
	course_id  = "None"
	user_name = "None"
	user_email = "None"
	user_score = "0"

        db = appmysqldb.mysql('localhost', 3306, 'edxapp', 'root', '')
        q = "SELECT id, user_id, course_id FROM student_anonymoususerid WHERE anonymous_user_id='" + self.n_user_id + "'"
        CommonFunc.debug("QUERY: %s" %(q))
        db.query(q)
        res = db.fetchall()
	for row in res:
                user_id   = row[1]
                course_id = row[2]


	q = "SELECT name FROM auth_userprofile WHERE user_id='%s' " % (user_id)
        CommonFunc.debug("QUERY: %s" %(q))
        db.query(q)
        res = db.fetchall()
        for row in res:
                user_name   = row[0]


	q = "SELECT email FROM auth_user WHERE id='%s' " % (user_id)
        CommonFunc.debug("QUERY: %s" %(q))
        db.query(q)
        res = db.fetchall()
        for row in res:
                user_email   = row[0]

	
	""" getting course data from mongodb """
	# Mongo DB Connect
	from pymongo import Connection
	xmoduledb = "edxapp"
	connection = Connection()
	db_mongo = connection[xmoduledb]
	mongo_modulestore = db_mongo['modulestore']

	badge_list_problems = edxappCourseData.getListProblemsFromBadgeId(mongo_modulestore,self.bg_id,course_id)
	badge_problems_score = edxappCourseData.getScoreFromBadgeId(mongo_modulestore,self.bg_id,course_id)
	""" """

#nunpa
	#calculate badge_score 
	user_score = 0
	partial_user_score = []
	badge_partial_user_score = 0
	badge_percent_user_score = 0
	#calculate user partials
	if badge_problems_score>0:
		if len(badge_list_problems)>0:
			for problem in badge_list_problems:
				if 'problem_score' in problem:
					problem_score 	= problem['problem_score']
					problem_id 	= problem['problem_id']
					#getting partial values
					if int(problem_score)>0:
						q = "SELECT ((%s/max_grade)*grade) FROM courseware_studentmodule WHERE course_id='%s' AND student_id='%s' AND module_id='%s'" % (problem_score,course_id,user_id,problem_id)
						CommonFunc.debug("QUERY: %s" %(q))
						db.query(q)
						res = db.fetchall()
						for row in res:
							if row[0]>0:
								partial_user_score.append( float(row[0]) )
							
					badge_partial_user_score = sum(partial_user_score)
	#calculate total percent	
	if round(badge_partial_user_score,2)>0 and int(badge_problems_score)>0:
		badge_percent_user_score = ( badge_partial_user_score * 100.0 ) / badge_problems_score
		badge_percent_user_score = round(badge_percent_user_score,2)
	if int(badge_percent_user_score)>0:
		user_score = badge_percent_user_score

	#show results
	results = [user_id,course_id,user_name,user_email,user_score,badge_list_problems,badge_problems_score,badge_partial_user_score,badge_percent_user_score,badge_problems_score]
	
        return results


    def studio_view(self, context=None):
        """
        The primary view of the IBLBadges, shown to students
        when viewing courses.
        """
	html = self.resource_string("static/html/iblbadges_edit.html")

	options = "<option value=''> -- select your badge provider --</option>"
        for key in badgeproviders.BADGEPROVIDERS:
            if self.bg_provider ==key['id']:
                options = options + "<option value='" + key['id'] + "' selected='selected' >" + key['name'] + "</option>"
            else:
                options = options + "<option value='" + key['id'] + "' >" + key['name'] + "</option>"

        selector=u"""
            <script type="text/template" id="xblock-equality-template">
            </script>
            <select name='bg_provider' id='bg_provider'>
            {}
            </select>""".format(options)

	frag = Fragment(html.format(self=self,selector=selector))
        frag.add_css(self.resource_string("static/css/iblbadges.css"))
        frag.add_javascript(self.resource_string("static/js/src/iblbadges_edit.js"))
        frag.initialize_js('IBLBadgesEdit')
        return frag


    @XBlock.json_handler
    def student_claim_save(self,claimdata,suffix=''):
	#parse data to claim badge
	import json
	award_result = 'error'
	if claimdata:
		#get new token
		self.claim_prov_access_token = achievery_api_client.process_get_access_token(self.claim_prov_name,self.claim_prov_url_token,self.claim_prov_usr,self.claim_prov_pwd)
		#parse returned data
		claimdata_dict= dict( entry.split('=') for entry in claimdata.split('&') )
		award_data = achievery_api_client.set_form_data_to_award(self.claim_prov_name,claimdata_dict)
		set_award_single = achievery_api_client.set_award_single_badge(self.claim_prov_name, self.claim_prov_url_claim,self.claim_prov_access_token,award_data)
		#debug achievery
		if self.debug_mode == "1":
			debug_result = award_data +'<hr>'+set_award_single
			return { 'result' : debug_result }

		#result award. we need to use eval to use the returned data as dict
		if set_award_single is not '':
			award_result_prov	= achievery_api_client.get_award_result(self.claim_prov_name,eval(set_award_single))
			#format award_result
			if award_result_prov !='error':
				award_result_prov = self.claim_prov_url_earn+str(award_result_prov)
			award_result            = achievery_api_client.get_award_result_formatted(self.claim_prov_name,award_result_prov,self.congratulations_text)
		else:
			award_result_prov = 'error'
			#format award_result
			award_result            = achievery_api_client.get_award_result_formatted(self.claim_prov_name,award_result_prov,self.congratulations_text)
	
	return { 'result' :  award_result }

    @XBlock.json_handler
    def studio_save(self, data, suffix=''):
        """
        Called when submitting the form in Studio.
        """
        self.debug_mode = data['debug_mode']
        self.bg_id = data['bg_id']
        self.bg_provider = data['bg_provider']
        self.form_text = data['form_text']
        self.congratulations_text = data['congratulations_text']
        self.enough_text = data['enough_text']
        self.required_score = data['required_score']
	self.claim_prov_usr = data['badge_pro_user']
	self.claim_prov_pwd = data['badge_pro_pwd']
        return {
            'result': 'success',
        }



    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("IBLBadges",
             """<vertical_demo>
                <iblbadges/>
                <iblbadges/>
                <iblbadges/>
                </vertical_demo>
             """),
        ]
