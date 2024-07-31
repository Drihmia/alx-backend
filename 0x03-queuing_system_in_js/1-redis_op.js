import { createClient, print as rprint } from 'redis';

const client = createClient();

client.on('error', (err) => console.error('Redis client not connected to the server:', err));

function setNewSchool(schoolName, value) {
  client.set(schoolName, value, (err, repl) => {
    if (err) {
      console.error('Error setting value', err);
    } else {
      rprint(`Reply: ${repl}`);
    }
  });
}

function displaySchoolValue(schoolName) {
  client.get(schoolName, (err, val) => {
    if (err) {
      console.error('Error getting value', err);
    } else {
      console.log(val);
    }
  });
}

client.on('connect', () => {
  console.log('Redis client connected to the server');
  displaySchoolValue('Holberton');
  setNewSchool('HolbertonSanFrancisco', '100');
  displaySchoolValue('HolbertonSanFrancisco');
});
