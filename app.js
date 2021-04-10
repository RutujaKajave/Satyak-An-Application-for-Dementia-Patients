const express = require("express"); // import library
const app = express(); // initialise express library
const registerRoute = require("./routes/register");
const bodyParser = require("body-parser");
const patientRoute = require("./routes/patient");
require("./services/connection");

//middlewares
app.use(bodyParser.json());
app.use("/registerRoute", registerRoute);
app.use("/patientsRoute", patientRoute);

app.get("/", (request, response) => {
  response.send("Welcome to Server").status(200);
}); // default routes

app.post("/", (request, response) => {
  response.send("Welcome to Server").status(200);
}); // default route

app.listen(3000); //server listens to this particular port
