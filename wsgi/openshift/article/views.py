from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from article.models import Article
from django.shortcuts import render
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from article.models import Article
from article.models import Arctic
from article.models import Postjob
from article.models import Candidate
from article.models import Resume
from django.template import RequestContext
from time import time
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
import os
import datetime
import base64
# Create your views here.
def home(request):
    name="Sheesh"
    t= get_template('login_page2.html')
    html=t.render(Context({'name':name}))
    return HttpResponse(html)

def signup(request):
    a='out'
    if 'emailid' in request.session:
	if request.session['emailid']==a:
	    request.session['remailid']=a
	    return render_to_response('Signup.html',context_instance=RequestContext(request))
	else:
	    return HttpResponseRedirect('/profile/')
    else:
        request.session['remailid']=a
        return render_to_response('Signup.html',context_instance=RequestContext(request))

def register(request):
    email = request.POST.get('email', '')
    mobile_no = request.POST.get('mobile_no', '')
    confirm_email = request.POST.get('confirm_email', '')
    passwd = request.POST.get('passwd', '')
    confirm_passwd = request.POST.get('confirm_passwd', '')
    country_code = request.POST.get('country_code', '')
    agree = request.POST.get('agree', '')
    p = Article(email = email, confirm_email = confirm_email, passwd = passwd, confirm_passwd = confirm_passwd, country_code = country_code, mobile_no = mobile_no, agree = agree)
    q = Candidate(email=email)
    r = Resume(email=email)
    if Article.objects.filter(email = email).exists():
	return HttpResponseRedirect('/error/')
    else:
	p.save()
	q.save()
	r.save()
	condition = "Registration Successfull, Enter the credentials to login."
        return render_to_response('Signup.html',{ 'cond':condition }, context_instance=RequestContext(request))

def error(request):
     return render_to_response('error.html')

def login(request):
    email = request.POST.get('email', '')
    passwd = request.POST.get('passwd', '')
    if Article.objects.filter(email = email).exists():
	a = Article.objects.get(email=email)
	if a.passwd == passwd:
	    request.session['emailid'] = a.email
	    return HttpResponseRedirect('/profile/')
	else:
	    return HttpResponseRedirect('/signinerror/')
    else:
	return HttpResponseRedirect('/signinerror/')



def profile(request):
    a='out'
    request.session['remailid']=a
    if request.session['emailid']==a:
	return HttpResponseRedirect('/signinerror/')
    else:
	details = Article.objects.get(email = request.session['emailid'])
	try:
	    profile = Candidate.objects.get(email = request.session['emailid'])
	    resum = Resume.objects.get(email = request.session['emailid'])
	except:
	    profile =[]
	    resum = []
        return render_to_response('profile.html', {'email': request.session['emailid'], 'profile':profile, 'resum':resum})

def editprofile(request):
    a='out'
    if 'emailid' in request.session:
        request.session['remailid'] = a
        if request.session['emailid']==a:
	    return HttpResponseRedirect('/signinerror/')
        else:
	    try:
                profile = Candidate.objects.get(email = request.session['emailid'])
	        resum = Resume.objects.get(email = request.session['emailid'])
	    except:
	        profile =[]
	        resum = []
            return render_to_response('edit_profile.html',{'profile':profile, 'email': request.session['emailid'], 'resum':resum},context_instance=RequestContext(request))
    else:
	return HttpResponseRedirect('/signinerror/')

