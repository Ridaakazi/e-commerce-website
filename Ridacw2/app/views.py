from flask import Flask,flash, render_template, request, redirect, url_for, session, jsonify
from app import app, db,login_manager
from .forms import LoginForm,RegisterForm,SearchForm
from .models import User,Product,UserCart
from flask_login import login_user, LoginManager,login_required,logout_user,current_user
from app import bcrypt


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('shop'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')
            return redirect(url_for('login'))
    return render_template("login.html", form=form)



@app.route('/logout', methods=['GET', 'POST'])
# so that only if the user has logged in he can access the page
@login_required
def logout():
    logout_user()
    return redirect(url_for('login')) 

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = RegisterForm()

    if form.validate_on_submit():
        # Check if the email already exists
        existing_user_email = User.query.filter_by(email=form.email.data).first()
        if existing_user_email:
            flash('Email is already in use. Please use a different one.', 'danger')
            return redirect(url_for('sign_up'))

        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("sign_up.html", form=form)


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    user_cart_item = UserCart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    product = Product.query.get_or_404(product_id)

    if product.stock <= 0:
        flash('Item is out of stock', 'danger')
        return jsonify({'message': 'Item is out of stock', 'cart_count': get_cart_count()})

    if user_cart_item:
        if user_cart_item.quantity < product.stock:
            user_cart_item.quantity += 1
        else:
            flash('Item quantity exceeds stock level', 'danger')
    else:
        new_cart_item = UserCart(user_id=current_user.id, product_id=product_id, quantity=1)
        db.session.add(new_cart_item)

    db.session.commit()

    cart_count = get_cart_count()
    return jsonify({'message': 'Item added to the cart successfully', 'cart_count': cart_count})


#to get cart count
def get_cart_count():
    if current_user.is_authenticated:
        user_cart_items = UserCart.query.filter_by(user_id=current_user.id).all()
        total_quantity = sum(item.quantity for item in user_cart_items)
        return total_quantity
    return 0

@app.route('/remove_one_from_cart/<int:product_id>', methods=['POST'])
@login_required
def remove_one_from_cart(product_id):
    # find in db which the user wants to remove
    user_cart_item = UserCart.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    if user_cart_item:
        user_cart_item.quantity -= 1

        if user_cart_item.quantity == 0:
            db.session.delete(user_cart_item)

        db.session.commit()
    else:
        flash('Item not found in the cart', 'danger')


    return redirect(url_for('cart'))

@app.route('/cart',methods=['GET','POST'])
@login_required
def cart():
    username = current_user.username if current_user.is_authenticated else None
      
    form = SearchForm()
  
    user_cart = UserCart.query.filter_by(user_id=current_user.id).options(db.joinedload(UserCart.product)).all()

    total_cart_price=round(sum(cart_item.quantity * cart_item.product.price for cart_item in user_cart), 2)
   
    return render_template('cart.html',username=username,form=form, user_cart=user_cart,total_cart_price=total_cart_price)

@app.route('/checkout',methods=['GET','POST'])
@login_required
def checkout():
    username = current_user.username if current_user.is_authenticated else None
      
    form = SearchForm()
  
    user_cart = UserCart.query.filter_by(user_id=current_user.id).options(db.joinedload(UserCart.product)).all()

    total_cart_price=round(sum(cart_item.quantity * cart_item.product.price for cart_item in user_cart), 2)
   
    return render_template('checkout.html', username=username, form=form, user_cart=user_cart, total_cart_price=total_cart_price)

@app.route('/remove_from_wishlist/<int:product_id>', methods=['POST'])
@login_required
def remove_from_wishlist(product_id):
    product = Product.query.get_or_404(product_id)
    
    if product.in_wishlist:
        product.in_wishlist = False
        db.session.commit()
       
    else:
        flash('Product not found in the wishlist.', 'info')

    return redirect(url_for('wishlist'))

@app.route('/search', methods=['POST'])
@login_required
def search():
    username =current_user.username if current_user.is_authenticated else None

    user_cart = UserCart.query.filter_by(user_id=current_user.id).options(db.joinedload(UserCart.product)).all()


    form = SearchForm()
    products = None
    searched_term = None  

   
    cart_count = get_cart_count()

    if form.validate_on_submit():
        searched_term = form.searched.data
        
        products = Product.query.filter(Product.name.ilike('%' + searched_term + '%')).order_by(Product.id).all()

    return render_template('search.html', username=username, products=products, user_cart=user_cart, form=form,
                           searched=searched_term, cart_count=cart_count)

@app.route('/add_to_wishlist/<int:product_id>', methods=['POST'])
@login_required
def add_to_wishlist(product_id):
    product = Product.query.get_or_404(product_id)

    
    if product.in_wishlist:
        flash('Product is already in the wishlist.', 'info')
    else:
        product.in_wishlist = True
        db.session.commit()
     

    return redirect(url_for('shop'))


@app.route('/wishlist', methods=['GET', 'POST'])
@login_required
def wishlist():
    username = current_user.username if current_user.is_authenticated else None
    user_wishlist = Product.query.filter_by(in_wishlist=True).all()

    form = SearchForm()

    if form.validate_on_submit():
        pass
      
    cart_count = get_cart_count()

    return render_template("wishlist.html",cart_count=cart_count, username=username, user_wishlist=user_wishlist, form=form)


@app.route('/', methods=['GET', 'POST'])
@login_required
def shop():
    username = current_user.username if current_user.is_authenticated else None


    form = SearchForm()

    products = Product.query.all()
    products = Product.query.order_by(Product.id).all()
    cart_count = get_cart_count()

    return render_template("shop.html", username=username, products=products, cart_count=cart_count, form=form)

@app.route('/popular',methods=['GET','POST'])
def popular():

    username = current_user.username if current_user.is_authenticated else None


    form = SearchForm()
   
    products = Product.query.all()
    products = Product.query.order_by(Product.id).all()

    cart_count = get_cart_count()
    return render_template("popular.html", form=form, products=products, username=username, cart_count=cart_count)

@app.route('/new',methods=['GET','POST'])
def new():
    username = current_user.username if current_user.is_authenticated else None


    form = SearchForm()

    products = Product.query.all()
    products = Product.query.order_by(Product.id).all()

    cart_count = get_cart_count()

    return render_template("new.html", form=form, username=username, products=products, cart_count=cart_count)


# all the items data
with app.app_context():

    product_items = [
        {'name': 'Mangoes', 'price': 10.00, 'image': 'static/imgs/mangoes.jpg', 'tag':'new','stock':'3'},
        {'name': 'Cookies', 'price': 1.30, 'image': 'static/imgs/cookies.jpg', 'tag':'new','stock':'13'},
        {'name': 'Potatoes', 'price': 8.00, 'image': 'static/imgs/potato.jpg', 'tag':'new','stock':'7'},
        {'name': 'Bread', 'price': 3.00, 'image': 'static/imgs/bread.jpg' , 'tag':'new','stock':'14'},
        
        {'name': 'Wraps', 'price': 0.50, 'image': 'static/imgs/wraps.jpg', 'tag':'new','stock':'32'},
        {'name': 'Tomato', 'price': 2.00, 'image': 'static/imgs/tomato.jpg', 'tag':'new','stock':'37'},
        {'name': 'Apples', 'price': 8.20, 'image': 'static/imgs/apples.jpg' , 'tag':'new','stock':'21'},
        
        
        {'name': 'Pineapple', 'price': 4.00, 'image': 'static/imgs/pinap.jpg', 'tag':'popular','stock':'13'},
        {'name': 'Chocolate Cookies', 'price': 1.30, 'image': 'static/imgs/cococookies.jpg', 'tag':'popular','stock':'6'},
        {'name': 'Cherries', 'price': 8.00, 'image': 'static/imgs/cherries.jpg', 'tag':'popular','stock':'43'},
        {'name': 'Fruit Bread', 'price': 3.00, 'image': 'static/imgs/fbread.jpg', 'tag':'popular','stock':'13' },
        
        {'name': 'Chocolate Milk', 'price': 2.50, 'image': 'static/imgs/cmilk.jpg', 'tag':'popular','stock':'12'},
        {'name': 'Brown Bread', 'price': 5.00, 'image': 'static/imgs/bbread.jpg', 'tag':'popular','stock':'10'},
        {'name': 'Apple Juice', 'price': 1.20, 'image': 'static/imgs/applej.jpg', 'tag':'popular' ,'stock':'9'},
        {'name': 'Blueberries', 'price': 3.00, 'image': 'static/imgs/blue.jpg' , 'tag':'popular','stock':'38'},

        
        {'name': 'Garlic', 'price': 2.00, 'image': 'static/imgs/garlic.jpg', 'tag':'shop' ,'stock':'27'},
        {'name': 'Grapes', 'price': 6.00, 'image': 'static/imgs/grapes.jpg','tag':'shop' ,'stock':'30'},
        {'name': 'Milk', 'price': 1.10, 'image': 'static/imgs/milk.jpg','tag':'shop','stock':'13' },
        {'name': 'M&M Cookies', 'price': 5.00, 'image': 'static/imgs/mnm.jpg','tag':'shop' ,'stock':'4'},
        {'name': 'Oat Milk', 'price': 3.00, 'image': 'static/imgs/oat.jpg', 'tag':'shop','stock':'6'},

        {'name': 'Orange Juice', 'price': 12.00, 'image': 'static/imgs/ojuice.jpg' ,'tag':'shop','stock':'31'},
        {'name': 'Rice', 'price': 3.00, 'image': 'static/imgs/rice.jpg','tag':'shop' ,'stock':'3'},
        {'name': 'Strawberries', 'price': 15.00, 'image': 'static/imgs/straw.jpg','tag':'new' ,'stock':'13'},
        {'name': 'Water', 'price': 3.00, 'image': 'static/imgs/water.jpg','tag':'new' ,'stock':'3'}       

    ]
    
    for items in product_items:
        existing_item = Product.query.filter_by(name=items['name']).first()
        if not existing_item:
            item = Product(**items)
            db.session.add(item)

    db.session.commit()


