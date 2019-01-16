from busboy.model import Stop

church_cross_east = "7338653551721429731"
church_cross_west = "7338653551721416881"
parnell_place = "7338653551721440301"
parnell_place_city = "7338653551721428451"

stops_by_route = {
    "201": {
        "Dennehy's Cross (Opp Cork Farm Ctr)": "7338653551721425361",
        "Boherboy Rd (Opp Soccer Pitch)": "7338653551721425551",
        "Boherboy Road (Lotabeg Estate)": "7338653551721425571",
        "Curraheen Road (Firgrove Gardens)": "7338653551721429061",
    },
    "202": {
        "Merchants Quay (Dunnes Stores A)": "7338653551721484281",
        "Mahon Point (Omniplex)": "7338653551721432401",
        "Hollyhill (Apple)": "7338653551721484231",
        "Merchants Quay (Riverside)": "7338653551721484301",
    },
    "203": {
        "Grand Parade (Argos)": "7338653551721425971",
        "Watercourse Road (Blackpool Pharmacy)": "7338653551721427621",
        "St. Patrick Street (Marks and Spencer)": "7338653551721427001",
        "Manor Farm (Southbound)": "7338653551721421141",
    },
    "205": {
        "Cork Institute of Technology": "7338653551721395481",
        "Grand Parade (Argos)": "7338653551721425971",
        "Washington Street (Four Star Pizza)": "7338653551721425791",
        "Model Farm Rd (Opposite Mount Mercy)": "7338653551721427081",
    },
    "206": {
        "Cork City Hall": "7338653551721436121",
        "Grange (Dunvale)": "7338653551721426351",
        "Grange (Frankfield Estate)": "7338653551721425981",
        "South Terrace (Opp Irish Pensions)": "7338653551721426191",
    },
    "207": {
        "Donnybrook (Scairt Cross Terminus)": "7338653551721419201",
        "Douglas Road (Opp Eglantine School)": "7338653551721426691",
        "Grand Parade (City Library)": "7338653551721426741",
        "Summerhill North (St. Luke's Cross)": "7338653551721481421",
        "Glen Avenue (Opp Comeragh Park)": "7338653551721428901",
        "Glenheights Park Terminus": "7338653551721426891",
        "Summerhill North (Chamber of Comm)": "7338653551721425751",
        "Cork City Hall": "7338653551721436121",
        "Douglas Road (Ardfallen Shopping Mall)": "7338653551721426541",
    },
    "207A": {
        "Glenthorn (Glenheights Square B)": "7338653551721431731",
        "Watercourse Road (Opp Blackpool Church)": "7338653551721428841",
        "Summerhill North (Chamber of Comm)": "7338653551721425751",
        "Merchants Quay (Dunnes Stores B)": "7338653551721398511",
        "Summerhill North (St. Luke's Cross)": "7338653551721481421",
        "Watercourse Rd (Blackpool Church)": "7338653551721427941",
    },
    "208": {
        "St. Patrick Street (Savoy Complex)": "7338653551721425451",
        "St. Patrick Street Debenhams": "7338653551721425771",
        "Ashmount (Turning Circle)": "7338653551721431771",
        "Curraheen Village": "7338653551721395491",
    },
    "209": {
        "St. Patrick Street (Marks and Spencer)": "7338653551721427001",
        "Audley Place (Lansdowne Court)": "7338653551721429331",
        "Lotamore Drive (Southbound)": "7338653551721398431",
        "Lotamore Drive (Northbound)": "7338653551721431141",
        "Summerhill North (St. Luke's Cross)": "7338653551721481421",
        "Merchants Quay (Dunnes Stores B)": "7338653551721398511",
    },
    "209A": {
        "Summerhill South (Capwell Garage)": "7338653551721415371",
        "Lwr Friars Walk (Connolly Road Junction)": "7338653551721427531",
        "Derrynane Road (Northbound)": "7338653551721431521",
        "South Terrace (Opp Irish Pensions)": "7338653551721426191",
    },
    "214": {
        "St. Patrick St (Brown Thomas B)": "7338653551721428771",
        "Togher Road (Opp Earlwood Estate)": "7338653551721428501",
        "CUH (A and E)": "7338653551721428621",
        "Togher Road (Earlwood Estate)": "7338653551721428721",
    },
    "215": {
        "Jacobs Island (The Sanctuary)": "7338653551721428181",
        "Ballinlough Road (Knockrea)": "7338653551721428321",
        "Grand Parade (City Library)": "7338653551721426741",
        "North Point (Opp Business Park)": "7338653551721398561",
        "Cloghroe (Fairways Terminus)": "7338653551721398691",
        "Cloghroe (Coolflugh Terminus)": "7338653551721398701",
        "Blarney (Station Cross)": "7338653551721398791",
        "St. Patrick Street (Brown Thomas A)": "7338653551721426481",
        "Ballinlough Road (Shrewsbury Estate)": "7338653551721428081",
    },
    "215A": {
        "Grand Parade (City Library)": "7338653551721426741",
        "Skehard Road (Ashleigh Rise)": "7338653551721428111",
        "Jacobs Island (The Sanctuary)": "7338653551721428181",
    },
    "216": {
        "CUH (Main Gate)": "7338653551721429431",
        "South Mall (Opp Cork Passport Office)": "7338653551721427331",
        "Douglas Road (Ardfallen Shopping Mall)": "7338653551721426541",
        "Clarkes Hill (The Borough Southbound)": "7338653551721431281",
        "Mount Oval (Monswood Est)": "7338653551721440321",
        "Maryborough Woods (Greendale Rd))": "7338653551721431341",
        "Douglas Village East (Shopping Centre)": "7338653551721426651",
        "Douglas Road (Whitethorn)": "7338653551721426711",
        "Grand Parade (City Library)": "7338653551721426741",
        "Glasheen Road (Hartlands Ave)": "7338653551721475241",
    },
    "219": {
        "Ringmahon Road (Opp Garda Stn)": "7338653551721431571",
        "Mahon Point Rd (Opp CSO Office)": "7338653551721428231",
        "Douglas Village East ( Service Station)": "7338653551721426581",
        "South Douglas Rd (Opp Loreto Park)": "7338653551721426131",
        "Pearse Road (A.I.B)": "7338653551721427491",
        "Togher Road (Opp Earlwood Estate)": "7338653551721428501",
        "Bishopstown Road (Opp Garda Station)": "7338653551721425881",
        "Cork Institute of Technology": "7338653551721395481",
        "Spur Hill (Opposite Fernwood Estate)": "7338653551721428661",
        "Curragh Rd (Turners Cross Stadium)": "7338653551721427891",
        "Douglas Village East (Shopping Centre)": "7338653551721426651",
        "Ringmahon Road (Meadow Grove Est)": "7338653551721431561",
        "Mahon Point Rd (Opp City Gate)": "7338653551721428221",
    },
    "220": {
        "South Mall (Opp Cork Passport Office)": "7338653551721427331",
        "Grand Parade (City Library)": "7338653551721426741",
        "Carrigaline (Carrigaline Court Hotel)": "7338653551721430521",
        "Ballincollig (Shopping Centre)": "7338653551721429531",
        "Ballincollig (Opp Shopping Centre)": "7338653551721417701",
        "Carrigaline (Church)": "7338653551721430311",
    },
    "220X": {
        "Ovens (Grange Road Terminus)": "7338653551722184832",
        "Western Rd (Opp UCC Western Gateway)": "7338653551721425381",
        "Crosshaven (Yacht Club Southbound)": "7338653551721430361",
        "Crosshaven (Village Ctr Northbound)": "7338653551721430391",
        "Crosshaven (Village Ctr Southbound)": "7338653551721417121",
        "Carrigaline (Town Ctr Bridge Northbound)": "7338653551721430621",
        "Carrigrohane Rd (Cork County Hall)": "7338653551721416811",
    },
    "221": {
        "Cork (Bus Station - Parnell Place)": "7338653551721440301",
        "Lwr Glanmire Rd (Beales Hill)": "7338653551721429751",
        "Glanmire (O Cearnaigh Public House )": "7338653551721397311",
        "Glyntown Rd (Ardcarrig)": "7338653551721295021",
        "Knockraha (Church)": "7338653551721738661",
        "Knockraha (The Old Schoolhouse)": "7338653551721423131",
        "Lwr Glanmire Rd (Opp Belvedere Lodge)": "7338653551721430151",
    },
}

