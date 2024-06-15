// Importing Kue library
import kue from 'kue';

// Create a job queue with Kue
const queue = kue.createQueue();

// Jobs data array
const jobs = [
    {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account'
    },
    {
        phoneNumber: '4153518781',
        message: 'This is the code 4562 to verify your account'
    },
    {
        phoneNumber: '4153518743',
        message: 'This is the code 4321 to verify your account'
    },
    {
        phoneNumber: '4153538781',
        message: 'This is the code 4562 to verify your account'
    },
    {
        phoneNumber: '4153118782',
        message: 'This is the code 4321 to verify your account'
    },
    {
        phoneNumber: '4153718781',
        message: 'This is the code 4562 to verify your account'
    },
    {
        phoneNumber: '4159518782',
        message: 'This is the code 4321 to verify your account'
    },
    {
        phoneNumber: '4158718781',
        message: 'This is the code 4562 to verify your account'
    },
    {
        phoneNumber: '4153818782',
        message: 'This is the code 4321 to verify your account'
    },
    {
        phoneNumber: '4154318781',
        message: 'This is the code 4562 to verify your account'
    },
    {
        phoneNumber: '4151218782',
        message: 'This is the code 4321 to verify your account'
    }
];

// Iterate over the jobs array to create and manage each job
jobs.forEach((jobData, index) => {
    const job = queue.create('push_notification_code_2', jobData)
        .save((err) => {
            if (err) {
                console.error(`Notification job creation failed: ${err}`);
            } else {
                console.log(`Notification job created: ${job.id}`);
            }
        });

    // Setting up event listeners for job progress, completion, and failure
    job.on('complete', () => {
        console.log(`Notification job #${job.id} completed`);
    });

    job.on('failed', (err) => {
        console.log(`Notification job #${job.id} failed: ${err}`);
    });

    job.on('progress', (progress) => {
        console.log(`Notification job #${job.id} ${progress}% complete`);
    });
});
