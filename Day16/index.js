import express from "express";
import dotenv from "dotenv";
import { ConnectDB } from "./src/config/database.js";
import authRoutes from "./src/api/routes/auth.route.js";

const app = express();
dotenv.config();

app.use(express.json());

// Mount routes
app.use("/api/auth", authRoutes);

ConnectDB()
    .then(() => {
        app.listen(process.env.PORT, () => {
            console.log(`Server is running on port ${process.env.PORT}`);
        });
    })
    .catch((error) => {
        console.error(error);
    });