def savechanges(request):
    email = request.session['emailid']
    name = request.POST.get('f_name', '')
    location = request.POST.get('location', '')
    agree = request.POST.get('agree', '')
    gender = request.POST.get('gender', '')
    exp = request.POST.get('experience', '')
    title = request.POST.get('title', '')
    company = request.POST.get('company', '')
    skills = request.POST.get('skills', '')
    sector = request.POST.get('sector', '')
    functional = request.POST.get('functional', '')
    minsalary = request.POST.get('minsalary', '')
    qualification = request.POST.get('qualification', '')
    specialization = request.POST.get('specialization', '')
    certification = request.POST.get('certification', '')
    institute = request.POST.get('institute', '')
    passing = request.POST.get('passing', '')
    jtype = request.POST.get('course', '')
    resume = request.FILES.get('resume','')
    if not minsalary:
	minsalary=0
    if not passing:
	passing=1940
    if not exp:
	exp=0
    p = Candidate.objects.filter(email = request.session['emailid'])
    q = Resume.objects.get(email =request.session['emailid'])
    p.update(email=email, name=name, location=location, agree=agree, gender=gender, exp=exp, title=title.lower(), company=company, skills=skills.lower(), sector=sector, functional=functional, minsalary=minsalary, qualification=qualification, specialization=specialization.lower(), certification=certification.lower(), institute=institute.lower(), passing=passing, jtype=jtype, pubdate=datetime.date.today())
    if q.resume:
	if resume:
	    q.resume = resume
	    q.save()
	else:
    	    q.save()
    else:
	if resume:
	    q.resume = resume
	    q.save()
	else:
	    q.save()
    return HttpResponseRedirect('/profile/')

def signinerror(request):
    args = {}
    args.update(csrf(request))
    return render_to_response('Signinerror.html',args)

def logout(request):
    if 'emailid' in request.session:
	condition = "Logged Out Succesfully"
	a='out'
	request.session['emailid'] = a
	return render_to_response('error.html', {'condition':condition})
    else:
	return render_to_response('unknown.html')


def changec(request):
    a='out'
    if 'emailid' in request.session:
	if request.session['emailid']==a:
	    return HttpResponseRedirect('/signinerror/')
	else:
	    return render_to_response('changepasswordc.html',{'email':request.session['emailid']}, context_instance=RequestContext(request))
    else:
	return HttpResponseRedirect('/signinerror/')


def cprocesspasswd(request):
    a='out'
    if 'emailid' in request.session:
	if request.session['emailid']==a:
	    return HttpResponseRedirect('/signinerror/')
	else:
	    email = request.session['emailid']
	    oldpasswd = request.POST.get('oldpasswd', '')
	    passwd = request.POST.get('confirmpasswd', '')
	    a = Article.objects.filter(email = email)
	    if a[0].passwd == oldpasswd:
		a.update(passwd = passwd , confirm_passwd=passwd)
	        return HttpResponseRedirect('/profilec/')
	    else:
		return HttpResponseRedirect('/changepasswordc/incorrect/')
    else:
	return HttpResponseRedirect('/signinerror/')


def changecincorrect(request):
    a='out'
    condition='Wrong Current Password Entered'
    if 'emailid' in request.session:
	if request.session['emailid']==a:
	    return HttpResponseRedirect('/signinerror/')
	else:
	    return render_to_response('changepasswordc.html',{'email':request.session['emailid'], 'condition':condition}, context_instance=RequestContext(request))
    else:
	return HttpResponseRedirect('/signinerror/')



def profilec(request):
    condition="Password Changed Successfully"
    a='out'
    request.session['remailid']=a
    if request.session['emailid']==a:
	return HttpResponseRedirect('/signinerror/')
    else:
	details = Article.objects.get(email = request.session['emailid'])
	try:
	    profile = Candidate.objects.get(email = request.session['emailid'])
	    resum = Resume.objects.get(email = request.session['emailid'])
	except:
	    profile =[]
	    resume = []
        return render_to_response('profile.html', {'email': request.session['emailid'], 'profile':profile, 'resum':resum,'condition':condition})

def applysuccess(request):
    condition="Successfully Applied for the job"
    a='out'
    request.session['remailid']=a
    if request.session['emailid']==a:
	return HttpResponseRedirect('/signinerror/')
    else:
	details = Article.objects.get(email = request.session['emailid'])
	try:
	    profile = Candidate.objects.get(email = request.session['emailid'])
	    resum = Resume.objects.get(email = request.session['emailid'])
	except:
	    profile =[]
	    resume = []
        return render_to_response('profile.html', {'email': request.session['emailid'], 'profile':profile, 'resum':resum,'condition':condition})

def unknown(request, another=0):
     return render_to_response('unknown.html')

#################################################################################################################################################

