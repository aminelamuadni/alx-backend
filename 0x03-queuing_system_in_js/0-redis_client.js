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
