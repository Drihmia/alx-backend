import { expect } from 'chai';
import kue from 'kue';
import createPushNotificationsJobs from './8-job';

const queue = kue.createQueue();

before(() => queue.testMode.enter());

after(() => queue.testMode.exit());

describe('createPushNotificationsJobs', () => {
  afterEach(() => queue.testMode.clear());

  it('display a error message if jobs is not an array, case of a number', () => {
    expect(() => createPushNotificationsJobs(12, queue)).to.throw('Jobs is not an array');
  });

  it('display a error message if jobs is not an array, case of an object', () => {
    expect(() => createPushNotificationsJobs({ red: 12 }, queue)).to.throw('Jobs is not an array');
  });

  it('should not display a error message if jobs is an array', () => {
    expect(() => createPushNotificationsJobs([{ red: 12 }], queue)).to.not
      .throw('Jobs is not an array');
  });

  it('Create a job', () => {
    const jobs = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account'
      },
      {
        phoneNumber: '4153518781',
        message: 'This is the code 4562 to verify your account'
      },
    ];
    createPushNotificationsJobs(jobs, queue);

    const createdJobs = queue.testMode.jobs;
    expect(createdJobs).to.have.lengthOf(2);
    for (const i in 2) {
      expect(createdJobs[i].data).to.deep.equal(jobs[i]);
      expect(createdJobs[i].type).to.equal('push_notification_code_3');
    }
  });
});