def recruiter(request):
    a='out'
    if 'remailid' in request.session:
        if request.session['remailid']==a:
            request.session['emailid'] = a
            c = {}
            c.update(csrf(request))
            return render_to_response('recruiter_signup.html',c)
	else:
	    return HttpResponseRedirect('/rprofile/')
    else:
	request.session['emailid'] = a
        c = {}
        c.update(csrf(request))
        return render_to_response('recruiter_signup.html',c)

def rerror(request):
     return render_to_response('rerror.html')

def rregister(request):
    company = request.POST.get('company', '')
    contact = request.POST.get('contact', '')
    email = request.POST.get('emailid', '')
    website = request.POST.get('website', '')
    location = request.POST.get('location', '')
    password = request.POST.get('passwd', '')
    confirmpasswd = request.POST.get('confirm_passwd', '')
    countrycode = request.POST.get('countrycode', '')
    mobile = request.POST.get('mobile_no', '')
    agree = request.POST.get('agree', '')
    p = Arctic(company = company, contact = contact, email = email, website = website, location = location, passwd = password, confirm_passwd = confirmpasswd, country_code = countrycode, mobile_no = mobile, agree = agree)
    if Arctic.objects.filter(email = email).exists():
	return HttpResponseRedirect('/rerror/')
    else:
	p.save()
        return HttpResponseRedirect('/recruiters/')

def recruiters(request):
    a='out'
    if 'remailid' in request.session:
        if request.session['remailid']==a:
            request.session['emailid'] = a
	    condition = "Registration Successfull. Enter the Credentials to login."
            return render_to_response('recruiter_signup.html', {'condition':condition}, context_instance=RequestContext(request))
	else:
	    return HttpResponseRedirect('/rprofile/')
    else:
	request.session['emailid'] = a
	condition = "Registration Successfull. Enter the Credentials to login."
        return render_to_response('recruiter_signup.html', {'condition':condition}, context_instance=RequestContext(request))

def rlogin(request):
    email = request.POST.get('email', '')
    passwd = request.POST.get('passwd', '')
    if Arctic.objects.filter(email = email).exists():
	a = Arctic.objects.get(email=email)
	if a.passwd == passwd:
	    request.session['remailid'] = a.email
	    return HttpResponseRedirect('/rprofile/')
	else:
	    return HttpResponseRedirect('/rsigninerror/')
    else:
	return HttpResponseRedirect('/rsigninerror/')

def rprofile(request):
    details = Arctic.objects.get(email = request.session['remailid'])
    return render_to_response('rprofile.html', {'email': request.session['remailid'], 'details':details})

def postjob(request):
    if 'remailid' in request.session:
	a='out'
	context = {'email': request.session['remailid']}
	request.session['emailid'] = a
	if request.session['remailid']==a:
	    return HttpResponseRedirect('/rsigninerror/')
	else:
	    return render_to_response('post_job.html', context ,context_instance=RequestContext(request))
    else:
	return HttpResponseRedirect('/rsigninerror/')

def rsigninerror(request):
    args = {}
    args.update(csrf(request))
    return render_to_response('rSigninerror.html',args)

def rlogout(request):
    if 'remailid' in request.session:
	condition = "Logged Out Succesfully"
	a='out'
	request.session['remailid'] = a
	return render_to_response('rerror.html', {'condition':condition})
    else:
	return render_to_response('unknown.html')

def post_job(request):
    email = request.session['remailid']
    title = request.POST.get('title', '')
    description = request.POST.get('description', '')
    industry = request.POST.get('industry', '')
    functional = request.POST.get('functional', '')
    minexp = request.POST.get('minexp', '')
    maxexp = request.POST.get('maxexp', '')
    minsalary = request.POST.get('minsalary', '')
    maxsalary = request.POST.get('maxsalary', '')
    location = request.POST.get('location', '')
    jtype = request.POST.get('type', '')
    qualification = request.POST.get('qualification', '')
    p = Postjob(email = email, title = title.lower(), description = description, industry = industry, functional = functional, minexp = minexp, maxexp = maxexp, minsalary = minsalary, maxsalary = maxsalary, location = location.lower(), jtype = jtype, qualification = qualification)
    p.save()
    return HttpResponseRedirect('/jobs/all/')

