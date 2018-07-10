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


class BreakdownView(View):
    template_name = 'switchinweb/breakdown.html'
    def get(self, request):
        policy = Policy.objects.get(pk=request.session["policypk"])
        city = City.objects.get(pk=policy.city)
        state = city.state
        pop_vehicle = Vehicle.objects.get(pk=state.pop_vehicle)
        return render(request, self.template_name, {'policy': policy, 'coverage': policy.coverage, 'city': city, 'pop_vehicle': pop_vehicle})

class DetailView(View):
    template_name = 'switchinweb/detail.html'
    def get(self, request):
        policy = Policy.objects.get(pk=request.session["policypk"])
        pdl_rec = recPropertyDamage(policy)
        bil_rec_person = recBodilyInjury(policy)
        bil_rec_accident = bil_rec_person * 2
        pip_rec = recPIP(policy)
        col_rec = recCollision(policy)
        com_rec = recComprehensive(policy)
        upd_rec = recUninsuredProperty(policy)
        # umi_rec = recBodilyInjury(policy)
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
        vehicle = policyinfo["make"] + " " + policyinfo["model"] + " " + str(policyinfo["year"])
        policy = Policy(company_name=policyinfo["company_name"],
            policy_number=policyinfo["policy_number"],
            effective_date=policyinfo["effective_date"],
            expiration_date=policyinfo["expiration_date"],
            coverage=coverage, vin=policyinfo["vin"], mileage=mileage, vehicle=vehicle, city=city)
        policy.save()
        request.session["policypk"] = policy.id
        return HttpResponseRedirect(reverse('switchinweb:breakdown'))
    else:
        return render(request, 'switchinweb/index.html')

def manual(request):
    # Policy info
    company_name        = request.POST.get('company_name')
    policy_number       = request.POST.get('policy_number')
    effective_date      = request.POST.get('effective_date')
    expiration_date     = request.POST.get('expiration_date')
    state               = request.POST.get('state')
    vin                 = request.POST.get('vin')
    mileage             = request.POST.get('mileage')
    city                = request.POST.get('city')

    # Coverage info
    liability_property  = request.POST.get('liability_property')
    liability_person    = request.POST.get('liability_person')
    liability_accident  = request.POST.get('liability_accident')
    personal_injury     = request.POST.get('personal_injury')
    comprehensive       = request.POST.get('comprehensive')
    collision           = request.POST.get('collision')
    uninsured_property  = request.POST.get('uninsured_property')
    uninsured_person    = request.POST.get('uninsured_person')
    uninsured_accident  = request.POST.get('uninsured_accident')

    make                = request.POST.get('make')
    models              = request.POST.get('model')
    year                = request.POST.get('year')
    vin                 = request.POST.get('vin')

    vehicle = policyinfo["make"] + " " + policyinfo["model"] + " " + str(policyinfo["year"])
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
    policy = Policy(company_name=company_name,
        policy_number=policy_number,
        effective_date=effective_date,
        expiration_date=expiration_date,
        coverage=coverage, vin=vin, mileage=mileage, vehicle=vehicle, city=city)
    policy.save()
    request.session["policypk"] = policy.id
    return HttpResponseRedirect(reverse('switchinweb:breakdown'))
