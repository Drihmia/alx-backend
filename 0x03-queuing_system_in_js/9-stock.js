import express from 'express';
import { createClient } from 'redis';

const { promisify } = require('util');

// Instantiate objects ---------------------------------------
const app = express();
const client = createClient();

// Promisify get method of Redis so we cas use async/await. --
const getAsync = promisify(client.get).bind(client);

// Fake data -------------------------------------------------
const listProducts = [
  {
    id: 1, name: 'Suitcase 250', price: 50, stock: 4,
  },
  {
    id: 2, name: 'Suitcase 450', price: 100, stock: 10,
  },
  {
    id: 3, name: 'Suitcase 650', price: 350, stock: 2,
  },
  {
    id: 4, name: 'Suitcase 1050', price: 550, stock: 5,
  },
];

// Utility functions -----------------------------------------
function getItemById(id) {
  return listProducts[id - 1];
}

function reserveStockById(itemId, stock) {
  client.set(itemId, stock, (err, repl) => {
    if (err) {
      console.error('Error while reserving:', err);
      return;
    }
    console.log(`Reply: ${repl}`);
  });
}

async function getCurrentReservedStockById(itemId) {
  const stock = await getAsync(itemId);

  return stock;
}

// API's endpoints -------------------------------------------
app.get('/list_products', (req, res) => {
  const listItems = [];

  listProducts.forEach((product) => {
    const {
      id: itemId, name: itemName, price, stock: initialAvailableQuantity,
    } = product;

    listItems.push({
      itemId, itemName, price, initialAvailableQuantity,
    });
  });
  res.json(listItems);
});

app.get('/list_products/:itemId', async (req, res) => {
  const { params } = { ...req };

  const id = params.itemId;

  const item = getItemById(id);
  if (!item) {
    res.status(500).json({ status: 'Product not found' });
    return;
  }

  const {
    id: itemId, name: itemName, price,
  } = { ...item };

  const stock = await getCurrentReservedStockById(id);

  res.json({
    itemId, itemName, price, stock,
  });
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const { params } = { ...req };

  const id = params.itemId;

  const stockRedis = await getCurrentReservedStockById(id);
  if (stockRedis === null) {
    const item = getItemById(id);
    if (!item) {
      res.status(500).json({ status: 'Product not found' });
      return;
    }

    reserveStockById(id, item.stock - 1);
    res.json({ status: 'Reservation confirmed', itemId: id });
    return;
  }

  if (stockRedis < 1) {
    res.json({ status: 'Not enough stock available', itemId: id });
    return;
  }

  reserveStockById(id, stockRedis - 1);
  res.json({ status: 'Reservation confirmed', itemId: id });
});

// Listen to port 1245 ---------------------------------------
app.listen(1245);
