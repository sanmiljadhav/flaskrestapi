const express = require("express");
const app = express();
const port = 3000;

app.set("view engine", "ejs");

app.get("/", (req, res) => {
  res.render("index");
});

app.get("/register", (req, res) => {
  res.render("userregister");
});

app.get("/loginn", (req, res) => {
  res.render("userlogin");
});

app.get("/userprofile", (req, res) => {
  res.render("userprofile");
});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});
