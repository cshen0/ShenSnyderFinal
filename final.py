import mysql.connector

# connect to database
db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root4834"
)

# choose database
def chooseDB():
    cursor = db.cursor()
    cursor.execute('USE final') 
    
# home page for anyone
def showHomePage():
    print("Welcome to our online merch platform! Please select your role:")
    print("R: Retailer")
    print("C: Customer")
    print("E: Exit")

    role = input("Enter role: ")

    if role.upper() == "R":
        retailerHomePage()
    elif role.upper() == "C":
        customerHomePage()
    elif role.upper() == "E":
        exit()
    
    # invalid input, restart
    else:
        print("Invalid input.")
        showHomePage()

# home page for retailer
def retailerHomePage():
    print("------------")
    print("Welcome! Please enter your retailerID from the list below or generate platform inventory report: ")
    print("Retailer 1 ID: 1234")
    print("Retailer 2 ID: 5678")
    print("Retailer 3 ID: 9012")
    print("G: Generate platform inventory report")
    print("H: return to homepage")

    action = input("Enter action/id: ")

    if action == "1234" or action == "5678" or action == "9012":
        retailerLogIn(action)
    if action.upper() == "G":
        getAllInventoryReport()
    if action.upper() == "H":
        showHomePage()
    else:
        print("Invalid action/retailer ID.")
        retailerHomePage()
        
# retailer logged in page
def retailerLogIn(retailerID):
    print("------------")
    print("Retailer " + retailerID + ", choose an action below:")
    print("I: insert inventory")
    print("U: update inventory")
    print("D: delete inventory")
    print("G: get inventory report")
    print("H: return to retailer homepage")

    action = input("Enter action: ")
    if action.upper() == "I":
        insertInventory(retailerID)
    elif action.upper() == "U":
        updateInventory(retailerID)
    elif action.upper() == "D":
        deleteInventory(retailerID)
    elif action.upper() == "G":
        getInventoryReport(retailerID)
    elif action.upper() == "H":
        retailerHomePage()
    else:
        print("Invalid action.")
        retailerLogIn(retailerID)

def showCategoryIDs():
    cursor = db.cursor()

    print("------------")
    print("Category IDs")

    query = "SELECT * FROM MerchCategory"
    cursor.execute(query)

    resultList = cursor.fetchall()

    db.commit()

    for element in resultList: 
        print("Category ID: "+element[0]+", Category Name: "+element[1])

# DONE DONE
def insertInventory(retailerID):

    try:
        cursor = db.cursor()

        showCategoryIDs()

        print("------------")
        print("Insert Inventory")
        categoryID = input("Category ID Number: ")
        quantity = input("Quantity: ")
        price = input("Price (in whole dollars): ")
        name = input("Name: ")
        color = input("Color: ")

        query = "INSERT INTO Merchandise \
            (retailer_id, category_id, quantity, price, name, color) \
            VALUES (%s, %s, %s, %s, %s, %s)"
        values = (retailerID, categoryID, quantity, price, name, color)

        cursor.execute(query, values)
        db.commit()
        print("Inventory has been added.")

    except mysql.connector.Error as error:
            print("Failed to insert inventory: {}".format(error))
            # reverting changes because of exception

            db.rollback()

    retailerLogIn(retailerID)

# DONE DONE   
def updateInventory(retailerID):
    try:
        cursor = db.cursor()

        query = "SELECT * FROM Merchandise \
            WHERE retailer_id = %s"
        values = (retailerID, )
        
        cursor.execute(query, values)
        resultList = cursor.fetchall()

        print("------------")
        print("Current Inventory:")

        for element in resultList:
            print("Merch ID: " +str(element[0])+ ", Retailer ID: " +str(element[1])+ 
            ", Category ID: " +str(element[2])+ ", Quantity: " +str(element[3])+ 
            ", Price:" +str(element[4])+ ", Name: " +element[5]+ ", Color: " +element[6])

        if len(resultList) == 0:
            print("No Inventory to update.")
        else:
            print("------------")
            print("Would you like restock available inventory?")
            action = input("Y/N: ")
            if action.upper() == "Y":
                print("------------")
                print("Update (Restock) Inventory")
                
                merchID = input("Merch ID Number: ")
                restockAmt = input("Restock amount: ")

                query = "SELECT * FROM Merchandise \
                    WHERE merch_id = %s"
                values = (merchID, )

                cursor.execute(query, values)
                resultList = cursor.fetchall()

                if len(resultList) == 0:
                    print("Merch ID not found.")
                    retailerLogIn(retailerID)

                query = "UPDATE Merchandise \
                    SET quantity = quantity + %s \
                    WHERE merch_id = %s AND retailer_id = %s"
                values = (restockAmt, merchID, retailerID)
                
                cursor.execute(query, values)
                db.commit()
                print("Inventory has been updated.")
            else:
                print("No inventory updates.")
    except mysql.connector.Error as error:
            print("Failed to update inventory: {}".format(error))
            # reverting changes because of exception

            db.rollback()

    retailerLogIn(retailerID)

