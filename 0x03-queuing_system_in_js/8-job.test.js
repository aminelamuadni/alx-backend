import chai from 'chai';
import sinon from 'sinon';
import kue from 'kue';
import createPushNotificationsJobs from './8-job.js';

const expect = chai.expect;
const queue = kue.createQueue();

describe('createPush. NotificationsJobs', function () {
    before(function () {
        queue.testMode.enter();
    });

    after(function () {
        queue.testMode.exit();
    });

    beforeEach(function () {
        queue.testMode.clear();  // Clear the queue before each test
    });

    it('should throw an error if jobs is not an array', function () {
        expect(() => createPushNotificationsJobs({}, queue)).to.throw(Error, 'Jobs is not an array');
    });

    it('should create and manage multiple jobs correctly', function () {
        const jobs = [
            { phoneNumber: '1234567890', message: 'Your verification code is 1234' },
            { phoneNumber: '0987654321', message: 'Complete your profile soon' }
        ];
        createPushNotificationsJobs(jobs, queue);

        expect(queue.testMode.jobs.length).to.equal(2);
        expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
        expect(queue.testMode.jobs[1].type).to.equal('push_notification_code_3');
    });

    // Simplified job event tests
    it('should handle job completion events', function (done) {
        const job = queue.create('push_notification_code_3', {
            phoneNumber: '1234567890',
            message: 'Final notice: Your account will be closed'
        }).save();

        queue.testMode.jobs[0].on('complete', () => {
            done();
        });

        queue.testMode.jobs[0].emit('complete');
    });

    it('should handle job failure events', function (done) {
        const job = queue.create('push_notification_code_3', {
            phoneNumber: '0987654321',
            message: 'Urgent: Verify now!'
        }).save();

        queue.testMode.jobs[0].on('failed', error => {
            expect(error.message).to.equal('Simulated failure');
            done();
        });

        queue.testMode.jobs[0].emit('failed', new Error('Simulated failure'));
    });

    it('should monitor job progress', function (done) {
        const job = queue.create('push_notification_code_3', {
            phoneNumber: '1234567890',
            message: 'Processing your request...'
        }).save();

        queue.testMode.jobs[0].on('progress', progress => {
            expect(progress).to.equal(50);
            done();
        });

        queue.testMode.jobs[0].emit('progress', 50);
    });
});
