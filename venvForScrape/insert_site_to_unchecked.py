import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('website_leads.db')
cur = conn.cursor()

# List of websites to be inserted
sites = [
"https://www.adultloveboutiquesm.com/%3Futm_source%3Dgoogle%26utm_medium%3Dgmb%26utm_campaign%3Dseo",
"https://locations.loversstores.com/ca/culver-city/5901-s-sepulveda-blvd/",
"http://romanceattack.biz/",
"http://broadwayerotic.com/",
"https://locations.loversstores.com/ca/cerritos/11332-south-st/",
"https://locations.loversstores.com/ca/brea/690-e-imperial-hwy/",
"http://suzies.com/",
"https://goldendreams1.com/",
"http://suzies.com/",
"http://suzies.com/",
"http://cupidscloset.com/",
"http://www.adultwarehouseoutlet.com/",
"http://www.thelovestore.com/",
"http://naughty-or-nice-boutique.mybigcommerce.com/login.php",
"http://suzies.com/",
"https://www.romantix.com/s/",
"http://toyboxupland.com/",
"http://they-not.com/",
"http://www.spankysonline.com/",
"http://diamondadult.com/",
"http://www.andysadultworld.com/",
"http://amorsexstore.com/",
"https://exoticzoneshop.com/",
"http://amorlingerie.com/",
"https://shop-camouflage.com/",
"https://secretsloveboutique.com/",
"http://suzies.com/",
"https://www.temporarysatisfaction.com/",
"http://www.secretsboutiques.com/",
"https://cupidscloset.com/",
"https://www.goodvibes.com/s/content/c/Good-Vibes-Store-Locations",
"http://www.redhotthrillz.com/",
"https://www.romantix.com/s/",
"http://suzies.com/",
"http://funzonelancaster.com/",
"http://www.couplesmo.com/",
"http://adultfactoryoutlet.com/",
"http://wildwillysworld.com/",
"http://www.adultmegastores.com/",
"http://www.secretsboutiques.com/",
"http://www.myexclusivetouch.com/",
"http://www.secretsboutiques.com/",
"http://www.excitementgirl.net/",
"http://www.secretsboutiques.com/",
"http://www.secretsboutiques.com/",
"http://passioncityadult.com/",
"http://www.secretsboutiques.com/",
"http://suzies.com/",
"https://spearmintrhinosuperstore.com/",
"http://www.goodvibes.com/",
"https://loversoutlet.business.site/",
"http://secretsboutiques.com/",
"http://adultemporiumsd.com/",
"http://suzies.com/",
"https://www.instagram.com/adultvec",
"http://www.secretsboutiques.com/",
"http://www.couplesmo.com/",
"http://roysadultfantasy.com/",
"https://thelovestore.com/",
"http://www.diamondadult.com/",
"http://www.secretsboutiques.com/",
"http://www.secretsboutiques.com/",
"http://www.xxxpleasureisland.net/",
"http://www.oohlalamonterey.com/",
"http://www.ghettoff.com/",
"http://www.suzies.com/",
"https://naughty-adult-store.business.site/%3Futm_source%3Dgmb%26utm_medium%3Dreferral",
"https://dr-loves-outlet.business.site/%3Futm_source%3Dgmb%26utm_medium%3Dreferral",
"http://suzies.com/",
"https://www.secretsboutiques.com/",
"http://www.secretsboutiques.com/",
"http://www.secretsboutiques.com/",
"http://e-tique.org/",
"https://drlovesoutlet.business.site/%3Futm_source%3Dgmb%26utm_medium%3Dreferral",
"http://feelmore510.com/",
"http://suzies.com/",
"http://www.adultmegastores.com/",
"http://www.goodvibes.com/",
"http://www.blackcocktoys.com/",
"https://adultys.com/",
"https://intimatedesiresadult.com/",
"https://sextcstore.com/?utm_campaign=gmb"
]

# Prepare the SQL statement for inserting data
sql = "INSERT INTO urls_to_check (website) VALUES (?)"

# Insert each site into the database
for site in sites:
    cur.execute(sql, (site,))

# Commit the changes
conn.commit()

# Close the connection
conn.close()