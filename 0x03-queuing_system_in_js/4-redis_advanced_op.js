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

// Function to store multiple field-value pairs in a hash
function setHashValues() {
    const hashKey = 'HolbertonSchools';
    client.hset(hashKey, 'Portland', '50', redis.print);
    client.hset(hashKey, 'Seattle', '80', redis.print);
    client.hset(hashKey, 'New York', '20', redis.print);
    client.hset(hashKey, 'Bogota', '20', redis.print);
    client.hset(hashKey, 'Cali', '40', redis.print);
    client.hset(hashKey, 'Paris', '2', redis.print);

    // After setting all values, retrieve and display the hash
    client.hgetall(hashKey, (err, result) => {
        if (err) {
            console.error(err);
            return;
        }
        console.log(result);
    });
}

// Call the function to perform Redis operations
setHashValues();
