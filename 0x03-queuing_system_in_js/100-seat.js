import { createClient } from 'redis';
import { promisify } from 'util';
import { createQueue } from 'kue';
import express from 'express';

// Instantiate objects ---------------------------------------
const client = createClient();
const queue = createQueue();
const app = express();

// Promisify get method of Redis so we cas use async/await. --
const getAsync = promisify(client.get).bind(client);

// Utility functions -----------------------------------------
function reserveSeat(number) {
  client.set('available_seats', number, (err, repl) => {
    if (err) {
      console.log('Error while setting available seats:', err);
    } else {
      console.log(`Reply: ${repl}`);
    }
  });
}
async function getCurrentAvailableSeats() {
  const availableSeats = await getAsync('available_seats');
  return availableSeats;
}

// Creating 50 available seats and enable reservation. -------
reserveSeat(50);
let reservationEnabled = true;

// API's endpoints -------------------------------------------
app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }

  const job = queue.create('reserve_seat');
  job.save((err) => {
    if (err) {
      res.json({ status: 'Reservation failed' });
    } else {
      res.json({ status: 'Reservation in process' });
    }
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (err) => {
    console.log(`Seat reservation job ${job.id} failed: ${err}`);
  });
});

app.get('/process', (req, res) => {
  res.json({ status: 'Queue processing' });
  queue.process('reserve_seat', async (job, done) => {
    const currentAvailableSeats = await getCurrentAvailableSeats();
    if (currentAvailableSeats < 1) {
      // Blocking any new reservations.
      reservationEnabled = false;
      done(new Error('Not enough seats available'));
      return;
    }
    // Reserving by decreasing the number of available seats in Redis.
    reserveSeat(currentAvailableSeats - 1);
    done();
  });
});

// Listen to port 1245 ---------------------------------------
app.listen(1245);
