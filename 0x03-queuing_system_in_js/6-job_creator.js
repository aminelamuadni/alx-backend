// Importing Kue library
import kue from 'kue';

// Creating a job queue
const queue = kue.createQueue();

// Job data object
const jobData = {
    phoneNumber: '415-123-4567',
    message: 'This is the code to verify your account'
};

// Creating a job in the 'push_notification_code' queue with the job data
const job = queue.create('push_notification_code', jobData)
    .save((err) => {
        if (err) {
            console.error('Failed to create job', err);
        } else {
            console.log(`Notification job created: ${job.id}`);
        }
    });

// Setup event listener for job completion
job.on('complete', () => {
    console.log('Notification job completed');
});

// Setup event listener for job failure
job.on('failed', (errorMessage) => {
    console.log('Notification job failed', errorMessage);
});