# DONE DONE
def deleteInventory(retailerID):
    try:
        cursor = db.cursor()

        query = "SELECT * FROM Merchandise \
            WHERE retailer_id = %s"
        values = (retailerID, )
        
        cursor.execute(query, values)
        resultList = cursor.fetchall()

        print("------------")
        print("Current Inventory:")

        for element in resultList:
            print("Merch ID: " +str(element[0])+ ", Retailer ID: " +str(element[1])+ 
            ", Category ID: " +str(element[2])+ ", Quantity: " +str(element[3])+ 
            ", Price:" +str(element[4])+ ", Name: " +element[5]+ ", Color: " +element[6])

        if len(resultList) == 0:
            print("No Inventory to delete.")
        else:
            print("------------")
            print("Would you like delete available inventory?")
            action = input("Y/N: ")
            if action.upper() == "Y":
                print("------------")
                print("Delete Item from Inventory")

                merchID = input("Merch ID Number: ")

                query = "SELECT * FROM Merchandise \
                    WHERE merch_id = %s"
                values = (merchID, )

                cursor.execute(query, values)
                resultList = cursor.fetchall()

                if len(resultList) == 0:
                    print("Merch ID not found.")
                    retailerLogIn(retailerID)

                query = "DELETE FROM Merchandise \
                    WHERE merch_id = %s AND retailer_id = %s"
                values = (merchID, retailerID)
                
                cursor.execute(query, values)
                db.commit()
                print("Inventory has been deleted.")
            else:
                print("No inventory deletions.")
    except mysql.connector.Error as error:
        print("Failed to delete inventory: {}".format(error))
        # reverting changes because of exception

        db.rollback()

    retailerLogIn(retailerID)

# DONE DONE
def getInventoryReport(retailerID):
    cursor = db.cursor()

    print("------------")
    print("Reatiler " + retailerID + " inventory report: ")

    query = "SELECT * FROM Merchandise \
        WHERE retailer_id = %s"
    values = (retailerID, )
    
    cursor.execute(query, values)
    resultList = cursor.fetchall()
    db.commit()

    for element in resultList:
        print("Merch ID: " +str(element[0])+ ", Retailer ID: " +str(element[1])+ 
            ", Category ID: " +str(element[2])+ ", Quantity: " +str(element[3])+ 
            ", Price:" +str(element[4])+ ", Name: " +element[5]+ ", Color: " +element[6])

    retailerLogIn(retailerID)

# DONE DONE
def getAllInventoryReport():
    cursor = db.cursor()

    print("------------")
    print("Get All Inventory Report")

    print("Choose how you would like to sort the report:")
    print("PA: price ascending")
    print("PD: price decending")
    print("R: retailer")
    print("QA: quantity ascending")
    print("QD: quantity descending")

    action = input("Enter your action: ")

    if action.upper() == "PA":
        query = "SELECT * FROM Merchandise \
        ORDER BY price ASC"

    elif action.upper() == "PD":
        query = "SELECT * FROM Merchandise \
        ORDER BY price DESC"

    elif action.upper() == "R":
        query = "SELECT * FROM Merchandise \
        ORDER BY retailer_id"

    elif action.upper() == "QA":
        query = "SELECT * FROM Merchandise \
        ORDER BY quantity ASC"

    elif action.upper() == "QD":
        query = "SELECT * FROM Merchandise \
        ORDER BY quantity DESC"
    
    else:
        print("Invalid action.")
        getAllInventoryReport()
    
    cursor.execute(query)
    resultList = cursor.fetchall()
    db.commit()

    for element in resultList:
        print("Merch ID: " +str(element[0])+ ", Retailer ID: " +str(element[1])+ 
        ", Category ID: " +str(element[2])+ ", Quantity: " +str(element[3])+ 
        ", Price: " +str(element[4])+ ", Name: " +element[5]+ ", Color: " +element[6])

    retailerHomePage()


