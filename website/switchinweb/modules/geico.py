from .utility import convertDateFormat, str_to_num

def geicoCoverage(policyinfo):
    coverage = {"liability_property": str_to_num(policyinfo["Property Damage Liability"]),
    "liability_person": 0, "liability_accident": 0,
    "personal_injury": str_to_num(policyinfo["Personal Injury Protection"]),
    "comprehensive": str_to_num(policyinfo["Comprehensive"]),
    "collision": str_to_num(policyinfo["Collision"]),
    "uninsured_property": str_to_num(policyinfo["Uninsured Motorist Property Damage"]),
    "uninsured_person": 0, "uninsured_accident": 0,
    "under_property": 0, "under_person": 0, "under_accident": 0}
    bodily_injury = policyinfo.pop("Bodily Injury Liability", "")
    if (bodily_injury):
        bodily_injury = bodily_injury.split("/")
        coverage["liability_person"] = str_to_num(bodily_injury[0])
        coverage["liability_accident"] = str_to_num(bodily_injury[1])
    uninsured_motorist = policyinfo.pop("Uninsured Motorist/Nonstacked", "")
    if (uninsured_motorist):
        uninsured_motorist = uninsured_motorist.split("/")
        coverage["uninsured_person"] = str_to_num(uninsured_motorist[0])
        coverage["uninsured_accident"] = str_to_num(uninsured_motorist[1])
    under_motorist = policyinfo.pop("Uninsured &Underinsured Motorists", "")
    if (under_motorist):
        under_motorist = under_motorist.split("/")
        coverage["under_person"] = str_to_num(under_motorist[0])
        coverage["under_accident"] = str_to_num(under_motorist[1])
    return coverage

def geicoGeneral(policyinfo):
    general = {"company_name": policyinfo["Company Name"],
    "policy_number": policyinfo["Policy Number"],
    "effective_date": convertDateFormat(policyinfo["Effective Date"]),
    "expiration_date": convertDateFormat(policyinfo["Expiration Date"]),
    "vin": policyinfo["VIN"]}
    return general

def geicoVehicle(policyinfo):
    vehicle = {"make": policyinfo["Make"], "model": policyinfo["Model"],
    "year": int(policyinfo["Vehicle Year"])}
    return vehicle

def geicoFormat(policyinfo):
    coverage = geicoCoverage(policyinfo)
    general = geicoGeneral(policyinfo)
    vehicle = geicoVehicle(policyinfo)
    coverage.update(general)
    coverage.update(vehicle)
    return coverage