import express from "express";
import testRouter from "./src/routers/test.router.js";
import userRouter from "./src/routers/user.router.js";

const app = express();

app.use(express.json());

app.use("/api", testRouter);
app.use("/api/users", userRouter);

app.listen(3000, () => {
    console.log("Server is running at port 3000...");
});