# home page for customer
def customerHomePage():
    print("------------")
    print("Log in or create a user profile")
    print("L: log in to existing user profile")
    print("C: create new user profile")
    print("H: return to homepage")

    action = input("Enter action: ")

    if action.upper() == "C":
        createUserProfile()
    
    elif action.upper() == "L":
        userLogIn()

    elif action.upper() == "H":
        showHomePage()
    
    else:
        print("Invalid action.")
        customerHomePage()

# DONE DONE
def createUserProfile():
    try:
        cursor = db.cursor()
        db.start_transaction()

        print("------------")
        print("Create User Profile")
        # enter info, include transaction rollback

        username = input("Username: ")
        password = input("Password (not case sensitive): ")
        name = input("Name: ")

        # need explicit begin transaction and commit statement

        # create shopping cart for new user
        query1 = "INSERT INTO ShoppingCart (total_price) \
            VALUES (0)"
        cursor.execute(query1)
        shoppingCart_id = cursor.lastrowid

        # create new user profile
        query2 = "INSERT INTO User \
            (shoppingCart_id, username, password, name) \
            VALUES (%s, %s, %s, %s)"
        values2 = (shoppingCart_id, username, password, name)
        cursor.execute(query2, values2)

        query3 = "SELECT * FROM User \
            WHERE shoppingCart_id = %s"
        value3 = (shoppingCart_id, )
        cursor.execute(query3, value3)
        resultList = cursor.fetchall()
        
        db.commit()

        print("Your account has been created!")
        print("Your UserID: " +str(resultList[0][0]))
        print("Your ShoppingCart ID: " +str(resultList[0][1]))
        print("Your username: " + str(resultList[0][2]))

    except mysql.connector.Error as error:
            print("Failed to update record to database rollback: {}".format(error))
            # reverting changes because of exception

            db.rollback()

    customerHomePage()

# DONE DONE
def userLogIn():
    cursor = db.cursor()

    print("------------")
    print("Enter your userID")
    userID = input("userID: ")
    
    # check if the userID is in the table or not

    query = "SELECT * FROM User \
        WHERE user_id = %s"
    values = (userID, )

    cursor.execute(query, values)
    resultList = cursor.fetchall()
    db.commit()

    if len(resultList) == 0:
        print("UserId not found.")
        customerHomePage()

    else:
        # then, proceed to next step
        print("Enter your password")
        password = input("password: ")

        query2 = "SELECT * FROM User \
            WHERE user_id = %s AND password = %s"
        values2 = (userID, password)

        cursor.execute(query2, values2)
        resultList = cursor.fetchall()
        db.commit()

        if len(resultList) == 0:
            print("Password does not match.")
            customerHomePage()

        else:
            userActions(userID)  

# DONE DONE
def userActions(userID):
    print("------------")
    print("User " + userID + " choose an action below:")
    print("A: add new cart item")
    print("U: update cart item")
    print("C: clear shopping cart")
    print("S: submit order")
    print("O: see order history")
    print("H: return to customer home page")

    action = input("Enter an action: ")

    if action.upper() == "A":
        addCartItem(userID)
    elif action.upper() == "U":
        updateCartItem(userID)
    elif action.upper() == "C":
        clearShoppingCart(userID)
    elif action.upper() == "S":
        submitOrder(userID)
    elif action.upper() == "O":
        getOrderHistory(userID)
    elif action.upper() == "H":
        customerHomePage()
    else:
        print("Invalid input.")
        userActions(userID)

# DONE DONE
def browseInventory():
    cursor = db.cursor()

    print("------------")
    print("All Available Items:")

    query = "SELECT merch_id, price, name, color, quantity FROM Merchandise \
        WHERE quantity > 0 \
        ORDER BY quantity DESC"
    
    cursor.execute(query)
    resultList = cursor.fetchall()
    db.commit()

    for element in resultList:
        print("Merch ID: " +str(element[0])+ ", price: "+str(element[1])+", name: "+element[2]+", color: "+element[3]+", quantity: "+str(element[4]))

    return resultList

