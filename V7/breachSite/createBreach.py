import json
import random
import threading

with open("words_dictionary.json", 'r') as f:
    word_list_Json = json.load(f)
word_list = list(word_list_Json.keys())

with open("first-names.json") as d:
    names = json.load(d)

breach_data = [
    {
        "email": "vader@imperialed.mil",      
        "password": "StrengthThroughFear2023!",  
        "risk_level": "High"                 
    },
    {
        "email": "palpatine@imperialed.mil",  
        "password": "IamYourFather42!",        
        "risk_level": "High"                 
    }
]

def passphrase_generator(num_words=3, min_length=5, max_length=50, separator='', word_list=None):
    if word_list is None:
        word_list = []
    
    filtered_words = [
        word for word in word_list
        if len(word) >= min_length and len(word) <= max_length
    ]
    
    if not filtered_words or len(filtered_words) < num_words:
        raise ValueError(
            "Not enough words in the filtered list. "
            "Try adjusting min_length and max_length or use a different word list."
        )
    
    selected_words = random.SystemRandom().choices(filtered_words, k=num_words)
    
    return separator.join(selected_words)

def stormTrooper(amount=500, word_list=None):
    if word_list is None:
        word_list = []
    breached_data = []
    for i in range(amount):
        troopNumber = random.randint(1000, 5000)
        password = passphrase_generator(word_list=word_list)
        breached_data.append({
            "email": f"TK-{troopNumber}@imperialed.mil",
            "password": password,
            "risk_level": "Low"
        })
    return breached_data

def navy(amount=100, word_list=None, names=None):
    if names is None:
        names = []
    breach_data = []
    for i in range(amount):
        name = random.choice(names)
        password = passphrase_generator(word_list=word_list)
        breach_data.append({
            "email": f"{name}@imperialed.mil",
            "password": password,
            "risk_level": "Low"
        })
    return breach_data

imperial_services = [
    "Imperial Catering Services Inc.",
    "Imperial Telecommunications Network",
    "Imperial Medical Services Consortium",
    "Imperial Maintenance and Repair Division",
    "Imperial Security Bureau Services",
    "Imperial News Network",
    "Imperial Logistics and Transportation Command",
    "Imperial Energy and Power Solutions",
    "Imperial Defense Contractors League",
    "Imperial Law Enforcement Agency",
    "Imperial Legal Services Group",
    "Imperial Educational Services",
    "Imperial Construction and Development Corp.",
    "Imperial Space Operations Unit",
    "Imperial Information Technology Division",
    "Imperial Financial Services Authority",
    "Imperial Casino and Entertainment Division",
    "Imperial Research and Development Institute",
    "Imperial News and Propaganda Bureau",
    "Imperial Exploration and Mining Consortium"
]

def breach(results, word_list, names):
    selected = random.choice(imperial_services)
    date = f"{random.randint(1984, 2024)}-0{random.randint(1, 9)}-{random.randint(1, 31)}"
    navies = navy(names=names, word_list=word_list)
    storm = stormTrooper(word_list=word_list)
    alldata = navies + storm
    if random.random() > 0.35:
        alldata += breach_data.copy()
    for d in alldata:
        d["service_name"] = selected
        d['paste_date'] = date
    results.append(alldata)

def allbreaches(amount):
    threads = []
    completeData = []
    if amount > 20:
        print("Limiting to 20 threads due to resource constraints.")
        amount = 20
    results = []
    lock = threading.Lock()
    
    for i in range(amount):
        thread = threading.Thread(target=breach, args=(results, word_list, names))
        threads.append(thread)
    
    for t in threads:
        t.start()
    
    print("Started Waiting")
    for t in threads:
        t.join()
    
    for r in results:
        completeData.extend(r)
    
    return completeData

def save(data):
    with open("breaches.json", 'w') as final:
        json.dump(data, final)

if __name__ == "__main__":
    save(allbreaches(14))