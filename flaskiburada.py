import requests
from flask import Flask, render_template, flash, url_for, redirect, request
from forms import ProductForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from bs4 import BeautifulSoup
import configparser

app = Flask(__name__)
config = configparser.ConfigParser()
config.read('passwords.config') # where i keep my credentials

app.config['SECRET_KEY'] = config['APP']['SECRET_KEY'] 

#db 
app.config['SQLALCHEMY_DATABASE_URI'] = config['APP']['SQLALCHEMY_DATABASE_URI'] 
db = SQLAlchemy(app)
migrate = Migrate(app, db)

def getProduct(productID):
    return ProductsModel.query.get(productID)

def allProducts():
    return ProductsModel.query.all()

def deleteProduct(productID):
    ProductsModel.query.filter_by(id=productID).delete()
    db.session.commit()

def addProductToDbFromLink(productLink):
    r = requests.get(productLink)
    soup = BeautifulSoup(r.content, 'html.parser')
    productName = soup.find('h1', attrs={'class' : 'product-name'}).text.strip()
    product_price = soup.find('span', attrs={'class': 'price'}).get("content")
    product_image = soup.find('img', attrs={'class': 'product-image'}).get("src")
    
    product = ProductsModel(price=product_price, image=product_image, title=productName)
    db.session.add(product)
    db.session.commit()
    return product

class ProductsModel(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.String())
    image = db.Column(db.String())
    title = db.Column(db.String())

    def __init__(self, price, image, title):
        self.price = price
        self.image = image
        self.title = title

    def __repr__(self):
        return f"<Product {self.title}>"

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = ProductForm()
    if form.validate_on_submit():
        flash(f'The link {form.product_link.data} is an actual product on hepsiburada!', 'success')
        # process link here
        productID = addProductToDbFromLink(form.product_link.data).id
        return redirect(url_for('details', productID=productID)) 
    return render_template('home.html', form=form)

@app.route('/details/link?<productID>')
def details(productID):
    return render_template('details.html', product=getProduct(productID))

@app.route('/listproducts', methods=["GET", "POST"])
def listProducts():
    page = request.args.get('page', 1, type=int)
    products = ProductsModel.query.paginate(page=page, per_page=3)
    print("list")

    if request.method == "POST":
        print(request.form)   
        print("sup")
    return render_template('products.html', results=products)

@app.route('/delete/<productID>', methods=["GET", "POST", "DELETE"])
def delete(productID):
    productID = int(productID)
    deleteProduct(productID)
    return redirect(url_for('listProducts', page=1)) 

if __name__ == '__main__':
    app.run(debug=True) 