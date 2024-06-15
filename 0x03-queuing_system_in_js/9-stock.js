const express = require('express');
const { createClient } = require('redis');
const { promisify } = require('util');

const app = express();
const redisClient = createClient();
const getAsync = promisify(redisClient.get).bind(redisClient);

// Sample data
const listProducts = [
    { id: 1, name: "Suitcase 250", price: 50, stock: 4 },
    { id: 2, name: "Suitcase 450", price: 100, stock: 10 },
    { id: 3, name: "Suitcase 650", price: 350, stock: 2 },
    { id: 4, name: "Suitcase 1050", price: 550, stock: 5 }
];

// Helper functions
const getItemById = id => listProducts.find(item => item.id === id);

const reserveStockById = async (itemId, stock) => {
    await redisClient.set(`item.${itemId}`, stock);
};

const getCurrentReservedStockById = async itemId => {
    return await getAsync(`item.${itemId}`);
};

// Routes
app.get('/list_products', (req, res) => {
    const products = listProducts.map(product => ({
        itemId: product.id,
        itemName: product.name,
        price: product.price,
        initialAvailableQuantity: product.stock
    }));
    res.json(products);
});

app.get('/list_products/:itemId', async (req, res) => {
    const item = getItemById(parseInt(req.params.itemId));
    if (!item) {
        return res.status(404).json({ status: 'Product not found' });
    }
    const currentStock = await getCurrentReservedStockById(item.id) || item.stock;
    res.json({
        itemId: item.id,
        itemName: item.name,
        price: item.price,
        initialAvailableQuantity: item.stock,
        currentQuantity: currentStock
    });
});

app.get('/reserve_product/:itemId', async (req, res) => {
    const item = getItemById(parseInt(req.params.itemId));
    if (!item) {
        return res.status(404).json({ status: 'Product not found' });
    }
    const currentStock = await getCurrentReservedStockById(item.id) || item.stock;
    if (currentStock < 1) {
        return res.status(400).json({ status: 'Not enough stock available', itemId: item.id });
    }
    await reserveStockById(item.id, currentStock - 1);
    res.json({ status: 'Reservation confirmed', itemId: item.id });
});

// Start the server
app.listen(1245, () => {
    console.log('Server listening on port 1245');
});
