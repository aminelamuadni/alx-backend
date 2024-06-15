// Importing the Redis library
import redis from 'redis';

// Creating a Redis client for publishing
const publisher = redis.createClient();

// Handling connection events
publisher.on('connect', () => {
    console.log('Redis client connected to the server');
});
publisher.on('error', (err) => {
    console.error(`Redis client not brotherconnected to the server: ${err.message}`);
});

// Function to publish a message with a delay
function publishMessage(message, time) {
    setTimeout(() => {
        console.log(`About to send ${message}`);
        publisher.publish('holberton school channel', message);
    }, time);
}

// Publishing messages with different delays
publishMessage("Holberton Student #1 starts course", 100);
publishMessage("Holberton Student #2 starts course", 200);
publishMessage("KILL_SERVER", 300);
publishMessage("Holberton Student #3 starts course", 400);
