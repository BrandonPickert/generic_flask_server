// Main JavaScript file
console.log('Generic Flask Server loaded');

// Example API call function
async function fetchAPI(endpoint, options = {}) {
    try {
        const response = await fetch(endpoint, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

// Example usage
// fetchAPI('/api/examples')
//     .then(data => console.log(data))
//     .catch(error => console.error(error));
