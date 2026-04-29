const fs = require('fs');
const identity = JSON.parse(fs.readFileSync('/Users/mauricio/ANTIGRAVITY_PROJECTS_folder/NETMARLYN_site_websitefoldermake/netmarlyn_site_folder_macstudio/netmarlyn_website_00/MAUNET_SITE_SS_2/MAUNET_IDENTITY.json', 'utf-8'));
const forbidden = identity.safety_protocols.forbidden_concepts;

const MEMORY_QUERY_PATTERN = /me dijiste|me hablaste|me contaste de|de qu[eé] (enfermedad|tema|cosa)|cu[aá]l (enfermedad|tema)|despu[eé]s de|hablamos de/i;

const tests = [
    { input: "de que enfermedad sexual te pregunte", shouldBlock: false, reason: "Memory query - should NOT block" },
    { input: "computadora macintosh 126k de los 80s", shouldBlock: false, reason: "Legitimate word - should NOT block" },
    { input: "explicame sobre el sexo de los animales", shouldBlock: true, reason: "Real forbidden content" },
    { input: "eres una puta", shouldBlock: true, reason: "Real insult" },
];

for (const t of tests) {
    const inputLower = t.input.toLowerCase();
    const isLikelyMemoryQuery = MEMORY_QUERY_PATTERN.test(t.input);
    const safeInput = inputLower.replace(/computador\w*|computacion\w*|computación\w*|disput\w*|reputacion\w*|reputación\w*|imputa\w*|diputad\w*/g, '');
    const isForbidden = forbidden.some(kw => safeInput.includes(kw));
    const wouldBlock = isForbidden && !isLikelyMemoryQuery;
    
    const ok = wouldBlock === t.shouldBlock;
    console.log(`${ok ? '✅' : '❌'} "${t.input}"`);
    console.log(`   forbidden=${isForbidden}, memoryQ=${isLikelyMemoryQuery}, wouldBlock=${wouldBlock} (expected ${t.shouldBlock})`);
    console.log(`   ${t.reason}`);
}
