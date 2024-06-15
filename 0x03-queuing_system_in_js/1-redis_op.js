// Importing the Redis library
import redis from 'redis';

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

// Function to set a new key-value pair in Redis
function setNewSchool(schoolName, value) {
    client.set(schoolName, value, redis.print);
}

// Function to display the value of a given key
function displaySchoolValue(schoolName) {
    client.get(schoolName, (err, reply) => {
        if (err) {
            console.error(err);
            return;
        }
        console.log(reply);
    });
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');