// Importing the Redis library
import redis from 'redis';

// Creating a Redis client for subscribing
const subscriber = redis.createClient();

// Handling connection events
subscriber.on('connect', () => {
    console.log('Redis client connected to the server');
});
subscriber.on('error', (err) => {
    console.error(`Redis client not connected to the server: ${err.message}`);
});

// Subscribing to the 'holberton school channel'
subscriber.subscribe('holberton school channel');

// Handling messages on the 'holberton school channel'
subscriber.on('message', (channel, message) => {
    console.log(message);
    if (message === 'KILL_SERVER') {
        subscriber.unsubscribe();
        subscriber.quit();
    }
});
