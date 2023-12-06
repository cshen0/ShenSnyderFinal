import mysql.connector

# connect to database
db = mysql.connector.connect(
  host="localhost",  
  user="root", 
  passwd="root4834"
)

# create database
def createDB():
    cursor = db.cursor()
    cursor.execute('CREATE database final')
    cursor.execute('USE final')

# create tables
def createTables():
    cursor = db.cursor()

    createShoppingCart = "CREATE TABLE ShoppingCart( \
        shoppingCart_id int NOT NULL AUTO_INCREMENT, \
        total_price DECIMAL(10, 2) CHECK(total_price >= 0), \
        PRIMARY KEY (shoppingCart_id))"
    
    createMerchCategory = "CREATE TABLE MerchCategory( \
        category_id VARCHAR(10) NOT NULL, \
        name VARCHAR(20), \
        PRIMARY KEY (category_id))"

    createRetailer = "CREATE TABLE Retailer( \
        retailer_id VARCHAR(10) NOT NULL, \
        name VARCHAR(20), \
        address VARCHAR(50), \
        phoneNum CHAR(12), \
        email VARCHAR(20), \
        PRIMARY KEY (retailer_id))"

    createUser = "CREATE TABLE User( \
        user_id int NOT NULL AUTO_INCREMENT, \
        shoppingCart_id int NOT NULL, \
        username VARCHAR(20) NOT NULL, \
        password VARCHAR(25) NOT NULL, \
        name VARCHAR(20), \
        PRIMARY KEY (user_id))"
    
    createMerchandise = "CREATE TABLE Merchandise( \
        merch_id int NOT NULL AUTO_INCREMENT, \
        retailer_id VARCHAR(10) NOT NULL, \
        category_id VARCHAR(10) NOT NULL, \
        quantity INT CHECK(quantity >=0), \
        price DECIMAL(10, 2) CHECK(price > 1), \
        name VARCHAR(15), \
        color VARCHAR(10), \
        PRIMARY KEY (merch_id))"
    
    createCartItem = "CREATE TABLE CartItem( \
        merch_id int NOT NULL, \
        cart_id int NOT NULL AUTO_INCREMENT, \
        shoppingCart_id int NOT NULL, \
        cartQuantity INT CHECK (cartQuantity >= 1), \
        CONSTRAINT pk_cartItem PRIMARY KEY (cart_id, merch_id))"
    
    createOrder = "CREATE TABLE `Order`( \
        order_id int NOT NULL AUTO_INCREMENT, \
        shoppingCart_id int NOT NULL, \
        total_price DECIMAL(10, 2) CHECK(total_price >=0), \
        PRIMARY KEY (order_id))"

    createOrderItem = "CREATE TABLE OrderItem( \
        orderItem_id int NOT NULL AUTO_INCREMENT, \
        order_id int NOT NULL, \
        merch_id int NOT NULL, \
        quantity INT CHECK(quantity >= 1), \
        CONSTRAINT pk_orderItem PRIMARY KEY (orderItem_id, merch_id))" 
    
    cursor.execute(createShoppingCart)
    cursor.execute(createMerchCategory)
    cursor.execute(createRetailer)
    cursor.execute(createUser)
    cursor.execute(createMerchandise)
    cursor.execute(createCartItem)
    cursor.execute(createOrder)
    cursor.execute(createOrderItem)

# set foreign keys for each table
def setForeignKeys():
    cursor = db.cursor()
    
    addUserSCID = "ALTER Table User \
        ADD FOREIGN KEY (shoppingCart_id) \
            REFERENCES ShoppingCart(shoppingCart_id)"
    
    addMerchandiseCatID = "ALTER Table Merchandise \
        ADD FOREIGN KEY (category_id) \
            REFERENCES MerchCategory(category_id)"
    
    addMerchandiseRetailerID = "ALTER Table Merchandise \
        ADD FOREIGN KEY (retailer_id) \
            REFERENCES Retailer(retailer_id)"

    addOrderSCID = "ALTER Table `Order` \
        ADD FOREIGN KEY (shoppingCart_id) \
            REFERENCES ShoppingCart(shoppingCart_id)"

    addCartItemSCID = "ALTER Table CartItem \
        ADD FOREIGN KEY (shoppingCart_id) \
            REFERENCES ShoppingCart(shoppingCart_id)"

    addCartItemMerchID = "ALTER Table CartItem \
        ADD FOREIGN KEY (merch_id) \
            REFERENCES Merchandise(merch_id)"
    
    addOrderItemOrderID = "ALTER Table OrderItem \
        ADD FOREIGN KEY (order_id) \
            REFERENCES `Order`(order_id)"
    
    addOrderItemMerchID = "ALTER Table OrderItem \
        ADD FOREIGN KEY (merch_id) \
            REFERENCES Merchandise(merch_id)"
    
    cursor.execute(addUserSCID)
    cursor.execute(addMerchandiseCatID)
    cursor.execute(addMerchandiseRetailerID)
    cursor.execute(addOrderSCID)
    cursor.execute(addCartItemSCID)
    cursor.execute(addCartItemMerchID)
    cursor.execute(addOrderItemOrderID)
    cursor.execute(addOrderItemMerchID)

# pre-populate Retailer table
def setRetailerInfo():
    cursor = db.cursor()
    
    retailer1 = "INSERT INTO Retailer \
        (retailer_id, name, address, phoneNum, email) \
        VALUES (%s, %s, %s, %s, %s)"
    values1 = ("1234", "bob", "1234 Bob Drive", "123-456-7890", "bob@bob.com")

    retailer2 = "INSERT INTO Retailer \
        (retailer_id, name, address, phoneNum, email) \
        VALUES (%s, %s, %s, %s, %s)"
    values2 = ("5678", "sally", "5678 Sally Drive", "123-456-5678", "sally@sally.com")

    retailer3 = "INSERT INTO Retailer \
        (retailer_id, name, address, phoneNum, email) \
        VALUES (%s, %s, %s, %s, %s)"
    values3 = ("9012", "fred", "1234 Fred Drive", "123-456-9012", "fred@fred.com")

    cursor.execute(retailer1, values1)
    cursor.execute(retailer2, values2)
    cursor.execute(retailer3, values3)
    db.commit()

# pre-populate MerchCategory table
def setMerchCategory():
    cursor = db.cursor()
    
    cat1 = "INSERT INTO MerchCategory \
        (category_id, name) \
        VALUES (%s, %s)"
    values1 = ("1", "tops")
    
    cat2 = "INSERT INTO MerchCategory \
        (category_id, name) \
        VALUES (%s, %s)"
    values2 = ("2", "bottoms")

    cat3 = "INSERT INTO MerchCategory \
        (category_id, name) \
        VALUES (%s, %s)"
    values3 = ("3", "outerear")

    cat4 = "INSERT INTO MerchCategory \
        (category_id, name) \
        VALUES (%s, %s)"
    values4 = ("4", "accessories")

    cat5 = "INSERT INTO MerchCategory \
        (category_id, name) \
        VALUES (%s, %s)"
    values5 = ("5", "jerseys")

    cursor.execute(cat1, values1)
    cursor.execute(cat2, values2)
    cursor.execute(cat3, values3)
    cursor.execute(cat4, values4)
    cursor.execute(cat5, values5)

    db.commit()

if __name__ == '__main__':
    createDB()
    createTables()
    setForeignKeys()
    setRetailerInfo()
    setMerchCategory()
