from model import(Base, session,engine,Products, Brands)
import csv,datetime, time


def menu():
    while True: 
        print(''' 
              \n********** PRODUCTS MENU ***********
             \rPress V to display Products
              \rPress N to add new Product
              \rPress A for analysis
              \rPress B for backup
              \rPress E to exit
              ''')
        choice = input('What would you like to do? ').upper()
        if choice in ['V','N','A','B','E']:
            return choice
        else:
            input('''
                  \rPlease choose one of the options above
                  \r [V,  N,  A,  B, E]
                  \rPress enter to try again.
                  ''')

def cleaned_quantity(quantity_str):
    try:
        product_quantity = int(quantity_str)
    except ValueError:
        print('''
            \n******** Product Quantity Error *********
             Product quanity must be a whole number''')
        input('Press enter to try again: ')
    else:
        return product_quantity
        

def cleaned_id(id_str, options):
    try:
        product_id = int(id_str)
    except ValueError:  
            input(''' 
              \n ***** Product ID ERROR *****
              \r ID must me a number and within id options range
              \r Press enter to try again
              ''')
            return
    else:
        if product_id in options:
            return product_id
        else:
            input(''' 
                  \n ****** ID error *******
                   \nID must me a number and within id options range
                   \nPress enter to try again
                  ''')
            time.sleep(1.2)
            return
    
            
            
def cleaned_date(date_str):
    try:
        split_date = date_str.split('/')
        year = int(split_date[2])
        month = int(split_date[0])
        day = int(split_date[1])
        return_date = datetime.date(year=year,month=month, day=day)
    except ValueError:
        input(''' 
              \n *** DATE ERROR ***
              \r The date format should include a valid day/month/year
              \r ex: 24/12/2023 
              \r Press enter to try again''')
        return
    else:
         return return_date 
 
            
def cleaned_price(price_str):
    try:
        new_price = price_str.replace('$', '')
        new_price = float(new_price)
        new_price = int(new_price * 100)
    except ValueError:
             print(''' 
              \n *** Price Error ***
              \r Price should be a number exp: 10.99
              ''')
             return None
    else:
        return new_price
    
   


def add_inventory_csv():
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        header = next(data)
        for row in data: 
            # print(row[3])
            product_in_db = session.query(Products).filter(Products.product_name==row[0]).one_or_none()
            if product_in_db ==None:
                brand = session.query(Brands).filter(Brands.brand_name == row[4]).one_or_none()
                brand_id = brand.brand_id if brand else None # code to extract brand id from brand name
                product_name = row[0]
                product_price = cleaned_price(row[1])
                product_quantity = row[2]
                date_updated = cleaned_date(row[3])
                brand_name = row[4]
                brand_id = brand_id
                new_products = Products(product_name=product_name, product_quantity=product_quantity, product_price=product_price, date_updated =date_updated,brand_id=brand_id)
                session.add(new_products)
        session.commit()
        

def add_brands_csv():
    with open('brands.csv') as csvfile:
        data = csv.reader(csvfile)
        header = next(data)
        for row in data:
            # print(row)
            brands_in_db = session.query(Brands).filter(Brands.brand_name ==row[0]).one_or_none()
            if brands_in_db == None:
                brand_name = row[0]
                new_brands = Brands(brand_name=brand_name)
                session.add(new_brands)
        session.commit()
        
def app():  
    add_brands_csv() # loading brand_csv file into the model
    add_inventory_csv() # loading iventory_csv file into the model
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'V':
            # view products by id
            print('******** Search for Product by ID **********')
            id_options = []
            for product in session.query(Products):
                id_options.append(product.product_id)
            id_error = True
            while id_error:
                id_choice = input(f''' 
                 \nProduct_ID : {id_options}
                \nProduct ID :  ''')
                id_choice = cleaned_id(id_choice,id_options)
                if type(id_choice) == int:
                    id_error = False
            the_product = session.query(Products).filter(Products.product_id==id_choice).first()
            print(f'''
                  \nProduct_id : {the_product.product_id} | Product_name: {the_product.product_name}\r
                 \nProduct_quantity : {the_product.product_quantity}\r
                  \nProduct_price : ${the_product.product_price /100}\r
                  \nDate_updated : {the_product.date_updated}\r
                  \nBrand_id : {the_product.brand_id}\r
                  ''')
            input('Press enter to return to the main')
                  
                
        elif choice == 'N':
            # add product
            product_name =input('Product name: ')
            quantity_error = True
            while quantity_error:
                product_quantity = input('Product quantity:')
                product_quantity = cleaned_quantity(product_quantity)
                if type(product_quantity) == int:
                    quantity_error = False  
            price_error = True
            while price_error:
                product_price = input('Price of the Product:$')
                product_price = cleaned_price(product_price)
                if product_price is not None:
                    price_error = False 
                brand_name = input("What's the Brand name of the product: ")
                brand = session.query(Brands).filter(Brands.brand_name==brand_name).first()
                if not brand:
                    brand = Brands(brand_name=brand_name)
                    session.add(brand)
                    session.flush() # temporarily add id to the newly created brand name without committing it to the db
                new_product = Products(
                    product_name = product_name,
                    product_quantity = product_quantity,
                    product_price = product_price,
                    date_updated = datetime.date.today(),
                    brand_id = brand.brand_id    
                )
                session.add(new_product)
                session.commit()
                time.sleep(1.3)
                print('Product added successfully!')
                
                
           
            
            
        elif choice == 'A':
            # analyse product
            most_exp = session.query(Products).order_by(Products.product_price.desc()).first()
            least_exp = session.query(Products).order_by(Products.product_price).first()
            
            brands = session.query(Brands).all()
            
            max_brand = None
            max_count = 0

            for brand in brands:
                # print(brand)
                count = len(brand.pro)
                if count > max_count:
                    max_count = count
                    max_brand = brand
            print('************** ANALYSIS ***************\n')
            print(f'Most expensive Product is {most_exp.product_name} with price of ${most_exp.product_price/100}\n')
            print(f'Least expensive Product is {least_exp.product_name} with price of ${least_exp.product_price/100}\n')
            print(f'Brand with most products: {max_brand.brand_name}\n')
            input('Press enter to return to the main menu')
                
        elif choice == 'B':
            # backup product
            products = session.query(Products).all()
            with open('backup.csv', 'w', newline='') as file:
                writer = csv.writer(file)

                writer.writerow([
                    'product_id',
                    'product_name',
                    'product_quantity',
                    'product_price',
                    'date_updated',
                    'brand_id'
                ])

                for p in products:
                    writer.writerow([
                        p.product_id,
                        p.product_name,
                        p.product_quantity,
                        p.product_price,
                        p.date_updated,
                        p.brand_id
            ])
            time.sleep(1.3)
            print("Backup created successfully!")
            input("Press enter to return to menu")
                
            
        else:
            time.sleep(1.2)
            print('GOOD BYE!')
            app_running = False
    
        
 
 
 
 
 
 
 
 
 
 
 
 
if __name__ =='__main__':
      Base.metadata.create_all(engine)
      app()