cycle_stops = {id for r, stops in stops_by_route.items() for n, id in stops.items()}

stop_passage_tdi = "http://buseireann.ie/inc/proto/stopPassageTdi.php"
route_cover = {
    "7338653551721318801",
    "7338653551721517341",
    "7338653551722041491",
    "7338653551721794391",
    "7338653551721515931",
    "7338653551721743471",
    "7338653551721425741",
    "7338653551721708071",
    "7338653551721537481",
    "7338653551721294431",
    "7338653551721790851",
    "7338653551721340621",
    "7338653551721706621",
    "7338653551721536001",
    "7338653551721740381",
    "7338653551721474091",
    "7338653551721435441",
    "7338653551721293341",
    "7338653551721400431",
    "7338653551721340751",
    "7338653551721756281",
    "7338653551721420381",
    "7338653551721516191",
    "7338653551721816501",
    "7338653551721516161",
    "7338653551721325921",
    "7338653551721294941",
    "7338653551721822151",
    "7338653551721326581",
    "7338653551721318771",
    "7338653551721821631",
    "7338653551721536061",
    "7338653551721436121",
    "7338653551721820311",
    "7338653551721337741",
    "7338653551721715301",
    "7338653551721538171",
    "7338653551721816491",
    "7338653551721431781",
    "7338653551721516751",
    "7338653551721538001",
    "7338653551721821111",
    "7338653551721286541",
    "7338653551721790861",
    "7338653551721320811",
    "7338653551721741591",
    "7338653551721320471",
    "7338653551721286901",
    "7338653551721323171",
    "7338653551721521591",
    "7338653551721788421",
    "7338653551721316651",
    "7338653551721708491",
    "7338653551721520851",
    "7338653551721540921",
    "7338653551721311351",
    "7338653551721429581",
    "7338653551721517421",
    "7338653551721519411",
    "7338653551721321141",
    "7338653551721756351",
    "7338653551721340671",
    "7338653551721427541",
    "7338653551721397511",
    "7338653551721320281",
    "7338653551721792211",
    "7338653551721820621",
    "7338653551721291431",
    "7338653551721416171",
    "7338653551721735481",
    "7338653551721537731",
    "7338653551721415571",
    "7338653551721316411",
    "7338653551721425881",
    "7338653551721395511",
    "7338653551721715571",
    "7338653551721399371",
    "7338653551721294371",
    "7338653551721288631",
    "7338653551721536341",
    "7338653551721517331",
    "7338653551721341211",
    "7338653551721816671",
    "7338653551721337701",
    "7338653551721430221",
    "7338653551721435381",
    "7338653551721792711",
    "7338653551722184919",
    "7338653551721316691",
    "7338653551721718441",
    "7338653551721708091",
    "7338653551721336331",
    "7338653551721395681",
    "7338653551721744821",
    "7338653551721747291",
    "7338653551721519621",
    "7338653551721317731",
    "7338653551721735291",
    "7338653551721440301",
    "7338653551721720481",
    "7338653551721747361",
    "7338653551721321171",
    "7338653551721185382",
    "7338653551721317771",
    "7338653551721816691",
    "7338653551721418461",
    "7338653551721521621",
    "7338653551721324681",
    "7338653551721426851",
    "7338653551721293891",
    "7338653551721747341",
    "7338653551721421691",
    "7338653551721741171",
    "7338653551721326391",
    "7338653551721287931",
    "7338653551721325121",
    "7338653551721708821",
    "7338653551721715511",
    "7338653551721641311",
    "7338653551721816431",
    "7338653551721401091",
    "7338653551721740901",
    "7338653551721185297",
    "7338653551721515981",
    "7338653551721820941",
    "7338653551721816581",
    "7338653551721421851",
    "7338653551721437351",
    "7338653551721685441",
    "7338653551721294381",
    "7338653551721739091",
    "7338653551721322551",
    "7338653551721822251",
    "7338653551721519291",
    "7338653551721294351",
    "7338653551721428621",
    "7338653551721743611",
    "7338653551721326961",
    "7338653551721326091",
    "7338653551721739371",
    "7338653551721440961",
    "7338653551721794651",
    "7338653551721426781",
    "7338653551721536171",
    "7338653551721294041",
    "7338653551721311291",
    "7338653551721431841",
    "7338653551721186992",
    "7338653551721296661",
    "7338653551721326411",
    "7338653551721185372",
    "7338653551721294481",
    "7338653551721794871",
    "7338653551721495481",
    "7338653551721821911",
    "7338653551721709191",
    "7338653551721429331",
    "7338653551721285991",
    "7338653551721740331",
    "7338653551721792811",
    "7338653551721317311",
    "7338653551721289841",
    "7338653551721816481",
    "7338653551721428361",
}

