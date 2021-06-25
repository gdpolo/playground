db.createUser({
    user: "gilda",
    pwd:  "123456",
    roles: [ {role: "readWrite", db: "local_search_data"} ]
})