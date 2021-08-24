// Set constants
const email = "joe@example.com" // Set the email of the user to grant access
const subdomain = "dev.host" // Set the subdomain for your environment

// Retrieve bearer token from local storage
let bearerToken = null
for (key in localStorage) {
    try {
        const value = JSON.parse(localStorage.getItem(key));
        if (value && value.access_token !== undefined) {
            bearerToken = value.access_token
            break;
        }
    } catch (e) { }
}
if (bearerToken === null) {
    console.error("Missing access token. Are you sure you're logged in?")
}

const baseUrl = `https://api.${subdomain}.commure.com/api/v1/r4`

// Fetch a specific person resource
fetch(`${baseUrl}/Person?telecom=${email}`, {
    method: "GET",
    headers: {
        Authorization: `Bearer ${bearerToken}`,
        "Content-Type": "application/json"
    }
})
    .then(resp => resp.json())
    .then(resp => {
        const persons = resp.entry.map(entry => entry.resource);
        persons.forEach(async person => {
            const personId = person.id;
            const updatedPersonResource = {
                ...person,
                meta: {
                    ...person.meta,
                    tag: [
                        {
                            system: "https://example.com/fhir/app/role",
                            code: "admin"
                        }
                    ]
                }
            };
            const response = fetch(`${baseUrl}/Person/${personId}`, {
                method: "PUT",
                headers: {
                    Authorization: `Bearer ${bearerToken}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(updatedPersonResource)
            })
                .then(resp => resp.json())
                .then(resp => console.log(resp));
        });
    });
