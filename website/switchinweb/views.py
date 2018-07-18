from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View, generic
from .forms import PolicyForm, ManualForm
from .models import Coverage, Vehicle, Policy, City, Vehicle
from .modules.textExtract import extractInfo
from .modules.recAlgo import recPropertyDamage, recBodilyInjury, recPIP, recCollision, recComprehensive, recUninsuredProperty
from django.conf import settings

class IndexView(View):
    template_name = 'switchinweb/index.html'
    def get(self, request):
        return render(request, self.template_name)
    def post(self, request):
        return upload(request) if ('uploadDoc' in request.POST) else manual(request)

class AboutView(View):
    template_name = 'switchinweb/about.html'
    def get(self, request):
        return render(request, self.template_name)

class TeamView(View):
    template_name = 'switchinweb/team.html'
    def get(self, request):
        return render(request, self.template_name)

class ContactView(View):
    template_name = 'switchinweb/contact.html'
    def get(self, request):
        return render(request, self.template_name)


class BreakdownView(View):
    template_name = 'switchinweb/breakdown.html'
    def get(self, request):
        policy = Policy.objects.get(pk=request.session["policypk"])
        city = City.objects.get(pk=policy.city)
        state = city.state
        pop_vehicle = Vehicle.objects.get(pk=state.pop_vehicle)

        pdl_rec = recPropertyDamage(policy)
        bil_rec_person = recBodilyInjury(policy)
        bil_rec_accident = bil_rec_person * 2
        pip_rec = recPIP(policy)
        col_rec = recCollision(policy)
        com_rec = recComprehensive(policy)
        upd_rec = recUninsuredProperty(policy)

        request.session["pdl_rec"] = pdl_rec
        request.session["bil_rec_person"] = bil_rec_person
        request.session["bil_rec_accident"] = bil_rec_accident
        request.session["pip_rec"] = pip_rec
        request.session["col_rec"] = col_rec
        request.session["com_rec"] = com_rec
        request.session["upd_rec"] = upd_rec
        return render(request, self.template_name, {'policy': policy, 'coverage': policy.coverage, 'city': city, 'pop_vehicle': pop_vehicle, 'pdl_rec': pdl_rec, 'bil_rec_person': bil_rec_person,
            'bil_rec_accident': bil_rec_accident,
            'pip_rec': pip_rec, 'col_rec': col_rec, 'com_rec': com_rec,
            'upd_rec': upd_rec})

class DetailView(View):
    template_name = 'switchinweb/detail.html'
    def get(self, request):
        policy = Policy.objects.get(pk=request.session["policypk"])
        pdl_rec = request.session["pdl_rec"]
        bil_rec_person = request.session["bil_rec_person"]
        bil_rec_accident = request.session["bil_rec_accident"]
        pip_rec = request.session["pip_rec"]
        col_rec = request.session["col_rec"]
        com_rec = request.session["com_rec"]
        upd_rec = request.session["upd_rec"]
        return render(request, self.template_name, {'policy': policy,
            'pdl_rec': pdl_rec, 'bil_rec_person': bil_rec_person,
            'bil_rec_accident': bil_rec_accident,
            'pip_rec': pip_rec, 'col_rec': col_rec, 'com_rec': com_rec,
            'upd_rec': upd_rec})

def upload(request):
    form = PolicyForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        doc = request.FILES['document']
        city = request.POST['city']
        mileage = request.POST['mileage']
        policyinfo = extractInfo(settings.MEDIA_ROOT + "uploads/" + doc.name)
        coverage = Coverage(liability_property=policyinfo["liability_property"],
            liability_person=policyinfo["liability_person"],
            liability_accident=policyinfo["liability_accident"],
            personal_injury=policyinfo["personal_injury"],
            comprehensive=policyinfo["comprehensive"],
            collision=policyinfo["collision"],
            uninsured_property=policyinfo["uninsured_property"],
            uninsured_person=policyinfo["uninsured_person"],
            uninsured_accident=policyinfo["uninsured_accident"],
            under_property=policyinfo["under_property"],
            under_person=policyinfo["under_person"],
            under_accident=policyinfo["under_accident"])
        coverage.save()
        vehicle = str(policyinfo["year"]) + " " + policyinfo["make"] + " " + policyinfo["model"]
        policy = Policy(company_name=policyinfo["company_name"],
            policy_number=policyinfo["policy_number"],
            coverage=coverage, vin=policyinfo["vin"], mileage=mileage, vehicle=vehicle, city=city)
        policy.save()
        if(policyinfo["effective_date"] !=""):
            policy.effective_date=policyinfo["effective_date"]
            policy.save()
        if(policyinfo["expiration_date"] != ""):
            policy.expiration_date=policyinfo["expiration_date"]
            policy.save()
        request.session["policypk"] = policy.id
        request.session["policyinfo"] = policyinfo["liability_person"]
        return HttpResponseRedirect(reverse('switchinweb:breakdown'))
    else:
        return render(request, 'switchinweb/index.html')

def manual(request):
    # Policy info
    company_name        = request.POST.get('company_name')
    mileage             = request.POST.get('mileage')
    city                = request.POST.get('city')

    # Coverage info
    liability_property  = int(request.POST.get('liability_property')) if request.POST.get('liability_property') != "N/A" else 0
    liability_injury    = request.POST.get('liability_injury')
    liability_person    = 0
    liability_accident  = 0

    if (liability_injury == "N/A"):
        liability_person = 0
        liability_accident = 0
    else:
        liability_injury = liability_injury.split('/')
        liability_person = int(liability_injury[0])
        liability_accident = int(liability_injury[1])

    personal_injury     = int(request.POST.get('personal_injury')) if request.POST.get('personal_injury') != "N/A" else 0
    comprehensive       = int(request.POST.get('comprehensive')) if request.POST.get('comprehensive') != "N/A" else 0
    collision           = int(request.POST.get('collision')) if request.POST.get('collision') != "N/A" else 0
    uninsured_property  = int(request.POST.get('uninsured_property')) if request.POST.get('uninsured_property') != "N/A" else 0
    uninsured_injury    = request.POST.get('uninsured_injury')
    uninsured_person    = 0
    uninsured_accident  = 0

    if (uninsured_injury == "N/A"):
        uninsured_person = 0
        uninsured_accident = 0
    else:
        uninsured_injury = uninsured_injury.split('/')
        uninsured_person = int(uninsured_injury[0])
        uninsured_accident = int(uninsured_injury[1])


    vehicle             = request.POST.get('vehicle_info').upper()

    coverage = Coverage(liability_property=liability_property,
        liability_person=liability_person,
        liability_accident=liability_accident,
        personal_injury=personal_injury,
        comprehensive=comprehensive,
        collision=collision,
        uninsured_property=uninsured_property,
        uninsured_person=uninsured_person,
        uninsured_accident=uninsured_accident)
    coverage.save()
    policy = Policy(company_name=company_name, coverage=coverage,
        mileage=mileage, vehicle=vehicle, city=city)
    policy.save()
    request.session["policypk"] = policy.id
    return HttpResponseRedirect(reverse('switchinweb:breakdown'))