def alljobs(request):
    a = 'out'
    if request.session['remailid']==a:
	return HttpResponseRedirect('/rsigninerror/')
    else:
	jobs = Postjob.objects.all().filter(email = request.session['remailid']).order_by('-id')
	details = Arctic.objects.get(email = request.session['remailid'])
        context = {'jobs':jobs, 'email' : request.session['remailid'], 'details':details}
        return render_to_response('jobdetails.html', context)

def job(request, articleid=1):
    a = 'out'
    if request.session['remailid']==a:
	return HttpResponseRedirect('/rsigninerror/')
    else:
	try:
	    job = Postjob.objects.get(id=articleid)
	    details = Arctic.objects.get(email = request.session['remailid'])
	    return render_to_response('job.html', {'job': job, 'email':request.session['remailid'], 'details': details })
	except:
	    return HttpResponseRedirect('/rkhhg/')


def change(request):
    a='out'
    if 'remailid' in request.session:
	if request.session['remailid']==a:
	    return HttpResponseRedirect('/rsigninerror/')
	else:
	    return render_to_response('changepassword.html',{'email':request.session['remailid']}, context_instance=RequestContext(request))
    else:
	return HttpResponseRedirect('/rsigninerror/')

def processpasswd(request):
    a='out'
    if 'remailid' in request.session:
	if request.session['remailid']==a:
	    return HttpResponseRedirect('/rsigninerror/')
	else:
	    email = request.session['remailid']
	    oldpassword = request.POST.get('oldpasswd', '')
	    passwd = request.POST.get('confirmpasswd', '')
	    a = Arctic.objects.filter(email = email)
	    if a[0].passwd == oldpassword:
		a.update(passwd = passwd , confirm_passwd=passwd)
	        return HttpResponseRedirect('/rprofilec/')
	    else:
		return HttpResponseRedirect('/changepassword/incorrect/')
    else:
	return HttpResponseRedirect('/rsigninerror/')

def changeincorrect(request):
    a='out'
    condition='Wrong Current Password Entered'
    if 'remailid' in request.session:
	if request.session['remailid']==a:
	    return HttpResponseRedirect('/rsigninerror/')
	else:
	    return render_to_response('changepassword.html',{'email':request.session['remailid'], 'condition':condition}, context_instance=RequestContext(request))
    else:
	return HttpResponseRedirect('/rsigninerror/')



def rprofilec(request):
    condition="Password Changed Successfully"
    details = Arctic.objects.get(email = request.session['remailid'])
    return render_to_response('rprofile.html', {'email': request.session['remailid'], 'details':details, 'condition':condition})

#####################################################################################################################################################

def searchjob(request):
    return render_to_response('searchjob.html',context_instance=RequestContext(request))

def findjob(request):
    location = request.POST.get('location', '')
    title = request.POST.get('title', '')
    experience = request.POST.get('minexp', '')
    if location=="" and title=="" and experience=="":
	c=[]
    else:
        a = Postjob.objects.filter(location__icontains = location.lower())
        b = a.all().filter(title__icontains = title.lower())
        if not experience:
	    experience=30
        c = b.all().exclude(minexp__gt = int(experience))
    return render_to_response('searchedjobdetails.html', { 'jobs' : c})

def jobsearch(request, articleid=1):
    job = Postjob.objects.get(id=articleid)
    details = Arctic.objects.get(email = job.email)
    return render_to_response('uniquejobsearchdetails.html', {'job': job, 'details':details })

