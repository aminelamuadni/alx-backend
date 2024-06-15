// Importing Kue library
import kue from 'kue';

// Create a job queue with Kue
const queue = kue.createQueue();

// Blacklisted phone numbers
const blacklistedNumbers = ['4153518780', '4153518781'];

// Function to send a notification
function sendNotification(phoneNumber, message, job, done) {
    job.progress(0, 100);

    if (blacklistedNumbers.includes(phoneNumber)) {
        return done(new Error(`Phone number ${phoneNumber} is blacklisted`));
    }

    job.progress(50, 100);
    console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
    done();
}

// Process two jobs at a time from the queue 'push_notification_code_2'
queue.process('push_notification_code_2', 2, (job, done) => {
    sendNotification(job.data.phoneNumber, job.data.message, job, done);
});

// Graceful shutdown
process.on('SIGTERM', () => {
    queue.shutdown(5000, (err) => {
        console.log('Shutdown: ', err || 'Kue shutdown');
        process.exit(0);
    });
});
