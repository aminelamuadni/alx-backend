const express = require('express');
const { createClient } = require('redis');
const { promisify } = require('util');
const kue = require('kue');

// Initialize Express app
const app = express();
const port = 1245;

// Initialize Redis client
const redisClient = createClient();
const getAsync = promisify(redisClient.get).bind(redisClient);
const setAsync = promisify(redisClient.set).bind(redisClient);

// Initialize Kue queue
const queue = kue.createQueue();

// Initial values
const initialSeats = 50;
let reservationEnabled = true;

// Helper functions
const reserveSeat = async (number) => {
    await setAsync('available_seats', number);
};

const getCurrentAvailableSeats = async () => {
    const seats = await getAsync('available_seats');
    return parseInt(seats);
};

// Set initial available seats
reserveSeat(initialSeats);

// Routes
app.get('/available_seats', async (req, res) => {
    const numberOfAvailableSeats = await getCurrentAvailableSeats();
    res.json({ numberOfAvailableSeats });
});

app.get('/reserve_seat', (req, res) => {
    if (!reservationEnabled) {
        return res.json({ status: "Reservation are blocked" });
    }

    const job = queue.create('reserve_seat').save((err) => {
        if (err) {
            return res.json({ status: "Reservation failed" });
        } else {
            return res.json({ status: "Reservation in process" });
        }
    });

    job.on('complete', () => {
        console.log(`Seat reservation job ${job.id} completed`);
    });

    job.on('failed', (err) => {
        console.log(`Seat reservation job ${job.id} failed: ${err.message}`);
    });
});

app.get('/process', (req, res) => {
    res.json({ status: "Queue processing" });

    queue.process('reserve_seat', async (job, done) => {
        let availableSeats = await getCurrentAvailableSeats();
        if (availableSeats <= 0) {
            reservationEnabled = false;
            return done(new Error('Not enough seats available'));
        }
        availableSeats -= 1;
        await reserveSeat(availableSeats);

        if (availableSeats <= 0) {
            reservationEnabled = false;
        }
        done();
    });
});

// Start the server
app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
});
