import { createClient, print as rprint } from 'redis';

const { promisify } = require('util');

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

const getAsync = promisify(client.get).bind(client);

async function displaySchoolValue(schoolName) {
  const value = await getAsync(schoolName);
  console.log(value);
}

async function main() {
  await displaySchoolValue('Holberton');
  setNewSchool('HolbertonSanFrancisco', '100');
  await displaySchoolValue('HolbertonSanFrancisco');
}

client.on('connect', () => {
  console.log('Redis client connected to the server');
  main();
});
