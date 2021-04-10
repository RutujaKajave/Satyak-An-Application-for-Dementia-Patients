const express = require("express");
const connection = require("../services/connection");
const router = express.Router();

router.get("/", (req, res) => {
  connection.query("SELECT * FROM patients", (err, rows) => {
    if (err) {
      console.log("no patients");
      res.sendStatus(400);
    } else {
      res.send(rows).status(200);
    }
  });
});

module.exports = router;
