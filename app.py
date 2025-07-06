import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_bcrypt import Bcrypt
from flask_session import Session
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from models import db, User, Product, UserBehavior, MarketingMessage
from journey_engine import JourneyEngine
from gpt_generator import GPTGenerator
from sms_sender import SMSSender

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ai_journey.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'

db.init_app(app)
bcrypt = Bcrypt(app)
Session(app)

# Initialize services
journey_engine = JourneyEngine()
gpt_generator = GPTGenerator()
sms_sender = SMSSender()

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('register.html')
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return render_template('register.html')

        user = User(username=username, email=email, phone=phone)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    journey_engine.track_behavior(
        user_id=session.get('user_id'),
        session_id=session.get('session_id', 'anonymous'),
        action='view',
        product_id=product_id
    )
    return render_template('product_detail.html', product=product)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = int(request.form['product_id'])
    quantity = int(request.form.get('quantity', 1))
    if 'cart' not in session:
        session['cart'] = {}
    if str(product_id) in session['cart']:
        session['cart'][str(product_id)] += quantity
    else:
        session['cart'][str(product_id)] = quantity
    session.modified = True
    journey_engine.track_behavior(
        user_id=session.get('user_id'),
        session_id=session.get('session_id', 'anonymous'),
        action='add_to_cart',
        product_id=product_id,
        data=json.dumps({'quantity': quantity})
    )
    flash('Product added to cart!', 'success')
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    cart_items = []
    total = 0
    if 'cart' in session:
        for product_id, quantity in session['cart'].items():
            product = Product.query.get(int(product_id))
            if product:
                subtotal = product.price * quantity
                cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
                total += subtotal
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = request.form['product_id']
    if 'cart' in session and product_id in session['cart']:
        del session['cart'][product_id]
        session.modified = True
        journey_engine.track_behavior(
            user_id=session.get('user_id'),
            session_id=session.get('session_id', 'anonymous'),
            action='remove_from_cart',
            product_id=int(product_id)
        )
        flash('Product removed from cart!', 'info')
    return redirect(url_for('cart'))

@app.route('/checkout')
def checkout():
    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty!', 'error')
        return redirect(url_for('index'))
    session['cart'] = {}
    session.modified = True
    journey_engine.track_behavior(
        user_id=session.get('user_id'),
        session_id=session.get('session_id', 'anonymous'),
        action='purchase'
    )
    flash('Purchase completed successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        response = gpt_generator.generate_response(message)
        return jsonify({'response': response, 'status': 'success'})
    except Exception:
        return jsonify({'response': 'Sorry, I encountered an error. Please try again.', 'status': 'error'})

@app.route('/api/track_behavior', methods=['POST'])
def track_behavior():
    try:
        data = request.get_json()
        journey_engine.track_behavior(
            user_id=session.get('user_id'),
            session_id=session.get('session_id', 'anonymous'),
            action=data.get('action'),
            product_id=data.get('product_id'),
            data=json.dumps(data.get('data', {}))
        )
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/admin')
def admin_dashboard():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    users = User.query.all()
    products = Product.query.all()
    behaviors = UserBehavior.query.order_by(UserBehavior.timestamp.desc()).limit(100).all()
    messages = MarketingMessage.query.order_by(MarketingMessage.sent_at.desc()).limit(50).all()
    return render_template('admin.html', users=users, products=products, behaviors=behaviors, messages=messages)

def create_sample_data():
    if Product.query.count() == 0:
        sample_products = [
            {'name': 'Premium Wireless Headphones', 'description': 'High-quality wireless headphones with noise cancellation and premium sound quality.', 'price': 199.99, 'image_url': 'https://images.pexels.com/photos/3394650/pexels-photo-3394650.jpeg?auto=compress&cs=tinysrgb&w=500', 'category': 'Electronics'},
            {'name': 'Smart Fitness Watch', 'description': 'Advanced fitness tracking with heart rate monitoring and GPS capabilities.', 'price': 299.99, 'image_url': 'https://images.pexels.com/photos/437037/pexels-photo-437037.jpeg?auto=compress&cs=tinysrgb&w=500', 'category': 'Fitness'},
            {'name': 'Portable Bluetooth Speaker', 'description': 'Compact speaker with powerful sound and long battery life.', 'price': 79.99, 'image_url': 'https://images.pexels.com/photos/1649771/pexels-photo-1649771.jpeg?auto=compress&cs=tinysrgb&w=500', 'category': 'Electronics'},
            {'name': 'Professional Camera', 'description': 'High-resolution camera perfect for photography enthusiasts.', 'price': 899.99, 'image_url': 'https://images.pexels.com/photos/90946/pexels-photo-90946.jpeg?auto=compress&cs=tinysrgb&w=500', 'category': 'Photography'},
            {'name': 'Ergonomic Office Chair', 'description': 'Comfortable office chair with lumbar support and adjustable height.', 'price': 249.99, 'image_url': 'https://images.pexels.com/photos/586062/pexels-photo-586062.jpeg?auto=compress&cs=tinysrgb&w=500', 'category': 'Furniture'},
            {'name': 'Smartphone', 'description': 'Latest flagship smartphone with advanced camera and processing power.', 'price': 699.99, 'image_url': 'https://images.pexels.com/photos/699122/pexels-photo-699122.jpeg?auto=compress&cs=tinysrgb&w=500', 'category': 'Electronics'}
        ]
        for product_data in sample_products:
            product = Product(**product_data)
            db.session.add(product)
        db.session.commit()
        print("Sample products created successfully!")

def setup_abandoned_cart_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=journey_engine.check_abandoned_carts, trigger="interval", minutes=2, id='abandoned_cart_check')
    scheduler.start()

@app.before_request
def set_session_id():
    if 'session_id' not in session:
        session['session_id'] = os.urandom(16).hex()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_sample_data()
        setup_abandoned_cart_scheduler()
    app.run(debug=os.getenv('DEBUG', 'True').lower() == 'true', port=int(os.getenv('PORT', 5000)), host='0.0.0.0')
