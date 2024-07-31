import { createClient, print as rprint } from 'redis';

const client = createClient();

client.on('error', (err) => console.log('Redis client not connected to the server:', err));

function callbac(err, repl) {
  if (err) {
    console.log('Error Setting hashset');
  } else {
    rprint(`Replay: ${repl}`);
  }
}

const setHashValue = () => {
  client.hset('HolbertonSchools', 'Portland', 50, callbac);
  client.hset('HolbertonSchools', 'Seattle', 80, callbac);
  client.hset('HolbertonSchools', 'New York', 20, callbac);
  client.hset('HolbertonSchools', 'Bogota', 20, callbac);
  client.hset('HolbertonSchools', 'Cali', 40, callbac);
  client.hset('HolbertonSchools', 'Paris', 2, callbac);
};

const getHashValue = (channelName) => {
  client.hgetall(channelName, (err, repl) => {
    if (err) {
      console.log(`Redis Getting hashset: ${err}`);
    } else {
      console.log(repl);
    }
  });
};

client.on('connect', () => {
  console.log('Redis client connected to the server');

  setHashValue();
  getHashValue('HolbertonSchools');
});
