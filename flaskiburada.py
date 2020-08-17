import requests
from flask import Flask, render_template, flash, url_for, redirect
from forms import ProductForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from bs4 import BeautifulSoup


app = Flask(__name__)
app.config['SECRET_KEY'] = '6d65c8f1540d2885e69dfe8eb06f319c'

#db 
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:dontyoudb@localhost:5432/hepsiflask"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

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

db.create_all()

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = ProductForm()
    if form.validate_on_submit():
        flash(f'The link {form.product_link.data} is an actual product on hepsiburada!', 'success')
        # process link here
        fileLink = form.product_link.data.split('.com/')[1]
        return redirect(url_for('details', product=fileLink)) 
    return render_template('home.html', form=form)

@app.route('/details/link?<product>')
def details(product):
    r = requests.get('http://www.hepsiburada.com/' + product)
    soup = BeautifulSoup(r.content, 'html.parser')
    productName = soup.find('h1', attrs={'class' : 'product-name'}).text.strip()
    product_price = soup.find('span', attrs={'class': 'price'}).get("content")
    product_image = soup.find('img', attrs={'class': 'product-image'}).get("src")
    
    product = ProductsModel(price=product_price, image=product_image, title=productName)
    db.session.add(product)
    db.session.commit()

    print(product_price)
    print(f"Image {product_image}")
    return render_template('details.html', product=product)

@app.route('/listproducts')
def listProducts():
    products = ProductsModel.query.all()
    results = [
            {
                "id": product.id,
                "price": product.price,
                "image": product.image,
                "title": product.title
            } for product in products]
    return render_template('products.html', results=results)
    


if __name__ == '__main__':
    app.run(debug=True)