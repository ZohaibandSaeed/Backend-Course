import express from "express";
import dotenv from "dotenv";
import { ConnectDB } from "./src/config/database.js";

const app = express();
dotenv.config();

ConnectDB()
    .then(() => {
        app.listen(process.env.PORT, () => {
            console.log(`Server is running on port ${process.env.PORT}`);
        })
    })
    .catch((error) => {
        console.error(error);
    })
