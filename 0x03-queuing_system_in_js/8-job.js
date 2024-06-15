// Importing Kue library is not strictly necessary here, since we are exporting the function
// to be used in another file where the Kue is configured.

// Function to create push notification jobs
function createPushNotificationsJobs(jobs, queue) {
    // Check if jobs is actually an array
    if (!Array.isArray(jobs)) {
        throw new Error('Jobs is not an array');
    }

    jobs.forEach(jobData => {
        // Creating a new job in the 'push_notification_code_3' queue
        const job = queue.create('push_notification_code_3', jobData)
            .save((err) => {
                if (err) {
                    console.error(`Failed to create job: ${err}`);
                } else {
                    console.log(`Notification job created: ${job.id}`);
                }
            });

        // Setting up listeners for job events
        job.on('complete', () => {
            console.log(`Notification job ${job.id} completed`);
        });

        job.on('failed', err => {
            console.log(`Notification job ${job.id} failed: ${err.message}`);
        });

        job.on('progress', progress => {
            console.log(`Notification job ${job.id} ${progress}% complete`);
        });
    });
}

// Exporting the function for use in other files
export default createPushNotificationsJobs;