def applied(request, articleid=1):
    a = 'out'
    if 'emailid' in request.session:
	if request.session['emailid']!=a:
            job = Postjob.objects.get(id = articleid)
            details = Arctic.objects.get(email = job.email)
	    candidate = Candidate.objects.get(email = request.session['emailid'])
	    plaintext = get_template('emaily.txt')
	    htmly = get_template('email.html')
	    d = Context({ 'email': job.email, 'title': job.title, 'description': job.description, 'industry':job.industry, 'functional':job.functional, 'minexp':job.minexp, 'maxexp':job.maxexp, 'minsalary':job.minsalary, 'maxsalary':job.maxsalary, 'location':job.location, 'jtype':job.jtype, 'qualification':job.qualification, 'company':details.company, 'contact':details.contact, 'website':details.website, 'location':details.location, 'name':candidate.name, 'exp':candidate.exp, 'skills':candidate.skills, 'institute':candidate.institute, 'qualification':candidate.qualification, 'passing':candidate.passing, 'cemail':request.session['emailid'] })
	    text_content = plaintext.render(d)
	    html_content = htmly.render(d)
	    msg = EmailMultiAlternatives('Job Application', text_content, 'Sheesh@rragroups.com', [job.email])
	    msg.attach_alternative(html_content, "text/html")
	    msg.send()
	    return HttpResponseRedirect('/appliedsuccessfully/')
	else:
	    condition = "Login First to apply to a job"
	    request.session['remailid']=a
	    return render_to_response('Signup.html',{'cond':condition},context_instance=RequestContext(request))
    else:
	condition = "Login First to apply to a job"
	request.session['remailid']=a
	return render_to_response('Signup.html',{'cond':condition},context_instance=RequestContext(request))

#####################################################################################################################################################

def buyonline(request):
    return render_to_response('buyonline.html')

#####################################################################################################################################################


def resumeservice(request):
    return render_to_response('resumesearch.html',context_instance=RequestContext(request))


def findresumes(request):
    locationa = request.POST.get('locationa', '')
    location = request.POST.get('location', '')
    minexp = request.POST.get('expmin','')
    maxexp = request.POST.get('expmax', '')
    minsalary = request.POST.get('minsalary', '')
    maxsalary = request.POST.get('maxsalary', '')
    title = request.POST.get('title', '')
    skills = request.POST.get('skills', '')
    sector = request.POST.get('sector', '')
    functional = request.POST.get('functional', '')
    qualification = request.POST.get('qualification', '')
    specialization = request.POST.get('specialization', '')
    certification = request.POST.get('certification', '')
    passingmin = request.POST.get('passingmin', '')
    passingmax = request.POST.get('passingmax', '')
    jtype = request.POST.get('course', '')
    resume = request.POST.get('attached', '')
    confirmemail = request.POST.get('confirmmail', '')
    confirmmobile = request.POST.get('confirmmobile', '')
    active = request.POST.get('active', '')
    z = Candidate.objects.all().filter(location__icontains = locationa.lower())
    a = z.all().filter(location__icontains = location)
    if not minexp:
	minexp = 0
    b = a.all().filter(exp__gte = int(minexp))
    if not maxexp:
	maxexp = 40
    c = b.all().filter(exp__lte = int(maxexp))
    if not minsalary:
	minsalary = 0.0
    d = c.all().filter(minsalary__gte = float(minsalary))
    if not maxsalary:
	maxsalary = 50.0
    e = d.all().filter(minsalary__lte = float(maxsalary))
    q = e.all().filter(title__icontains = title)
    f = q.all().filter(skills__icontains = skills)
    g = f.all().filter(sector__icontains = sector)
    h = g.all().filter(functional__icontains = functional)
    i = h.all().filter(qualification__icontains = qualification)
    j = i.all().filter(specialization__icontains = specialization)
    k = j.all().filter(certification__icontains = certification)
    if not passingmin:
	passingmin = 1940
    l = k.all().filter(passing__gte = int(passingmin))
    if not passingmax:
	passingmax = datetime.date.today().year + 4
    m = l.all().filter(passing__lte = passingmax)
    n = m.all().filter(jtype__icontains = jtype)
    if not active:
	active = 1000
    o = n.all().filter(pubdate__gte = datetime.date.today()-datetime.timedelta(int(active)))
    if resume:
	w = [],v=[]
	for x in o:
	    y = Resume.objects.get(email = x.email)
	    if y.resume:
		v.append(y)
		w.append(x)
		return render_to_response('resultresume.html', {'result':w})
    else:
	w = o
    	return render_to_response('resultresume.html', {'result':w})



####################################################         For Jobseeker Login        ############################################################

def forgot(request):
    return render_to_response('forgotpage.html',context_instance=RequestContext(request))