# DONE DONE
def addCartItem(userID):
    cursor = db.cursor()

    try:
        #display all available items in the inventory
        inventory = browseInventory()

        if len(inventory) == 0:
            print("no inventory to choose from.")
        else:
            print("------------")
            print("Would you like to add an available item to your cart?")
            action = input("Y/N: ")
            if action.upper() == "Y":

                db.start_transaction()
                
                #User provides merch_id, their shoppingCart_id, and the quantity they want to add to their cart
                print("------------")
                print("Add Item To Cart")
                merch_id = input("Merch ID Number: ")
                requested_quantity = input("Quantity: ")

                query = "SELECT * FROM Merchandise \
                    WHERE merch_id = %s"
                values = (merch_id, )

                cursor.execute(query, values)
                resultList = cursor.fetchall()

                if len(resultList) == 0:
                    print("Merch ID not found.")
                    userActions(userID)

                #check to make sure the shopper's quantity is less than the total inventory
                query1 = "SELECT * FROM Merchandise \
                    WHERE merch_id = %s"
                value1 = (merch_id, )
                cursor.execute(query1, value1)
                merch = cursor.fetchall()
                merch_quantity = merch[0][3]

                if int(requested_quantity) > merch_quantity:
                    print("Not enough inventory in stock.")
                    userActions(userID)

                else:
                    #get shopping cart for user
                    query3 = "SELECT * FROM User JOIN ShoppingCart \
                        WHERE user_id = %s"
                    value3 = (userID, )
                    cursor.execute(query3, value3)
                    shoppingCart = cursor.fetchall()
                    shoppingCart_id = shoppingCart[0][0]

                    #insert the merch_id and shoppingCart_id into the CartItem table
                    query2 = "INSERT INTO CartItem \
                        (merch_id, shoppingCart_id, cartQuantity) \
                        VALUES (%s, %s, %s)"
                    values2 = (merch_id, shoppingCart_id, int(requested_quantity))
                    cursor.execute(query2, values2)

                    #get price of the merchandise item * shopper's requested quantity 
                    merch_price = merch[0][4]
                    total_price = merch_price * int(requested_quantity)

                    #increment the total_price of the shoppingCart by the price of the merch_id*shopper_quantity
                    query3 = "UPDATE ShoppingCart \
                        SET total_price = total_price + %s \
                        WHERE shoppingCart_id = %s"
                    values3 = (total_price, shoppingCart_id)
                    cursor.execute(query3, values3)

                    #decrement the merchandise quantity
                    query4 = "UPDATE Merchandise \
                        SET quantity = quantity - %s \
                        WHERE merch_id = %s"
                    values4 = (requested_quantity, merch_id)
                    cursor.execute(query4, values4)

                    db.commit()
                    print("Item added.")
            
            else:
                print("No item added.")
    
    except mysql.connector.Error as error:
        print("Failed to add Cart Item: {}".format(error))
        # reverting changes because of exception
        db.rollback()

    userActions(userID)

#DONE DONE
def viewShoppingCart(userID):
    cursor = db.cursor()

    print("------------")
    print("Your Current Shopping Cart:")

    query = "SELECT MerchCategory.name, Merchandise.merch_id, CartItem.cart_id, Merchandise.name, Merchandise.price, CartItem.cartQuantity \
        FROM MerchCategory INNER JOIN Merchandise INNER JOIN CartItem INNER JOIN ShoppingCart INNER JOIN User \
        WHERE MerchCategory.category_id = Merchandise.category_id AND Merchandise.merch_id = CartItem.merch_id AND \
        CartItem.shoppingCart_id = ShoppingCart.shoppingCart_id AND ShoppingCart.shoppingCart_id = User.shoppingCart_id AND user_id = %s"
    values = (userID,)
    cursor.execute(query, values)
    resultList = cursor.fetchall()
    db.commit()

    for element in resultList:
        print("Merch Category: " +element[0]+ ", Merch ID: "+str(element[1])+", Cart Item ID: "+str(element[2])+
              ", Item Name: "+element[3]+", Price: "+str(element[4])+", Cart Item Quantity: "+str(element[5]))

    return resultList

