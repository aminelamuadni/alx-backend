// Importing necessary libraries
import redis from 'redis';
import { promisify } from 'util';

// Creating a Redis client
const client = redis.createClient();

// Listening for the 'connect' event to confirm connection
client.on('connect', () => {
    console.log('Redis client connected to the server');
});

// Handling connection error
client.on('error', (err) => {
    console.error(`Redis client not connected to the server: ${err.message}`);
});

// Promisifying Redis client methods
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Async function to set a new key-value pair in Redis
async function setNewSchool(schoolName, value) {
    try {
        const reply = await setAsync(schoolName, value);
        console.log(`Reply: ${reply}`);
    } catch (err) {
        console.error(err);
    }
}

// Async function to display the value of a given key
async function displaySchoolValue(schoolName) {
    try {
        const value = await getAsync(schoolName);
        console.log(value);
    } catch (err) {
        console.error(err);
    }
}

// Executing functions in sequence using async/await
async function runOperations() {
    await displaySchoolValue('Holberton');
    await setNewSchool('HolbertonSanFrancisco', '100');
    await displaySchoolValue('HolbertonSanFrancisco');
}

runOperations();
