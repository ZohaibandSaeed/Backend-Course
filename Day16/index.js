import express from "express";
import dotenv from "dotenv";
import { ConnectDB } from "./src/config/database.js";
import authRoutes from "./src/api/routes/auth.route.js";
import adminRoutes from "./src/api/routes/admin.route.js";
import recipeRoutes from "./src/api/routes/recipe.route.js";

const app = express();
dotenv.config();

app.use(express.json());

// Mount routes
app.use("/api/auth", authRoutes);
app.use("/api/admin", adminRoutes);
app.use("/api/recipes", recipeRoutes);

ConnectDB()
    .then(() => {
        app.listen(process.env.PORT, () => {
            console.log(`Server is running on port ${process.env.PORT}`);
        });
    })
    .catch((error) => {
        console.error(error);
    });
