from flask import Flask, render_template, redirect, request, url_for, session, flash, jsonify
import sqlite3
from database import get_database
import shortuuid
import razorpay

app = Flask(__name__)
app.secret_key = "This_is_a_secret_key"
client = razorpay.Client(auth=("rzp_test_I4RI6OLrPcJeSM", "O0bjtxZVNQNNLbrLwOfL6p4E"))

def generate_short_uuid():
    return shortuuid.uuid()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/courses')
def courses():
    db = get_database()
    cursor = db.cursor()
    products = cursor.execute("SELECT * FROM product").fetchall()
    return render_template('courses.html', products=products)

@app.route('/add_cart', methods=['POST'])
def add_cart():
    product_id = request.form.get('product_id')
    if product_id:
        cart = session.get('cart', {})
        if product_id not in cart:
            cart[product_id] = 1
        else:
            flash('You can add one product only !!', 'warning')
        session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/remove_cart', methods=["POST"])
def remove_cart():
    product_id = request.form.get('product_id')
    if product_id:
        cart = session.get('cart', {})
        if product_id in cart:
            if cart[product_id] > 1:
                cart[product_id] -= 1
            else:
                del cart[product_id]
        session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    db = get_database()
    cart_items = []
    total_amount = 0
    for product_id, quantity in cart.items():
        cur = db.execute("SELECT * FROM product WHERE id = ?", (product_id,))
        product = cur.fetchone()
        if product:
            cart_items.append((product, quantity))
            total_amount += product['price'] * quantity
    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        if 'user_id' not in session:
            session['user_id'] = generate_short_uuid()

        user_id = session['user_id']
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip')
        cart = session.get('cart', {})

        db = get_database()
        product_ids = ','.join(map(str, cart.keys()))
        placeholders = ', '.join('?' for _ in cart.keys())
        query = f"SELECT * FROM product WHERE id IN ({placeholders})"
        products = db.execute(query, list(cart.keys())).fetchall()
        total_amount = sum(product['price'] for product in products)
        session['total'] = total_amount
        db.execute('''INSERT INTO orders (user_id, product_ids, total_amount, status, name, email, phone, address, city, state, zip_code)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (user_id, product_ids, total_amount, 'Pending', name, email, phone, address, city, state, zip_code))
        db.commit()

        return redirect(url_for("pay"))

    if request.method == 'GET':
        if 'user_id' not in session:
            session['user_id'] = generate_short_uuid()

        cart = session.get('cart', {})
        product_ids = list(cart.keys())
        db = get_database()
        products = []
        total = 0
        if product_ids:
            try:
                placeholders = ', '.join('?' for _ in product_ids)
                query = f"SELECT * FROM product WHERE id IN ({placeholders})"
                products = db.execute(query, product_ids).fetchall()
                total = sum(product['price'] for product in products)
            except Exception as e:
                flash('Error fetching products from the database.', 'danger')
                print(e)

        return render_template('checkout.html', products=products, total=total)



@app.route('/pay', methods=["GET", "POST"])
def pay():
    if 'total' in session and session['total'] != "":
        order_id = session['user_id']
        amount = session['total']
        amount = int(amount) * 100
        data = { "amount": amount, "currency": "INR", "receipt": order_id }
        payment = client.order.create(data=data)
        pdata = [amount, payment["id"]]
        print(pdata)
        db = get_database()
        cursor = db.cursor()
        users = cursor.execute("SELECT * FROM orders WHERE user_id = ?", (session['user_id'],)).fetchone()
        return render_template("pay.html", pdata=pdata,users=users)
    return redirect("/")

@app.route('/success', methods=["POST"])
def success():
    pid = request.form.get("razorpay_payment_id")
    ordid = request.form.get("razorpay_order_id")
    sign = request.form.get("razorpay_signature")
    print(f"The payment id : {pid}, order id : {ordid} and signature : {sign}")
    params = {
        'razorpay_order_id': ordid,
        'razorpay_payment_id': pid,
        'razorpay_signature': sign
    }
    final = client.utility.verify_payment_signature(params)
    db = get_database()
    order_id = session.get('user_id')
    if final:
        db.execute('UPDATE orders SET status = ? , razr_pid = ? , razr_ordid = ? WHERE user_id = ?', ('Completed',pid, ordid, order_id))
        db.commit()
        session.clear()
    else:
        db.execute('UPDATE orders SET status = ? WHERE user_id = ?', ('Cancelled', order_id))
        db.commit()
    db.commit()
    return redirect("/", code=301)

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/contact')
def contact():
    return render_template('contact-us.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy-policy.html')

@app.route('/refund')
def refund():
    return render_template('refund-policy.html')

@app.route('/terms')
def terms():
    return render_template('terms&condition.html')

@app.route('/trial')
def trial():
    return render_template('trialclass.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == 'admin':
            flash('Login Successful', 'success')
            session['user'] = username
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('admin_login.html')

    

@app.route('/admin')
def admin_dashboard():
    if 'user' in session:
        return render_template('admin_dashboard.html')
    else:
        return redirect(url_for('admin_login'))

@app.route('/admin/add_product', methods=['GET', 'POST'])
def admin_add_product():
    if 'user' in session:
        if request.method == 'POST':
            product_name = request.form.get('product_name')
            price = request.form.get('price')
            image_url = request.form.get('image_url')
            description = request.form.get('description')
            level = request.form.get('level') or None
            classes = request.form.get('classes') or None
            audience = request.form.get('audience') or None
            rating = request.form.get('rating') or None

            db = get_database()
            db.execute('''INSERT INTO product (product_name, price, image_url, description, level, classes, audience, rating)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                    (product_name, price, image_url, description, level, classes, audience, rating))
            db.commit()
            flash('Product added successfully', 'success')
            return redirect(url_for('admin_add_product'))
        return render_template('admin_add_product.html')
    else:
        return redirect(url_for('admin_login'))

@app.route('/admin/all_product')
def admin_all_product():
    if 'user' in session:
        db = get_database()
        products = db.execute("SELECT * FROM product").fetchall()
        return render_template("admin_all_products.html", products=products)
    else:
        return redirect(url_for('admin_login'))

@app.route('/admin/orders')
def admin_orders():
    if 'user' in session:
        db = get_database()
        orders = db.execute("SELECT * FROM orders").fetchall()
        products = db.execute("SELECT * FROM product").fetchall()
        product_dict = {product['id']: product for product in products}
        
        order_details = []
        for order in orders:
            product_ids = order['product_ids'].split(',')
            order_products = []
            for pid in product_ids:
                if pid.isdigit():
                    product_id = int(pid)
                    if product_id in product_dict:
                        order_products.append(product_dict[product_id])
            order_details.append({
                'order': order,
                'products': order_products
            })
        
        return render_template('admin_orders.html', order_details=order_details)
    else:
        return redirect(url_for('admin_login'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('user', None)  # Remove the user from the session
    flash('You have been logged out.', 'success')  # Optional: flash a message
    return redirect(url_for('admin_login'))  # Redirect to the login page



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
