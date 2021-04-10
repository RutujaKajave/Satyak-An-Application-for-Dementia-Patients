const { response, request } = require("express");
const express = require("express");
const connection = require("../services/connection");
const router = express.Router();

router.get("/", (req, res) => {
  res.send("register");
});

router.post("/", (req, res) => {
  console.log(req.body);
  var name = req.body.name;
  var number = req.body.number;
  var email = req.body.email;
  var gender = req.body.gender;
  var dob = req.body.dob;
  connection.query(
    "INSERT INTO patients VALUES('" +
      name +
      "','" +
      number +
      "','" +
      email +
      "','" +
      gender +
      "','" +
      dob +
      "')",
    (err, rows, fields) => {
      if (err) {
        console.log("error on query");
        response.sendStatus(400);
      } else {
        console.log("successfull query");
        response.sendStatus(201);
      }
    }
  );
});

module.exports = router;
