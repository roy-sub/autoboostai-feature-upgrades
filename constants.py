from urllib.parse import urlparse

EXCLUDE_WORDS = {
    'yelp', 'schema', 'w3', 'gstatic', 'ssl', 'comparis', 'local',
    'instagram', 'reddit', 'medium', 'onedoc', 'medicosearch',
    'doctena', 'inyourpocket', 'facebook', 'amazon', 'dictionary',
    'youtube', 'tiktok', 'google', 'pinterest'
}

EXCLUDE_URLS = [
    "https://www.herold.at", "https://www.firmenabc.at", "https://firmen.wko.at",
    "https://www.karriere.at", "https://www.my-hammer.at", "https://www.willhaben.at",
    "https://www.tripadvisor.de", "https://www.gelbeseiten.de", "https://www.11880.com",
    "https://www.dasoertliche.de", "https://de.indeed.com", "https://www.dastelefonbuch.de",
    "https://www.stepstone.de", "https://www.kleinanzeigen.de", "https://home.meinestadt.de",
    "https://de.wikipedia.org", "https://branchenbuch.meinestadt.de", "https://de.linkedin.com",
    "https://www.firmenabc.com", "https://www.kalaydo.de", "https://www.monster.de",
    "https://www.jobware.de", "https://www.xing.com", "https://www.goyellow.de",
    "https://www.meinestadt.de", "https://www.quoka.de", "https://www.autoscout24.de",
    "https://www.immobilienscout24.de", "https://www.holidaycheck.de",
    "https://www.derstandard.at/marktplatz", "https://www.job.at", "https://www.immowelt.at",
    "https://www.gebrauchtwagen.at", "https://www.urlauburlaub.at", "https://www.jobs.ch",
    "https://www.comparis.ch", "https://www.anibis.ch", "https://www.autoscout24.ch",
    "https://www.immoscout24.ch", "https://www.tutti.ch", "https://www.hotelplan.ch", "https://www.forbes.com"
]

EXCLUDE_DOMAINS = {urlparse(url).netloc.replace('www.', '') for url in EXCLUDE_URLS}
