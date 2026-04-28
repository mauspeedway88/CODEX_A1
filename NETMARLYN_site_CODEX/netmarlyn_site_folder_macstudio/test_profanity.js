const fs = require('fs');

const identity = JSON.parse(fs.readFileSync('/Users/mauricio/ANTIGRAVITY_PROJECTS_folder/NETMARLYN_site_websitefoldermake/netmarlyn_site_folder_macstudio/netmarlyn_website_00/MAUNET_SITE_SS_2/MAUNET_IDENTITY.json', 'utf-8'));

const forbidden = identity.safety_protocols.forbidden_concepts;

const testStrings = [
    "hola como estas , explicame como funcioanlas macisntos computer 126k computadoras viejas",
    "hola como estas , explicame como funcioanlas macisntos computer 126k",
    "computadora macintosh 126k de los 80s",
    "macintosh 126k de los 80s"
];

for (const input of testStrings) {
    const inputLower = input.toLowerCase();
    
    // original logic
    const isForbidden1 = forbidden.some(kw => inputLower.includes(kw));
    const which1 = forbidden.filter(kw => inputLower.includes(kw));
    
    // safe logic
    const safeInputForProfanity = inputLower.replace(/computadora|computacion|computación|disputa|reputacion|reputación|imputar|computar|computo|diputad/g, '');
    const isForbidden2 = forbidden.some(kw => safeInputForProfanity.includes(kw));
    const which2 = forbidden.filter(kw => safeInputForProfanity.includes(kw));
    
    console.log(`\nInput: "${input}"`);
    console.log(`Original: ${isForbidden1} [${which1}]`);
    console.log(`Safe logic: ${isForbidden2} [${which2}]`);
    console.log(`Safe string: "${safeInputForProfanity}"`);
}
