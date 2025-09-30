const storeList = [
  {
    "type": "Feature",
    "geometry": { "type": "Point", "coordinates": [73.8689, 18.6743] },
    "properties": {
      "name": "Tata Motors – Pimpri MIDC",
      "address": "Pimpri MIDC, Pune, Maharashtra",
      "sector": "Automobile Manufacturing",
      "category": "Automobile",
      "phone": "+91 20 1234 5678",
      "website": "https://www.tatamotors.com"
    }
  },
  {
    "type": "Feature",
    "geometry": { "type": "Point", "coordinates": [73.8493, 18.6633] },
    "properties": {
      "name": "Bajaj Auto – Akurdi",
      "address": "Akurdi MIDC, Pune, Maharashtra",
      "sector": "Two-Wheeler Manufacturing",
      "category": "Automobile",
      "phone": "+91 20 2345 6789",
      "website": "https://www.bajajauto.com"
    }
  },
  {
    "type": "Feature",
    "geometry": { "type": "Point", "coordinates": [73.8010, 18.6169] },
    "properties": {
      "name": "Mercedes-Benz India – Chakan",
      "address": "Chakan MIDC, Pune, Maharashtra",
      "sector": "Luxury Automobile",
      "category": "Automobile",
      "phone": "+91 20 3456 7890",
      "website": "https://www.mercedes-benz.co.in"
    }
  },
  {
    "type": "Feature",
    "geometry": { "type": "Point", "coordinates": [73.8122, 18.6235] },
    "properties": {
      "name": "Volkswagen India – Chakan",
      "address": "Chakan Industrial Area, Pune, Maharashtra",
      "sector": "Automobile",
      "category": "Automobile",
      "phone": "+91 20 9876 5432",
      "website": "https://www.volkswagen.co.in"
    }
  },
  {
    "type": "Feature",
    "geometry": { "type": "Point", "coordinates": [73.8365, 18.6711] },
    "properties": {
      "name": "JCB India – Talegaon",
      "address": "Talegaon MIDC, Pune, Maharashtra",
      "sector": "Construction Equipment",
      "category": "Construction",
      "phone": "+91 20 1111 2222",
      "website": "https://www.jcb.com/en-in"
    }
  },
  {
    "type": "Feature",
    "geometry": { "type": "Point", "coordinates": [73.7583, 18.7322] },
    "properties": {
      "name": "General Motors Technical Center",
      "address": "Hinjewadi Phase 3, Pune, Maharashtra",
      "sector": "Automobile R&D",
      "category": "Automobile",
      "phone": "+91 20 8765 4321",
      "website": "https://www.gm.com"
    }
  },
  {
    "type": "Feature",
    "geometry": { "type": "Point", "coordinates": [73.6856, 18.5921] },
    "properties": {
      "name": "LG Electronics – Ranjangaon",
      "address": "Ranjangaon MIDC, Shirur, Pune",
      "sector": "Electronics & Appliances",
      "category": "Electronics",
      "phone": "+91 20 2222 3333",
      "website": "https://www.lg.com/in"
    }
  },
  {
    "type": "Feature",
    "geometry": { "type": "Point", "coordinates": [73.7002, 18.6134] },
    "properties": {
      "name": "Tata Steel Processing – Ranjangaon",
      "address": "Ranjangaon MIDC, Pune",
      "sector": "Steel Processing",
      "category": "Metals & Steel",
      "phone": "+91 20 4444 5555",
      "website": "https://www.tatasteel.com"
    }
  },
  {
    "type": "Feature",
    "geometry": { "type": "Point", "coordinates": [73.8329, 18.6504] },
    "properties": {
      "name": "SKF Bearings – Chinchwad",
      "address": "Chinchwad MIDC, Pune",
      "sector": "Engineering & Bearings",
      "category": "Engineering",
      "phone": "+91 20 6666 7777",
      "website": "https://www.skf.com/in"
    }
  },
  {
    "type": "Feature",
    "geometry": { "type": "Point", "coordinates": [73.8448, 18.6392] },
    "properties": {
      "name": "Forbes Marshall – Kasarwadi",
      "address": "Kasarwadi, MIDC Pimpri, Pune",
      "sector": "Steam Engineering & Controls",
      "category": "Engineering",
      "phone": "+91 20 9999 8888",
      "website": "https://www.forbesmarshall.com"
    }
  },
  {
    "type": "Feature",
    "geometry": { "type": "Point", "coordinates": [73.7844, 18.6511] },
    "properties": {
      "name": "Sandvik Asia – Dapodi",
      "address": "Dapodi, Pune",
      "sector": "Engineering Solutions",
      "category": "Engineering",
      "phone": "+91 20 1357 2468",
      "website": "https://www.home.sandvik"
    }
  },
  {
    "type": "Feature",
    "geometry": { "type": "Point", "coordinates": [73.8612, 18.6342] },
    "properties": {
      "name": "KSB Pumps – Pimpri",
      "address": "Pimpri MIDC, Pune",
      "sector": "Pumps & Valves",
      "category": "Engineering",
      "phone": "+91 20 9870 6543",
      "website": "https://www.ksb.com/ksb-in"
    }
  },
  {
    "type": "Feature",
    "geometry": { "type": "Point", "coordinates": [73.8135, 18.5432] },
    "properties": {
      "name": "Cummins India – Kothrud",
      "address": "Kothrud, Pune",
      "sector": "Engines & Power Systems",
      "category": "Automobile",
      "phone": "+91 20 2468 1357",
      "website": "https://www.cummins.com"
    }
  },
  {
    "type": "Feature",
    "geometry": { "type": "Point", "coordinates": [73.9045, 18.6598] },
    "properties": {
      "name": "Atlas Copco – Dapodi",
      "address": "Dapodi, Pune",
      "sector": "Industrial Tools & Equipment",
      "category": "Engineering",
      "phone": "+91 20 5432 6789",
      "website": "https://www.atlascopco.com/en-in"
    }
  },
  {
    "type": "Feature",
    "geometry": { "type": "Point", "coordinates": [73.8756, 18.5672] },
    "properties": {
      "name": "Thermax – Ranjangaon",
      "address": "Ranjangaon MIDC, Pune",
      "sector": "Energy & Environment",
      "category": "Energy",
      "phone": "+91 20 1122 3344",
      "website": "https://www.thermaxglobal.com"
    }
  }
];
