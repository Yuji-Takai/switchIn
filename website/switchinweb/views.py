from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View, generic
from .forms import PolicyForm, ManualForm
from .models import Coverage, Policy, Vehicle
from .textExtract import extractInfo
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
        return render(request, self.template_name, {'policy': policy, 'vehicle': policy.vehicle, 'coverage': policy.coverage})

class DetailView(View):
    template_name = 'switchinweb/detail.html'
    def get(self, request):
        policy = Policy.objects.get(pk=request.session["policypk"])
        message = "Hi"
        return render(request, self.template_name, {'policy': policy, 'message': message})

def upload(request):
    form = PolicyForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        doc = request.FILES['document']
        policyinfo = extractInfo(settings.MEDIA_ROOT + "uploads/" + doc.name)
        vehicle = Vehicle(year=policyinfo["Vehicle Year"], make=policyinfo["Make"], model=policyinfo["Model"], vin=policyinfo["VIN"])
        vehicle.save()
        coverage = Coverage(liability_property=policyinfo["Property Damage Liability"], liability_injury=policyinfo["Bodily Injury Liability"], personal_injury=policyinfo["Personal Injury Protection"], comprehensive=policyinfo["Comprehensive"], collision=policyinfo["Collision"], uninsured_injury=policyinfo["Uninsured &Underinsured Motorists"])
        coverage.save()
        policy = Policy(company_name=policyinfo["Company Name"], policy_number=policyinfo["Policy Number"], effective_date=policyinfo["Effective Date"], expiration_date=policyinfo["Expiration Date"], state=policyinfo["Registered State"], coverage=coverage, vehicle=vehicle)
        policy.save()
        request.session["policypk"] = policy.id
        return HttpResponseRedirect(reverse('switchinweb:breakdown'))
    else:
        return render(request, 'switchinweb/index.html')

def manual(request):
    company_name = request.POST.get('company_name')
    policy_number = request.POST.get('policy_number')
    effective_date = request.POST.get('effective_date')
    expiration_date = request.POST.get('expiration_date')
    state = request.POST.get('state')
    coverage = request.POST.get('coverage')
    year = request.POST.get('year')
    make = request.POST.get('make')
    model = request.POST.get('model')
    vin = request.POST.get('vin')
    liability_property = request.POST.get('liability_property')
    liability_injury = request.POST.get('liability_injury')
    personal_injury = request.POST.get('personal_injury')
    comprehensive = request.POST.get('comprehensive')
    collision = request.POST.get('collision')
    uninsured_injury = request.POST.get('uninsured_injury')
    vehicle = Vehicle(year=year, make=make, model=model, vin=vin)
    vehicle.save()
    coverage = Coverage(liability_property=liability_property, liability_injury=liability_injury, personal_injury=personal_injury, comprehensive=comprehensive, collision=collision, uninsured_injury=uninsured_injury)
    coverage.save()
    policy = Policy(company_name=company_name, policy_number=policy_number, effective_date=effective_date, expiration_date=expiration_date, state=state, coverage=coverage, vehicle=vehicle)
    policy.save()
    request.session["policypk"] = policy.id
    return HttpResponseRedirect(reverse('switchinweb:breakdown'))
