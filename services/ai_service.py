def analyze_incident(description):


    if "fire" in description.lower():

        return "HIGH"


    elif "flood" in description.lower():

        return "MEDIUM"


    else:

        return "LOW"
