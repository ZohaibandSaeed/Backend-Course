import express from "express";
import dotenv from "dotenv";

import { ConnectDB } from "./src/config/database.js";
import authRouter from "./src/routes/auth.route.js";

dotenv.config();

const app = express();

ConnectDB();

app.use(express.json());
app.use("/api/auth", authRouter);

app.get("/", (req, res) => {
    console.log("Hello Word");
    res.send("Hello Word");
});

const PORT = process.env.PORT || 3000;

app.listen(process.env.PORT, () => {
    console.log(`Server is running on port ${process.env.PORT}`);
});