stops_on_220 = [
    Stop(
        "7338653551722184832",
        "Ovens (Grange Road Terminus)",
        51.87648,
        -8.64687,
        246671,
    ),
    Stop("7338653551722184836", "Ovens (Opp Grange Manor)", 51.87303, -8.64554, 246681),
    Stop(
        "7338653551722184834",
        "Killumney Road (Kilumney Cross)",
        51.87273,
        -8.64505,
        246691,
    ),
    Stop("7338653551721431071", "Ovens (EMC Terminus)", 51.87687, -8.63864, 245791),
    Stop(
        "7338653551721484641",
        "Ballincollig West (Classes Lake)",
        51.88184,
        -8.62694,
        299361,
    ),
    Stop(
        "7338653551721429551",
        "Ballincollig West (Opp Aylsbury Estate)",
        51.88377,
        -8.62097,
        244271,
    ),
    Stop(
        "7338653551721431091",
        "Ballincollig West (Opp Old Quarry)",
        51.88582,
        -8.61717,
        245811,
    ),
    Stop(
        "7338653551721431081",
        "Ballincollig West (Opp Coolroe Heights)",
        51.8858,
        -8.61353,
        245801,
    ),
    Stop(
        "7338653551721429561",
        "Ballincollig West (Op White Horse Bar)",
        51.88628,
        -8.60814,
        244281,
    ),
    Stop(
        "7338653551721417761",
        "Ballincollig (Opp Jctn Barrys Road)",
        51.88666,
        -8.60465,
        232481,
    ),
    Stop(
        "7338653551721429531",
        "Ballincollig (Shopping Centre)",
        51.88801,
        -8.59634,
        244251,
    ),
    Stop(
        "7338653551721429571",
        "Ballincollig Town Centre (Garda St)",
        51.88807,
        -8.59077,
        244291,
    ),
    Stop("7338653551721429581", "Ballincollig (East Gate)", 51.88872, -8.58343, 244301),
    Stop(
        "7338653551721429591",
        "Ballincollig (Opp Rosewood Est)",
        51.88996,
        -8.57499,
        244311,
    ),
    Stop(
        "7338653551721429601",
        "Model Farm Rd (Guide Dog Centre)",
        51.8923,
        -8.56321,
        244321,
    ),
    Stop(
        "7338653551721429611",
        "Model Farm Rd (Inchaggin Eastbound)",
        51.89197,
        -8.54919,
        244331,
    ),
    Stop(
        "7338653551721431721", "Model Farm Road (Eden Hall)", 51.88993, -8.53861, 246441
    ),
    Stop(
        "7338653551721427141",
        "Model Farm Rd (Opp Ultralase Ireland)",
        51.88892,
        -8.53033,
        241861,
    ),
    Stop(
        "7338653551721418811",
        "Model Farm Rd (IDA Technology Park)",
        51.88887,
        -8.52555,
        233531,
    ),
    Stop(
        "7338653551721427181",
        "Model Farm Rd (Dept of Agriculture)",
        51.88896,
        -8.51953,
        241901,
    ),
    Stop(
        "7338653551721427161",
        "Model Farm Road (Farranlea Park)",
        51.88845,
        -8.5149,
        241881,
    ),
    Stop(
        "7338653551721427201",
        "Model Farm Rd (Bishopstown Park)",
        51.88879,
        -8.50994,
        241921,
    ),
    Stop(
        "7338653551722184417",
        "Model Farm Rd (Dennehy's Cross Jctn)",
        51.88896,
        -8.50781,
        241911,
    ),
    Stop(
        "7338653551721425361",
        "Dennehy's Cross (Opp Cork Farm Ctr)",
        51.89009,
        -8.50677,
        240081,
    ),
    Stop(
        "7338653551722184416",
        "Victoria Cross (Victoria Lodge)",
        51.89205,
        -8.50618,
        240091,
    ),
    Stop(
        "7338653551721425381",
        "Western Rd (Opp UCC Western Gateway)",
        51.89364,
        -8.50033,
        240101,
    ),
    Stop(
        "7338653551721425391",
        "Western Rd (Opp UCC Castlewhite)",
        51.8942,
        -8.49751,
        240111,
    ),
    Stop(
        "7338653551721440371", "Western Road (Gaol Crossl)", 51.89472, -8.49465, 255091
    ),
    Stop(
        "7338653551721425401",
        "Western Road (Opp University College Gat",
        51.89541,
        -8.49066,
        240121,
    ),
    Stop(
        "7338653551721425411",
        "Mardyke Walk (St. Joseph's School)",
        51.89666,
        -8.48793,
        240131,
    ),
    Stop(
        "7338653551721425421",
        "Mardyke (Presentation College)",
        51.89727,
        -8.48476,
        240141,
    ),
    Stop(
        "7338653551721425961",
        "Sheares Street (Mercy Hospital)",
        51.89828,
        -8.4806,
        240681,
    ),
    Stop(
        "7338653551722184421",
        "Grand Parade (Caseys Furniture)",
        51.89668,
        -8.47456,
        241481,
    ),
    Stop(
        "7338653551721427331",
        "South Mall (Opp Cork Passport Office)",
        51.89739,
        -8.46861,
        242051,
    ),
    Stop("7338653551721436121", "Cork City Hall", 51.89639, -8.46591, 250841),
    Stop(
        "7338653551721426501",
        "Southern Rd (Opp Owl Printers)",
        51.89223,
        -8.46564,
        241221,
    ),
    Stop(
        "7338653551721426511",
        "Douglas Road (Opp St Finbarrs Hospital)",
        51.89013,
        -8.46207,
        241231,
    ),
    Stop(
        "7338653551721426521",
        "Douglas Road (Glengesh Bellair)",
        51.88859,
        -8.45775,
        241241,
    ),
    Stop(
        "7338653551721421251",
        "Douglas Road (Cross Douglas Rd Jctn)",
        51.88727,
        -8.45495,
        235971,
    ),
    Stop(
        "7338653551721426531",
        "Douglas Road (Before Woolharra Park)",
        51.88586,
        -8.4521,
        241251,
    ),
    Stop(
        "7338653551721426541",
        "Douglas Road (Ardfallen Shopping Mall)",
        51.88397,
        -8.44832,
        241261,
    ),
    Stop(
        "7338653551721426551",
        "Douglas Road (Endsleigh Estate)",
        51.88157,
        -8.44355,
        241271,
    ),
    Stop(
        id="7338653551721426561",
        name="Douglas Road (Clermont Ave)",
        latitude=51.88033,
        longitude=-8.44087,
        number=241281,
    ),
    Stop(
        id="7338653551721417221",
        name="Douglas East Village (Opp Tramway Tce)",
        latitude=51.87706,
        longitude=-8.43554,
        number=231941,
    ),
    Stop(
        id="7338653551721430251",
        name="Maryborough Hill (Op The Paddocks)",
        latitude=51.87423,
        longitude=-8.42505,
        number=244971,
    ),
    Stop(
        id="7338653551721432261",
        name="Maryborough Hill (Hotel and Spa)",
        latitude=51.87258,
        longitude=-8.42216,
        number=246981,
    ),
    Stop(
        id="7338653551721430601",
        name="Maryborough Hill (Lissadell Southbound)",
        latitude=51.86906,
        longitude=-8.41722,
        number=245321,
    ),
    Stop(
        id="7338653551721430611",
        name="Maryborough Hill (Broadale Southbound)",
        latitude=51.86417,
        longitude=-8.41308,
        number=245331,
    ),
    Stop(
        id="7338653551721431101",
        name="Maryborough Hill (Hilltown Southbound)",
        latitude=51.84916,
        longitude=-8.39799,
        number=245821,
    ),
    Stop(
        id="7338653551721419241",
        name="Carrigaline (Opp Carrignacurra)",
        latitude=51.82798,
        longitude=-8.39605,
        number=233961,
    ),
    Stop(
        id="7338653551721430261",
        name="Carrigaline (Herons Wood)",
        latitude=51.82433,
        longitude=-8.39453,
        number=244981,
    ),
    Stop(
        id="7338653551721430291",
        name="Carrigaline (Opp Glenview)",
        latitude=51.82086,
        longitude=-8.39228,
        number=245011,
    ),
    Stop(
        id="7338653551721430301",
        name="Carrigaline (Cork Rd LyndenDental)",
        latitude=51.81801,
        longitude=-8.39146,
        number=245021,
    ),
    Stop(
        id="7338653551721430311",
        name="Carrigaline (Church)",
        latitude=51.81593,
        longitude=-8.39142,
        number=245031,
    ),
    Stop(
        id="7338653551721416751",
        name="Carrigaline (Town Ctr Bridge Southbound)",
        latitude=51.81345,
        longitude=-8.39233,
        number=231471,
    ),
    Stop(
        id="7338653551721417941",
        name="Carrigaline (Lr Kilmoney Opp Serv Statio",
        latitude=51.81156,
        longitude=-8.39462,
        number=232661,
    ),
    Stop(
        id="7338653551721430321",
        name="Carrigaline (Lr Kilmoney Abbey View)",
        latitude=51.81111,
        longitude=-8.40109,
        number=245041,
    ),
    Stop(
        id="7338653551721430331",
        name="Carrigaline (Lr Kilmoney Clevedon)",
        latitude=51.81073,
        longitude=-8.40376,
        number=245051,
    ),
    Stop(
        id="7338653551721430341",
        name="Carrigaline (Uppr Kilmoney Forest Pk)",
        latitude=51.80642,
        longitude=-8.40409,
        number=245061,
    ),
    Stop(
        id="7338653551721430351",
        name="Carrigaline (Uppr Kilmoney Clevedon)",
        latitude=51.80773,
        longitude=-8.40126,
        number=245071,
    ),
    Stop(
        id="7338653551721418091",
        name="Carrigaline (Liosbourne)",
        latitude=51.80883,
        longitude=-8.39741,
        number=232811,
    ),
    Stop(
        id="7338653551721431151",
        name="Carrigaline (Ferney Road)",
        latitude=51.80877,
        longitude=-8.39143,
        number=245871,
    ),
    Stop(
        id="7338653551721431991",
        name="Carrigaline (Forrest Hills)",
        latitude=51.8084,
        longitude=-8.38483,
        number=246711,
    ),
    None,
    Stop(
        id="7338653551721418971",
        name="Kilnagleary Rd (O Learys Cross Southboun",
        latitude=51.80973,
        longitude=-8.35985,
        number=233691,
    ),
    Stop(
        id="7338653551721430361",
        name="Crosshaven (Yacht Club Southbound)",
        latitude=51.80348,
        longitude=-8.3072,
        number=245081,
    ),
    Stop(
        id="7338653551721430371",
        name="Crosshaven (Opp The Grand Apts)",
        latitude=51.80429,
        longitude=-8.30224,
        number=245091,
    ),
    Stop(
        id="7338653551721430381",
        name="Crosshaven (Opp Buckleys Pub)",
        latitude=51.8038,
        longitude=-8.29691,
        number=245101,
    ),
    Stop(
        id="7338653551721417121",
        name="Crosshaven (Village Ctr Southbound)",
        latitude=51.80266,
        longitude=-8.2961,
        number=231841,
    ),
    Stop(
        id="7338653551721431191",
        name="Camden Road (Upper)",
        latitude=51.80707,
        longitude=-8.28837,
        number=245911,
    ),
    Stop(
        id="7338653551721417391",
        name="Fort Camden",
        latitude=51.8096,
        longitude=-8.28123,
        number=232111,
    ),
]
