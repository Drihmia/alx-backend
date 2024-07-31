import { createQueue } from 'kue';

const queue = createQueue();

function sendNotification(phoneNumber, message) {
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
}

// queue.on('job enqueue', (id, type) => {
// Job.get(id, (err, job) => {
// if (!err) sendNotification(job.data.phoneNumber, job.data.message);
// });
// });

queue.process('push_notification_code', (job, done) => {
  const { phoneNumber, message } = job.data;
  sendNotification(phoneNumber, message);
  done();
});

// Handle unexpected errors beyond the job execution
process.on('uncaughtException', (err) => {
  console.error(`Unexpected Error: ${err}`);
});
