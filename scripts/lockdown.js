db = db.getSiblingDB("zombietracker");
db.addUser("EliteZombieTracker", "impossiblepassword");

db = db.getSiblingDB("admin");
db.addUser("Admin", "supersecret");