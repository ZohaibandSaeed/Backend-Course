import express from "express";
import dotenv from "dotenv";

dotenv.config();

const app = express();

app.use(express.json());

app.get("/", (req, res) => {
    console.log("Hello Word");
    res.send("Hello Word");
});

const PORT = process.env.PORT || 3000;

app.listen(process.env.PORT, () => {
    console.log(`Server is running on port ${process.env.PORT}`);
});