#DONE DONE
def updateCartItem(userID):
    cursor = db.cursor()

    #display current Shopping Cart 
    shoppingCart = viewShoppingCart(userID)

    if len(shoppingCart) == 0:
        print("No shopping cart to edit.")
    else:
        print("------------")
        print("Would you like to remove an item to your cart?")
        action = input("Y/N: ")
        if action.upper() == "Y":
            #get the shoppingcart_id for the user
            query3 = "SELECT * FROM User JOIN ShoppingCart \
                WHERE user_id = %s"
            value3 = (userID, )
            cursor.execute(query3, value3)
            shoppingCart = cursor.fetchall()
            shoppingCart_id = shoppingCart[0][0]

            print("------------")
            print("Remove Item From Cart:")

            merchID = input("Merch ID Number: ")
            cartID = input("Cart Item ID Number: ")

            #check for merch_id
            query = "SELECT * FROM CartItem \
                WHERE merch_id = %s AND shoppingCart_id = %s"
            values = (merchID, shoppingCart_id)
            cursor.execute(query, values)
            resultList = cursor.fetchall()

            if len(resultList) == 0:
                print("Merch ID not found.")
                userActions(userID)

            #check for cart_id
            query = "SELECT * FROM CartItem \
                WHERE cart_id = %s"
            values = (cartID, )

            cursor.execute(query, values)
            resultList = cursor.fetchall()

            if len(resultList) == 0:
                print("Cart ID not found.")
                userActions(userID)

            #save the cart item quantity (for later)
            query1 = "SELECT * FROM CartItem \
                WHERE merch_id = %s AND cart_id = %s"
            values1 = (merchID, cartID )
            cursor.execute(query1, values1)
            cartItem = cursor.fetchall()
            cartItem_quantity = cartItem[0][3]

            #remove the item from the table
            query2 = "DELETE FROM CartItem \
                WHERE merch_id = %s AND cart_id = %s"
            values2 = (merchID, cartID)
            cursor.execute(query2, values2)

            #get the price of the item removed * quantity of the cart item
            query4 = "SELECT * FROM Merchandise \
                WHERE merch_id = %s"
            value4 = (merchID, )
            cursor.execute(query4, value4)
            merch = cursor.fetchall()
            merch_price = merch[0][4]
            cartItem_price = merch_price * cartItem_quantity

            #update the total price of the user's shopping cart
            query5 = "UPDATE ShoppingCart \
                    SET total_price = total_price - %s \
                    WHERE shoppingCart_id = %s"
            values5 = (cartItem_price, shoppingCart_id)
            cursor.execute(query5, values5)

            #decrement the merchandise quantity
            query6 = "UPDATE Merchandise \
                SET quantity = quantity + %s \
                WHERE merch_id = %s"
            values6 = (cartItem_quantity, merchID)
            cursor.execute(query6, values6)

            db.commit()

            print("Your cart has been updated.")
        else:
            print("No updates to your shopping cart.")
    userActions(userID)

# DONE DONE
def clearShoppingCart(userID):
    cursor = db.cursor()

    #display current Shopping Cart 
    shoppingCart = viewShoppingCart(userID)

    if len(shoppingCart) == 0:
        print("No shopping cart to clear.")
    else:
        print("------------")
        print("Would you like to clear to your cart?")
        action = input("Y/N: ")
        if action.upper() == "Y":
            print("------------")
            print("Clear Your Shopping Cart")

            #get the shoppingcart_id for the user
            query3 = "SELECT * FROM User JOIN ShoppingCart \
                WHERE user_id = %s"
            value3 = (userID, )
            cursor.execute(query3, value3)
            shoppingCart = cursor.fetchall()
            shoppingCart_id = shoppingCart[0][0]

            query = "SELECT * FROM CartItem \
                WHERE shoppingCart_id = %s"
            value = (shoppingCart_id, )
            cursor.execute(query, value)
            resultList = cursor.fetchall()

            #increment merchandise quantity 
            for element in resultList:
                query = "UPDATE Merchandise \
                    SET quantity = quantity + %s \
                    WHERE merch_id = %s"
                values = (element[3], element[0])
                cursor.execute(query, values)

            query = "DELETE FROM CartItem \
                WHERE shoppingCart_id = %s"
            values = (shoppingCart_id, )
            cursor.execute(query, values)

            query2 = "UPDATE ShoppingCart \
                SET total_price = 0 \
                WHERE shoppingCart_id = %s"
            values2 = (shoppingCart_id, )
            cursor.execute(query2, values2)

            db.commit()

            print("Your shopping cart has been cleared.")
        else:
            print("No updates to your shopping cart.")
    userActions(userID)

