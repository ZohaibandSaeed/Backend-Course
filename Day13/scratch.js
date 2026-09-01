import { db } from "./src/prisma/db.ts";
async function run() {
    try {
        const user = await db.orm.public.User.create({
            name: "Test",
            email: "test@example.com"
        });
        console.log("Success flat:", user);
    } catch (e) {
        console.log("Error flat:", e.message);
    }
}
run();
