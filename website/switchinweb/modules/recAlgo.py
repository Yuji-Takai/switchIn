from switchinweb.models import Coverage, Vehicle, State, City, Policy

def recPropertyDamage(policy):
    city = City.objects.get(pk=policy.city)
    state = city.state
    user_vehicle = Vehicle.objects.get(pk=policy.vehicle)
    pop_vehicle = Vehicle.objects.get(pk=state.pop_vehicle)
    avg_property = state.avg_property
    return int(avg_property * (pop_vehicle.iso_coll/user_vehicle.iso_coll) * (user_vehicle.mass/pop_vehicle.mass))

def recBodilyInjury(policy):
    city = City.objects.get(pk=policy.city)
    state = city.state
    user_vehicle = Vehicle.objects.get(pk=policy.vehicle)
    pop_vehicle = Vehicle.objects.get(pk=state.pop_vehicle)
    avg_injury = avgBodilyInjury(state)
    return int(avg_injury * (pop_vehicle.iso_coll/user_vehicle.iso_coll) * (user_vehicle.mass/pop_vehicle.mass))

def avgBodilyInjury(state):
    total_accident = state.severe_num + state.visible_num + state.pain_num
    return ((state.avg_severe * (state.severe_num/total_accident)
        + state.avg_visible * (state.visible_num/total_accident)
        + state.avg_pain * (state.pain_num/total_accident)) / 3)

def recPIP(policy):
    city = City.objects.get(pk=policy.city)
    state = city.state
    user_vehicle = Vehicle.objects.get(pk=policy.vehicle)
    pop_vehicle = Vehicle.objects.get(pk=state.pop_vehicle)
    avg_injury = avgBodilyInjury(state)
    return int(avg_injury * (user_vehicle.iso_coll/pop_vehicle.iso_coll) * (pop_vehicle.mass/user_vehicle.mass))

def recCollision(policy):
    mileage = policy.mileage
    city = City.objects.get(pk=policy.city)
    avg_mileage = city.state.avg_mileage
    base = 1000
    if (mileage < 0.5 * avg_mileage):
        base = 1000
    elif (mileage < 1 * avg_mileage):
        base = 800
    elif (mileage < 1.5 * avg_mileage):
        base = 600
    elif (mileage < 2.0  * avg_mileage):
        base = 400
    else:
        base = 200

    return int(base * city.state.total_pop / city.state.vehicle_pop)

def recComprehensive(policy):
    city = City.objects.get(pk=policy.city)
    crime_rate = city.crime_rate
    pop_vehicle = Vehicle.objects.get(pk=city.state.pop_vehicle)
    user_vehicle = Vehicle.objects.get(pk=policy.vehicle)
    base = 1000
    if (crime_rate < 0.005):
        base = 1000
    elif (crime_rate < 0.01):
        base = 800
    elif (crime_rate < 0.015):
        base = 600
    elif (crime_rate < 0.02):
        base = 400
    else:
        base = 200
    return int(base * pop_vehicle.iso_comp / user_vehicle.iso_comp)

def recUninsuredProperty(policy):
    city = City.objects.get(pk=policy.city)
    state = city.state
    user_vehicle = Vehicle.objects.get(pk=policy.vehicle)
    pop_vehicle = Vehicle.objects.get(pk=state.pop_vehicle)
    avg_property = state.avg_property
    base = avg_property * (user_vehicle.iso_coll/pop_vehicle.iso_coll) * (pop_vehicle.mass/user_vehicle.mass)
    multiplier = 1
    if (state.uninsured_rate < 0.05):
        multiplier = 0.2
    elif (state.uninsured_rate < 0.1):
        multiplier = 0.4
    elif (state.uninsured_rate < 0.15):
        multiplier = 0.6
    elif (state.uninsured_rate < 0.2):
        multiplier = 0.8
    else:
        multiplier = 1
    return int(base * multiplier)

def recUninsuredInjury(policy):
    city = City.objects.get(pk=policy.city)
    state = city.state
    user_vehicle = Vehicle.objects.get(pk=policy.vehicle)
    pop_vehicle = Vehicle.objects.get(pk=state.pop_vehicle)
    avg_injury = avgBodilyInjury(state)
    base = avg_injury * (user_vehicle.iso_coll/pop_vehicle.iso_coll) * (pop_vehicle.mass/user_vehicle.mass)
    multiplier = 1
    if (state.uninsured_rate < 0.05):
        multiplier = 0.2
    elif (state.uninsured_rate < 0.1):
        multiplier = 0.4
    elif (state.uninsured_rate < 0.15):
        multiplier = 0.6
    elif (state.uninsured_rate < 0.2):
        multiplier = 0.8
    else:
        multiplier = 1
    return int(base * multiplier)