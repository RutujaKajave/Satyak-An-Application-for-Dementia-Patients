const mysql = require('mysql2');
const { connect } = require('../routes/register');

// create the connection to database
const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root', password: '',
    database: 'satyak'
});

connection.connect((err) => {
    if (err) {
        console.log('Error while Connecting');
    } else {
        console.log('Connection Successfull');
    }
});

module.exports = connection;