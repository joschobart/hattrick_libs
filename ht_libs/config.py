""" ht_libs constants. """


from os import environ

OAUTH_KEY = environ["HATTRICK_OAUTH_CONSUMER_KEY"]
OAUTH_SECRET = environ["HATTRICK_OAUTH_CONSUMER_SECRET"]


REQUEST_TOKEN_URL = "https://chpp.hattrick.org/oauth/request_token.ashx"
ACCESS_TOKEN_URL = "https://chpp.hattrick.org/oauth/access_token.ashx"
AUTHORIZE_URL = "https://chpp.hattrick.org/oauth/authorize.aspx"
BASE_URL = "https://chpp.hattrick.org/chppxml.ashx"
TOKEN_STATUS_URL = "https://chpp.hattrick.org/oauth/check_token.ashx"


ALL_FLAGS = [
    ["128", "Iraq", "IQ"],
    ["127", "Kuwait", "KW"],
    ["77", "Morocco", "MA"],
    ["106", "Jordan", "JO"],
    ["133", "Yemen", "YE"],
    ["118", "Algeria", "DZ"],
    ["105", "Andorra", "AD"],
    ["130", "Angola", "AO"],
    ["7", "Argentina", "AR"],
    ["129", "Azerbaijan", "AZ"],
    ["123", "Bahrain", "BH"],
    ["132", "Bangladesh", "BD"],
    ["124", "Barbados", "BB"],
    ["91", "Belarus", "BY"],
    ["44", "Belgium", "BE"],
    ["158", "Belize", "BZ"],
    ["139", "Benin", "BJ"],
    ["74", "Bolivia", "BO"],
    ["69", "Bosnia and Herzegovina", "BA"],
    ["160", "Botswana", "BW"],
    ["16", "Brazil", "BR"],
    ["136", "Brunei", "BN"],
    ["62", "Bulgaria", "BG"],
    ["167", "Burkina Faso", "BF"],
    ["125", "Cape Verde", "CV"],
    ["146", "Cameroon", "CM"],
    ["17", "Canada", "CA"],
    ["52", "Czech Republic", "CZ"],
    ["18", "Chile", "CL"],
    ["34", "People's Republic of China", "CN"],
    ["60", "Chinese Taipei", "TW"],
    ["19", "Colombia", "CO"],
    ["151", "Comoros", "KM"],
    ["81", "Costa Rica", "CR"],
    ["126", "Côte d’Ivoire", "CI"],
    ["131", "Montenegro", "ME"],
    ["147", "Cuba", "CU"],
    ["153", "Curaçao", "CW"],
    ["61", "Wales", "GB"],
    ["89", "Cyprus", "CY"],
    ["11", "Denmark", "DK"],
    ["141", "Qatar", "QA"],
    ["3", "Germany", "DE"],
    ["144", "Maldives", "MV"],
    ["73", "Ecuador", "EC"],
    ["56", "Estonia", "EE"],
    ["100", "El Salvador", "SV"],
    ["2", "England", "GB"],
    ["36", "Spain", "ES"],
    ["76", "Faroe Islands", "FO"],
    ["5", "France", "FR"],
    ["137", "Ghana", "GH"],
    ["166", "Grenada", "GD"],
    ["154", "Guam", "GU"],
    ["107", "Guatemala", "GT"],
    ["164", "Haiti", "HT"],
    ["30", "South Korea", "KR"],
    ["122", "Armenia", "AM"],
    ["50", "Greece", "GR"],
    ["99", "Honduras", "HN"],
    ["59", "Hong Kong", "HK"],
    ["58", "Croatia", "HR"],
    ["20", "India", "IN"],
    ["54", "Indonesia", "ID"],
    ["85", "Iran", "IR"],
    ["21", "Ireland", "IE"],
    ["38", "Iceland", "IS"],
    ["63", "Israel", "IL"],
    ["4", "Italy", "IT"],
    ["156", "Ethiopia", "ET"],
    ["94", "Jamaica", "JM"],
    ["138", "Cambodia", "KH"],
    ["112", "Kazakhstan", "KZ"],
    ["95", "Kenya", "KE"],
    ["102", "Kyrgyzstan", "KG"],
    ["53", "Latvia", "LV"],
    ["84", "Luxembourg", "LU"],
    ["117", "Liechtenstein", "LI"],
    ["66", "Lithuania", "LT"],
    ["120", "Lebanon", "LB"],
    ["159", "Madagascar", "MG"],
    ["51", "Hungary", "HU"],
    ["45", "Malaysia", "MY"],
    ["101", "Malta", "MT"],
    ["6", "Mexico", "MX"],
    ["33", "Egypt", "EG"],
    ["135", "Mozambique", "MZ"],
    ["103", "Moldova", "MD"],
    ["119", "Mongolia", "MN"],
    ["161", "Myanmar", "MM"],
    ["14", "Netherlands", "NL"],
    ["168", "Nepal", "NP"],
    ["111", "Nicaragua", "NI"],
    ["75", "Nigeria", "NG"],
    ["22", "Japan", "JP"],
    ["9", "Norway", "NO"],
    ["93", "Northern Ireland", "GB"],
    ["145", "Uzbekistan", "UZ"],
    ["15", "Oceania", "AU"],
    ["134", "Oman", "OM"],
    ["39", "Austria", "AT"],
    ["71", "Pakistan", "PK"],
    ["148", "Palestine", "PS"],
    ["96", "Panama", "PA"],
    ["72", "Paraguay", "PY"],
    ["23", "Peru", "PE"],
    ["55", "Philippines", "PH"],
    ["24", "Poland", "PL"],
    ["25", "Portugal", "PT"],
    ["31", "Thailand", "TH"],
    ["165", "Puerto Rico", "PR"],
    ["155", "DR Congo", "CD"],
    ["88", "Dominican Republic", "DO"],
    ["37", "Romania", "RO"],
    ["35", "Russia", "RU"],
    ["157", "Saint Vincent and the Grenadines", "VC"],
    ["104", "Georgia", "GE"],
    ["163", "San Marino", "SM"],
    ["149", "São Tomé e Príncipe", "ST"],
    ["79", "Saudi Arabia", "SA"],
    ["46", "Switzerland", "CH"],
    ["26", "Scotland", "GB"],
    ["121", "Senegal", "SN"],
    ["97", "North Macedonia", "MK"],
    ["98", "Albania", "AL"],
    ["47", "Singapore", "SG"],
    ["64", "Slovenia", "SI"],
    ["67", "Slovakia", "SK"],
    ["27", "South Africa", "ZA"],
    ["57", "Serbia", "RS"],
    ["152", "Sri Lanka", "LK"],
    ["12", "Finland", "FI"],
    ["113", "Suriname", "SR"],
    ["140", "Syria", "SY"],
    ["1", "Sweden", "SE"],
    ["142", "Tanzania", "TZ"],
    ["80", "Tunisia", "TN"],
    ["110", "Trinidad & Tobago", "TT"],
    ["32", "Turkey", "TR"],
    ["143", "Uganda", "UG"],
    ["68", "Ukraine", "UA"],
    ["83", "United Arab Emirates", "AE"],
    ["28", "Uruguay", "UY"],
    ["8", "USA", "US"],
    ["29", "Venezuela", "VE"],
    ["70", "Vietnam", "VN"],
    ["162", "Zambia", "ZM"],
    ["169", "Guyana", "GY"],
    ["170", "Tahiti", "PF"],
    ["171", "Guinea", "GN"],
]
