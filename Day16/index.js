import express from "express";
import dotenv from "dotenv";
import { ConnectDB } from "./src/config/database.js";
import mongoose from "mongoose";

const Test = new mongoose.Schema({
    name: String,
    email: String,
    phone: String,
    address: String,
    test: String,
}, { timestamps: true });

const TestDB = mongoose.model("Test", Test);

const app = express();
dotenv.config();

app.use(express.json());

app.post("/test", async (req, res) => {
    try {
        const data = await TestDB.create({
            name: "John",
            email: "zohaibsaeed1701@gmail.com",
            phone: "1234567890",
            address: "123 Main St",
            test: "Test",
        });

        res.status(201).json({
            success: true,
            message: "Data created successfully",
            data,
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: error.message,
        });
    }
});


ConnectDB()
    .then(() => {
        app.listen(process.env.PORT, () => {
            console.log(`Server is running on port ${process.env.PORT}`);
        });
    })
    .catch((error) => {
        console.error(error);
    });