# DONE DONE
def submitOrder(userID):
    cursor = db.cursor()

    #display current Shopping Cart 
    shoppingCart = viewShoppingCart(userID)

    if len(shoppingCart) == 0:
        print("No shopping cart to submit.")
        userActions(userID)
    

    print("------------")
    print("Would you like to submit your order?")

    action = input("Y/N: ")

    if action.upper() == 'Y':
        try: 
            db.start_transaction()

            #Get shoppingCart_id
            query = "SELECT shoppingCart_id FROM User \
                WHERE user_id = %s"
            value = (userID, )
            cursor.execute(query, value)
            resultList = cursor.fetchall()
            shoppingCart_id = resultList[0][0]

            #Create an order id in the Order table
            query1 = "INSERT INTO `Order` (shoppingCart_id, total_price) \
                VALUES (%s, %s)"
            values1 = (shoppingCart_id, 0)
            cursor.execute(query1, values1)
            order_id = cursor.lastrowid

            #Create an order item for each stopping cart item associated with the user's shopping cart id and decrease merch quantity
            shoppingCart = viewShoppingCart(userID)

            for element in shoppingCart:
                queryn = "INSERT INTO OrderItem (order_id, merch_id, quantity) \
                    VALUES (%s, %s, %s)"
                valuesn = (order_id, element[1], element[5])
                cursor.execute(queryn, valuesn)

                # querym = "UPDATE Merchandise \
                #     SET quantity = quantity - %s \
                #     WHERE merch_id = %s"
                # valuesm = (element[5], element[1])
                # cursor.execute(querym, valuesm)

                queryo = "UPDATE `Order` \
                    SET total_price = total_price + %s \
                    WHERE order_id = %s"
                valueso = (int(element[4])*int(element[5]), order_id)
                cursor.execute(queryo, valueso)

            #Clear the shopping cart

            query2 = "UPDATE ShoppingCart \
                SET total_price = 0 \
                WHERE shoppingCart_id = %s"
            values2 = (shoppingCart_id, )
            cursor.execute(query2, values2)

            query3 = "DELETE FROM CartItem \
                WHERE shoppingCart_id = %s"
            values3 = (shoppingCart_id, )
            cursor.execute(query3, values3)

            db.commit()

            print("Your order has been submitted.")

        except mysql.connector.Error as error:
            print("Failed to submit order: {}".format(error))
            # reverting changes because of exception

            db.rollback()
    
    elif action.upper() == 'N':
        print("Order was not submitted.")
    
    else:
        print("Invalid action.")

    userActions(userID)

# DONE DONE 
def getOrderHistory(userID):
    cursor = db.cursor()

    print("------------")
    print("Your Order History:")

    query = "SELECT `Order`.order_id, OrderItem.orderItem_id, Merchandise.merch_id, Merchandise.name, Merchandise.price, OrderItem.quantity \
        FROM Merchandise INNER JOIN OrderItem INNER JOIN `Order` INNER JOIN ShoppingCart INNER JOIN User \
        WHERE Merchandise.merch_id = OrderItem.merch_id AND OrderItem.order_id = `Order`.order_id AND \
        `Order`.shoppingCart_id = ShoppingCart.shoppingCart_id AND ShoppingCart.shoppingCart_id = User.shoppingCart_id AND user_id = %s"
    values = (userID,)
    cursor.execute(query, values)
    resultList = cursor.fetchall()
    db.commit()

    for element in resultList:
        print("Order ID: " +str(element[0])+ ", Order Item ID: "+str(element[1])+", Merch ID: "+str(element[2])
              +", Item Name: "+element[3]+", Price: "+str(element[4])+", Cart Item Quantity: "+str(element[5]))

    userActions(userID)
        
if __name__ == '__main__':
    chooseDB()
    showHomePage()
