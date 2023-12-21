import numpy as np
import pandas as pd
import os
folder_path = os.getcwd()
df = pd.read_csv(folder_path+"/data.csv", delimiter=";", decimal=",")


msg = """
Vid prissättning av skadeförsäkring är Generalized Linear Models (GLM) ett vanligt verktyg.
GLM ger ett sätt att bestämma en tariff där det på ett kvantitativt sätt går att räkna ut
premien för olika kategorier av försäkringstagare. Man passar en sannolikhetsfördelning
dels till skadefrekvensen, dels till väntevärdet på en skada, och räknar sedan ut tariffen
baserat på detta.

I det aktuella fallet har vi dels väldigt få datapunkter, så det är inte meningsfullt att
försöka passa någon sannolikhetsfördelning till datan. Vi har heller ingen information om
våra försäkringstagare, så det finns ingen indelning i kategorier att tala om. Jag väljer
därför att göra en betydligt enklare analys än så.

Vi tittar först på några grundläggande insikter utifrån vårt dataset. Jag har här valt att
endast presentera nollskilda skador, dvs skador där vi faktiskt betalade ut något till
försäkringstagaren. Det är ett vanligt antagande att göra, men det går bra att följa vilken
konvention man vill så länge man är konsekvent.

"""
print(msg)

claims = {}
means = {}
claims_percentages = {}
years = [2018, 2019, 2020, 2021]
vehicles = {2018: 1, 2019: 2, 2020: 87, 2021: 100}

for year in years:
    # Masks för att plocka ut nollskilda skador från varje år i datan.
    year_mask = df["year"] == year
    claims_mask = np.logical_and(year_mask, df["claim"] > 0)
    claims[year] = np.array(df.loc[claims_mask, "claim"])
    # Räkna ut medelvärde och antal skador som procent av  för de olika åren
    means[year] = np.mean(claims[year]).astype(int)
    claims_percentages[year] = round(len(claims[year])/vehicles[year]*100, 2)

    msg = f"År: {year}\n"
    msg += f"Medelvärde nollskilda skador: {means[year]}\n"
    msg += f"Antal nollskilda skador: {len(claims[year])}\n"
    msg += f"Antal fordon: {vehicles[year]}\n"
    msg += f"Nollskilda skador som procent av antal fordon: {claims_percentages[year]}\n"
    msg += f"Total skadekostnad: {int(sum(claims[year]))}\n"
    print(msg)

msg = f"""
Jag bedömer att det bara är 2020 och 2021 som över huvud taget är meningsfulla att titta på
i vår analys, i och med att det bara fanns 1 respektive 2 försäkrade fordon under 2018 och
2019. Jag antar också att de fordon som är försäkrade ett år är oberoende från de fordon som
är försäkrade nästa år.

Nollskilda skador som procent av antal fordon låg på ca {int(claims_percentages[2020])}% år 2020 och ca {int(claims_percentages[2021])}% år 2021, så
jag antar att det fortsätter så även under 2022. Uppskattningsvis blir alltså antalet
nollskilda skador år 2022 totalt 17 st.


Medelvärdet för nollskilda skador var {int(means[2020])} SEK/skada 2020 och {int(means[2021])} SEK/skada 2021. Med mer
data skulle vi kunna försöka passa en sannolikhetsfördelning till skadebeloppen, men med så
få datapunkter bedömer jag att det inte är någon idé. Jag gör istället ett antagande om 
16 000 SEK/skada för 2022, baserat på det större medelvärdet från 2020, och då uppgår 
den totala skadekostnaden för 2022 till 17 * 16 000 = 272 000 SEK. 

Mitt resonemang ovan är förstås en grov uppskattning, kanske till och med godtyckligt, och
skulle helst underbyggas med mer data och analys än vad jag har möjlighet till här, men
poängen är följande: Om vi erbjuder en premie på 395 000 SEK för 100 fordon har vi fortfarande
en mycket stor säkerhetsmarginal -- skadekostnaden skulle behöva bli nästan {int(round((395000/(17*16000)-1)*100, -1))}% större än
uppskattat för att vi ska gå med förlust.

Givet att skadekostnaden inte skjuter i höjden gör vi en god vinst på affären med denna
premie, och det ger oss dessutom en konkurrensfördel mot vår närmaste konkurrent som
sannolikt skulle kunna leda till att vi ökade vår försäljning.

Det är samtidigt viktigt att beakta risken för att vi attraherar högriskkunder om vi sätter
vårt pris för lågt. Vi kan potentiellt göra en kortsiktig vinst genom att ta ut en låg premie,
men det föreligger samtidigt en risk för att vi långsiktigt gör en förlust på utbetalningar
för skador till högriskkunder. Jag bedömer inte att den information jag har tillgång till är
tillräcklig för att göra en kvantitativ bedömning av denna risk, men i ett verkligt scenario
är det något vi skulle behöva ta i beaktande, och potentiellt söka upp mer data om våra
kunder innan vi fattar ett beslut.

Jag bedömer att det inte är relevant att ta hänsyn till inflation i den här analysen. Vi har
alldeles för lite data och för stor osäkerhet i uppskattningarna för att det ska vara rimligt att
påstå att en inflationsjustering av storleksordningen 395 000 * 0,02 = 7 900 SEK har tagits 
med i beräkningen.

Sammanfattning:
-- Baserat på att andelen nollskilda skador var ca 17% av antalet fordon både 2020 och
   2021 uppskattar jag att det kommer in 17 nollskilda skador 2022.
-- Utgår vi från det högre av de senaste två årens medelvärden för nollskilda skadebelopp
   kan vi uppskatta att den totala skadekostnaden för 2022 uppgår till ett belopp av ca
   272 000 SEK.
-- Om vi erbjuder premien 395 000 för 100 fordon har vi en säkerhetsmarginal på nästan
   50% relativt den uppskattade skadekostnaden. Det ger oss dessutom en konkurrensfördel
   gentemot vår närmaste konkurrent.
-- I ett verkligt scenario hade man behövt väga det potentiella inflöde av nya kunder som
   en lägre premie skulle medföra emot risken att attrahera högriskkunder.
-- Den knappa mängden data och de stora osäkerheter i uppskattningar som det medför gör
   att inflation inte är relevant att ta hänsyn till i den här analysen.
"""

print(msg)