def sendmail(request):
    c = 'out'
    email = request.POST.get('email', '')
    if Article.objects.filter(email = email).exists():
	a = email.encode('zip')
        b = base64.b64encode(a)
        send_mail("Job Portal-Reset Your Password","Click on the link to reset your password--  http://rragroups-jportal.rhcloud.com/resetpassword/%s/" % b, 'Sheesh@rragroups.com', [email], fail_silently=False)
        return HttpResponseRedirect('/sendingsuccessfull/')
    else:
	cond = "Email id does not exists, Register Yourself first!!!"
	request.session['remailid']=c
        return render_to_response('Signup.html',{'cond':cond}, context_instance=RequestContext(request))


def sendingsuccess(request):
    a = 'out'
    request.session['remailid']=a
    cond = "An Activation link has been sent to your email to reset your password"
    return render_to_response('Signup.html',{'cond':cond}, context_instance=RequestContext(request))

def resetpassword(request, another="a"):
    c = 'out'
    b = base64.b64decode(another)
    a = b.decode('zip')
    if Article.objects.filter(email=a).exists():
	request.session['email']=a
	return render_to_response('resetpage.html',context_instance=RequestContext(request))
    else:
        cond = "Invalid Link Entered"
	request.session['remailid']=c
        return render_to_response('Signup.html',{'cond':cond}, context_instance=RequestContext(request))

def resettingpassword(request):
    a='out'
    request.session['emailid']=a
    request.session['remailid']=a
    password = request.POST.get('password', '')
    confirmpassword = request.POST.get('confirmpassword', '')
    b = Article.objects.get(email=request.session['email'])
    b.passwd=password
    b.confirm_passwd =password
    b.save()
    del request.session['email']
    return HttpResponseRedirect('/changedsuccessfull/')

def changedsuccessfull(request):
    a = 'out'
    request.session['remailid']=a
    cond = "Password Changed Successfully"
    return render_to_response('Signup.html',{'cond':cond}, context_instance=RequestContext(request))

#######################################################      For Recruiter Login      ###############################################################

def rforgot(request):
    return render_to_response('rforgotpage.html',context_instance=RequestContext(request))

def rsendmail(request):
    email = request.POST.get('email', '')
    if Arctic.objects.filter(email = email).exists():
	a = email.encode('zip')
        b = base64.b64encode(a)
        send_mail("Job Portal-Reset Your Password","Click on the link to reset your password--  http://rragroups-jportal.rhcloud.com/rresetpassword/%s/" % b, 'Sheesh@rragroups.com', [email], fail_silently=False)
        return HttpResponseRedirect('/rsendingsuccessfull/')
    else:
	cond = "Email id does not exists, Register Yourself first!!!"
        return render_to_response('recruiter_signup.html',{'condition':cond}, context_instance=RequestContext(request))

def rsendingsuccess(request):
    cond = "An Activation link has been sent to your email to reset your password"
    return render_to_response('recruiter_signup.html',{'condition':cond}, context_instance=RequestContext(request))

def rresetpassword(request, another="a"):
    b = base64.b64decode(another)
    a = b.decode('zip')
    if Arctic.objects.filter(email=a).exists():
	request.session['email']=a
	return render_to_response('rresetpage.html',context_instance=RequestContext(request))
    else:
        cond = "Invalid Link Entered"
        return render_to_response('recruiter_signup.html',{'condition':cond}, context_instance=RequestContext(request))

def rresettingpassword(request):
    a='out'
    request.session['emailid']=a
    request.session['remailid']=a
    password = request.POST.get('password', '')
    confirmpassword = request.POST.get('confirmpassword', '')
    b = Arctic.objects.get(email=request.session['email'])
    b.passwd=password
    b.confirm_passwd =password
    b.save()
    del request.session['email']
    return HttpResponseRedirect('/rchangedsuccessfull/')

def rchangedsuccessfull(request):
    cond = "Password Changed Successfully"
    return render_to_response('recruiter_signup.html',{'condition':cond}, context_instance=RequestContext(request))

#####################################################################################################################################################
def credit(request):
    return render_to_response('creditcard.html', context_instance=RequestContext(request))
